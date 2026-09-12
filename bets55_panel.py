# -*- coding: utf-8 -*-
"""[R6-PLUS12] وحدة ربط لوحة الوكيل (55bets / Affigates API).

تعمل مباشرة مع الـAPI الخلفي للوحة (خلف واجهة React):
    POST /global/api/User/signIn               {username, password}
    GET  /global/api/User/get-current-user-info
    POST /global/api/Player/getPlayersForCurrentAgent
    POST /global/api/Player/getPlayerBalanceById  {playerId}
    POST /global/api/Player/registerPlayer
    POST /global/api/Player/depositToPlayer       {amount, comment, playerId, currencyCode}
    POST /global/api/Player/withdrawFromPlayer    (النموذج نفسه)

الجلسة كوكيز (Set-Cookie) — يديرها aiohttp.CookieJar تلقائياً.
بيانات الدخول من البيئة:
    BETS55_PANEL_URL  (افتراضي https://agents.55bets.net)
    BETS55_AGENT_USER
    BETS55_AGENT_PASS
    BETS55_CURRENCY   (افتراضي NSP)
"""

import os
import re
import asyncio
import logging
import secrets
from datetime import datetime, timezone

try:
    import aiohttp
except ImportError:  # pragma: no cover
    aiohttp = None

try:  # [PROXY-OUT] دعم socks5:// (اختياري)
    import aiohttp_socks
except ImportError:  # pragma: no cover
    aiohttp_socks = None

logger = logging.getLogger("bot.panel")

DEFAULT_PANEL_URL = "https://agents.55bets.net"


class PanelError(Exception):
    """فشل عملية على اللوحة — رسالة جاهزة للعرض."""


class PanelNotConfigured(PanelError):
    """بيانات اللوحة غير مضبوطة في البيئة."""


class PanelAuthError(PanelError):
    """الخادم رفض الوصول (401/403) — يستدعي إعادة دخول تلقائية."""


def panel_config() -> dict:
    """قراءة إعدادات اللوحة من البيئة (بلا استثناء)."""
    return {
        "base": (os.getenv("BETS55_PANEL_URL") or DEFAULT_PANEL_URL)
        .strip()
        .rstrip("/"),
        "user": (os.getenv("BETS55_AGENT_USER") or "").strip(),
        "pass": (os.getenv("BETS55_AGENT_PASS") or "").strip(),
        "currency": (os.getenv("BETS55_CURRENCY") or "NSP").strip(),
        "country": (os.getenv("BETS55_COUNTRY") or "SY").strip(),
    }


def panel_configured() -> bool:
    c = panel_config()
    return bool(c["user"] and c["pass"])


def parse_wallet(raw: str) -> float:
    """تحويل «NSP 20892.50» إلى 20892.5."""
    m = re.search(r"(-?\d[\d,]*(?:\.\d+)?)", str(raw or ""))

    if not m:
        return 0.0

    return float(m.group(1).replace(",", ""))


# [R6-PLUS13] حالة آخر تواصل مع اللوحة — تظهر في /ops
PANEL_STATE = {
    "last_ok": "",       # آخر تواصل ناجح (ISO)
    "last_error": "",    # آخر خطأ (نص مختصر)
    "last_error_at": "",
    "wallet": None,      # آخر رصيد محفظة معروف
    "available": None,
    "currency": "",
    "players": None,     # آخر عدد لاعبين معروف
}


def panel_state() -> dict:
    """نسخة من حالة اللوحة للعرض."""
    return dict(PANEL_STATE)


def _state_note_ok(**kw):
    PANEL_STATE["last_ok"] = datetime.now(timezone.utc).strftime(
        "%Y-%m-%d %H:%M",
    )
    PANEL_STATE["last_error"] = ""
    PANEL_STATE["last_error_at"] = ""

    for k, v in kw.items():
        if v is not None:
            PANEL_STATE[k] = v


def _state_note_err(err: str):
    PANEL_STATE["last_error"] = str(err)[:120]
    PANEL_STATE["last_error_at"] = datetime.now(timezone.utc).strftime(
        "%Y-%m-%d %H:%M",
    )


class PanelClient:
    """عميل لوحة الوكيل — جلسة واحدة مع إعادة دخول تلقائي."""

    def __init__(self, config: dict = None):
        self.cfg = config or panel_config()
        self._sess: "aiohttp.ClientSession | None" = None
        self._logged = False
        self._lock = asyncio.Lock()

    async def close(self):
        if self._sess and not self._sess.closed:
            await self._sess.close()

        self._sess = None
        self._logged = False

    # ---------------- أساسيات ----------------

    def _api(self, path: str) -> str:
        return f"{self.cfg['base']}/global/api/{path}"

    @staticmethod
    def _headers() -> dict:
        """هيدرز شبيهة بالمتصفح — بعض جدران الحماية ترفض عملاء المكتبات."""
        return {
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "X-Requested-With": "XMLHttpRequest",
            "Accept-Language": "en-GB,en;q=0.9",
        }

    @staticmethod
    def _proxy_url() -> str | None:
        """[PROXY-OUT] بروكسي صادر اختياري (env فقط — بلا ملفات)."""
        p = (os.getenv("BETS55_PROXY")
             or os.getenv("OUTBOUND_PROXY") or "").strip()
        return p or None

    def _new_session(self) -> "aiohttp.ClientSession":
        """جلسة جديدة عبر البروكسي إن ضُبط (socks5 عبر connector)."""
        timeout = aiohttp.ClientTimeout(total=30)
        proxy = self._proxy_url()
        connector = None

        if proxy and proxy.lower().startswith("socks"):
            if aiohttp_socks is None:
                raise PanelError(
                    "لدعم SOCKS5 ثبّت: pip install aiohttp-socks",
                )

            connector = aiohttp_socks.ProxyConnector.from_url(proxy)

        return aiohttp.ClientSession(
            timeout=timeout,
            cookie_jar=aiohttp.CookieJar(unsafe=True),
            connector=connector,
        )

    def _origin_headers(self) -> dict:
        h = self._headers()
        h["Origin"] = self.cfg["base"]
        h["Referer"] = f"{self.cfg['base']}/"
        h["User-Agent"] = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
        )
        return h

    async def _request(self, method: str, path: str, json_body=None):
        """طلب واحد — يرمي PanelError عند فشل الشبكة."""
        if aiohttp is None:
            raise PanelError("مكتبة aiohttp غير متوفرة")

        if self._sess is None or self._sess.closed:
            self._sess = self._new_session()

        url = self._api(path)
        headers = self._origin_headers()
        proxy = self._proxy_url()

        if proxy and proxy.lower().startswith("socks"):
            proxy = None  # socks يمر عبر connector الجلسة

        try:
            async with self._sess.request(
                method, url, json=json_body,
                headers=headers, proxy=proxy,
            ) as resp:
                text = await resp.text()

                if resp.status in (401, 403):
                    # تشخيص الحجب: جدار حماية/Cloudflare يرد HTML
                    head = text[:200].lstrip().lower()

                    if head.startswith(("<!doctype", "<html")):
                        logger.warning(
                            "[panel] HTTP %s من %s — رد HTML "
                            "(حجب جدار حماية/Cloudflare على هذه الشبكة)",
                            resp.status, path,
                        )
                        raise PanelAuthError(
                            "اللوحة تحجب الوصول من هذه الشبكة "
                            "(جدار حماية/Cloudflare) — جرب شبكة أخرى/VPN",
                        )

                    logger.warning(
                        "[panel] HTTP %s من %s — %s",
                        resp.status, path, text[:120],
                    )
                    raise PanelAuthError(
                        f"اللوحة رفضت الوصول (HTTP {resp.status})",
                    )

                if resp.status >= 500:
                    raise PanelError(f"خطأ من اللوحة ({resp.status})")

                try:
                    data = await resp.json(content_type=None)
                except Exception:
                    raise PanelError(f"رد غير متوقع ({resp.status})")

                return resp.status, data
        except asyncio.TimeoutError:
            raise PanelError("انتهت مهلة الاتصال باللوحة")
        except aiohttp.ClientError as exc:
            raise PanelError(f"تعذر الاتصال باللوحة: {type(exc).__name__}")

    @staticmethod
    def _unwrap(data) -> object:
        """استخراج result من غلاف {status, result}."""
        if not isinstance(data, dict):
            raise PanelError("رد غير مفهوم من اللوحة")

        if data.get("status") is not True:
            msg = ""

            res = data.get("result")

            if isinstance(res, dict):
                msg = str(res.get("message") or "")

            if not msg:
                notif = data.get("notification")

                if isinstance(notif, list) and notif:
                    first = notif[0]

                    if isinstance(first, dict):
                        msg = str(first.get("content")
                                  or first.get("message") or "")

            raise PanelError(msg or "رفضت اللوحة الطلب")

        res = data.get("result")

        # [PANEL-STR] جلسة منتهية قد ترد 200 + نص بدل البيانات —
        # نرفع استثناء مصادقة ليُعاد الدخول تلقائياً ويُعاد الطلب مرة
        if isinstance(res, str):
            raise PanelAuthError(
                f"رد غير متوقع من اللوحة ({res[:40] or 'فارغ'})",
            )

        return res

    async def _authed(self, method: str, path: str, json_body=None):
        """طلب بعد ضمان الدخول — إعادة دخول واحدة عند أي شبهة جلسة.

        [PANEL-STR] يشمل الرفض 401/403 وردّ «نتيجة نصية» — كلاهما
        يُجرّب بعد تسجيل دخول جديد مرة واحدة ثم يظهر الخطأ بوضوح.
        """
        async with self._lock:
            if not self._logged:
                await self.login()

            for attempt in (1, 2):
                try:
                    status, data = await self._request(
                        method, path, json_body,
                    )
                    result = self._unwrap(data)
                    _state_note_ok()
                    return result
                except PanelAuthError:
                    if attempt == 2:
                        _state_note_err("انتهت جلسة اللوحة")
                        raise

                    self._logged = False
                    await self.login()
                except PanelError as exc:
                    _state_note_err(exc)
                    raise

        raise PanelError("تعذر التواصل مع اللوحة")  # لا يُصل إليه

    # ---------------- الدخول ----------------

    async def login(self):
        if not panel_configured():
            raise PanelNotConfigured(
                "بيانات لوحة الوكيل غير مضبوطة (BETS55_AGENT_USER/PASS)",
            )

        try:
            status, data = await self._request(
                "POST", "User/signIn",
                {"username": self.cfg["user"], "password": self.cfg["pass"]},
            )
        except PanelError as exc:
            self._logged = False
            _state_note_err(exc)
            raise

        if status != 200:
            self._logged = False
            _state_note_err(f"HTTP {status} عند الدخول")
            raise PanelError("فشل تسجيل الدخول للوحة")

        res = data.get("result") if isinstance(data, dict) else None

        # اللوحة الحقيقية تعيد status:true حتى مع بيانات خاطئة
        # (result=false + notification error) — النجاح هو result فعلي.
        if data.get("status") is True and res not in (False, None):
            self._logged = True
            logger.info("[panel] تم الدخول للوحة الوكيل بنجاح")
            return True

        msg = ""

        if isinstance(res, dict):
            msg = str(res.get("message") or "")

        if not msg:
            notif = data.get("notification") \
                if isinstance(data, dict) else None

            if isinstance(notif, list) and notif \
                    and isinstance(notif[0], dict):
                msg = str(notif[0].get("content")
                          or notif[0].get("message") or "")

        self._logged = False
        err = f"بيانات الدخول غير صحيحة ({msg})" if msg \
            else "بيانات الدخول غير صحيحة — راجع BETS55_AGENT_USER/PASS"
        _state_note_err(err)
        raise PanelError(err)

    # ---------------- العمليات ----------------

    async def agent_info(self) -> dict:
        """معلومات الوكيل + رصيد محفظته."""
        res = await self._authed("GET", "User/get-current-user-info")

        if not isinstance(res, dict):  # [PANEL-STR] حزام أمان
            raise PanelError("رد معلومات الوكيل غير مفهوم")

        wallet = res.get("currentWallet") or ""
        available = res.get("availableWallet") or wallet
        info = {
            "username": res.get("username"),
            "affiliate_id": res.get("affiliateId"),
            "currency": res.get("mainCurrency")
            or self.cfg["currency"],
            "wallet": parse_wallet(wallet),
            "available": parse_wallet(available),
            "raw_available": str(available),
        }
        _state_note_ok(
            wallet=info["wallet"],
            available=info["available"],
            currency=info["currency"],
        )
        return info

    async def players(self) -> list:
        """قائمة لاعبي الوكيل."""
        res = await self._authed(
            "POST", "Player/getPlayersForCurrentAgent", {},
        )

        if isinstance(res, dict):
            rows = list(res.get("records") or [])
        else:
            rows = list(res or [])

        if rows:
            _state_note_ok(players=len(rows))

        return rows

    async def all_wallets(self) -> list:
        """[AGENT-FULL] محافظ الوكيل بكل العملات (متاح/رصيد/مكافآت/مجمّد)."""
        res = await self._authed("POST", "Agent/getAgentAllWallets", {})
        return list(res or [])

    async def last_wallet_tx(self) -> dict:
        """[AGENT-FULL] آخر حركة على محفظة الوكيل."""
        res = await self._authed("POST", "Agent/getAgentWallet", {})
        return res if isinstance(res, dict) else {}

    async def wallet_transactions(self, page: int = 1,
                                  limit: int = 10) -> list:
        """[AGENT-FULL] سجل حركات محفظة الوكيل."""
        res = await self._authed(
            "POST", "Agent/getAgentTransactionList",
            {"page": page, "limit": limit},
        )

        if isinstance(res, dict):
            return list(res.get("records") or [])

        return list(res or [])

    async def available_currencies(self) -> dict:
        """[AGENT-FULL] العملات المتاحة لحساب الوكيل."""
        res = await self._authed(
            "POST", "Agent/getAgentAvailableCurrencies", {},
        )
        return res if isinstance(res, dict) else {}

    async def find_player(self, username: str) -> dict | None:
        """بحث لاعب باسمه (مقارنة غير حساسة للحالة)."""
        q = (username or "").strip().lower()

        if not q:
            return None

        for p in await self.players():
            if str(p.get("username") or "").lower() == q:
                return p

        return None

    async def player_balance(self, player_id) -> float:
        """رصيد اللاعب الرئيسي."""
        res = await self._authed(
            "POST", "Player/getPlayerBalanceById", {"playerId": player_id},
        )

        if isinstance(res, list) and res:
            for entry in res:
                if entry.get("main"):
                    return float(entry.get("balance") or 0)

            return float(res[0].get("balance") or 0)

        if isinstance(res, dict):
            return float(res.get("balance") or 0)

        return 0.0

    async def register_player(
        self, username: str, password: str,
        currency: str = None, country_code: str = None,
    ) -> dict:
        """[PLAYER-CREATE] إنشاء لاعب — الصيغة الحقيقية المؤكدة حياً.

        الخادم يتوقع حرفياً:
            {"player": {"login", "password", "email", "parentId"}}
        login بدل userName، بريد فريد إلزامي (يُرفض المكرر)،
        وparentId = رقم الوكيل فقط (يُجلب من الحساب أو BETS55_PARENT_ID).
        (currency/country محفوظان للتوافق — الخادم لا يطلبهما)
        """
        # بريد عشوائي فريد — المكرر يرفض بـ«Duplicate email»
        email = f"p{secrets.token_hex(5)}@gmail.com"

        parent_id = (os.getenv("BETS55_PARENT_ID") or "").strip()

        if not parent_id:
            info = await self.agent_info()
            parent_id = str(info.get("affiliate_id") or "")

        if not parent_id:
            raise PanelError(
                "معرف الوكيل الأب غير معروف — عيّن BETS55_PARENT_ID",
            )

        body = {"player": {
            "login": username,
            "password": password,
            "email": email,
            "parentId": parent_id,
        }}

        await self._authed("POST", "Player/registerPlayer", body)

        # الخادم يعيد result=1 — التأكيد النهائي بجلب اللاعب
        player = await self.find_player(username)

        if player:
            return player

        raise PanelError("أُرسل الطلب لكن لم أستطع تأكيد إنشاء اللاعب")

    async def deposit_to_player(
        self, player_id, amount: float,
        comment: str = "", currency: str = None,
    ) -> dict:
        """تحويل رصيد من محفظة الوكيل إلى اللاعب."""
        if amount <= 0:
            raise PanelError("المبلغ يجب أن يكون أكبر من صفر")

        body = {
            "amount": amount,
            "comment": comment or "bot",
            "playerId": player_id,
            "currencyCode": currency or self.cfg["currency"],
        }

        res = await self._authed("POST", "Player/depositToPlayer", body)
        return {"ok": True, "result": res}

    async def withdraw_from_player(
        self, player_id, amount: float,
        comment: str = "", currency: str = None,
    ) -> dict:
        """سحب رصيد من اللاعب إلى محفظة الوكيل."""
        if amount <= 0:
            raise PanelError("المبلغ يجب أن يكون أكبر من صفر")

        body = {
            "amount": amount,
            "comment": comment or "bot",
            "playerId": player_id,
            "currencyCode": currency or self.cfg["currency"],
        }

        res = await self._authed("POST", "Player/withdrawFromPlayer", body)
        return {"ok": True, "result": res}


# عميل مشترك للبوت (يُنشأ عند الحاجة)
_panel_client: PanelClient | None = None


def get_panel() -> PanelClient:
    global _panel_client

    if _panel_client is None:
        _panel_client = PanelClient()

    return _panel_client
