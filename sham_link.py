# -*- coding: utf-8 -*-
"""[R6-PLUS14] ربط حساب شام كاش عبر QR — وحدة مستقلة للبوت.

التدفق (مطابق حرفياً لتطبيق/موقع شام كاش الرسمي):
1) gen_link() يولّد جلسة (uuid + مفتاح داخلي) وحمولة QR مشفرة بالمفتاح الثابت
2) المالك يمسح الـQR من «الأجهزة المرتبطة» في التطبيق ويعتمد
3) check_session() يستطلع Session/check حتى النجاح ثم يفك encData بالمفتاح الداخلي
4) authed_call() يستدعي نقاط الحساب (Bearer token + accessToken داخل الجسم)
   ويفك ردود encData بنفس المفتاح الداخلي

بلا أي أسرار بهذا الملف — الجلسة تُخزَّن مشفرة لدى البوت (Fernet).
"""

import base64
import json
import os
import re
import secrets
import string
import uuid

try:
    import aiohttp
except ImportError:  # pragma: no cover
    aiohttp = None

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

API = "https://api.shamcash.sy/v4/api"

# مفتاح التطبيق/الموقع الثابت (مضمّن في طرفهما أصلاً — ليس سراً من أسرارنا)
STATIC_AES = b"g0Zrgp8XRK/BN2ZAtUfJDQ=="  # 24 بايت = AES-192-GCM

DEFAULT_DEVICE = "Redmi Note 11 Pro"

# [RAND-DEV 5.17] أسماء أجهزة أندرويد واقعية شائعة — يُختار أحدها
# عشوائياً عند كل ربط جديد لتفادي تشابه بصمة اسم الجهاز بين نسخ.
DEVICE_POOL = (
    "Redmi Note 10", "Redmi Note 11", "Redmi Note 12",
    "Redmi 9C", "Redmi 10", "Redmi 12",
    "Galaxy A12", "Galaxy A32", "Galaxy A52", "Galaxy A54",
    "Galaxy S21", "Huawei P30", "Huawei nova 9", "Honor X8",
    "Oppo A54", "Oppo A78", "Realme C35",
    "Infinix Hot 11", "Infinix Note 12", "Tecno Camon 19",
)

WEB_PEM_PKCS1 = """-----BEGIN RSA PUBLIC KEY-----
MIIBCgKCAQEAuj8jcVjIoCND5p0ZIDMcNkPV3YzF3zywvB0az6Vorb+VHeAlUHut
WNRMmyVr3Eu+pPx27v+V7V60Nq9j5QSTeHXC4ndMuHrRUDc8IEhDcbOFdPEwrA6Q
UH+K1d8VQUcXOHPRcx0xEDtNwW8dKP6ySI3tt61HWp+/s133+OIAUKyH5BmWmauj
tJWaRfxwVA3okvwHMgWRfK0Nyxe6yFnmO4izOqKt/Pph0uPZVXL4/JawC5lvuwbk
SMuPGJjRN34YuMje1mkvArHTSeJ7dplqG6rXIg1X75m1elFu4GiLCc76SqgQBmXW
KSe5sprj2OrooP5B/liFD0LnsuVBWRarFQIDAQAB
-----END RSA PUBLIC KEY-----"""

CURR_NAMES = {1: "USD", 2: "SYP", 3: "EUR"}


class ShamError(Exception):
    """فشل عملية شام كاش — رسالة جاهزة للعرض."""


def _b64(data: bytes) -> str:
    return base64.b64encode(data).decode()


def aes_gcm_enc(key: bytes, text: str) -> str:
    """صيغة الموقع: b64(ct||tag) + '.' + b64(iv12)."""
    iv = os.urandom(12)
    sealed = AESGCM(key).encrypt(iv, text.encode("utf-8"), None)
    return _b64(sealed) + "." + _b64(iv)


def dec_field(key: bytes, enc: str) -> bytes:
    """فك حقل مشفّر بصيغة الموقع — يرمي ShamError عند الفشل."""
    try:
        left, iv_b64 = enc.split(".", 1)
        ct = base64.b64decode(left)
        iv = base64.b64decode(iv_b64)
        return AESGCM(key).decrypt(iv, ct, None)
    except Exception as exc:
        raise ShamError(f"فشل فك التشفير: {type(exc).__name__}") from exc


def _spki_der_from_pkcs1(pem_text: str) -> bytes:
    """غلاف SPKI لمفتاح PKCS#1 ليقرأه cryptography."""
    b64 = "".join(pem_text.strip().splitlines()[1:-1])
    pkcs1 = base64.b64decode(b64)

    def _len(n: int) -> bytes:
        if n < 0x80:
            return bytes([n])
        b = n.to_bytes((n.bit_length() + 7) // 8, "big")
        return bytes([0x80 | len(b)]) + b

    alg = bytes.fromhex("300d06092a864886f70d0101010500")
    bits = b"\x00" + pkcs1
    inner = alg + b"\x03" + _len(len(bits)) + bits
    return b"\x30" + _len(len(inner)) + inner


def _web_public_key():
    der = _spki_der_from_pkcs1(WEB_PEM_PKCS1)
    return serialization.load_der_public_key(der)


def encrypt_hybrid(json_str: str) -> dict:
    """يشفّر جسم الطلب: encData هجين + aesKey ملفوف RSA-PKCS1v15."""
    pub = _web_public_key()
    aes_str = base64.b64encode(os.urandom(16)).decode().replace("+", "-").replace(
        "/", "_",
    )
    enc_data = aes_gcm_enc(aes_str.encode("utf-8"), json_str)
    wrapped = pub.encrypt(aes_str.encode("utf-8"), padding.PKCS1v15())
    return {"encData": enc_data, "aesKey": _b64(wrapped)}


def gen_link(device_name: str = "") -> dict:
    """توليد جلسة ربط جديدة + حمولة QR مطابقة لتوليد التطبيق.

    [RAND-DEV 5.17] بلا اسم صريح → اسم جهاز عشوائي واقعي من
    DEVICE_POOL (مختلف لكل ربط) — والاسم الصريح يُحترم كما هو.
    """
    if not device_name:
        device_name = secrets.choice(DEVICE_POOL)

    raw_sid = str(uuid.uuid4())
    inner_key = base64.b64encode(os.urandom(16)).decode()
    sid_enc = aes_gcm_enc(STATIC_AES, raw_sid)
    pubkey_enc = aes_gcm_enc(STATIC_AES, inner_key)

    alphabet = string.ascii_letters + string.digits + "-_"
    fcm = "APA91bF" + "".join(secrets.choice(alphabet) for _ in range(150))

    payload = {
        "sessionId": f"{sid_enc}#{fcm}",
        "publicKey": pubkey_enc,
        "infoDevice": {"browser": "Mobile", "os": "Android",
                       "deviceName": device_name},
    }
    data = json.dumps(payload, separators=(",", ":"), ensure_ascii=False)
    return {"raw_sid": raw_sid, "inner_key": inner_key,
            "payload": data, "device": device_name}


def qr_png(payload: str):
    """صورة QR بصيغة PNG (bytes) — None إن كانت المكتبة غائبة."""
    try:
        import io

        import qrcode
    except ImportError:  # pragma: no cover
        return None

    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_L,
                       box_size=12, border=4)
    qr.add_data(payload)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", background_color="white")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


# ============================================================
# الشبكة
# ============================================================

async def _post(path: str, body_obj: dict, token: str = None,
                timeout: int = 20) -> dict:
    """طلب واحد مشفر هجينياً — يرمي ShamError عند فشل الشبكة.

    [LINK-REVERT 5.18.3] أُزيلت ترويسة deviceName (تجربة 5.17.1):
    ربط حي بترويسة = 401 «وصول غير مصرح» مرتين، وبنفس اللحظة
    بلا ترويسة (5.16.3) = نجاح — بصمة 5.16.3 المُجرَّبة هي المرجع.
    """
    if aiohttp is None:
        raise ShamError("مكتبة aiohttp غير متوفرة")

    headers = {"Content-Type": "application/json",
               "Accept": "application/json",
               "x-Requested-With": "XMLHttpRequest",
               "lang": "ar", "e": "true",
               "User-Agent": "Dart/3.5 (dart:io)"}

    if token:
        headers["Authorization"] = f"Bearer {token}"

    body = encrypt_hybrid(json.dumps(body_obj, separators=(",", ":")))
    url = f"{API}/{path}"

    # [PROXY-OUT] بروكسي صادر اختياري: http(s) مباشر، socks5 عبر connector
    proxy = (os.getenv("SHAM_PROXY")
             or os.getenv("OUTBOUND_PROXY") or "").strip() or None
    connector = None

    if proxy and proxy.lower().startswith("socks"):
        try:
            import aiohttp_socks
        except ImportError as exc:
            raise ShamError(
                "لدعم SOCKS5 ثبّت: pip install aiohttp-socks",
            ) from exc

        connector = aiohttp_socks.ProxyConnector.from_url(proxy)
        proxy = None

    try:
        async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=timeout),
            connector=connector,
        ) as sess:
            async with sess.post(url, data=json.dumps(body).encode("utf-8"),
                                 headers=headers, proxy=proxy) as resp:
                # [AUTO-FIX 5.18.18] إظهار حالة HTTP عند رد غير JSON —
                # كان 401/400 يظهر كفشل اتصال عام بلا تفاصيل
                try:
                    return await resp.json(content_type=None)
                except Exception:
                    snippet = ""

                    try:
                        snippet = (await resp.text())[:200]
                    except Exception:
                        pass

                    raise ShamError(
                        f"رد غير JSON من شام كاش (HTTP {resp.status})"
                        + (f": {snippet}" if snippet else ""),
                    )
    except ShamError:
        raise
    except Exception as exc:
        raise ShamError(f"تعذر الاتصال بشام كاش: {type(exc).__name__}: {exc}") from exc


def _unwrap_enc(res: dict, inner_key: bytes):
    """إن كان الرد يحمل encData يُفك ويرجع ككائن، وإلا يرجع الرد كما هو."""
    data = res.get("data")

    if isinstance(data, dict) and isinstance(data.get("encData"), str):
        return json.loads(dec_field(inner_key, data["encData"]).decode("utf-8"))

    return data if res.get("succeeded") else res


async def check_session_ex(link: dict):
    """استطلاع مفصّل — يعيد (توكنات أو None، وصف آخر رد من الخادم)."""
    res = await _post("Session/check", {"sessionId": link["raw_sid"]})

    if res.get("succeeded"):
        data = res.get("data") or {}
        enc = data.get("encData")

        if not enc:
            return None, "نجاح بلا بيانات مشفرة"

        try:
            out = json.loads(
                dec_field(link["inner_key"].encode(), enc).decode("utf-8"),
            )
        except ShamError as exc:
            return None, str(exc)

        return out, "تم"

    code = res.get("result")
    msg = str(res.get("message") or "")

    if code:
        return None, f"{msg} ({code})" if msg else f"كود {code}"

    return None, msg or "رد غير معروف"


async def check_session(link: dict):
    """استطلاع مختصر — التوكنات أو None."""
    data, _ = await check_session_ex(link)
    return data


async def authed_call(sess: dict, path: str, extra: dict = None):
    """نداء محمي: Bearer + accessToken بالجسم + فك encData."""
    res = await _post(path, {"accessToken": sess.get("access_token", ""),
                             **(extra or {})}, token=sess.get("token", ""))
    return _unwrap_enc(res, sess["inner_key"].encode())


async def profile(sess: dict):
    return await authed_call(sess, "Account/myProfile")


async def balances(sess: dict):
    return await authed_call(sess, "Account/balances")


async def history(sess: dict, page: int = None):
    extra = {"pageIndex": page} if page else {}
    return await authed_call(sess, "Transaction/history-logs", extra)


# ═══ [AUTO-WD] التحويل الصادر + التحقق المستقل من السجل ═══
# ملاحظة صريحة: صيغة جسم Exchange/createTransactionToSomeone مستنتجة
# من التحليل الساكن (PROTOCOL_NOTES §7) ولم تُطلق حياً بعد — أول محاولة
# حية قد تعيد أخطاء حقول من الخادم؛ التصحيح يكون هنا فقط (حقول الجسم).

TX_TO_SOMEONE = "Exchange/createTransactionToSomeone"
TX_REF_KEYS = ("strTranId", "tranId", "transactionId")


async def send_transfer(sess: dict, dest: str, amount: float,
                        note: str = "", currency_id: int = 1) -> dict:
    """تحويل صادر من محفظة الجلسة إلى حساب شام آخر.

    يعيد الرد المفكوك كما هو — تقييمه (نجاح/رفض/غامض) على المتصل،
    والتحقق المستقل يكون من Transaction/history-logs (find_outgoing).
    """
    body = {
        "toAccountNumber": str(dest).strip(),
        "amount": f"{float(amount):.2f}",
        "currencyId": int(currency_id),
        "note": (note or "")[:100],
    }
    return await authed_call(sess, TX_TO_SOMEONE, body)


def tx_ref_from_res(res) -> str:
    """استخراج مرجع العملية من رد الإرسال إن وُجد (شكله يُثبَّت حياً)."""
    if not isinstance(res, dict):
        return ""

    for scope in (res, res.get("data")):
        if not isinstance(scope, dict):
            continue

        for k in TX_REF_KEYS:
            v = scope.get(k)

            if v:
                return str(v)

    return ""


def res_failed(res) -> bool:
    """رفض واضح من الخادم؟ (succeeded=False بمغلف شام كاش)."""
    return isinstance(res, dict) and res.get("succeeded") is False


async def find_outgoing(sess: dict, amount: float, dest: str,
                        pages: int = 2):
    """البحث بالسجل عن صادر مطابق (نوع 2 + المبلغ + ذيل الوجهة).

    يعيد قاموس العملية أو None. ذيل الوجهة يُقارن فقط إن احتوت
    الوجهة 4 أرقام فأكثر (السجل يخفي الأرقام بصيغة ****NNNN).
    """
    digits = re.sub(r"\D", "", str(dest))
    tail = digits[-4:]
    have_tail = len(digits) >= 4

    for page in range(1, max(1, pages) + 1):
        try:
            data = await history(sess, page)
        except ShamError:
            return None

        rows = []

        if isinstance(data, list):
            rows = data
        elif isinstance(data, dict):
            for k in ("items", "logs", "records", "data", "transactions"):
                v = data.get(k)

                if isinstance(v, list):
                    rows = v
                    break

        for tx in rows:
            if not isinstance(tx, dict):
                continue

            if str(tx.get("tranKind") or "") != "2":
                continue  # الصادر فقط

            try:
                amt = float(tx.get("amount") or 0)
            except (TypeError, ValueError):
                continue

            if abs(amt - float(amount)) > 0.009:
                continue

            peer = re.sub(r"\D", "", str(tx.get("peerAccountNumber") or ""))

            if have_tail and peer and peer[-4:] != tail:
                continue

            return tx

    return None


async def logout(sess: dict):
    try:
        return await authed_call(sess, "Session/logout")
    except ShamError:
        return None


def format_balances(bal) -> str:
    """تنسيق الأرصدة للعرض."""
    if not isinstance(bal, dict) or not bal.get("balances"):
        return "❌ تعذر قراءة الأرصدة"

    lines = []

    for b in bal["balances"]:
        name = b.get("currencyName") or CURR_NAMES.get(
            b.get("currencyId"), f"#{b.get('currencyId')}",
        )
        line = f"• <b>{name}</b>: {float(b.get('balance') or 0):.2f}"

        if float(b.get("blocked") or 0):
            line += f" (محجوز {float(b['blocked']):.2f})"

        lines.append(line)

    text = "💰 <b>أرصدة شام كاش</b>\n\n" + "\n".join(lines)

    if bal.get("hasTransactionPending"):
        text += "\n\n⚠️ توجد معاملة معلقة"

    return text
