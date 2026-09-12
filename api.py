"""
Web API + Mini App لبوت الشحن
=============================
[NEW 14] Web API بـ FastAPI يقرأ نفس قاعدة البيانات.
[NEW 15] صفحة Mini App (عرض الرصيد والعمليات) تعمل داخل تلجرام.

التشغيل:
    uvicorn api:app --host 0.0.0.0 --port 8000

ملاحظات أمنية:
- نقاط الكتابة (POST) تتطلب ترويسة X-API-Key المطابقة لـ API_KEY في .env
- صفحة Mini App محمية بتوقيع بسيط (hash) — للإنتاج استخدم
  التحقق الكامل من Telegram WebApp initData.
"""

import hashlib
import hmac
import html
import json
import os
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException, Query, Request
from fastapi.responses import HTMLResponse

load_dotenv()

API_KEY = os.getenv("API_KEY", "").strip()

import bot as b  # noqa: E402  (يستخدم نفس .env وقاعدة البيانات)

app = FastAPI(
    title="Bot Finance API",
    version="1.0",
    docs_url="/api/docs",
)


def _require_api_key(key: Optional[str]):
    if not API_KEY:
        raise HTTPException(
            status_code=503,
            detail="API_KEY غير مضبوط في .env — نقاط الكتابة معطلة.",
        )
    if not key or not hmac.compare_digest(key, API_KEY):
        raise HTTPException(status_code=401, detail="مفتاح API غير صالح.")


def _miniapp_token(telegram_id: int) -> str:
    return hashlib.sha256(
        f"{telegram_id}:{API_KEY}".encode()
    ).hexdigest()[:24]


@app.get("/api/health")
async def health():
    db = await b.get_db()
    try:
        cur = await db.execute("SELECT COUNT(*) AS c FROM users")
        users = (await cur.fetchone())["c"]
    finally:
        await db.close()
    return {"status": "ok", "users": users}


@app.get("/api/user/{telegram_id}")
async def get_user(
    telegram_id: int,
    x_api_key: Optional[str] = Header(default=None),
):
    """بيانات مستخدم (بدون كلمات المرور). [NEW 14]"""
    _require_api_key(x_api_key)

    user = await b.get_user(telegram_id)
    if not user:
        raise HTTPException(status_code=404, detail="المستخدم غير موجود.")

    return {
        "telegram_id": user["telegram_id"],
        "full_name": user["full_name"],
        "username": user["username"],
        "site_username": user["site_username"],
        "balance": float(user["balance"] or 0),
        "is_banned": bool(user["is_banned"]),
        "created_at": user["created_at"],
    }


@app.get("/api/user/{telegram_id}/transactions")
async def get_user_transactions(
    telegram_id: int,
    limit: int = Query(default=20, ge=1, le=100),
    x_api_key: Optional[str] = Header(default=None),
):
    """آخر عمليات المستخدم. [NEW 14]"""
    _require_api_key(x_api_key)

    user = await b.get_user(telegram_id)
    if not user:
        raise HTTPException(status_code=404, detail="المستخدم غير موجود.")

    db = await b.get_db()
    try:
        cur = await db.execute(
            "SELECT type, amount, note, created_at FROM transactions"
            " WHERE user_id = ? ORDER BY id DESC LIMIT ?",
            (user["id"], limit),
        )
        rows = await cur.fetchall()
    finally:
        await db.close()

    return {
        "transactions": [
            {
                "type": r["type"],
                "amount": float(r["amount"] or 0),
                "note": r["note"],
                "created_at": r["created_at"],
            }
            for r in rows
        ]
    }


@app.post("/api/balance/adjust")
async def adjust_balance(
    telegram_id: int,
    amount: float,
    x_api_key: Optional[str] = Header(default=None),
):
    """
    تعديل رصيد من الموقع مباشرة. [NEW 14]
    يستخدم نفس الدالة الذرية + سجل التدقيق في البوت.
    """
    _require_api_key(x_api_key)

    value = b.parse_amount(str(amount), allow_negative=True)
    if value is None:
        raise HTTPException(status_code=400, detail="مبلغ غير صالح.")

    result = await b.apply_balance_adjust(
        telegram_id, value, admin_id=0,  # 0 = تعديل عبر الـ API
    )

    if result is None:
        raise HTTPException(
            status_code=400,
            detail="المستخدم غير موجود أو الرصيد سيصبح سالبًا.",
        )

    old_balance, new_balance = result
    return {
        "ok": True,
        "old_balance": old_balance,
        "new_balance": new_balance,
    }


@app.get("/miniapp/{telegram_id}", response_class=HTMLResponse)
async def miniapp(
    telegram_id: int,
    t: str = Query(default=""),
):
    """[NEW 15] صفحة Mini App مبسطة (رصيد + آخر العمليات)."""
    if not API_KEY or t != _miniapp_token(telegram_id):
        raise HTTPException(status_code=403, detail="رابط غير صالح.")

    user = await b.get_user(telegram_id)
    if not user:
        raise HTTPException(status_code=404, detail="المستخدم غير موجود.")

    db = await b.get_db()
    try:
        cur = await db.execute(
            "SELECT type, amount, created_at FROM transactions"
            " WHERE user_id = ? ORDER BY id DESC LIMIT 10",
            (user["id"],),
        )
        rows = await cur.fetchall()
    finally:
        await db.close()

    tx_html = "".join(
        f"<li>"
        f"<span>{html.escape(str(r['type']))}</span>"
        f"<b>{b.money(r['amount'])}</b>"
        f"<small>{html.escape(str(r['created_at']))}</small>"
        f"</li>"
        for r in rows
    ) or "<li class='empty'>لا توجد عمليات</li>"

    return f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>حسابي</title>
<style>
  body {{ font-family: -apple-system, 'Segoe UI', Tahoma, sans-serif;
         background:#0e1621; color:#e8edf2; margin:0; padding:16px; }}
  .card {{ background:#182533; border-radius:14px; padding:18px;
          margin-bottom:14px; }}
  .balance {{ font-size:2.2em; font-weight:800; color:#4fc3f7; }}
  h1 {{ font-size:1.05em; color:#8fa4b3; margin:0 0 6px; }}
  ul {{ list-style:none; padding:0; margin:0; }}
  li {{ display:flex; justify-content:space-between; gap:8px;
       padding:9px 0; border-bottom:1px solid #223344; }}
  li small {{ color:#7a8fa0; }}
  li b {{ color:#81c784; }}
  .empty {{ color:#7a8fa0; justify-content:center; }}
</style>
</head>
<body>
  <div class="card">
    <h1>👤 {html.escape(user['full_name'] or '')}</h1>
    <div>الرصيد الحالي</div>
    <div class="balance">{b.money(user['balance'])}</div>
  </div>
  <div class="card">
    <h1>📜 آخر العمليات</h1>
    <ul>{tx_html}</ul>
  </div>
</body>
</html>"""


# ============================================================
# PAYMENT WEBHOOK [NEW 35]
# ============================================================

def _verify_webhook_signature(raw: bytes, signature: str) -> bool:
    """
    التحقق من توقيع HMAC-SHA256 (hex) لهيئة الطلب الخام.
    المفتاح: PAYMENT_WEBHOOK_SECRET في .env
    بدون مفتاح مضبوط: الويب هوك معطّل تماماً.
    """
    secret = os.getenv("PAYMENT_WEBHOOK_SECRET", "").strip()
    if not secret:
        return False

    expected = hmac.new(secret.encode(), raw, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, (signature or "").strip().lower())


SUCCESS_EVENTS = {
    "payment.succeeded",
    "payment.success",
    "payment_success",
    "payment.paid",
    "succeeded",
    "success",
    "paid",
}


@app.post("/api/webhooks/payment")
async def payment_webhook(request: Request):
    """
    استقبال إشعار الدفع من البوابة وإضافة الرصيد تلقائياً. [NEW 35]

    - التوقيع إلزامي (X-Signature = HMAC-SHA256 hex للجسم الخام)
    - Idempotency: نفس event_id لا يُحتسب مرتين أبداً
    - duplicate يُرجع 200 حتى تتوقف البوابة عن إعادة الإرسال
    - conflict (نفس id بمحتوى مختلف) يُرجع 409
    """
    raw = await request.body()

    if not _verify_webhook_signature(
        raw, request.headers.get("X-Signature", ""),
    ):
        raise HTTPException(status_code=401, detail="توقيع غير صالح.")

    try:
        data = json.loads(raw)
    except Exception:
        raise HTTPException(status_code=400, detail="JSON غير صالح.")

    if not isinstance(data, dict):
        raise HTTPException(status_code=400, detail="الحمولة يجب أن تكون كائن JSON.")

    event_id = str(
        data.get("event_id")
        or data.get("payment_id")
        or data.get("id")
        or ""
    ).strip()

    if not event_id:
        raise HTTPException(status_code=400, detail="event_id مفقود.")

    payload_hash = hashlib.sha256(raw).hexdigest()

    # أحداث غير الدفع الناجح: نؤكد الاستلام بدون إجراء (200)
    event = str(data.get("event") or data.get("type") or "").lower()
    if event and event not in SUCCESS_EVENTS:
        return {"status": "ignored", "event": event}

    telegram_id = data.get("telegram_id")
    if telegram_id is None:
        telegram_id = (data.get("metadata") or {}).get("telegram_id")

    try:
        telegram_id = int(telegram_id)
    except (TypeError, ValueError):
        raise HTTPException(status_code=400, detail="telegram_id غير صالح.")

    try:
        amount = float(data.get("amount"))
    except (TypeError, ValueError):
        raise HTTPException(status_code=400, detail="amount غير صالح.")

    status, balance = await b.credit_via_webhook(
        event_id=event_id,
        telegram_id=telegram_id,
        amount=amount,
        note=f"webhook={event_id}",
        payload_hash=payload_hash,
    )

    if status == "conflict":
        raise HTTPException(
            status_code=409,
            detail="نفس event_id بمحتوى مختلف.",
        )
    if status == "invalid":
        raise HTTPException(status_code=400, detail="مبلغ غير صالح.")
    if status == "user_not_found":
        raise HTTPException(status_code=404, detail="المستخدم غير موجود.")

    if status == "credited":
        # إشعار المستخدم والأدمن (أفضل جهد)
        try:
            await b.bot.send_message(
                telegram_id,
                "💰 <b>تم شحن رصيدك تلقائياً</b>\n\n"
                f"💵 المبلغ: {b.money(amount)}\n"
                f"💳 الرصيد الجديد: {b.money(balance)}\n"
                f"🧾 المرجع: <code>{event_id}</code>",
            )
        except Exception:
            pass

        try:
            await b.bot.send_message(
                int(os.getenv("ADMIN_USER_ID", "0")),
                "🌐 <b>شحن تلقائي عبر بوابة الدفع</b>\n\n"
                f"👤 <code>{telegram_id}</code>\n"
                f"💵 {b.money(amount)}\n"
                f"🧾 {event_id}",
            )
        except Exception:
            pass

    return {"status": status, "balance": balance}


# ============================================================
# SHAM CASH NOTIFICATION BRIDGE [R6-PLUS13]
# ============================================================

@app.post("/api/webhooks/shamcash")
async def shamcash_bridge(request: Request):
    """
    جسر إشعارات شام كاش [R6-PLUS13].

    يستقبل إشعار تحويل (من جسر مستقبلي: SMS→تليجرام أو تطبيق وسيط)
    وينشئ طلب شحن معلقاً كاملاً ببطاقة ✅/❌ للإدارة —
    **لا يضيف رصيداً تلقائياً إطلاقاً** (الاعتماد يدوي بضغطة).

    - نفس توقيع بوابة الدفع: X-Signature = HMAC-SHA256 hex للجسم الخام
      بمفتاح PAYMENT_WEBHOOK_SECRET.
    - الحمولة: {telegram_id, amount, txid, method?, sender?, raw?}
    - يعمل فقط إذا كانت ميزة dep_bridge مفعّلة من لوحة البوت.
    """
    raw = await request.body()

    if not _verify_webhook_signature(
        raw, request.headers.get("X-Signature", ""),
    ):
        raise HTTPException(status_code=401, detail="توقيع غير صالح.")

    try:
        data = json.loads(raw)
    except Exception:
        raise HTTPException(status_code=400, detail="JSON غير صالح.")

    if not isinstance(data, dict):
        raise HTTPException(status_code=400, detail="الحمولة يجب أن تكون كائن JSON.")

    telegram_id = data.get("telegram_id")

    try:
        telegram_id = int(telegram_id)
    except (TypeError, ValueError):
        raise HTTPException(status_code=400, detail="telegram_id غير صالح.")

    status, rid = await b.ingest_bridge_deposit(
        telegram_id,
        data.get("amount"),
        str(data.get("txid") or ""),
        method=str(data.get("method") or "شام كاش"),
        sender=str(data.get("sender") or ""),
        raw=str(data.get("raw") or ""),
    )

    if status == "disabled":
        raise HTTPException(
            status_code=503,
            detail="جسر شام كاش غير مفعّل (ميزة dep_bridge).",
        )
    if status == "invalid":
        raise HTTPException(status_code=400, detail="مبلغ أو رقم عملية غير صالح.")
    if status == "user_not_found":
        raise HTTPException(status_code=404, detail="المستخدم غير موجود.")

    return {"status": status, "request_id": rid}


# ============================================================
# PAYOUTS API [NEW 36]
# ============================================================

@app.get("/api/payouts")
async def list_payouts(
    status: str = Query(default="pending"),
    limit: int = Query(default=20, ge=1, le=100),
    x_api_key: Optional[str] = Header(default=None),
):
    """قائمة أوامر الدفع حسب الحالة. [NEW 36]"""
    _require_api_key(x_api_key)

    if status not in ("pending", "processing", "paid", "failed", "all"):
        raise HTTPException(status_code=400, detail="حالة غير معروفة.")

    db = await b.get_db()

    try:
        if status == "all":
            cur = await db.execute(
                "SELECT * FROM payouts ORDER BY id DESC LIMIT ?",
                (limit,),
            )
        else:
            cur = await db.execute(
                "SELECT * FROM payouts WHERE status = ?"
                " ORDER BY id DESC LIMIT ?",
                (status, limit),
            )
        rows = await cur.fetchall()
    finally:
        await db.close()

    return {
        "payouts": [
            {
                "id": r["id"],
                "user_tid": r["user_tid"],
                "amount": float(r["amount"]),
                "method": r["method"],
                "status": r["status"],
                "external_id": r["external_id"],
                "created_at": r["created_at"],
                "processed_at": r["processed_at"],
            }
            for r in rows
        ]
    }


@app.post("/api/payouts")
async def create_payout_api(
    request: Request,
    telegram_id: int,
    amount: float,
    destination: str = "",
    x_api_key: Optional[str] = Header(default=None),
):
    """
    إنشاء أمر دفع (سحب) من الموقع مباشرة. [NEW 36]

    - يخصم المبلغ ذرياً من رصيد المستخدم
    - يدعم Idempotency-Key header: نفس المفتاح لا ينشئ أمرين
    - لو فشل التحويل لاحقاً: mark_payout_failed_and_refund يرجع المبلغ
    """
    _require_api_key(x_api_key)

    value = b.parse_amount(str(amount))
    if value is None:
        raise HTTPException(status_code=400, detail="مبلغ غير صالح.")

    idem_key = (
        request.headers.get("Idempotency-Key", "").strip()[:100]
    )

    db = await b.get_db()

    try:
        await db.execute("BEGIN IMMEDIATE")

        # Idempotency: نفس المفتاح -> نفس النتيجة بدون إنشاء جديد
        if idem_key:
            cur = await db.execute(
                "SELECT user_tid, amount FROM webhook_events"
                " WHERE event_id = ?",
                (f"payout_api:{idem_key}",),
            )
            seen = await cur.fetchone()
            if seen:
                await db.rollback()
                return {
                    "status": "duplicate",
                    "telegram_id": seen["user_tid"],
                    "amount": float(seen["amount"]),
                }

        cur = await db.execute(
            "SELECT * FROM users WHERE telegram_id = ?",
            (telegram_id,),
        )
        user = await cur.fetchone()

        if not user:
            await db.rollback()
            raise HTTPException(status_code=404, detail="المستخدم غير موجود.")

        if user["is_banned"]:
            await db.rollback()
            raise HTTPException(status_code=400, detail="المستخدم محظور.")

        old_balance = b.round2(float(user["balance"] or 0))

        if old_balance < value:
            await db.rollback()
            raise HTTPException(status_code=400, detail="الرصيد غير كافٍ.")

        new_balance = b.round2(old_balance - value)

        await db.execute(
            "UPDATE users SET balance = ? WHERE telegram_id = ?",
            (new_balance, telegram_id),
        )

        cur = await db.execute(
            """
            INSERT INTO payouts
            (user_tid, amount, method, destination, status, created_by,
             created_at)
            VALUES (?, ?, 'api', ?, 'pending', 0, ?)
            """,
            (telegram_id, value, destination[:200], b.now_iso()),
        )
        payout_id = cur.lastrowid

        await db.execute(
            """
            INSERT INTO transactions
            (user_id, type, amount, note, created_at)
            VALUES (?, 'withdraw', ?, ?, ?)
            """,
            (
                user["id"],
                value,
                f"api_payout={payout_id}",
                b.now_iso(),
            ),
        )

        if idem_key:
            await db.execute(
                """
                INSERT INTO webhook_events
                (event_id, source, payload_hash, result, user_tid, amount,
                 created_at)
                VALUES (?, 'payout_api', '', 'created', ?, ?, ?)
                """,
                (f"payout_api:{idem_key}", telegram_id, value, b.now_iso()),
            )

        await db.commit()

    except HTTPException:
        try:
            await db.rollback()
        except Exception:
            pass
        raise
    except Exception:
        try:
            await db.rollback()
        except Exception:
            pass
        raise

    finally:
        await db.close()

    await b.audit(
        0, "api_payout_created",
        f"payout={payout_id}",
        f"user={telegram_id};amount={value};idem={idem_key or '-'}",
    )

    return {
        "status": "created",
        "payout_id": payout_id,
        "telegram_id": telegram_id,
        "amount": value,
        "old_balance": old_balance,
        "new_balance": new_balance,
    }


@app.post("/api/payouts/{payout_id}/mark_paid")
async def mark_payout_paid_api(
    payout_id: int,
    external_id: str = "",
    x_api_key: Optional[str] = Header(default=None),
):
    """تعليم أمر الدفع كمدفوع (idempotent). [NEW 36]"""
    _require_api_key(x_api_key)

    ok = await b.mark_payout_paid(payout_id, external_id=external_id)

    if not ok:
        raise HTTPException(
            status_code=409,
            detail="تمت معالجته مسبقاً أو غير موجود.",
        )

    await b.audit(0, "api_payout_paid", f"payout={payout_id}")
    return {"status": "paid", "payout_id": payout_id}


@app.post("/api/payouts/{payout_id}/mark_failed")
async def mark_payout_failed_api(
    payout_id: int,
    error: str = "provider_rejected",
    x_api_key: Optional[str] = Header(default=None),
):
    """فشل أمر الدفع + إرجاع المبلغ تلقائياً (idempotent). [NEW 36]"""
    _require_api_key(x_api_key)

    changed, refunded = await b.mark_payout_failed_and_refund(
        payout_id, error=error,
    )

    if not changed:
        raise HTTPException(
            status_code=409,
            detail="تمت معالجته مسبقاً أو غير موجود.",
        )

    await b.audit(0, "api_payout_failed", f"payout={payout_id}")
    return {
        "status": "failed",
        "payout_id": payout_id,
        "refunded": refunded,
    }
