"""
Telegram Bot - Fixed Version
============================
كل إصلاح معلّم بوسم [FIX n] المطابق لتقرير الفحص.

[FIX 1] /admin و /cancel مسجّلان قبل معالجات FSM حتى لا تبتلع الحالات الأوامر.
[FIX 2] أزرار القائمة تمسح حالة FSM عند الضغط عليها.
[FIX 3] safe_edit() تعالج خطأ "message is not modified" مع رجوع لإرسال رسالة جديدة.
[FIX 4] قائمة المشرفين محدودة بـ LIMIT مع تنبيه عند وجود المزيد.
[FIX 5] فهرس UNIQUE على site_username + فحص التكرار قبل الحفظ.
[FIX 6] إزالة الإغلاق المكرر لجلسة البوت (start_polling يغلقها تلقائياً).
[FIX 7] تقريب المبالغ لمنزلتين عشريتين في كل عمليات الرصيد (تقليل انجراف float)
        + رفض إدخال NaN/Infinity وأكثر من منزلتين.
[FIX 8] المشرف المحظور أو إيقاف البوت يمنعان صلاحيات الإدارة أيضاً.
[FIX 9] إحصائيات الأرصدة العامة للأدمن/المشرفين فقط؛ للمستخدم العادي إحصاء شخصي.
[FIX 10] أكواد الهدايا تُنشأ بدون أحرف ملتبسة (O/0/I/1) — الإدخال لا يزال يقبلها للأكواد القديمة.
[FIX 11] البوت يستجيب في الخاص فقط (فلتر على مستوى الـ Router).
[FIX 12] قائمة أكواد الهدايا بترقيم صفحات (10 لكل صفحة) بدل 50 رسالة.
[FIX 13] استخدام logging بدل print.

تحديثات النسخة المطورة:
[NEW 14] تصدير تقارير CSV (مستخدمين/عمليات/طلبات) بترميز يدعم العربية في Excel.
[NEW 15] إشعار جميع المشرفين ذوي صلاحية finance بالطلبات الجديدة.
[NEW 16] بث رسائل جماعي مع معاينة وتأكيد وتقرير نتائج.
[NEW 17] إدارة نصوص (الشروحات/العروض/الشروط) من لوحة الأدمن.
[NEW 18] زر "معلومات" في القائمة الرئيسية لعرض النصوص للمستخدمين.
[NEW 19] صلاحية جديدة reports للمشرفين.

خريطة التطوير الشاملة:
[NEW 20] تشفير كلمات مرور الموقع (Fernet) + زر استرجاع كلمة المرور.
[NEW 21] حماية من السبام (Throttling Middleware).
[NEW 22] سجل تدقيق إداري كامل + عرضه من اللوحة.
[NEW 23] نسخ احتياطي تلقائي يومي يُرسل للأدمن.
[NEW 24] تأكيد ثنائي للتعديلات المالية الكبيرة.
[NEW 25] انتهاء صلاحية الطلبات المعلقة تلقائياً بعد 24 ساعة.
[NEW 26] نظام عمولة شحن قابل للضبط من اللوحة.
[NEW 27] حدود شحن/سحب قابلة للضبط من اللوحة.
[NEW 28] ملخص يومي تلقائي يُرسل للأدمن.
[NEW 29] نظام إحالات (ref_X) مع مكافأة قابلة للضبط.
[NEW 30] سجل عمليات شخصي للمستخدم مع ترقيم صفحات.
[NEW 31] أزرار مبالغ سريعة للشحن.
[NEW 32] إيصالات PDF للعمليات المالية.
[NEW 33] تعدد لغات (عربي/إنجليزي) لرحلة المستخدم الأساسية.
[NEW 34] رسم بياني لنشاط آخر 14 يوماً (للأدمن).
[NEW 35] Payment Webhook مع توقيع HMAC + Idempotency كاملة (دفتر webhook_events).
[NEW 36] نظام Payouts: أمر دفع يُنشأ داخل معاملة الموافقة، حالات
         (pending/paid/failed) مع استرداد تلقائي مرة واحدة،
         وإدارة كاملة من اللوحة + API خارجي محمي.
[NEW 37] بحث مستخدمين + كارت شامل + قائمة بترقيم صفحات.
[NEW 38] طابور موحد + تذاكر دعم + مراسلة مستخدم من الإدارة.
[NEW 39] صلاحيات المشرف بالأزرار (تبديل ON/OFF).
[NEW 40] إيقاف مؤقت للمشرفين دون حذفهم.
[NEW 41] سقوف سحب يومية (لكل مستخدم + إجمالي).
[NEW 42] لوحة KPI حية قابلة للتحديث.
[NEW 43] تصدير ZIP شامل (CSV×4 + قاعدة البيانات).
[NEW 44] قوائم فرعية للوحة (إعدادات/أدوات).
[NEW 45] نافذة صيانة مجدولة تلقائية.
[NEW 46] تنبيهات ذكية دورية للأدمن.
[UI-1..5] شريط حالة حي، كلمة سر خلف Spoiler بحذف تلقائي، روابط القائمة، شاشة صيانة، ترقيم موحد.
[ADM-1..6] دفعات أكواد، موافقة مزدوجة للسحوبات الضخمة، إيقاف الخدمات منفرداً بسبب، ZIP يومي مجدول، نسخة احتياطية فورية بفحص سلامة.
[USR-1..4] تحويل رصيد P2P بسقف يومي، كشف حساب PDF، «تذاكري» للمستخدم، كود هدية من الرصيد باسترداد تلقائي بعد 7 أيام.
[USR2-1..7] طلباتي، إحالاتي+مشاركة، حملة مكافأة الإيداع، كود إعفاء عمولة، سحب سريع، فلتر السجل، تقييم الدعم.
[ADM2-1..7] بث مستهدف، ملاحظات على المستخدم، حصة مالية للمشرف، تقرير P&L شهري، سجل الويب هوك، حماية تلقائية، أداء المشرفين.
[ADM3-1..12] غرفة مراقبة (Mirror)، رسالة اختبار، آخر نشاط المشرفين، PIN تأكيد للعمليات الحساسة،
ردود جاهزة للتذاكر، ميزانية سحوبات يومية، تراجع عن تعديل رصيد، محاكي شحن، إخفاء الأرصدة عن المشرفين،
تنظيف بيانات قديمة، بث مجدول، تقرير أسبوعي تلقائي.
[ADM4-1..6] وسوم المستخدمين (CRM)، مسابقة الإحالات بجوائز تلقائية، اعتماد سحوبات تلقائي لقائمة الثقة،
لوحة إعلانات بتتبع قراءة، كشف شواذ فوري، تقرير محاسبي PDF.
[USR4-1..6] مستويات ولاء بخصم عمولة، دفتر وجهات سحب، مكافأة حضور يومي بسلسلة، منحنى رصيد PNG،
حاسبة شحن، تصدير بيانات ذاتي.
"""

import csv
import hashlib
import io
import os
import re
import asyncio
import json
import logging
import math
import secrets
import string
import sqlite3
import html
import time
import urllib.parse
from types import SimpleNamespace
import zipfile
from datetime import datetime, timezone, timedelta
from typing import Optional

import aiosqlite
from aiogram import Bot, Dispatcher, types, F, BaseMiddleware
from aiogram.types import (
    BotCommand,
    BotCommandScopeChat,
    BotCommandScopeDefault,
    BufferedInputFile,
)

try:  # [R6-PLUS12] ربط لوحة الوكيل
    import bets55_panel as ipanel
except ImportError:  # pragma: no cover
    ipanel = None

try:  # [R6-PLUS14] شام كاش — ربط QR وقراءة الحساب
    import sham_link as sham
except ImportError:  # pragma: no cover
    sham = None

try:  # [NEW 20] تشفير اختياري إذا كانت المكتبة متوفرة
    from cryptography.fernet import Fernet, InvalidToken
except ImportError:  # pragma: no cover
    Fernet = None
    InvalidToken = Exception

from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dotenv import load_dotenv


# ============================================================
# CONFIG
# ============================================================

load_dotenv()

logger = logging.getLogger("bot")  # [FIX 13]

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()

try:
    ADMIN_USER_ID = int(os.getenv("ADMIN_USER_ID", "0"))
except ValueError:
    ADMIN_USER_ID = 0

DB_PATH = os.getenv("DB_PATH", "bot.db")

if not BOT_TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN غير موجود في ملف .env")

if ADMIN_USER_ID <= 0:
    raise RuntimeError("ADMIN_USER_ID غير صالح في ملف .env")

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)

dp = Dispatcher()

# [FIX 11] البوت يعمل في المحادثات الخاصة فقط
dp.message.filter(F.chat.type == "private")
dp.callback_query.filter(F.message.chat.type == "private")


# [NEW 21] حماية من السبام: تجاهل الرسائل/الأزرار السريعة جدًا
class ThrottlingMiddleware(BaseMiddleware):

    def __init__(self, delay: float = 0.4):
        self.delay = delay
        self._last = {}

    async def __call__(self, handler, event, data):
        user = getattr(event, "from_user", None)
        uid = user.id if user else 0

        now = time.monotonic()
        if now - self._last.get(uid, 0.0) < self.delay:
            return  # تجاهل صامت

        if len(self._last) > 10_000:
            self._last.clear()

        self._last[uid] = now
        return await handler(event, data)


dp.message.middleware(ThrottlingMiddleware(0.4))
dp.callback_query.middleware(ThrottlingMiddleware(0.5))


# ============================================================
# CONSTANTS
# ============================================================

MAX_AMOUNT = 1_000_000

GIFTS_PAGE_SIZE = 10  # [FIX 12]

REPORT_ROW_LIMIT = 10_000  # [NEW 14] حد أقصى لصفوف تقارير CSV
BOT_VERSION = "5.18.17 (PMLINK)"  # إصلاح زر مال اللاعب (نمط aiogram3 + حد 64B) + نافذة زمنية لحساب حارس المحفظة
SCHEMA_VERSION = 6  # [R6-PLUS6] رقم مخطط/إصدار القاعدة

# [NEW 17] النصوص القابلة للإدارة من لوحة الأدمن
BOT_TEXTS = {
    "tutorials": "🎓 الشروحات",
    "offers": "🍀 العروض الحالية",
    "terms": "📜 الشروط والأحكام",
}

ALLOWED_SUPERVISOR_PERMISSIONS = {
    "users",
    "finance",
    "gifts",
    "reports",
    "all",
}

# [NEW 20] تشفير كلمات مرور الموقع
def _load_or_create_fernet():
    if Fernet is None:
        logger.error(
            "مكتبة cryptography غير مثبتة — ستُخزن كلمات المرور نصاً صريحاً! "
            "ثبّتها: pip install cryptography"
        )
        return None

    key_env = os.getenv("PASSWORD_ENCRYPTION_KEY", "").strip()
    if key_env:
        try:
            return Fernet(key_env.encode())
        except Exception:
            logger.warning(
                "PASSWORD_ENCRYPTION_KEY غير صالح — سيتم استخدام مفتاح ملفي."
            )

    key_file = os.path.join(
        os.path.dirname(os.path.abspath(DB_PATH)) or ".",
        "secret.key",
    )

    try:
        if os.path.exists(key_file):
            with open(key_file, "rb") as fh:
                return Fernet(fh.read().strip())

        key = Fernet.generate_key()
        with open(key_file, "wb") as fh:
            fh.write(key)
        try:
            os.chmod(key_file, 0o600)
        except Exception:
            pass
        logger.warning(
            "تم توليد مفتاح تشفير وحفظه في %s — احتفظ به، فقده يعني "
            "فقدان كلمات المرور المشفرة!", key_file,
        )
        return Fernet(key)

    except Exception as exc:
        logger.error("تعذر تجهيز مفتاح التشفير (%s) — تخزين بدون تشفير!", exc)
        return None


_fernet = _load_or_create_fernet()


def encrypt_password(plain: str) -> str:
    """[NEW 20] تشفير كلمة المرور قبل التخزين."""
    if _fernet is None:
        return plain
    return _fernet.encrypt(plain.encode()).decode()


def decrypt_password(stored) -> str:
    """[NEW 20] فك التشفير مع دعم كلمات المرور القديمة غير المشفرة."""
    if not stored:
        return ""
    stored = str(stored)
    if _fernet is not None:
        try:
            return _fernet.decrypt(stored.encode()).decode()
        except InvalidToken:
            return stored  # كلمة مرور قديمة (نص صريح)
    return stored


# [NEW 24/25/26/27/29] ثوابت وقيم افتراضية قابلة للضبط
DEFAULT_LIMITS = {
    "deposit_min": 1.0,
    "deposit_max": float(MAX_AMOUNT),
    "withdraw_min": 1.0,
    "withdraw_max": float(MAX_AMOUNT),
}

# [NEW 41] حقول الحدود والسقوف القابلة للضبط
LIM_FIELDS = set(DEFAULT_LIMITS) | {
    "daily_withdraw_per_user",
    "daily_withdraw_total",
    "transfer_daily_cap",  # [USR-1]
    "daily_wd_count",  # [R6-PLUS5] حد عدد طلبات السحب اليومي
}
CONFIRM_THRESHOLD_DEFAULT = 1000.0
REQUEST_EXPIRY_HOURS = 24

BOT_USERNAME = ""  # [NEW 29] يُملأ تلقائياً عند بدء التشغيل

# [NEW 33] نصوص رحلة المستخدم (عربي/إنجليزي)
STRINGS = {
    "welcome": {
        "ar": "مرحبا,كيف يمكنني مساعدتك اليوم :",  # [R6]
        "en": "Welcome {name}! 👋\n\nChoose an option:",
    },
    "maintenance": {  # [UI-4]
        "ar": "🚧 <b>نطوّر الخدمة حالياً</b>\n\nنعمل على تحسين البوت، نعود قريباً{end}",
        "en": "🚧 <b>Under maintenance</b>\n\nWe are upgrading the bot, back soon{end}",
    },
    "maint_announce": {  # [R6-PLUS7 E4] إعلان مسبق للصيانة
        "ar": ("🔔 <b>تنبيه صيانة مجدولة</b>\n\n"
               "سنتوقف مؤقتاً للصيانة اليوم من {s} إلى {e} بتوقيت UTC.\n"
               "شكراً لصبرك 🙏"),
        "en": ("🔔 <b>Scheduled maintenance</b>\n\n"
               "We will be briefly offline today from {s} to {e} UTC.\n"
               "Thank you for your patience 🙏"),
    },
    "rates_limits": {  # [R6-PLUS7 U32] الأسعار والحدود
        "ar": ("📊 <b>الأسعار والحدود</b>\n\n"
               "⭐ نقاط الولاء: <b>{ppu}</b> نقطة لكل 1$ شحن\n"
               "💸 عمولة السحب: <b>{fee}%</b>\n\n"
               "🛒 حدود الشحن: <b>{dmin} — {dmax}$</b>\n"
               "🏦 حدود السحب: <b>{wmin} — {wmax}$</b>\n"
               "📅 حد السحوبات اليومي: <b>{wcnt}</b>"),
        "en": ("📊 <b>Rates &amp; Limits</b>\n\n"
               "⭐ Loyalty points: <b>{ppu}</b> per 1$ deposit\n"
               "💸 Withdrawal fee: <b>{fee}%</b>\n\n"
               "🛒 Deposit limits: <b>{dmin} — {dmax}$</b>\n"
               "🏦 Withdrawal limits: <b>{wmin} — {wmax}$</b>\n"
               "📅 Daily withdrawal count cap: <b>{wcnt}</b>"),
    },
    "maint_until": {  # [UI-4]
        "ar": "\n⏰ نعود عند الساعة {t} (UTC)",
        "en": "\n⏰ Back at {t} (UTC)",
    },
    "pw_mask": {  # [UI-2]
        "ar": "🔑 حسابك في الموقع\n\n👤 الحساب: {u}\n🔒 كلمة السر: ••••••••\n\n⏳ تُحذف الرسالة تلقائياً بعد 30 ثانية.",
        "en": "🔑 Your site account\n\n👤 User: {u}\n🔒 Password: ••••••••\n\n⏳ Auto-deletes in 30s.",
    },
    "pw_revealed": {  # [UI-2]
        "ar": "🔑 حسابك في الموقع\n\n👤 الحساب: {u}\n🔒 كلمة السر: <tg-spoiler>{p}</tg-spoiler>\n\n👁 اضغط على النقاط لكشفها.\n⏳ تُحذف الرسالة تلقائياً بعد 30 ثانية.",
        "en": "🔑 Your site account\n\n👤 User: {u}\n🔒 Password: <tg-spoiler>{p}</tg-spoiler>\n\n👁 Tap the dots to reveal.\n⏳ Auto-deletes in 30s.",
    },
    "btn_reveal": {"ar": "👁 إظهار", "en": "👁 Reveal"},  # [UI-2]
    "btn_del_now": {"ar": "🗑 إخفاء الآن", "en": "🗑 Hide now"},  # [UI-2]
    "lnk_channel": {"ar": "📢 القناة", "en": "📢 Channel"},  # [UI-3]
    "lnk_site": {"ar": "🌐 الموقع", "en": "🌐 Website"},  # [UI-3]
    "lnk_support": {"ar": "💬 الدعم", "en": "💬 Support"},  # [UI-3]
    "pause_dep": {  # [ADM-3]
        "ar": "🛑 <b>الإيداعات متوقفة مؤقتاً</b>\n\n{reason}",
        "en": "🛑 <b>Deposits are paused</b>\n\n{reason}",
    },
    "pause_wd": {  # [ADM-3]
        "ar": "🛑 <b>السحوبات متوقفة مؤقتاً</b>\n\n{reason}",
        "en": "🛑 <b>Withdrawals are paused</b>\n\n{reason}",
    },
    "pause_default": {"ar": "حاول لاحقاً.", "en": "Please try later."},
    "btn_transfer": {"ar": "💸 تحويل رصيد", "en": "💸 Transfer"},  # [USR-1]
    "btn_mytickets": {"ar": "💬 تذاكري", "en": "💬 My tickets"},  # [USR-3]
    "ann_btn": {"ar": "📢 الإعلانات", "en": "📢 News"},  # [ADM4-4]
    "checkin_btn": {"ar": "🔥 حضور اليوم", "en": "🔥 Daily check-in"},  # [USR4-3]
    "tr_prompt_tid": {  # [USR-1]
        "ar": "💸 <b>تحويل رصيد</b>\n\nأرسل Telegram ID للمستلم:\n\nللإلغاء أرسل /cancel",
        "en": "💸 <b>Transfer balance</b>\n\nSend the recipient's Telegram ID:\n\n/cancel to abort",
    },
    "tr_prompt_amount": {  # [USR-1]
        "ar": "👤 المستلم: {name}\n💳 رصيدك: {bal}\n\nأرسل المبلغ:\n\nللإلغاء أرسل /cancel",
        "en": "👤 Recipient: {name}\n💳 Your balance: {bal}\n\nSend the amount:\n\n/cancel to abort",
    },
    "tr_confirm": {  # [USR-1]
        "ar": "📋 <b>تأكيد التحويل</b>\n\n👤 إلى: <code>{tid}</code> ({name})\n💵 المبلغ: {amount}\n\nهل أنت متأكد؟",
        "en": "📋 <b>Confirm transfer</b>\n\n👤 To: <code>{tid}</code> ({name})\n💵 Amount: {amount}\n\nAre you sure?",
    },
    "tr_done": {"ar": "✅ تم التحويل.\n💵 {amount} → <code>{tid}</code>", "en": "✅ Transfer complete.\n💵 {amount} → <code>{tid}</code>"},
    "tr_received": {"ar": "📥 <b>وصلتك حوالة</b>\n\n💵 {amount}\n👤 من: <code>{tid}</code>", "en": "📥 <b>You received a transfer</b>\n\n💵 {amount}\n👤 From: <code>{tid}</code>"},
    "tr_err_self": {"ar": "❌ لا يمكنك التحويل لنفسك.", "en": "❌ You cannot transfer to yourself."},
    "tr_err_notfound": {"ar": "❌ لا يوجد مستخدم بهذا المعرف.", "en": "❌ No user with this ID."},
    "tr_err_banned": {"ar": "❌ المستلم محظور.", "en": "❌ Recipient is banned."},
    "tr_err_insufficient": {"ar": "❌ رصيدك لا يكفي.", "en": "❌ Insufficient balance."},
    "tr_cap": {"ar": "🛑 سقف التحويل اليومي {cap}.\nالمتباح الآن: {left}", "en": "🛑 Daily transfer cap is {cap}.\nAvailable now: {left}"},
    "gift_own_btn": {"ar": "🎟 اصنع كود لصديق", "en": "🎟 Create gift code"},  # [USR-4]
    "gift_own_prompt": {  # [USR-4]
        "ar": "🎟 <b>كود هدية من رصيدك</b>\n\nرصيدك: {bal}\nأرسل مبلغ الهدية:\n\nللإلغاء أرسل /cancel",
        "en": "🎟 <b>Gift code from your balance</b>\n\nBalance: {bal}\nSend the gift amount:\n\n/cancel to abort",
    },
    "gift_own_confirm": {  # [USR-4]
        "ar": "سيُخصم {amount} من رصيدك ويتولد كود تشاركه مع صديقك.\n⏳ إن لم يُستخدم خلال 7 أيام يُلغى ويرجع المبلغ لرصيدك.\n\nهل تريد المتابعة؟",
        "en": "{amount} will be deducted and a shareable code generated.\n⏳ Unused codes expire after 7 days with auto-refund.\n\nContinue?",
    },
    "gift_own_done": {  # [USR-4]
        "ar": "🎁 كودك جاهز:\n\n<code>{code}</code>\n💵 القيمة: {amount}\n\n⏳ صلاحية 7 أيام — بعدها يُلغى ويرجع المبلغ تلقائياً.",
        "en": "🎁 Your code:\n\n<code>{code}</code>\n💵 Value: {amount}\n\n⏳ Valid 7 days — auto-refunded after.",
    },
    "gift_own_insufficient": {"ar": "❌ رصيدك لا يكفي لهذا المبلغ.", "en": "❌ Insufficient balance."},
    "tk_none": {"ar": "📭 لا توجد تذاكر سابقة.", "en": "📭 No tickets yet."},  # [USR-3]
    "tk_title": {"ar": "💬 <b>تذاكري</b>\n\n", "en": "💬 <b>My tickets</b>\n\n"},  # [USR-3]
    "tk_open": {"ar": "🟢 مفتوحة", "en": "🟢 Open"},  # [USR-3]
    "tk_answered": {"ar": "✅ مُجيبة", "en": "✅ Answered"},  # [USR-3]
    "tk_closed": {"ar": "➖ مغلقة", "en": "➖ Closed"},  # [USR-3]
    "tk_new": {"ar": "✉️ تذكرة جديدة", "en": "✉️ New ticket"},  # [USR-3]
    "pdf_unavailable": {"ar": "⚠️ خدمة PDF غير متاحة حالياً.", "en": "⚠️ PDF service unavailable."},  # [USR-2]
    "pdf_caption": {"ar": "🧾 كشف حساب — آخر {n} عملية\n💳 رصيدك: {bal}", "en": "🧾 Statement — last {n} transactions\n💳 Balance: {bal}"},  # [USR-2]
    "rq_title": {"ar": "📋 <b>طلباتي المالية</b>", "en": "📋 <b>My requests</b>"},  # [USR2-1]
    "rq_none": {"ar": "📭 لا توجد طلبات سابقة.", "en": "📭 No requests yet."},
    "rq_pending": {"ar": "🟡 معلق", "en": "🟡 Pending"},  # [USR2-1]
    "rq_approved": {"ar": "✅ مقبول", "en": "✅ Approved"},
    "rq_rejected": {"ar": "❌ مرفوض", "en": "❌ Rejected"},
    "rq_expired": {"ar": "⌛ منتهي", "en": "⌛ Expired"},
    "rq_awaiting": {"ar": "👁 بانتظار الإدارة", "en": "👁 Awaiting admin"},
    "rq_btn": {"ar": "📋 طلباتي", "en": "📋 Requests"},  # [USR2-1]
    "ref_btn": {"ar": "🤝 إحالاتي", "en": "🤝 My referrals"},  # [USR2-2]
    "ref_title": {"ar": "🤝 <b>إحالاتي</b>\n\n👥 العدد: {n}\n💰 أرباحك منهم: {earned}\n\n", "en": "🤝 <b>My referrals</b>\n\n👥 Count: {n}\n💰 Earned: {earned}\n\n"},
    "ref_none": {"ar": "📭 لا إحالات بعد — شارك رابطك وابدأ الربح!", "en": "📭 No referrals yet — share your link!"},
    "ref_share": {"ar": "📤 شارك رابطك", "en": "📤 Share link"},
    "hf_all": {"ar": "📂 الكل", "en": "📂 All"},  # [USR2-6]
    "hf_dep": {"ar": "💰 شحن", "en": "💰 Dep"},
    "hf_wd": {"ar": "🏦 سحب", "en": "🏦 WD"},
    "hf_tr": {"ar": "💸 تحويل", "en": "💸 Transf"},
    "hf_gift": {"ar": "🎁 هدايا", "en": "🎁 Gifts"},
    "wd_last": {"ar": "⚡ آخر مبلغ: {amt}", "en": "⚡ Last: {amt}"},  # [USR2-5]
    "rate_ask": {  # [USR2-7]
        "ar": "⭐ كيف كانت خدمة الدعم؟",
        "en": "⭐ How was our support?",
    },
    "rate_thanks": {"ar": "🙏 شكراً لتقييمك!", "en": "🙏 Thanks for your feedback!"},
    "rate_done": {"ar": "سبق تقييم هذه التذكرة.", "en": "Already rated."},
    "bonus_badge": {  # [USR2-3]
        "ar": "\n🎁 عرض الآن: مكافأة +{pct:g}% على كل شحن!",
        "en": "\n🎁 Live offer: +{pct:g}% bonus on every deposit!",
    },
    "promo_btn": {  # [USR2-4]
        "ar": "🎟 كود إعفاء من العمولة",
        "en": "🎟 Commission-free code",
    },
    "promo_prompt": {  # [USR2-4]
        "ar": "🎟 أرسل كود الإعفاء:\n\nشحنتك القادمة ستكون بلا عمولة.\nللإلغاء أرسل /cancel",
        "en": "🎟 Send your waiver code:\n\nYour next deposit will be commission-free.\n/cancel to abort",
    },
    "promo_ok": {  # [USR2-4]
        "ar": "✅ كود مفعّل! شحنتك القادمة <b>بلا عمولة</b>.\n\nأرسل مبلغ الشحن الآن:",
        "en": "✅ Code activated! Your next deposit is <b>commission-free</b>.\n\nSend the deposit amount now:",
    },
    "promo_bad": {  # [USR2-4]
        "ar": "❌ الكود غير صالح أو منتهي.",
        "en": "❌ Invalid or exhausted code.",
    },
    "banned": {
        "ar": "🚫 تم حظر حسابك من استخدام البوت.",
        "en": "🚫 Your account has been banned.",
    },
    "stopped": {
        "ar": "⛔ البوت متوقف حاليًا للصيانة.",
        "en": "⛔ The bot is under maintenance.",
    },
    "fallback": {
        "ar": "استخدم أزرار القائمة للمتابعة 👇",
        "en": "Please use the menu buttons to continue 👇",
    },
    "cancel_none": {
        "ar": "لا توجد عملية قيد التنفيذ.",
        "en": "No operation in progress.",
    },
    "cancel_done": {
        "ar": "❌ تم إلغاء العملية.",
        "en": "❌ Operation cancelled.",
    },
    "btn_profile": {"ar": "👤 حسابي", "en": "👤 My account"},
    "btn_services": {"ar": "🛠 الخدمات", "en": "🛠 Services"},
    "btn_stats": {"ar": "📊 الإحصائيات", "en": "📊 Statistics"},
    "btn_gift": {"ar": "🎁 كود هدية", "en": "🎁 Gift code"},
    "btn_info": {"ar": "ℹ️ معلومات", "en": "ℹ️ Info"},
    "btn_history": {"ar": "📜 سجلي", "en": "📜 My history"},
    "back": {"ar": "🔙 رجوع", "en": "🔙 Back"},
    "main_title": {"ar": "مرحبا,كيف يمكنني مساعدتك اليوم :", "en": "Main menu:"},  # [R6]
    "services_title": {
        "ar": "🛠 <b>الخدمات</b>\n\nاختر الخدمة المطلوبة:",
        "en": "🛠 <b>Services</b>\n\nChoose a service:",
    },
    "svc_create": {"ar": "🆕 إنشاء حساب جديد", "en": "🆕 Create account"},
    "svc_deposit_btn": {"ar": "💰 شحن الرصيد", "en": "💰 Deposit"},
    "svc_withdraw_btn": {"ar": "🏦 سحب الأموال", "en": "🏦 Withdraw"},
    "create_prompt": {
        "ar": "🆕 أرسل اسم المستخدم الذي تريد ربطه بحساب الموقع:",
        "en": "🆕 Send the username you want to link to your site account:",
    },
    "deposit_prompt": {
        "ar": "💰 أرسل المبلغ الذي تريد شحنه\n(بين {min} و {max}):",
        "en": "💰 Send the amount you want to deposit\n(between {min} and {max}):",
    },
    "withdraw_prompt": {
        "ar": "🏦 أرسل المبلغ الذي تريد سحبه\n(بين {min} و {max}):",
        "en": "🏦 Send the amount you want to withdraw\n(between {min} and {max}):",
    },
    "gift_prompt": {
        "ar": "🎁 <b>أكواد الهدايا</b>\n\nيرجى إدخال كود الهدية للاستفادة منه:",  # [R6]
        "en": "🎁 Send your 8-character gift code:",
    },
    "create_pw_prompt": {  # [R6-REV] كلمة المرور من المستخدم
        "ar": "🔐 ممتاز! الآن أرسل <b>كلمة المرور</b> التي تريدها لحسابك:\n(6 أحرف/أرقام على الأقل — بدون مسافات)\n\nللإلغاء أرسل /cancel",
        "en": "🔐 Great! Now send the <b>password</b> you want for your account:\n(at least 6 characters — no spaces)\n\nSend /cancel to abort",
    },
    "create_pw_invalid": {
        "ar": "❌ كلمة المرور ضعيفة — يجب 6 أحرف/أرقام على الأقل وبدون مسافات.\nحاول مجدداً:",
        "en": "❌ Weak password — at least 6 characters, no spaces.\nTry again:",
    },
    "create_taken": {
        "ar": "❌ اسم المستخدم محجوز مسبقًا من مستخدم آخر.\nاختر اسمًا مختلفًا.",
        "en": "❌ This username is already taken.\nChoose a different one.",
    },
    "create_done": {
        "ar": ("✅ <b>تم إنشاء بيانات الحساب بنجاح!</b>\n\n"
               "👤 اسم المستخدم: <code>{u}</code>\n"
               "🔑 كلمة المرور: <code>{p}</code>\n\n"
               "⚠️ احتفظ بكلمة المرور في مكان آمن."),
        "en": ("✅ <b>Your account was created successfully!</b>\n\n"
               "👤 Username: <code>{u}</code>\n"
               "🔑 Password: <code>{p}</code>\n\n"
               "⚠️ Keep your password in a safe place."),
    },
    "profile_title": {"ar": "👤 <b>حسابك</b>", "en": "👤 <b>My account</b>"},
    "profile_name": {"ar": "الاسم", "en": "Name"},
    "profile_tid": {"ar": "Telegram ID", "en": "Telegram ID"},
    "profile_site": {"ar": "اسم الموقع", "en": "Site username"},
    "profile_balance": {"ar": "الرصيد", "en": "Balance"},
    "profile_refs": {"ar": "أصدقاء دعوتهم", "en": "Friends invited"},
    "profile_invite": {"ar": "رابط الدعوة", "en": "Invite link"},
    "not_linked": {"ar": "غير مرتبط", "en": "Not linked"},
    "history_title": {"ar": "📜 <b>سجل عملياتك</b>", "en": "📜 <b>My transactions</b>"},
    "history_empty": {"ar": "📭 لا توجد عمليات بعد.", "en": "📭 No transactions yet."},
    "info_title": {
        "ar": "ℹ️ <b>معلومات ومساعدة</b>\n\nاختر ما تريد:",
        "en": "ℹ️ <b>Info & help</b>\n\nChoose:",
    },
    "lang_saved": {
        "ar": "✅ تم تغيير اللغة إلى العربية.",
        "en": "✅ Language changed to English.",
    },
    "send_password_btn": {"ar": "🔑 إرسال كلمة المرور", "en": "🔑 Send password"},
    "no_password": {
        "ar": "❌ لا يوجد حساب موقع مرتبط بحسابك.",
        "en": "❌ No site account is linked.",
    },
    "password_msg": {
        "ar": "🔑 بيانات حسابك في الموقع:\n\n👤 Username: {u}\n🔒 Password: {p}",
        "en": "🔑 Your site account credentials:\n\n👤 Username: {u}\n🔒 Password: {p}",
    },
    "btn_support": {"ar": "💬 الدعم", "en": "💬 Support"},
    "btn_rates": {"ar": "📊 الأسعار والحدود", "en": "📊 Rates &amp; Limits"},  # [R6-PLUS7]
    "btn_calc": {"ar": "🧮 حاسبة الشحن", "en": "🧮 Deposit calculator"},  # [V13]
    "balalert_btn": {  # [R6-PLUS10 U36]
        "ar": "🔔 تنبيه الرصيد", "en": "🔔 Low-balance alert",
    },
    "balalert_prompt": {  # [U36]
        "ar": ("🔔 <b>تنبيه نزول الرصيد</b>\n\n"
               "الحد الحالي: <b>{cur}</b>\n\n"
               "أرسل المبلغ الذي تريد أن أبلغك حين ينزل رصيدك تحته\n"
               "أرسل <code>0</code> لإلغاء التنبيه.\nللإلغاء أرسل /cancel"),
        "en": ("🔔 <b>Low-balance alert</b>\n\n"
               "Current threshold: <b>{cur}</b>\n\n"
               "Send the amount — I will notify you when your balance"
               " drops below it\nSend <code>0</code> to disable.\n"
               "Send /cancel to abort"),
    },
    "balalert_saved": {  # [U36]
        "ar": "✅ سأبلغك فور نزول رصيدك تحت <b>{v}</b>.",
        "en": "✅ I will notify you when your balance drops"
              " below <b>{v}</b>.",
    },
    "balalert_cleared": {  # [U36]
        "ar": "🗑 أُلغي تنبيه الرصيد.",
        "en": "🗑 Low-balance alert disabled.",
    },
    "balalert_fired": {  # [U36]
        "ar": "🔔 رصيدك <b>{bal}</b> نزل تحت حدّك ({thr}) — وقت الشحن 🛒",
        "en": "🔔 Your balance <b>{bal}</b> dropped below your"
              " threshold ({thr}) — time to top up 🛒",
    },
    "favamt_prompt": {  # [R6-PLUS10 U37]
        "ar": ("⭐ <b>مبلغك المفضل</b>\n\n"
               "أرسل المبلغ الذي تشحنه عادة ليظهر زرّه أولاً بشاشة"
               " الشحن\nأرسل <code>0</code> للحذف.\nللإلغاء أرسل /cancel"),
        "en": ("⭐ <b>Your usual amount</b>\n\n"
               "Send the amount you usually deposit — its button will"
               " appear first on the deposit screen\nSend <code>0</code>"
               " to remove.\nSend /cancel to abort"),
    },
    "favamt_saved": {  # [U37]
        "ar": "✅ صار مبلغك المفضل <b>{v}</b> — زره أول قائمة الشحن.",
        "en": "✅ Your usual amount is now <b>{v}</b> — its button"
              " comes first.",
    },
    "favamt_cleared": {  # [U37]
        "ar": "🗑 أُزيل المبلغ المفضل.",
        "en": "🗑 Usual amount removed.",
    },
    "receipt_line": {  # [V5]
        "ar": "\n🔔 <i>سيصلك إشعار فور اعتماد الطلب — لا داعي لإعادة الإرسال.</i>",
        "en": "\n🔔 <i>You will be notified once approved — no need to"
              " resubmit.</i>",
    },
    "tour_title": {"ar": "🎓 <b>جولة سريعة</b> ({n}/3)", "en": "🎓 <b>Quick tour</b> ({n}/3)"},  # [V4]
    "tour_next": {"ar": "⬅️ التالي", "en": "⬅️ Next"},
    "tour_skip": {"ar": "تخطي", "en": "Skip"},
    "tour_start": {"ar": "🚀 ابدأ الآن", "en": "🚀 Start now"},
    "support_prompt": {
        "ar": "💬 اكتب رسالتك للإدارة وسيتم الرد عليك هنا:",
        "en": "💬 Write your message to the admin team:",
    },
    "support_sent": {
        "ar": "✅ وصلت رسالتك للإدارة، سنرد عليك هنا قريباً.",
        "en": "✅ Message received! We will reply here soon.",
    },
    "support_reply": {
        "ar": "📩 <b>رد من الإدارة:</b>\n\n{msg}",
        "en": "📩 <b>Reply from support:</b>\n\n{msg}",
    },
}


# ============================================================
# HELPERS
# ============================================================

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def money(value) -> str:
    try:
        value = float(value)
        if value.is_integer():
            return str(int(value))
        return f"{value:.2f}"
    except Exception:
        return str(value)


def round2(value: float) -> float:
    """تقريب المبالغ المالية لمنزلتين عشريتين. [FIX 7]"""
    return round(float(value), 2)


def esc(value) -> str:
    """Escape HTML before sending user-controlled text with ParseMode.HTML."""
    return html.escape(str(value or ""))


def generate_password(length: int = 10) -> str:
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return "".join(secrets.choice(chars) for _ in range(length))


def generate_code(length: int = 8) -> str:
    # [FIX 10] استبعاد الأحرف الملتبسة O/0/I/1 من الأكواد الجديدة
    ambiguous = set("O0I1")
    chars = "".join(
        c for c in (string.ascii_uppercase + string.digits)
        if c not in ambiguous
    )
    return "".join(secrets.choice(chars) for _ in range(length))


def parse_amount(raw, allow_negative: bool = False) -> Optional[float]:
    """
    [FIX 7] تحويل نص إلى مبلغ صالح:
    - رقم محدود (ليس NaN/Infinity)
    - أكبر من 0 (أو غير صفري إذا سُمح بالسالب)
    - لا يتجاوز MAX_AMOUNT
    - بمنزلتين عشريتين كحد أقصى
    """
    try:
        value = float(str(raw or "").strip().replace(",", "."))
    except (TypeError, ValueError):
        return None

    if not math.isfinite(value):
        return None

    if allow_negative:
        if value == 0:
            return None
    else:
        if value <= 0:
            return None

    if abs(value) > MAX_AMOUNT:
        return None

    if round2(value) != value:
        return None  # أكثر من منزلتين عشريتين

    return round2(value)


async def safe_edit(
    message: types.Message,
    text: str,
    reply_markup=None,
):
    """
    [FIX 3] تعديل آمن للرسالة:
    - يتجاهل خطأ "message is not modified" (الضغط على نفس الزر مرتين)
    - يرجع لإرسال رسالة جديدة إذا تعذر التعديل
    """
    try:
        await message.edit_text(text, reply_markup=reply_markup)
    except Exception as exc:
        if "message is not modified" in str(exc).lower():
            return
        try:
            await message.answer(text, reply_markup=reply_markup)
        except Exception:
            logger.warning("تعذر عرض الرسالة: %s", exc)


# ============================================================
# DATABASE
# ============================================================

def init_db():
    conn = sqlite3.connect(DB_PATH)

    try:
        cur = conn.cursor()

        cur.execute("PRAGMA journal_mode=WAL")
        cur.execute("PRAGMA foreign_keys=ON")

        cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER UNIQUE NOT NULL,
            username TEXT DEFAULT '',
            full_name TEXT DEFAULT '',
            site_username TEXT,
            site_password TEXT,
            balance REAL DEFAULT 0,
            is_banned INTEGER DEFAULT 0,
            created_at TEXT NOT NULL
        )
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            type TEXT NOT NULL,
            amount REAL DEFAULT 0,
            note TEXT DEFAULT '',
            created_at TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
                ON DELETE CASCADE
        )
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS admin_settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS gift_codes (
            code TEXT PRIMARY KEY,
            amount REAL NOT NULL,
            used_by INTEGER DEFAULT NULL,
            created_at TEXT NOT NULL,
            used_at TEXT DEFAULT NULL
        )
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS supervisors (
            telegram_id INTEGER PRIMARY KEY,
            permissions TEXT DEFAULT '[]',
            created_at TEXT NOT NULL
        )
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS finance_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER NOT NULL,
            type TEXT NOT NULL,
            amount REAL NOT NULL,
            status TEXT DEFAULT 'pending',
            created_at TEXT NOT NULL,
            processed_at TEXT DEFAULT NULL,
            processed_by INTEGER DEFAULT NULL
        )
        """)

        # [NEW 17] نصوص البوت القابلة للتعديل
        cur.execute("""
        CREATE TABLE IF NOT EXISTS bot_texts (
            key TEXT PRIMARY KEY,
            value TEXT DEFAULT '',
            updated_at TEXT
        )
        """)

        for text_key in BOT_TEXTS:
            cur.execute(
                "INSERT OR IGNORE INTO bot_texts(key, value, updated_at)"
                " VALUES (?, '', ?)",
                (text_key, now_iso()),
            )

        # [NEW 22] سجل التدقيق الإداري
        cur.execute("""
        CREATE TABLE IF NOT EXISTS admin_audit (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            admin_id INTEGER NOT NULL,
            action TEXT NOT NULL,
            target TEXT DEFAULT '',
            details TEXT DEFAULT '',
            created_at TEXT NOT NULL
        )
        """)
        cur.execute(
            "CREATE INDEX IF NOT EXISTS idx_audit_created"
            " ON admin_audit(created_at)"
        )

        # [NEW 35] دفتر أحداث الويب هوك — أساس نظام Idempotency
        cur.execute("""
        CREATE TABLE IF NOT EXISTS webhook_events (
            event_id TEXT PRIMARY KEY,
            source TEXT DEFAULT 'payment_webhook',
            payload_hash TEXT DEFAULT '',
            result TEXT DEFAULT '',
            user_tid INTEGER,
            amount REAL,
            created_at TEXT NOT NULL
        )
        """)

        # [USR2-4] أكواد إعفاء العمولة
        cur.execute("""
        CREATE TABLE IF NOT EXISTS promo_codes (
            code TEXT PRIMARY KEY,
            uses_left INTEGER DEFAULT 1,
            created_by INTEGER DEFAULT 0,
            created_at TEXT NOT NULL
        )
        """)

        # [ADM3-6] سجل تعديلات الرصيد اليدوية (للتراجع)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS balance_adjustments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            admin_id INTEGER NOT NULL,
            target_tid INTEGER NOT NULL,
            amount REAL NOT NULL,
            note TEXT DEFAULT '',
            undone INTEGER DEFAULT 0,
            created_at TEXT NOT NULL
        )
        """)

        # [ADM3-9] ردود جاهزة للتذاكر
        cur.execute("""
        CREATE TABLE IF NOT EXISTS canned_replies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT DEFAULT '',
            body TEXT DEFAULT '',
            created_at TEXT NOT NULL
        )
        """)

        # [ADM4-1] وسوم المستخدمين (CRM)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS user_tags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER NOT NULL,
            tag TEXT NOT NULL,
            created_at TEXT NOT NULL,
            UNIQUE(telegram_id, tag)
        )
        """)
        cur.execute(
            "CREATE INDEX IF NOT EXISTS idx_tags_tid"
            " ON user_tags(telegram_id)"
        )

        # [ADM4-4] لوحة الإعلانات + تتبع القراءة
        cur.execute("""
        CREATE TABLE IF NOT EXISTS announcements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            created_by INTEGER DEFAULT 0,
            created_at TEXT NOT NULL,
            expires_at TEXT NOT NULL
        )
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS announcement_reads (
            announcement_id INTEGER NOT NULL,
            telegram_id INTEGER NOT NULL,
            read_at TEXT NOT NULL,
            UNIQUE(announcement_id, telegram_id)
        )
        """)

        # [USR4-3] الحضور اليومي (سلسلة الستريك)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS checkins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER NOT NULL,
            day TEXT NOT NULL,
            streak INTEGER DEFAULT 1,
            amount REAL DEFAULT 0,
            created_at TEXT NOT NULL,
            UNIQUE(telegram_id, day)
        )
        """)

        # [ADM4-3] قائمة الثقة للاعتماد التلقائي
        cur.execute("""
        CREATE TABLE IF NOT EXISTS auto_wd_whitelist (
            telegram_id INTEGER PRIMARY KEY,
            created_by INTEGER DEFAULT 0,
            created_at TEXT NOT NULL
        )
        """)

        # [USR4-2] دفتر وجهات السحب
        cur.execute("""
        CREATE TABLE IF NOT EXISTS payout_accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER NOT NULL,
            label TEXT DEFAULT '',
            destination TEXT NOT NULL,
            created_at TEXT NOT NULL,
            UNIQUE(telegram_id, destination)
        )
        """)

        # [USR4-6] سجل التصدير الذاتي (مرة كل 24 ساعة)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS my_exports (
            telegram_id INTEGER PRIMARY KEY,
            created_at TEXT NOT NULL
        )
        """)

        # [ADM2-2] ملاحظات الإدارة على المستخدمين
        cur.execute("""
        CREATE TABLE IF NOT EXISTS user_notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            target_tid INTEGER NOT NULL,
            author_id INTEGER NOT NULL,
            note TEXT DEFAULT '',
            created_at TEXT NOT NULL
        )
        """)
        cur.execute(
            "CREATE INDEX IF NOT EXISTS idx_notes_target"
            " ON user_notes(target_tid)"
        )

        # [NEW 36] أوامر الدفع الصادرة (Payouts)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS payouts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_tid INTEGER NOT NULL,
            amount REAL NOT NULL,
            method TEXT DEFAULT 'manual',
            destination TEXT DEFAULT '',
            status TEXT DEFAULT 'pending',
            external_id TEXT DEFAULT '',
            error TEXT DEFAULT '',
            created_by INTEGER DEFAULT 0,
            created_at TEXT NOT NULL,
            processed_at TEXT
        )
        """)
        cur.execute(
            "CREATE INDEX IF NOT EXISTS idx_payouts_status"
            " ON payouts(status)"
        )

        # [NEW 29/33] أعمدة الإحالة واللغة (ترحيل آمن للقواعد القديمة)
        for col_def in ("referrer_id INTEGER", "lang TEXT DEFAULT 'ar'"):
            try:
                cur.execute(f"ALTER TABLE users ADD COLUMN {col_def}")
            except sqlite3.OperationalError:
                pass  # العمود موجود مسبقاً

        # [NEW 40] عمود إيقاف المشرف المؤقت
        try:
            cur.execute(
                "ALTER TABLE supervisors"
                " ADD COLUMN suspended INTEGER DEFAULT 0"
            )
        except sqlite3.OperationalError:
            pass

        # [ADM2-3] الحصة المالية اليومية للمشرف (0 = غير محدودة)
        try:
            cur.execute(
                "ALTER TABLE supervisors"
                " ADD COLUMN daily_quota REAL DEFAULT 0"
            )
        except sqlite3.OperationalError:
            pass

        # [USR-4] صانع كود الهدية (هدايا المستخدمين)
        try:
            cur.execute(
                "ALTER TABLE gift_codes"
                " ADD COLUMN created_by INTEGER DEFAULT 0"
            )
        except sqlite3.OperationalError:
            pass

        # [NEW 38] تذاكر الدعم
        cur.execute("""
        CREATE TABLE IF NOT EXISTS support_tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_tid INTEGER NOT NULL,
            message TEXT DEFAULT '',
            status TEXT DEFAULT 'open',
            created_at TEXT NOT NULL,
            answered_at TEXT,
            answered_by INTEGER
        )
        """)
        cur.execute(
            "CREATE INDEX IF NOT EXISTS idx_tickets_status"
            " ON support_tickets(status)"
        )

        # [USR2-4] كود الإعفاء المرتبط بطلب الشحن
        try:
            cur.execute(
                "ALTER TABLE finance_requests"
                " ADD COLUMN promo_code TEXT DEFAULT ''"
            )
        except sqlite3.OperationalError:
            pass

        # [R6] ملاحظة الطلب (الطريقة/رقم العملية/حساب الاستلام)
        try:
            cur.execute(
                "ALTER TABLE finance_requests"
                " ADD COLUMN note TEXT DEFAULT ''"
            )
        except sqlite3.OperationalError:
            pass

        # [R6-PLUS2] أعمدة المستخدم الجديدة
        for _col in (
            "wd_daily_cap REAL DEFAULT 0",
            "points INTEGER DEFAULT 0",
            "hide_balance INTEGER DEFAULT 0",
            "last_winback TEXT DEFAULT ''",
            "ban_until TEXT",
            "quick_amounts TEXT DEFAULT ''",
            "anniv_gifts TEXT DEFAULT ''",
            "digest_enabled INTEGER DEFAULT 0",
            "ann_notify INTEGER DEFAULT 0",
            "last_dep_method TEXT DEFAULT ''",
            "last_wd_method TEXT DEFAULT ''",
        ):
            try:
                cur.execute(f"ALTER TABLE users ADD COLUMN {_col}")
            except sqlite3.OperationalError:
                pass

        # [R6-PLUS2] صورة الإعلان + وقت تذكير الطلب المعلق
        try:
            cur.execute(
                "ALTER TABLE announcements"
                " ADD COLUMN photo_file_id TEXT DEFAULT ''"
            )
        except sqlite3.OperationalError:
            pass

        try:
            cur.execute(
                "ALTER TABLE finance_requests"
                " ADD COLUMN remind_at TEXT DEFAULT ''"
            )
        except sqlite3.OperationalError:
            pass

        # [R6-PLUS2] تقييمات السحب
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS payout_ratings (
                payout_id INTEGER PRIMARY KEY,
                telegram_id INTEGER NOT NULL,
                stars INTEGER NOT NULL,
                created_at TEXT NOT NULL
            )
           """
        )

        # [R6-CH] جدولة النشر الدوري للقنوات والمجموعات
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS channel_posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id TEXT NOT NULL,
                kind TEXT NOT NULL,
                custom_text TEXT DEFAULT '',
                interval_hours REAL DEFAULT 0,
                at_time TEXT DEFAULT '',
                enabled INTEGER DEFAULT 1,
                last_sent TEXT DEFAULT '',
                created_at TEXT NOT NULL
            )
            """
        )

        # [USR2-7] تقييم المستخدم لخدمة الدعم (1-5)
        try:
            cur.execute(
                "ALTER TABLE support_tickets"
                " ADD COLUMN rating INTEGER"
            )
        except sqlite3.OperationalError:
            pass

        cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_transactions_user
        ON transactions(user_id)
        """)

        cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_transactions_type
        ON transactions(type)
        """)

        cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_finance_requests_status
        ON finance_requests(status)
        """)

        cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_finance_requests_user
        ON finance_requests(telegram_id)
        """)

        cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_fr_created
        ON finance_requests(created_at)
        """)

        cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_tx_created
        ON transactions(created_at)
        """)

        cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_users_ref
        ON users(referrer_id)
        """)

        cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_payouts_created
        ON payouts(created_at)
        """)

        # [FIX 5] لا يمكن لنفس اسم حساب الموقع أن يكون لدى مستخدمين اثنين
        # (فهرس جزئي: يُنشأ فقط إذا لم تكن هناك بيانات قديمة مكررة)
        try:
            cur.execute("""
            CREATE UNIQUE INDEX IF NOT EXISTS idx_users_site_username
            ON users(site_username)
            WHERE site_username IS NOT NULL AND site_username != ''
            """)
        except sqlite3.IntegrityError:
            logger.warning(
                "تعذر إنشاء فهرس site_username الفريد: "
                "توجد أسماء مكررة في قاعدة البيانات الحالية — "
                "يجب تنظيف التكرارات يدوياً."
            )

        cur.execute("""
        INSERT OR IGNORE INTO admin_settings(key, value)
        VALUES('bot_active', '1')
        """)

        conn.commit()

    finally:
        conn.close()


init_db()


async def get_db():
    db = await aiosqlite.connect(DB_PATH)
    db.row_factory = aiosqlite.Row
    await db.execute("PRAGMA foreign_keys=ON")
    return db


# ============================================================
# USERS
# ============================================================

async def get_user(telegram_id: int):
    db = await get_db()

    try:
        cur = await db.execute(
            "SELECT * FROM users WHERE telegram_id = ?",
            (telegram_id,),
        )
        row = await cur.fetchone()
        return dict(row) if row else None
    finally:
        await db.close()


async def get_user_by_site_username(site_username: str):
    """[FIX 5] البحث عن مستخدم باسم حساب الموقع."""
    db = await get_db()

    try:
        cur = await db.execute(
            "SELECT * FROM users WHERE site_username = ?",
            (site_username,),
        )
        row = await cur.fetchone()
        return dict(row) if row else None
    finally:
        await db.close()


async def get_user_by_tg_username(username: str):
    """[R6-REV] البحث عن مستخدم بمعرف تلجرام (@username)."""
    db = await get_db()

    try:
        cur = await db.execute(
            "SELECT * FROM users WHERE LOWER(username) = LOWER(?)",
            (username,),
        )
        row = await cur.fetchone()
        return dict(row) if row else None
    finally:
        await db.close()


async def create_user(
    telegram_id: int,
    username: str = "",
    full_name: str = "",
):
    db = await get_db()

    try:
        cur = await db.execute(
            """
            INSERT OR IGNORE INTO users
            (telegram_id, username, full_name, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (telegram_id, username, full_name, now_iso()),
        )
        inserted = cur.rowcount

        await db.execute(
            """
            UPDATE users
            SET username = ?, full_name = ?
            WHERE telegram_id = ?
            """,
            (username, full_name, telegram_id),
        )

        await db.commit()
    finally:
        await db.close()

    # [R6-PLUS3] إشعار الأدمن بمستخدم جديد (ميزة قابلة للتفعيل)
    if inserted and telegram_id != ADMIN_USER_ID:
        try:
            if await feat_on("new_user_notify"):
                await bot.send_message(
                    ADMIN_USER_ID,
                    "🆕 <b>مستخدم جديد انضم للبوت</b>\n\n"
                    f"👤 {esc(full_name)}\n"
                    f"🔗 @{esc(username)}" if username else
                    f"👤 {esc(full_name)}\n"
                    f"🆔 <code>{telegram_id}</code>",
                )
        except Exception:
            pass


async def update_user(telegram_id: int, **kwargs):
    allowed_fields = {
        "username",
        "full_name",
        "site_username",
        "site_password",
        "balance",
        "is_banned",
        # [R6-PLUS2] أعمدة جولة الاقتراحات
        "wd_daily_cap",
        "points",
        "hide_balance",
        "last_winback",
        # [R6-PLUS5] جولة الإضافات الأخرى
        "quick_amounts",
        "anniv_gifts",
        # [R6-PLUS3] أعمدة جولة التحسينات
        "ban_until",
        "digest_enabled",
        "ann_notify",
        "last_dep_method",
        "last_wd_method",
    }

    if not kwargs:
        return

    invalid = set(kwargs) - allowed_fields
    if invalid:
        raise ValueError("حقول غير مسموحة: " + ", ".join(invalid))

    fields = ", ".join(f"{key} = ?" for key in kwargs)
    values = list(kwargs.values())
    values.append(telegram_id)

    db = await get_db()

    try:
        await db.execute(
            f"UPDATE users SET {fields} WHERE telegram_id = ?",
            values,
        )
        await db.commit()
    finally:
        await db.close()


async def add_transaction(
    user_id: int,
    transaction_type: str,
    amount: float,
    note: str = "",
):
    db = await get_db()

    try:
        await db.execute(
            """
            INSERT INTO transactions
            (user_id, type, amount, note, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (user_id, transaction_type, amount, note, now_iso()),
        )
        await db.commit()
    finally:
        await db.close()


# ============================================================
# SETTINGS
# ============================================================

async def get_setting(key: str) -> Optional[str]:
    db = await get_db()

    try:
        cur = await db.execute(
            "SELECT value FROM admin_settings WHERE key = ?",
            (key,),
        )
        row = await cur.fetchone()
        return row["value"] if row else None
    finally:
        await db.close()


async def set_setting(key: str, value: str):
    db = await get_db()

    try:
        await db.execute(
            "INSERT OR REPLACE INTO admin_settings(key, value) VALUES (?, ?)",
            (key, value),
        )
        await db.commit()
    finally:
        await db.close()


async def get_text(key: str) -> Optional[str]:
    """[NEW 17] قراءة نص قابل للإدارة من قاعدة البيانات."""
    db = await get_db()

    try:
        cur = await db.execute(
            "SELECT value FROM bot_texts WHERE key = ?",
            (key,),
        )
        row = await cur.fetchone()
        return row["value"] if row else None
    finally:
        await db.close()


async def set_text(key: str, value: str):
    """[NEW 17] حفظ نص قابل للإدارة."""
    db = await get_db()

    try:
        await db.execute(
            "INSERT OR REPLACE INTO bot_texts(key, value, updated_at)"
            " VALUES (?, ?, ?)",
            (key, value, now_iso()),
        )
        await db.commit()
    finally:
        await db.close()


def _parse_maintenance_window(window: str):
    """[UI-4] تحليل النافذة: (بداية_بالدقائق، نهاية_بالدقائق) أو None."""
    try:
        start_s, end_s = window.split("-")
        sh, sm = map(int, start_s.split(":"))
        eh, em = map(int, end_s.split(":"))
    except Exception:
        return None

    if not (0 <= sh < 24 and 0 <= sm < 60 and 0 <= eh < 24 and 0 <= em < 60):
        return None  # [NEW 45] قيم خارج النطاق تُتجاهل

    return sh * 60 + sm, eh * 60 + em


def _maintenance_end_if_active(window: str) -> str:
    """[UI-4] وقت الانتهاء HH:MM إن كانت النافذة فعّالة الآن، وإلا ''."""
    parsed = _parse_maintenance_window(window)

    if not parsed:
        return ""

    s_min, e_min = parsed
    now = datetime.now(timezone.utc)
    cur_min = now.hour * 60 + now.minute

    if s_min <= e_min:
        inside = s_min <= cur_min < e_min
    else:
        # نافذة تعبر منتصف الليل
        inside = cur_min >= s_min or cur_min < e_min

    if not inside:
        return ""

    return f"{e_min // 60:02d}:{e_min % 60:02d}"


async def _maintenance_active_now() -> bool:
    window = (await get_setting("maintenance_window") or "").strip()
    return bool(_maintenance_end_if_active(window))


async def _maint_fin_msg(message, state) -> bool:
    """[R6-PLUS7 E4] يمنع العمليات المالية خلال نافذة الصيانة.

    يعيد True إذا كانت النافذة فعّالة وأُرسلت رسالة الصيانة
    (وضع «مالية فقط» — في وضع الكل يمنع user_allowed أصلاً).
    """
    win = (await get_setting("maintenance_window") or "").strip()
    end = _maintenance_end_if_active(win)

    if not end:
        return False

    lang = await user_lang(message.from_user.id)
    await message.answer(tr(
        lang, "maintenance",
        end="\n\n⏰ " + tr(lang, "maint_until", t=end),
    ))
    await state.clear()
    return True


async def is_bot_active() -> bool:
    value = await get_setting("bot_active")
    if value == "0":
        return False

    # [NEW 45 + UI-4] نافذة الصيانة المجدولة (بتوقيت UTC)
    if await _maintenance_active_now():
        # [R6-PLUS7 E4] نطاق «مالية فقط»: التنقل يعمل والمالية تُمنع
        scope = (await get_setting("maintenance_scope") or "all").strip()

        if scope != "finance":
            return False

    return True


_maintenance_notice_ts: dict = {}


def _maintenance_notice_ok(telegram_id: int) -> bool:
    """[UI-4] رسالة الصيانة مرة واحدة كل 60 ثانية لكل مستخدم كحد أقصى."""
    now = time.monotonic()

    if time.monotonic() - _maintenance_notice_ts.get(telegram_id, 0.0) < 60:
        return False

    _maintenance_notice_ts[telegram_id] = now
    return True


# ============================================================
# PERMISSIONS
# ============================================================

async def is_admin_or_supervisor(
    telegram_id: int,
    required_perm: Optional[str] = None,
) -> bool:

    # الأدمن الرئيسي يتجاوز كل الفحوصات
    if telegram_id == ADMIN_USER_ID:
        return True

    # [FIX 8] المشرف المحظور أو توقف البوت يمنعان صلاحيات الإدارة
    if await is_banned(telegram_id):
        return False

    if not await is_bot_active():
        return False

    db = await get_db()

    try:
        cur = await db.execute(
            "SELECT permissions, suspended FROM supervisors"
            " WHERE telegram_id = ?",
            (telegram_id,),
        )
        row = await cur.fetchone()
    finally:
        await db.close()

    if not row:
        return False

    # [NEW 40] المشرف الموقوف مؤقتاً لا يملك صلاحيات
    if row["suspended"]:
        return False

    try:
        permissions = json.loads(row["permissions"] or "[]")
    except Exception:
        permissions = []

    if required_perm is None:
        return True

    return required_perm in permissions or "all" in permissions


async def is_banned(telegram_id: int) -> bool:
    user = await get_user(telegram_id)

    if not user:
        return False

    if user["is_banned"]:
        return True

    # [R6-PLUS3] حظر مؤقت بانتهاء تلقائي
    ban_until = (user["ban_until"] or "").strip() if "ban_until" in \
        user.keys() else ""

    if not ban_until:
        return False

    try:
        if datetime.fromisoformat(ban_until) > datetime.now(timezone.utc):
            return True
    except (ValueError, TypeError):
        pass

    db = await get_db()

    try:
        await db.execute(
            "UPDATE users SET ban_until = NULL WHERE telegram_id = ?",
            (telegram_id,),
        )
        await db.commit()
    finally:
        await db.close()

    return False


async def ensure_user(message: types.Message):
    await create_user(
        message.from_user.id,
        message.from_user.username or "",
        message.from_user.full_name or "",
    )


async def user_allowed(
    telegram_id: int,
    notify_message: Optional[types.Message] = None,
) -> bool:

    if telegram_id == ADMIN_USER_ID:
        return True

    if await is_banned(telegram_id):
        if notify_message:
            lang = await user_lang(telegram_id)
            await notify_message.answer(tr(lang, "banned"))
        return False

    if not await is_bot_active():
        if notify_message and _maintenance_notice_ok(telegram_id):
            lang = await user_lang(telegram_id)

            # [UI-4] تمييز: إيقاف يدوي أم نافذة صيانة مع وقت العودة
            window = (await get_setting("maintenance_window") or "").strip()
            end = _maintenance_end_if_active(window)

            if end:
                key, end_txt = "maintenance", tr(lang, "maint_until", t=end)
            else:
                key, end_txt = "stopped", ""

            await notify_message.answer(tr(lang, key, end=end_txt))

        return False

    return True


async def get_finance_staff_ids() -> list:
    """
    [NEW 15] قائمة من يستحق إشعاراً مالياً:
    الأدمن الرئيسي + المشرفون غير المحظورين ذوو صلاحية finance/all.
    """
    ids = [ADMIN_USER_ID]

    db = await get_db()

    try:
        cur = await db.execute(
            "SELECT telegram_id, permissions FROM supervisors"
        )
        rows = await cur.fetchall()
    finally:
        await db.close()

    for row in rows:
        try:
            perms = json.loads(row["permissions"] or "[]")
        except Exception:
            perms = []

        if "finance" not in perms and "all" not in perms:
            continue

        if await is_banned(row["telegram_id"]):
            continue

        ids.append(row["telegram_id"])

    return ids


async def notify_finance_staff(
    text: str,
    request_id: int,
    exclude_id: Optional[int] = None,
):
    """[NEW 15] إرسال إشعار مالي مع أزرار المعالجة لكل الفريق المالي."""
    show_card = await feat_on("quick_card")  # [AUDIT2]

    for staff_id in await get_finance_staff_ids():
        if staff_id == exclude_id:
            continue
        try:
            await bot.send_message(
                staff_id,
                text,
                reply_markup=finance_request_kb(request_id, show_card),
            )
        except Exception as exc:
            logger.warning("تعذر إرسال إشعار مالي إلى %s: %s", staff_id, exc)

    await mirror(text)  # [ADM3-2] نسخة لغرفة المراقبة


async def audit(
    admin_id: int,
    action: str,
    target="",
    details="",
):
    """[NEW 22] تسجيل عملية إدارية في سجل التدقيق."""
    db = await get_db()
    try:
        await db.execute(
            "INSERT INTO admin_audit"
            " (admin_id, action, target, details, created_at)"
            " VALUES (?, ?, ?, ?, ?)",
            (
                admin_id,
                action,
                str(target)[:100],
                str(details)[:300],
                now_iso(),
            ),
        )
        await db.commit()
    finally:
        await db.close()


async def get_float_setting(key: str, default: float) -> float:
    try:
        value = float(await get_setting(key))
        if math.isfinite(value):
            return value
    except (TypeError, ValueError):
        pass
    return default


async def amount_limits(kind: str) -> dict:
    """[NEW 27] حدود المبالغ الفعلية (من الإعدادات مع قيم افتراضية آمنة)."""
    default_min = DEFAULT_LIMITS.get(f"{kind}_min", 1.0)
    default_max = DEFAULT_LIMITS.get(f"{kind}_max", float(MAX_AMOUNT))

    mn = await get_float_setting(f"{kind}_min", default_min)
    mx = await get_float_setting(f"{kind}_max", default_max)

    mn = max(0.01, min(mn, float(MAX_AMOUNT)))
    mx = max(0.01, min(mx, float(MAX_AMOUNT)))
    if mn > mx:
        mn, mx = mx, mn
    return {"min": mn, "max": mx}


async def user_lang(telegram_id: int) -> str:
    """[NEW 33] لغة المستخدم (افتراضي: العربية)."""
    user = await get_user(telegram_id)
    if user and user.get("lang") == "en":
        return "en"
    return "ar"


def tr(lang: str, key: str, **kw) -> str:
    """[NEW 33] ترجمة مفتاح مع تنسيق اختياري."""
    entry = STRINGS.get(key, {})
    template = entry.get(lang) or entry.get("ar") or key
    try:
        return template.format(**kw)
    except (KeyError, IndexError):
        return template


def build_receipt_pdf(title: str, rows: list):
    """
    [NEW 32] إيصال PDF (عناوين لاتينية لضمان التوافق،
    والرسالة المرافقة في تلجرام عربية).
    يعيد None إذا كانت مكتبة fpdf2 غير مثبتة.
    """
    try:
        from fpdf import FPDF
    except ImportError:
        logger.warning("مكتبة fpdf2 غير مثبتة — لن تُنشأ إيصالات PDF.")
        return None

    def clean(value):
        return str(value).encode("ascii", "replace").decode()

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("helvetica", "B", 16)
    pdf.cell(0, 12, clean(title), ln=1, align="C")
    pdf.ln(2)
    pdf.set_font("helvetica", "", 12)

    for label, value in rows:
        pdf.cell(0, 9, f"{clean(label)}: {clean(value)}", ln=1)

    pdf.ln(4)
    pdf.set_font("helvetica", "I", 9)
    pdf.cell(0, 8, clean("Generated automatically by the bot"), ln=1)

    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    return BufferedInputFile(
        pdf.output(),
        filename=f"receipt_{stamp}.pdf",
    )


# ============================================================
# PAYMENT WEBHOOK CREDIT + PAYOUTS [NEW 35 / NEW 36]
# ============================================================

async def credit_via_webhook(
    event_id: str,
    telegram_id: int,
    amount,
    note: str = "",
    payload_hash: str = "",
):
    """
    [NEW 35] إضافة رصيد من بوابة دفع بشكل ذري وغير قابل للتكرار.

    داخل معاملة واحدة: فحص الدفتر -> إضافة الرصيد -> قيد مالي ->
    تسجيل الحدث. نفس event_id لا يمكن أن يُحتسب مرتين مهما تكرر
    إرسال الويب هوك من البوابة.

    يعيد (status, balance):
    credited | duplicate | conflict | user_not_found | invalid
    """
    value = parse_amount(amount)
    if value is None or not event_id:
        return "invalid", None

    db = await get_db()

    try:
        await db.execute("BEGIN IMMEDIATE")

        cur = await db.execute(
            "SELECT payload_hash FROM webhook_events WHERE event_id = ?",
            (event_id,),
        )
        existing = await cur.fetchone()

        if existing:
            # نفس المعرّف: إما تكرار حقيقي أو تعارض (نفس id بمحتوى مختلف)
            if (
                payload_hash
                and existing["payload_hash"]
                and existing["payload_hash"] != payload_hash
            ):
                await db.rollback()
                return "conflict", None
            await db.rollback()
            return "duplicate", None

        cur = await db.execute(
            "SELECT * FROM users WHERE telegram_id = ?",
            (telegram_id,),
        )
        user = await cur.fetchone()

        if not user:
            await db.rollback()
            return "user_not_found", None

        new_balance = round2(float(user["balance"] or 0) + value)

        await db.execute(
            "UPDATE users SET balance = ? WHERE telegram_id = ?",
            (new_balance, telegram_id),
        )
        await db.execute(
            """
            INSERT INTO transactions
            (user_id, type, amount, note, created_at)
            VALUES (?, 'deposit', ?, ?, ?)
            """,
            (user["id"], value, note or f"webhook={event_id}", now_iso()),
        )
        await db.execute(
            """
            INSERT INTO webhook_events
            (event_id, source, payload_hash, result, user_tid, amount,
             created_at)
            VALUES (?, 'payment_webhook', ?, 'credited', ?, ?, ?)
            """,
            (event_id, payload_hash, telegram_id, value, now_iso()),
        )

        await db.commit()

        # [ADM4-5] كشف الشواذ: إيداع ضخم / فوري لحساب جديد
        asyncio.create_task(
            check_anomaly_deposit(telegram_id, value, user["created_at"])
        )

        return "credited", new_balance

    except Exception:
        try:
            await db.rollback()
        except Exception:
            pass
        raise

    finally:
        await db.close()


async def create_payout(
    user_tid: int,
    amount: float,
    destination: str = "",
    method: str = "manual",
    created_by: int = 0,
) -> int:
    """[NEW 36] إنشاء أمر دفع (المبلغ يكون قد خُصم من الرصيد مسبقاً)."""
    db = await get_db()

    try:
        cur = await db.execute(
            """
            INSERT INTO payouts
            (user_tid, amount, method, destination, status, created_by,
             created_at)
            VALUES (?, ?, ?, ?, 'pending', ?, ?)
            """,
            (user_tid, amount, method, destination, created_by, now_iso()),
        )
        payout_id = cur.lastrowid
        await db.commit()
        return payout_id
    finally:
        await db.close()


async def get_payout(payout_id: int):
    db = await get_db()

    try:
        cur = await db.execute(
            "SELECT * FROM payouts WHERE id = ?",
            (payout_id,),
        )
        row = await cur.fetchone()
        return dict(row) if row else None
    finally:
        await db.close()


async def _ask_payout_rating(user_tid: int, payout_id: int):
    """[R6-PLUS2] طلب تقييم تجربة السحب بعد التحويل."""
    b = InlineKeyboardBuilder()

    for stars in (5, 4, 3, 2, 1):
        b.button(text="⭐" * stars, callback_data=f"rate:{stars}:{payout_id}")

    b.adjust(5)

    try:
        await bot.send_message(
            user_tid,
            "💸 تم تحويل سحبك بنجاح!\n"
            "كيف تقيّم سرعة وتجربة السحب؟",
            reply_markup=b.as_markup(),
        )
    except Exception:
        pass


@dp.callback_query(F.data.startswith("rate:"))
async def rate_vote(cb: types.CallbackQuery, state: FSMContext):
    """[R6-PLUS2] استلام تقييم المستخدم."""

    try:
        stars = int(cb.data.split(":")[1])
        payout_id = int(cb.data.split(":")[2])
    except (ValueError, IndexError):
        await cb.answer("تقييم غير صالح.", show_alert=True)
        return

    db = await get_db()

    try:
        await db.execute(
            "INSERT OR REPLACE INTO payout_ratings"
            " (payout_id, telegram_id, stars, created_at)"
            " VALUES (?, ?, ?, ?)",
            (payout_id, cb.from_user.id, stars, now_iso()),
        )
        await db.commit()
    finally:
        await db.close()

    await cb.answer("شكراً لتقييمك! 🌟", show_alert=True)


async def mark_payout_paid(
    payout_id: int,
    external_id: str = "",
    admin_id: int = 0,
) -> bool:
    """
    [NEW 36] تعليم أمر دفع كمدفوع — انتقال حالة واحد فقط
    (pending/processing -> paid). الاستدعاء المتكرر لا يفعل شيئاً.
    """
    db = await get_db()

    try:
        cur = await db.execute(
            """
            UPDATE payouts
            SET status = 'paid',
                external_id = ?,
                processed_at = ?
            WHERE id = ?
              AND status IN ('pending', 'processing')
            """,
            (external_id, now_iso(), payout_id),
        )
        changed = cur.rowcount
        await db.commit()
        return changed == 1
    finally:
        await db.close()


async def mark_payout_failed_and_refund(
    payout_id: int,
    error: str = "",
    admin_id: int = 0,
):
    """
    [NEW 36] فشل أمر الدفع: إرجاع المبلغ للمستخدم داخل نفس المعاملة،
    ومرة واحدة فقط. يعيد (changed, refunded_amount).
    """
    db = await get_db()

    try:
        await db.execute("BEGIN IMMEDIATE")

        cur = await db.execute(
            "SELECT * FROM payouts WHERE id = ?",
            (payout_id,),
        )
        payout = await cur.fetchone()

        if not payout:
            await db.rollback()
            return False, None

        cur = await db.execute(
            """
            UPDATE payouts
            SET status = 'failed',
                error = ?,
                processed_at = ?
            WHERE id = ?
              AND status IN ('pending', 'processing')
            """,
            (error[:200], now_iso(), payout_id),
        )

        if cur.rowcount != 1:
            # مدفوعة أو فاشلة مسبقاً — لا استرداد مزدوج
            await db.rollback()
            return False, None

        ucur = await db.execute(
            "SELECT * FROM users WHERE telegram_id = ?",
            (payout["user_tid"],),
        )
        user = await ucur.fetchone()

        refunded_amount = None

        if user:
            refund = round2(float(payout["amount"]))
            new_balance = round2(
                float(user["balance"] or 0) + refund
            )
            await db.execute(
                "UPDATE users SET balance = ? WHERE telegram_id = ?",
                (new_balance, payout["user_tid"]),
            )
            await db.execute(
                """
                INSERT INTO transactions
                (user_id, type, amount, note, created_at)
                VALUES (?, 'refund', ?, ?, ?)
                """,
                (
                    user["id"],
                    refund,
                    f"payout_{payout_id}_failed",
                    now_iso(),
                ),
            )
            refunded_amount = refund

        await db.commit()
        await audit(
            admin_id, "payout_failed",
            f"payout={payout_id}",
            f"refund={refunded_amount}",
        )
        return True, refunded_amount

    except Exception:
        try:
            await db.rollback()
        except Exception:
            pass
        raise

    finally:
        await db.close()


async def render_payouts_view():
    """[NEW 36] عرض أوامر الدفع المعلقة مع أزرار المعالجة."""

    db = await get_db()

    try:
        cur = await db.execute(
            """
            SELECT *
            FROM payouts
            WHERE status IN ('pending', 'processing')
            ORDER BY id
            LIMIT 10
            """
        )
        rows = await cur.fetchall()

        cur = await db.execute(
            """
            SELECT COUNT(*) AS c
            FROM payouts
            WHERE status IN ('pending', 'processing')
            """
        )
        total = (await cur.fetchone())["c"]
    finally:
        await db.close()

    if not rows:
        return (
            "🚀 <b>أوامر الدفع المعلقة:</b> 0"
            "\n\n📭 لا توجد مدفوعات معلقة.",
            back_kb("admin_finance"),
        )

    lines = [f"🚀 <b>أوامر الدفع المعلقة:</b> {total}\n"]
    kb = InlineKeyboardBuilder()

    for row in rows:
        lines.append(
            f"#{row['id']} | 👤 <code>{row['user_tid']}</code> | "
            f"💵 {money(row['amount'])} | {esc(row['method'])}"
            f"\n🕐 {esc(row['created_at'])}"
        )
        kb.button(
            text=f"✅ #{row['id']}",
            callback_data=f"payout_pay:{row['id']}",
        )
        kb.button(
            text=f"❌ #{row['id']}",
            callback_data=f"payout_fail:{row['id']}",
        )

    kb.button(text="🔙 رجوع", callback_data="admin_finance")

    sizes = [2] * len(rows) + [1]
    kb.adjust(*sizes)

    return "\n\n".join(lines), kb.as_markup()


# ============================================================
# FINANCE REQUESTS
# ============================================================

async def has_pending_finance_request(
    telegram_id: int,
    request_type: str,
) -> bool:

    db = await get_db()

    try:
        cur = await db.execute(
            """
            SELECT id
            FROM finance_requests
            WHERE telegram_id = ?
              AND type = ?
              AND status = 'pending'
            LIMIT 1
            """,
            (telegram_id, request_type),
        )
        row = await cur.fetchone()
        return bool(row)
    finally:
        await db.close()


async def create_finance_request(
    telegram_id: int,
    request_type: str,
    amount: float,
    promo_code: str = "",  # [USR2-4]
    note: str = "",  # [R6] الطريقة/رقم العملية/حساب الاستلام
) -> int:

    db = await get_db()

    try:
        cur = await db.execute(
            """
            INSERT INTO finance_requests
            (telegram_id, type, amount, status, promo_code, note,
             created_at)
            VALUES (?, ?, ?, 'pending', ?, ?, ?)
            """,
            (telegram_id, request_type, amount, promo_code or "",
             note or "", now_iso()),
        )
        request_id = cur.lastrowid
        await db.commit()

        # [EVDEP 5.18] نافذة تحقق حدثية لكل طلب شحن شام كاش
        if request_type == "deposit" and "شام كاش" in (note or ""):
            asyncio.create_task(_sham_verify_window(request_id))

        if request_type == "withdraw":  # [ADM4-5]
            asyncio.create_task(check_anomaly_withdraw(telegram_id))

            # [ADM4-3] اعتماد ودفعة تلقائية لقائمة الثقة
            asyncio.create_task(auto_process_withdraw(request_id))

        return request_id
    finally:
        await db.close()


async def process_finance_request(
    request_id: int,
    admin_id: int,
    approve: bool,
):

    db = await get_db()

    try:
        await db.execute("BEGIN IMMEDIATE")

        cur = await db.execute(
            "SELECT * FROM finance_requests WHERE id = ?",
            (request_id,),
        )
        request = await cur.fetchone()

        if not request:
            await db.rollback()
            return None, "not_found", None

        # [ADM-2] طلب بانتظار موافقة الأدمن:
        # الرفض لأي موظف، والاعتماد للأدمن الرئيسي فقط (يرقّيه ثم يعتمده)
        if request["status"] == "awaiting_admin":
            if approve and admin_id != ADMIN_USER_ID:
                await db.rollback()
                return request, "already_processed", None

            await db.execute(
                "UPDATE finance_requests SET status = 'pending'"
                " WHERE id = ? AND status = 'awaiting_admin'",
                (request_id,),
            )

        elif request["status"] != "pending":
            await db.rollback()
            return request, "already_processed", None

        # ---------- REJECT ----------

        if not approve:
            await db.execute(
                """
                UPDATE finance_requests
                SET status = 'rejected',
                    processed_at = ?,
                    processed_by = ?
                WHERE id = ?
                  AND status = 'pending'
                """,
                (now_iso(), admin_id, request_id),
            )

            # [R6-PLUS5] إعادة رصيد السحب المحتجز عند الرفض
            # [WDFIX 5.18.16] الإعادة بالإجمالي المحتجز (fee من النوتة)
            if "held=1" in (request["note"] or ""):
                _tid = request["telegram_id"]
                _m_gross = re.search(r"gross=([0-9.]+)",
                                     request["note"] or "")
                _refund = (float(_m_gross.group(1)) if _m_gross
                           else float(request["amount"]))

                await db.execute(
                    "UPDATE users SET balance = COALESCE(balance, 0) + ?"
                    " WHERE telegram_id = ?",
                    (_refund, _tid),
                )
                await db.execute(
                    "INSERT INTO transactions"
                    " (user_id, type, amount, note, created_at)"
                    " SELECT id, 'wd_refund', ?, ?, ? FROM users"
                    " WHERE telegram_id = ?",
                    (
                        _refund,
                        f"request={request_id}", now_iso(), _tid,
                    ),
                )

            await db.commit()
            await audit(  # [NEW 22]
                admin_id, "finance_reject",
                f"request={request_id}",
                f"amount={request['amount']}",
            )
            return request, "rejected", None

        # ---------- [ADM-2 + ADM2-3] الموافقة المزدوجة وحصة المشرف ----------
        if approve and admin_id != ADMIN_USER_ID and request["type"] == "withdraw":
            dual_threshold = await get_float_setting(
                "dual_approve_threshold", 0.0
            )

            req_amount = round2(float(request["amount"]))
            escalate = (
                dual_threshold > 0 and req_amount >= dual_threshold
            )  # عتبة عامة أو حصة المشرف — كلاهما يرفع للأدمن

            # [ADM2-3] حصة المشرف اليومية: تجاوزها يرفع للأدمن
            sup_cur = await db.execute(
                "SELECT daily_quota FROM supervisors"
                " WHERE telegram_id = ?",
                (admin_id,),
            )
            sup_row2 = await sup_cur.fetchone()

            if sup_row2 and float(sup_row2["daily_quota"] or 0) > 0:
                quota = float(sup_row2["daily_quota"])
                like_today = (
                    f"{datetime.now(timezone.utc):%Y-%m-%d}%"
                )
                used_cur = await db.execute(
                    """
                    SELECT COALESCE(SUM(amount), 0) AS s
                    FROM finance_requests
                    WHERE processed_by = ?
                      AND type = 'withdraw'
                      AND status IN ('approved', 'awaiting_admin')
                      AND created_at LIKE ?
                    """,
                    (admin_id, like_today),
                )
                used = float((await used_cur.fetchone())["s"])

                if round2(used + req_amount) > round2(quota):
                    escalate = True

            if escalate:
                await db.execute(
                    """
                    UPDATE finance_requests
                    SET status = 'awaiting_admin',
                        processed_at = ?,
                        processed_by = ?
                    WHERE id = ?
                    """,
                    (now_iso(), admin_id, request_id),
                )
                await db.commit()
                return request, "awaiting_admin", None

        # ---------- [ADM3-5] ميزانية السحوبات اليومية ----------
        if approve and request["type"] == "withdraw":
            budget = await get_float_setting("payout_budget_daily", 0.0)

            if budget > 0:
                like_today = (
                    f"{datetime.now(timezone.utc):%Y-%m-%d}%"
                )
                spent_cur = await db.execute(
                    "SELECT COALESCE(SUM(amount), 0) s FROM payouts"
                    " WHERE status IN ('pending','processing','paid')"
                    " AND created_at LIKE ?",
                    (like_today,),
                )
                spent = float((await spent_cur.fetchone())["s"])

                if round2(
                    spent + round2(float(request["amount"]))
                ) > round2(budget):
                    await db.rollback()
                    return request, "budget_exceeded", None

        # ---------- APPROVE ----------

        telegram_id = request["telegram_id"]
        amount = round2(float(request["amount"]))  # [FIX 7]
        commission = 0.0  # [NEW 26]
        payout_id = None  # [NEW 36]

        user_cur = await db.execute(
            "SELECT * FROM users WHERE telegram_id = ?",
            (telegram_id,),
        )
        user = await user_cur.fetchone()

        if not user:
            await db.rollback()
            return request, "user_not_found", None

        current_balance = round2(float(user["balance"] or 0))  # [FIX 7]

        if request["type"] == "deposit":
            # [USR2-4] كود إعفاء من العمولة (استهلاك ذرّي داخل المعاملة)
            promo_applied = ""
            promo_code = (request["promo_code"] or "").strip()

            if promo_code:
                pcur = await db.execute(
                    "SELECT uses_left FROM promo_codes"
                    " WHERE code = ? AND uses_left > 0",
                    (promo_code,),
                )

                if await pcur.fetchone():
                    pdec = await db.execute(
                        "UPDATE promo_codes"
                        " SET uses_left = uses_left - 1"
                        " WHERE code = ? AND uses_left > 0",
                        (promo_code,),
                    )

                    if pdec.rowcount == 1:
                        promo_applied = promo_code

            # [NEW 26] عمولة الشحن القابلة للضبط
            pct = max(
                0.0,
                min(
                    50.0,
                    await get_float_setting("commission_percent", 0.0),
                ),
            )

            if promo_applied:  # [USR2-4] الإعفاء الكامل
                commission = 0.0
            else:
                # [USR4-1] خصم مستوى الولاء يخفض نسبة العمولة
                loyal = await get_loyalty(telegram_id)
                pct = max(0.0, pct - loyal["discount"])
                commission = round2(amount * pct / 100.0)

            credited = round2(amount - commission)

            # [USR2-3] مكافأة الإيداع (حملة ترويجية)
            bonus = 0.0
            bonus_pct = await get_float_setting("bonus_percent", 0.0)

            if bonus_pct > 0:
                bonus = round2(credited * bonus_pct / 100.0)
                bonus_max = await get_float_setting("bonus_max", 0.0)

                if bonus_max > 0:
                    bonus = min(bonus, round2(bonus_max))

                if bonus > 0:
                    credited = round2(credited + bonus)

            new_balance = round2(current_balance + credited)  # [FIX 7]

            await db.execute(
                "UPDATE users SET balance = ? WHERE telegram_id = ?",
                (new_balance, telegram_id),
            )
            await db.execute(
                """
                INSERT INTO transactions
                (user_id, type, amount, note, created_at)
                VALUES (?, 'deposit', ?, ?, ?)
                """,
                (
                    user["id"],
                    credited,
                    f"approved_request={request_id};"
                    f"gross={amount};commission={commission}"
                    + (f";bonus={bonus:g}" if bonus > 0 else "")
                    + (f";promo={promo_applied}" if promo_applied else ""),
                    now_iso(),
                ),
            )

        elif request["type"] == "withdraw":
            # [R6-PLUS5] طلب محتجز رصيده لحظة الإنشاء — لا خصم هنا
            # [WDFIX 5.18.16] غير المحتجز: الخصم بالإجمالي (المبلغ +
            # عمولته) — العمولة تُحصَّل لا تُترك برصيد المستخدم
            _held = "held=1" in (request["note"] or "")
            _m_g2 = re.search(r"gross=([0-9.]+)", request["note"] or "")
            _gross = round2(float(_m_g2.group(1))) if _m_g2 else amount

            if not _held:
                if current_balance < _gross:
                    await db.rollback()
                    return request, "insufficient_balance", None

                new_balance = round2(current_balance - _gross)  # [FIX 7]

                await db.execute(
                    "UPDATE users SET balance = ? WHERE telegram_id = ?",
                    (new_balance, telegram_id),
                )
            await db.execute(
                """
                INSERT INTO transactions
                (user_id, type, amount, note, created_at)
                VALUES (?, 'withdraw', ?, ?, ?)
                """,
                (
                    user["id"],
                    amount,
                    f"approved_request={request_id}",
                    now_iso(),
                ),
            )

            # [NEW 36] أمر الدفع يُنشأ في نفس معاملة الخصم —
            # لا يمكن اعتماد سحب بدون أمر دفع مطابق أبداً.
            _wdm = re.search(r"dest=([^;]+)", request["note"] or "")
            _wd_dest = _wdm.group(1).strip() if _wdm else ""

            cur = await db.execute(
                """
                INSERT INTO payouts
                (user_tid, amount, method, destination, status, created_by,
                 created_at)
                VALUES (?, ?, 'manual', ?, 'pending', ?, ?)
                """,
                (telegram_id, round2(float(request["amount"])), _wd_dest,
                 admin_id, now_iso()),  # [WDFIX] الصافي للمستفيد دائماً
            )
            payout_id = cur.lastrowid

        else:
            await db.rollback()
            return request, "invalid_type", None

        # [R6-PLUS2] نقاط الولاء: كل 1$ شحن صافٍ = نقطة (قابلة للضبط)
        if request["type"] == "deposit" and await feat_on("points"):
            _rate = await get_float_setting("points_per_unit", 1.0)

            if _rate > 0 and credited > 0:
                _pts = int(round(credited * _rate))

                if _pts > 0:
                    await db.execute(
                        "UPDATE users SET points = COALESCE(points, 0)"
                        " + ? WHERE telegram_id = ?",
                        (_pts, telegram_id),
                    )
                    await db.execute(  # [R6-PLUS3] سجل النقاط
                        "INSERT INTO transactions"
                        " (user_id, type, amount, note, created_at)"
                        " VALUES (?, 'points_earn', ?, ?, ?)",
                        (
                            user["id"], float(_pts),
                            f"deposit#{request_id}", now_iso(),
                        ),
                    )

        await db.execute(
            """
            UPDATE finance_requests
            SET status = 'approved',
                processed_at = ?,
                processed_by = ?
            WHERE id = ?
              AND status = 'pending'
            """,
            (now_iso(), admin_id, request_id),
        )

        await db.commit()

        if request["type"] == "deposit":  # [ADM4-5]
            asyncio.create_task(
                check_anomaly_deposit(
                    telegram_id, amount, user["created_at"],
                )
            )

        await audit(  # [NEW 22]
            admin_id, "finance_approve",
            f"request={request_id}",
            f"type={request['type']};amount={request['amount']};"
            f"commission={commission}",
        )
        return request, "approved", payout_id

    except Exception:
        try:
            await db.rollback()
        except Exception:
            pass
        raise

    finally:
        await db.close()


async def apply_balance_adjust(
    telegram_id: int,
    amount: float,
    admin_id: int,
):
    """
    تنفيذ تعديل رصيد ذري مع قيد مالي وسجل تدقيق. [NEW 22/24]
    يعيد (الرصيد القديم، الجديد) أو None عند الفشل.
    """
    db = await get_db()

    try:
        await db.execute("BEGIN IMMEDIATE")

        cur = await db.execute(
            "SELECT * FROM users WHERE telegram_id = ?",
            (telegram_id,),
        )
        user = await cur.fetchone()

        if not user:
            await db.rollback()
            return None

        old_balance = round2(float(user["balance"] or 0))
        new_balance = round2(old_balance + amount)

        if new_balance < 0:
            await db.rollback()
            return None

        await db.execute(
            "UPDATE users SET balance = ? WHERE telegram_id = ?",
            (new_balance, telegram_id),
        )

        await db.execute(
            """
            INSERT INTO transactions
            (user_id, type, amount, note, created_at)
            VALUES (?, 'admin_adjust', ?, ?, ?)
            """,
            (user["id"], amount, f"admin={admin_id}", now_iso()),
        )

        # [ADM3-6] سجل قابل للتراجع
        await db.execute(
            """
            INSERT INTO balance_adjustments
            (admin_id, target_tid, amount, note, created_at)
            VALUES (?, ?, ?, '', ?)
            """,
            (admin_id, telegram_id, round2(amount), now_iso()),
        )

        await db.commit()

    except Exception:
        try:
            await db.rollback()
        except Exception:
            pass
        raise

    finally:
        await db.close()

    await audit(
        admin_id, "balance_adjust",
        telegram_id,
        f"{amount:+g} -> {new_balance}",
    )

    # [R6-NEW] إشعار المستخدم تلقائياً بتعديل رصيده (قابل للتعطيل
    # بالإعداد adjust_notify)
    if (await get_setting("adjust_notify") or "1") == "1":
        try:
            await bot.send_message(
                telegram_id,
                "💰 <b>تم تعديل رصيدك من قبل الإدارة</b>\n\n"
                f"{'📥 إضافة' if amount >= 0 else '📤 خصم'}: "
                f"<b>{money(abs(amount))}</b>\n"
                f"💳 رصيدك الجديد: <b>{money(new_balance)}</b>",
            )
        except Exception:
            pass

    return old_balance, new_balance


async def send_adjust_receipt(
    telegram_id: int,
    amount: float,
    old_balance: float,
    new_balance: float,
    admin_id: int,
):
    """[NEW 32] إيصال PDF لتعديل رصيد إداري."""
    receipt = build_receipt_pdf(
        "Balance Adjustment",
        [
            ("Telegram ID", telegram_id),
            ("Old balance", money(old_balance)),
            ("Adjustment", money(amount)),
            ("New balance", money(new_balance)),
            ("Date (UTC)", now_iso()),
            ("By admin", admin_id),
        ],
    )
    if receipt:
        try:
            await bot.send_document(
                telegram_id,
                receipt,
                caption="🧾 إيصال تعديل الرصيد",
            )
        except Exception as exc:
            logger.warning("تعذر إرسال إيصال التعديل: %s", exc)


# ============================================================
# GIFT CODES
# ============================================================

async def generate_unique_gift_code(amount: float) -> str:

    for _ in range(30):
        code = generate_code()

        db = await get_db()

        try:
            cur = await db.execute(
                "SELECT code FROM gift_codes WHERE code = ?",
                (code,),
            )
            exists = await cur.fetchone()

            if exists:
                continue

            await db.execute(
                """
                INSERT INTO gift_codes (code, amount, created_at)
                VALUES (?, ?, ?)
                """,
                (code, amount, now_iso()),
            )
            await db.commit()
            return code

        finally:
            await db.close()

    raise RuntimeError("تعذر إنشاء كود هدية فريد.")


async def redeem_gift_code(telegram_id: int, code: str):

    db = await get_db()

    try:
        await db.execute("BEGIN IMMEDIATE")

        cur = await db.execute(
            "SELECT * FROM gift_codes WHERE code = ?",
            (code,),
        )
        gift = await cur.fetchone()

        if not gift:
            await db.rollback()
            return False, "invalid", 0

        if gift["used_by"] is not None:
            await db.rollback()
            return False, "used", 0

        cur = await db.execute(
            "SELECT * FROM users WHERE telegram_id = ?",
            (telegram_id,),
        )
        user = await cur.fetchone()

        if not user:
            await db.rollback()
            return False, "user_not_found", 0

        amount = round2(float(gift["amount"]))  # [FIX 7]
        current_balance = round2(float(user["balance"] or 0))  # [FIX 7]
        new_balance = round2(current_balance + amount)  # [FIX 7]

        cur = await db.execute(
            """
            UPDATE gift_codes
            SET used_by = ?, used_at = ?
            WHERE code = ?
              AND used_by IS NULL
            """,
            (telegram_id, now_iso(), code),
        )

        if cur.rowcount != 1:
            await db.rollback()
            return False, "used", 0

        await db.execute(
            "UPDATE users SET balance = ? WHERE telegram_id = ?",
            (new_balance, telegram_id),
        )

        await db.execute(
            """
            INSERT INTO transactions
            (user_id, type, amount, note, created_at)
            VALUES (?, 'gift', ?, ?, ?)
            """,
            (user["id"], amount, f"code={code}", now_iso()),
        )

        await db.commit()
        return True, "success", amount

    except Exception:
        try:
            await db.rollback()
        except Exception:
            pass
        raise

    finally:
        await db.close()



# ============================================================
# FSM STATES
# ============================================================

class RegisterFSM(StatesGroup):
    site_username = State()
    site_password = State()  # [R6-REV] كلمة مرور يختارها المستخدم


class DepositFSM(StatesGroup):
    amount = State()
    txid = State()  # [R6] رقم العملية
    photo = State()  # [R6-NEW] صورة الإيصال (اختياري)


class WithdrawFSM(StatesGroup):
    account = State()  # [R6] حساب الاستلام
    amount = State()
    confirm = State()  # [R6-PLUS3] تأكيد السحب بالصافي
    dest_confirm = State()  # [R6-PLUS7 U31] تأكيد وجهة مشكوك بها


class GiftFSM(StatesGroup):
    code = State()


class AdminWdFeeFSM(StatesGroup):  # [R6-NEW] عمولة السحب
    value = State()


class AdminCooldownFSM(StatesGroup):  # [R6-NEW] تهدئة السحب
    value = State()


class AdminValSetFSM(StatesGroup):  # [AUDIT F5] إعدادات القيم
    value = State()


class AdminPhotoFSM(StatesGroup):  # [R6-PLUS9 V8] صورة الترحيب
    photo = State()


class UserBalAlertFSM(StatesGroup):  # [R6-PLUS10 U36] تنبيه الرصيد
    value = State()


class UserFavAmtFSM(StatesGroup):  # [R6-PLUS10 U37] مبلغ مفضل
    amount = State()


class PanelCreateFSM(StatesGroup):  # [R6-PLUS12] إنشاء لاعب باللوحة
    username = State()
    password = State()


class PanelMoneyFSM(StatesGroup):  # [R6-PLUS12] إيداع/سحب للاعب
    username = State()
    amount = State()


class QuickAmtFSM(StatesGroup):  # [R6-PLUS5] مبالغك السريعة
    value = State()


class SupportHoursFSM(StatesGroup):  # [R6-PLUS5] ساعات الدعم
    value = State()


class AdminTempBanFSM(StatesGroup):  # [R6-PLUS3] حظر مؤقت
    days = State()


class AdminUserCapFSM(StatesGroup):  # [R6-PLUS2] سقف سحب خاص
    value = State()


class AdminStaleFSM(StatesGroup):  # [R6-PLUS2] تذكير العالق
    value = State()


class AdminChPostFSM(StatesGroup):  # [R6-CH] نشر القنوات والمجموعات
    chat = State()
    text = State()
    value = State()


class AdminCreateUserFSM(StatesGroup):
    telegram_id = State()
    site_username = State()


class AdminBanFSM(StatesGroup):
    telegram_id = State()


class AdminAdjustBalanceFSM(StatesGroup):
    telegram_id = State()
    amount = State()


class AdminGiftCodeFSM(StatesGroup):
    amount = State()


class AdminSupervisorFSM(StatesGroup):
    telegram_id = State()
    permissions = State()


class AdminDeleteSupervisorFSM(StatesGroup):
    telegram_id = State()


class AdminBroadcastFSM(StatesGroup):  # [NEW 16 + ADM2-1]
    message = State()
    bal = State()  # [ADM2-1] حد أدنى للرصيد


class AdminEditTextFSM(StatesGroup):  # [NEW 17]
    value = State()


class AdminCommissionFSM(StatesGroup):  # [NEW 26]
    value = State()


class AdminLimitsFSM(StatesGroup):  # [NEW 27]
    value = State()


class AdminRefBonusFSM(StatesGroup):  # [NEW 29]
    value = State()


class SupportFSM(StatesGroup):  # [NEW 38]
    message = State()


class AdminSearchFSM(StatesGroup):  # [NEW 37]
    query = State()


class AdminMessageFSM(StatesGroup):  # [NEW 38]
    text = State()


class AdminTicketReplyFSM(StatesGroup):  # [NEW 38]
    text = State()


class AdminSuspendFSM(StatesGroup):  # [NEW 40]
    telegram_id = State()


class AdminMaintenanceFSM(StatesGroup):  # [NEW 45]
    value = State()


class AdminLinksFSM(StatesGroup):  # [UI-3] روابط القائمة
    value = State()


class AdminGiftBatchFSM(StatesGroup):  # [ADM-1] دفعة أكواد
    value = State()


class AdminPauseFSM(StatesGroup):  # [ADM-3] سبب إيقاف الخدمات
    reason_dep = State()
    reason_wd = State()


class AdminDualFSM(StatesGroup):  # [ADM-2] عتبة الموافقة المزدوجة
    value = State()


class AdminNoteFSM(StatesGroup):  # [ADM2-2] ملاحظة على مستخدم
    text = State()


class AdminMirrorFSM(StatesGroup):  # [ADM3-2] غرفة مراقبة
    value = State()


class AdminSimFSM(StatesGroup):  # [ADM3-7] محاكي الشحن
    amount = State()


class AdminPinFSM(StatesGroup):  # [ADM3-1] رمز التأكيد
    set_value = State()
    code = State()


class AdminCannedFSM(StatesGroup):  # [ADM3-9] ردود جاهزة
    value = State()


class AdminCleanFSM(StatesGroup):  # [ADM3-11] تنظيف قديم
    days = State()


class AdminBudgetFSM(StatesGroup):  # [ADM3-5] ميزانية السحوبات
    value = State()


class AdminBcastSchedFSM(StatesGroup):  # [ADM3-10] جدولة البث
    amount = State()
    time = State()


class AdminSupQuotaFSM(StatesGroup):  # [ADM2-3] حصة مالية للمشرف
    value = State()


class AdminBonusFSM(StatesGroup):  # [USR2-3] حملة مكافأة الإيداع
    value = State()


class AdminPromoFSM(StatesGroup):  # [USR2-4] كود إعفاء عمولة
    value = State()


class PromoCodeFSM(StatesGroup):  # [USR2-4] إدخال المستخدم للكود
    code = State()


class TransferFSM(StatesGroup):  # [USR-1] تحويل بين المستخدمين
    tid = State()
    amount = State()


class UserGiftFSM(StatesGroup):  # [USR-4] كود هدية من الرصيد
    amount = State()


# ============================================================
# KEYBOARDS
# ============================================================

def main_menu_kb(lang: str = "ar"):
    b = InlineKeyboardBuilder()
    b.button(text=tr(lang, "btn_profile"), callback_data="menu_profile")
    b.button(text=tr(lang, "btn_services"), callback_data="menu_services")
    b.button(text=tr(lang, "btn_stats"), callback_data="menu_stats")
    b.button(text=tr(lang, "btn_gift"), callback_data="menu_gift")
    b.button(text=tr(lang, "btn_info"), callback_data="menu_info")  # [NEW 18]
    b.button(text=tr(lang, "btn_history"), callback_data="my_history:0")  # [NEW 30]
    b.button(text=tr(lang, "btn_support"), callback_data="support_start")  # [NEW 38]
    b.button(text=tr(lang, "btn_mytickets"), callback_data="my_tickets")  # [USR-3]
    b.button(text=tr(lang, "ann_btn"), callback_data="ann_menu")  # [ADM4-4]
    b.button(text="🌐 EN/AR", callback_data="toggle_lang")  # [NEW 33]
    b.adjust(2)
    return b.as_markup()


def services_kb(lang: str = "ar", show_rates: bool = True):
    b = InlineKeyboardBuilder()
    b.button(text=tr(lang, "svc_create"), callback_data="svc_create_account")
    b.button(text=tr(lang, "svc_deposit_btn"), callback_data="svc_deposit")
    b.button(text=tr(lang, "svc_withdraw_btn"), callback_data="svc_withdraw")
    b.button(text=tr(lang, "btn_transfer"), callback_data="svc_transfer")  # [USR-1]
    b.button(
        text=tr(lang, "btn_calc"), callback_data="calc_dep",
    )  # [USR4-5 + V13]

    if show_rates:  # [AUDIT2] يختفي مع ميزة rates_screen المعطلة
        b.button(
            text=tr(lang, "btn_rates"), callback_data="menu_rates",
        )  # [R6-PLUS7 U32]

    b.button(text=tr(lang, "back"), callback_data="menu_back")
    b.adjust(2)
    return b.as_markup()


def back_kb(callback_data="menu_back", lang: str = "ar"):
    b = InlineKeyboardBuilder()
    b.button(text=tr(lang, "back"), callback_data=callback_data)
    return b.as_markup()


def profile_kb(lang: str = "ar"):
    """[NEW 20/30] أزرار الحساب."""
    b = InlineKeyboardBuilder()
    b.button(text=tr(lang, "send_password_btn"), callback_data="my_password")
    b.button(text=tr(lang, "btn_history"), callback_data="my_history:0")
    b.button(text=tr(lang, "checkin_btn"), callback_data="checkin")  # [USR4-3]
    b.button(text=tr(lang, "back"), callback_data="menu_back")
    b.adjust(1)
    return b.as_markup()


def quick_deposit_kb():
    """[NEW 31] أزرار مبالغ سريعة للشحن."""
    b = InlineKeyboardBuilder()
    for amount in (10, 25, 50, 100):
        b.button(text=f"＋{amount}", callback_data=f"dep_quick:{amount}")
    b.adjust(4)
    return b.as_markup()


def history_kb(page: int, has_more: bool, lang: str = "ar",
               filt: str = "all", mode: str = "full",
               show_lastreq: bool = False):
    """[NEW 30 + USR-2 + USR2-1/6 + V14] السجل: كشف PDF + طلباتي + فلاتر
    + مفتاح عرض مختصر/مفصل."""
    b = InlineKeyboardBuilder()

    if show_lastreq:  # [R6-PLUS10 U35]
        b.button(text="📍 آخر طلبي", callback_data="lastreq")

    b.button(text="🧾 كشف PDF", callback_data="history_pdf")  # [USR-2]
    b.button(  # [R6-PLUS9 V14]
        text=("📖 مفصل" if mode == "compact" else "🗂 مختصر"),
        callback_data=f"hist_toggle:{page}:{filt}:"
        + ("full" if mode == "compact" else "compact"),
    )
    b.button(text=tr(lang, "rq_btn"), callback_data="my_requests:0")  # [USR2-1]
    b.button(text="📈 منحنى رصيدي", callback_data="my_chart")  # [USR4-4]
    b.button(text="📦 بياناتي", callback_data="my_export")  # [USR4-6]

    for key, cb_name in (
        ("hf_all", "all"), ("hf_dep", "deposit"), ("hf_wd", "withdraw"),
        ("hf_tr", "transfer"), ("hf_gift", "gift"),
    ):
        mark = "✓ " if filt == cb_name else ""  # [USR2-6]
        b.button(
            text=mark + tr(lang, key),
            callback_data=f"my_history:0:{cb_name}",
        )

    if page > 0:
        b.button(text="⬅️", callback_data=f"my_history:{page - 1}:{filt}")
    if has_more:
        b.button(text="➡️", callback_data=f"my_history:{page + 1}:{filt}")
    b.button(text=tr(lang, "back"), callback_data="menu_back")
    sizes = [2, 2, 3, 2]
    if page > 0:
        sizes.append(1)
    if has_more:
        sizes.append(1)
    sizes.append(1)
    b.adjust(*sizes)
    return b.as_markup()


def admin_kb():
    b = InlineKeyboardBuilder()  # [R6]
    b.button(text="👑 لوحة تحكم الأدمن", callback_data="admin_home")
    return b.as_markup()


SETTINGS_TABS = {  # [UI-TABS 5.18.4]
    "money": ("💰 المالية والحدود", "💰 <b>الإعدادات — المالية والحدود</b>"),
    "users": ("👥 المستخدمون والولاء",
              "👥 <b>الإعدادات — المستخدمون والولاء</b>"),
    "content": ("📢 المحتوى والنصوص", "📢 <b>الإعدادات — المحتوى والنصوص</b>"),
    "ops": ("🧯 التشغيل والصيانة", "🧯 <b>الإعدادات — التشغيل والصيانة</b>"),
}


async def admin_settings_kb():
    """[PANELHUB 5.18.14] الجذر الموحد: تبويبات الإعدادات
    + تبويبات الأدوات المدمجة + مسابقة الإحالات + لوحة الوكيل (PHIDE)."""
    b = InlineKeyboardBuilder()
    for _tab, (label, _t) in SETTINGS_TABS.items():
        b.button(text=label, callback_data=f"set_tab:{_tab}")

    # [SETTOOLS 5.18.13] محتويات «🧰 الأدوات» انتقلت إلى هنا
    for _tab, (label, _t) in TOOLS_TABS.items():
        b.button(text=label, callback_data=f"tools_tab:{_tab}")
    b.button(text="🏆 مسابقة الإحالات", callback_data="admin_contest")

    if await panel_hidden_on():  # [PHIDE 5.18.2] يتبع الحالة
        b.button(text="🎰 إظهار لوحة الوكيل", callback_data="phide_off")
    else:
        b.button(text="🙈 إخفاء لوحة الوكيل", callback_data="phide_on")

    b.button(text="🔙 رجوع", callback_data="admin_home")  # [PANELHUB 5.18.14]
    b.adjust(2, 2, 2, 2, 1, 1)
    return b.as_markup()


async def _settings_tab_kb(tab: str):
    """[UI-TABS 5.18.4] أزرار تبويب إعدادات محدد — نفس المعالجات القائمة."""
    b = InlineKeyboardBuilder()
    hide_on = (await get_setting("staff_hide_balance") or "0") == "1"

    if tab == "money":
        rows = [
            ("٪ عمولة الشحن", "admin_commission"),
            ("⚖️ حدود وسقوف", "admin_limits"),
            ("💸 ميزانية السحب", "admin_budget"),
            ("🎁 مكافأة الإيداع", "admin_bonus"),
            ("🧮 محاكي الشحن", "admin_sim"),
            ("⚡ اعتماد تلقائي", "admin_autowd"),
            ("🔢 إعدادات القيم", "value_settings"),
        ]
    elif tab == "users":
        rows = [
            ("💎 مستويات الولاء", "admin_loyal"),
            ("🔥 الحضور اليومي", "admin_checkin"),
            ("🤝 مكافأة الإحالة", "admin_refbonus"),
            ("👥 موافقة مزدوجة", "admin_dual"),
            ("🚨 كشف الشواذ", "admin_anomaly"),
            # [ADM3-8 + R6-REV] تعكس الحالة الحية
            (("🙈 إخفاء الأرصدة: ✅ مفعّل" if hide_on
              else "🙈 إخفاء الأرصدة: ❌ معطل"), "admin_hidebal"),
        ]
    elif tab == "content":
        rows = [
            ("📝 النصوص", "admin_texts"),
            ("🔗 روابط القائمة", "admin_links"),
            ("🖼 ترحيب بصورة", "welcome_photo_set"),
            ("🕐 ساعات عمل الدعم", "support_hours_set"),
        ]
    elif tab == "ops":
        rows = [
            ("🕐 صيانة مجدولة", "admin_maintenance"),
            ("🚧 نطاق الصيانة", "toggle_maint_scope"),
            ("⏸️ إيقاف الخدمات", "admin_pause"),
            ("📦 جدولة ZIP اليومي", "admin_ziptgl"),
            ("📬 غرفة مراقبة", "admin_mirror"),
            ("🔑 رمز التأكيد", "admin_pinset"),
        ]
    else:
        return await admin_settings_kb()

    for t, c in rows:
        b.button(text=t, callback_data=c)

    b.button(text="🔙 رجوع للإعدادات", callback_data="admin_settings_menu")
    b.adjust(2)
    return b.as_markup()


@dp.callback_query(F.data.startswith("set_tab:"))
async def settings_tab_cb(cb: types.CallbackQuery, state: FSMContext):
    """[UI-TABS 5.18.4] فتح تبويب إعدادات محدد."""
    if not await is_admin_or_supervisor(cb.from_user.id):
        await cb.answer("غير مصرّح.", show_alert=True)
        return

    tab = cb.data.split(":", 1)[1]

    if tab not in SETTINGS_TABS:
        await cb.answer("تبويب غير معروف.", show_alert=True)
        return

    await cb.answer()
    await state.clear()
    status = await admin_status_line()
    await safe_edit(
        cb.message,
        f"{SETTINGS_TABS[tab][1]}\n{status}\n\nاختر ما تريد ضبطه:",
        await _settings_tab_kb(tab),
    )


TOOLS_TABS = {  # [UI-TABS 5.18.4]
    "bc": ("📣 البث والإعلانات", "📣 <b>الإعدادات — البث والإعلانات</b>"),
    "data": ("🗄 البيانات والنسخ", "🗄 <b>الإعدادات — البيانات والنسخ</b>"),
    "rep": ("📊 التقارير والفحص", "📊 <b>الإعدادات — التقارير والفحص</b>"),
}


def _tools_tab_kb(tab: str):
    """[UI-TABS 5.18.4] أزرار تبويب أدوات محدد — نفس المعالجات القائمة."""
    b = InlineKeyboardBuilder()

    if tab == "bc":
        rows = [
            ("📣 بث رسالة", "admin_broadcast"),
            ("📢 الإعلانات", "admin_anns"),
            ("📳 رسالة اختبار", "admin_test_ping"),
        ]
    elif tab == "data":
        rows = [
            ("📦 تصدير ZIP الآن", "admin_export_zip"),
            ("🗄 نسخة احتياطية الآن", "admin_backup_now"),
            ("🧹 تنظيف قديم", "admin_clean"),
            ("📜 سجل التدقيق", "admin_audit"),
            ("🧾 سجل الويب هوك", "admin_whlog"),
        ]
    elif tab == "rep":
        rows = [
            ("📊 رسم بياني", "admin_chart"),
            ("🧾 تقرير محاسبي", "admin_accreport"),
        ]
    else:
        return None

    for t, c in rows:
        b.button(text=t, callback_data=c)

    b.button(text="🔙 رجوع للإعدادات", callback_data="admin_tools_menu")
    b.adjust(2)
    return b.as_markup()


@dp.callback_query(F.data.startswith("tools_tab:"))
async def tools_tab_cb(cb: types.CallbackQuery, state: FSMContext):
    """[UI-TABS 5.18.4] فتح تبويب أدوات محدد."""
    if not await is_admin_or_supervisor(cb.from_user.id):
        await cb.answer("غير مصرّح.", show_alert=True)
        return

    tab = cb.data.split(":", 1)[1]

    if tab not in TOOLS_TABS:
        await cb.answer("تبويب غير معروف.", show_alert=True)
        return

    await cb.answer()
    await state.clear()
    status = await admin_status_line()
    await safe_edit(
        cb.message,
        f"{TOOLS_TABS[tab][1]}\n{status}\n\nاختر أداة:",
        _tools_tab_kb(tab),
    )


def admin_users_kb():
    b = InlineKeyboardBuilder()
    b.button(text="🔍 بحث عن مستخدم", callback_data="admin_user_search")  # [NEW 37]
    b.button(text="🕵️ مطابقات الوجهات",
             callback_data="admin_destmatch")  # [R6-PLUS2]
    b.button(text="📂 قائمة المستخدمين", callback_data="admin_user_list:0")  # [NEW 37]
    b.button(text="➕ إنشاء حساب لمستخدم", callback_data="admin_user_create")
    b.button(text="🏷 فلترة بالوسم", callback_data="admin_tagsearch")  # [ADM4-1]
    b.button(text="🚫 حظر / فك الحظر", callback_data="admin_user_ban")
    b.button(text="🔙 رجوع", callback_data="admin_panel")
    b.adjust(1)
    return b.as_markup()


def admin_finance_kb():
    b = InlineKeyboardBuilder()
    b.button(text="💵 تعديل رصيد مستخدم", callback_data="admin_finance_adjust")
    b.button(text="📋 الطلبات المعلقة", callback_data="admin_finance_pending")
    b.button(text="📊 سجل الشحن والسحب", callback_data="admin_finance_logs")
    b.button(
        text="🚀 المدفوعات (Payouts)",
        callback_data="admin_payouts",
    )  # [NEW 36]
    b.button(text="🔙 رجوع", callback_data="admin_panel")
    b.adjust(1)
    return b.as_markup()


def admin_gifts_kb():
    b = InlineKeyboardBuilder()
    b.button(text="➕ إنشاء كود هدية", callback_data="admin_gift_create")
    b.button(text="🎁 دفعة أكواد", callback_data="admin_gift_batch")  # [ADM-1]
    b.button(text="🎟 كود إعفاء عمولة", callback_data="admin_promo")  # [USR2-4]
    b.button(text="📋 قائمة الأكواد", callback_data="admin_gift_list:0")  # [FIX 12]
    b.button(text="🔙 رجوع", callback_data="admin_panel")
    b.adjust(1)
    return b.as_markup()


def admin_supervisors_kb():
    b = InlineKeyboardBuilder()
    b.button(text="➕ إضافة / تحديث مشرف", callback_data="admin_sup_add")
    b.button(text="📋 قائمة المشرفين", callback_data="admin_sup_list")
    b.button(text="⏸ إيقاف / تشغيل مشرف", callback_data="admin_sup_suspend")  # [NEW 40]
    b.button(text="💼 حصة مالية لمشرف", callback_data="admin_sup_quota")  # [ADM2-3]
    b.button(text="🏋️ أداء المشرفين", callback_data="admin_supstats")  # [ADM2-7]
    b.button(text="🗑 حذف مشرف", callback_data="admin_sup_delete")
    b.button(text="📊 نشاط المشرفين",
             callback_data="sup_report")  # [R6-PLUS2]
    b.button(text="🔙 رجوع", callback_data="admin_panel")
    b.adjust(1)
    return b.as_markup()


def admin_reports_kb(show_weekly: bool = True):
    """[NEW 14] قائمة التقارير."""
    b = InlineKeyboardBuilder()
    b.button(text="👥 تقرير المستخدمين", callback_data="report:users")
    b.button(text="💳 تقرير العمليات المالية", callback_data="report:transactions")
    b.button(text="📋 تقرير الطلبات", callback_data="report:requests")

    if show_weekly:  # [AUDIT2] بميزة weekly_now
        b.button(
            text="👁 معاينة التقرير الأسبوعي",
            callback_data="weekly_now",
        )  # [R6-PLUS10 E11]

    b.button(text="🔙 رجوع", callback_data="admin_panel")
    b.adjust(1)
    return b.as_markup()


def admin_texts_kb():
    """[NEW 17] قائمة النصوص القابلة للتعديل."""
    b = InlineKeyboardBuilder()
    for text_key, label in BOT_TEXTS.items():
        b.button(text=f"✏️ {label}", callback_data=f"admin_text_edit:{text_key}")
    b.button(text="🔙 رجوع", callback_data="admin_settings_menu")
    b.adjust(1)
    return b.as_markup()


def broadcast_confirm_kb():
    """[NEW 16] تأكيد البث."""
    b = InlineKeyboardBuilder()
    b.button(text="✅ نشر الآن", callback_data="admin_broadcast_confirm")
    b.button(text="❌ إلغاء", callback_data="admin_broadcast_cancel")
    b.adjust(2)
    return b.as_markup()


def info_menu_kb():
    """[NEW 18] قائمة المعلومات للمستخدمين."""
    b = InlineKeyboardBuilder()
    b.button(text="🎓 الشروحات", callback_data="info_text:tutorials")
    b.button(text="🍀 العروض", callback_data="info_text:offers")
    b.button(text="📜 الشروط والأحكام", callback_data="info_text:terms")
    b.button(text="🔙 رجوع", callback_data="menu_back")
    b.adjust(1)
    return b.as_markup()


def admin_limits_kb():
    """[NEW 27/41] لوحة الحدود والسقوف."""
    b = InlineKeyboardBuilder()
    b.button(text="أدنى شحن", callback_data="lim:deposit_min")
    b.button(text="أقصى شحن", callback_data="lim:deposit_max")
    b.button(text="أدنى سحب", callback_data="lim:withdraw_min")
    b.button(text="أقصى سحب", callback_data="lim:withdraw_max")
    b.button(
        text="🛑 سقف سحب/مستخدم",
        callback_data="lim:daily_withdraw_per_user",
    )  # [NEW 41]
    b.button(
        text="🛑 سقف سحب/كلي",
        callback_data="lim:daily_withdraw_total",
    )  # [NEW 41]
    b.button(
        text="🔢 حد سحب يومي",
        callback_data="lim:daily_wd_count",
    )  # [R6-PLUS5]
    b.button(text="🔙 رجوع", callback_data="admin_settings_menu")
    b.adjust(2)
    return b.as_markup()


def finance_request_kb(request_id: int, show_card: bool = True):
    b = InlineKeyboardBuilder()
    b.button(text="✅ موافقة", callback_data=f"finance_approve:{request_id}")
    b.button(text="❌ رفض", callback_data=f"finance_reject:{request_id}")

    if show_card:  # [AUDIT2] بميزة quick_card
        b.button(
            text="👤 الملف",
            callback_data=f"fcard:{request_id}",
        )  # [R6-PLUS9 V9]

    b.adjust(2, 1)
    return b.as_markup()


@dp.callback_query(F.data == "admin_back_last")
async def admin_back_last(cb: types.CallbackQuery, state: FSMContext):
    """[R6-PLUS9 V11] العودة لآخر شاشة إدارية زيّرها."""

    if not await is_admin_or_supervisor(cb.from_user.id):
        await cb.answer("غير مصرّح.", show_alert=True)
        return

    target = _last_admin_screen.get(cb.from_user.id) or "admin_panel"

    # إعادة توجيه نفس الكائن للمعالج الأصلي بالشاشة المحفوظة
    if target.startswith("admin_user_list:"):
        _with_data(cb, target)
        await admin_user_list(cb, state)
        return

    known = {
        "admin_kpi": admin_kpi,
        "admin_users": admin_users,
        "admin_inbox": admin_inbox,
        "admin_statistics": admin_statistics,
        "admin_finance": None,  # يُستكمل أدناه إن لم يُسجل
    }

    fn = known.get(target)

    if fn is not None:
        _with_data(cb, target)
        await fn(cb, state)
        return

    _with_data(cb, "admin_panel")
    await admin_panel(cb, state)


@dp.callback_query(F.data.startswith("fcard:"))
async def fcard_open(cb: types.CallbackQuery, state: FSMContext):
    """[R6-PLUS9 V9] فتح ملف صاحب الطلب من الإشعار المالي."""

    if not await is_admin_or_supervisor(cb.from_user.id, "finance"):
        await cb.answer("غير مصرّح.", show_alert=True)
        return

    try:
        rid = int(cb.data.split(":", 1)[1])
    except (ValueError, IndexError):
        await cb.answer("معرف غير صالح.", show_alert=True)
        return

    db = await get_db()

    try:
        cur = await db.execute(
            "SELECT * FROM finance_requests WHERE id = ?", (rid,),
        )
        req = await cur.fetchone()
    finally:
        await db.close()

    if not req:
        await cb.answer("الطلب غير موجود.", show_alert=True)
        return

    user = await get_user(req["telegram_id"])

    if not user:
        await cb.answer("المستخدم غير موجود.", show_alert=True)
        return

    await cb.answer()
    _last_admin_screen[cb.from_user.id] = "admin_inbox"  # [V11]
    text, kb = await render_user_card(user, cb.from_user.id)
    await safe_edit(cb.message, f"🧾 الطلب #{rid}\n\n" + text, kb)


# ============================================================
# PANEL HELPERS [R6-PLUS12]
# ============================================================

async def panel_hidden_on() -> bool:
    """[PHIDE 5.18.2] هل لوحة الوكيل مخفية من الواجهة؟"""
    return await feat_on("panel_hidden")


def panel_ready() -> bool:
    """اللوحة مربوطة (الوحدة موجودة + البيئة مضبوطة)."""
    return ipanel is not None and ipanel.panel_configured()


async def panel_call(coro_fn, *args, **kwargs):
    """استدعاء آمن للوحة — يرجع (نتيجة، خطأ_نصي)."""
    if not panel_ready():
        return None, "اللوحة غير مربوطة — راجع إعدادات البيئة"

    try:
        return await coro_fn(*args, **kwargs), None
    except ipanel.PanelNotConfigured as exc:
        return None, str(exc)
    except ipanel.PanelError as exc:
        return None, str(exc)
    except Exception as exc:
        logger.exception("[panel] خطأ غير متوقع")
        return None, f"خطأ غير متوقع: {type(exc).__name__}"


async def panel_ops_line() -> str:
    """[R6-PLUS13] سطر حالة اللوحة في /ops."""
    if ipanel is None or not ipanel.panel_configured():
        return "🎰 اللوحة: ❌ غير مربوطة (بلا بيانات بيئة)"

    st = ipanel.panel_state()

    if st["last_error"]:
        line = (
            f"🎰 اللوحة: ⚠️ آخر خطأ: {esc(st['last_error'])}"
            f" ({esc(st['last_error_at'])})"
        )
    elif st["last_ok"]:
        wallet_txt = ""

        if st["wallet"] is not None:
            wallet_txt = (
                f" | محفظة: {st['wallet']:.2f}"
                f" {esc(str(st['currency'] or ''))}"
            )

        players_txt = (
            f" | {st['players']} لاعب"
            if st["players"] is not None else ""
        )
        line = (
            f"🎰 اللوحة: ✅ آخر تواصل {esc(st['last_ok'])} UTC"
            + wallet_txt + players_txt
        )
    else:
        line = "🎰 اللوحة: ✅ مضبوطة (لا تواصل بعد)"

    return line


async def txid_duplicate(txid: str, method: str) -> bool:
    """[R6-PLUS13] هل رقم العملية مستخدم سلفاً بنفس الطريقة؟ (F8)"""
    db_x = await get_db()

    try:
        cur_x = await db_x.execute(
            "SELECT note FROM finance_requests"
            " WHERE type = 'deposit'"
            " AND status IN ('pending', 'approved')"
            " AND instr(note || ';', 'txid=' || ? || ';') > 0"
            " LIMIT 5",
            (txid,),
        )
        dup_rows = await cur_x.fetchall()
    finally:
        await db_x.close()

    for d in dup_rows:
        d_method = ""

        for part in (d["note"] or "").split(";"):
            if part.startswith("method="):
                d_method = part[7:]

        if d_method == method:
            return True

    return False


async def ingest_bridge_deposit(
    telegram_id: int,
    amount,
    txid: str,
    method: str = "شام كاش",
    sender: str = "",
    raw: str = "",
):
    """[R6-PLUS13] جسر إشعارات شام كاش — يصنع طلب شحن معلقاً كاملاً.

    لا يُ adds أي رصيد تلقائياً — الاعتماد بضغطة ✅ كما هو.
    يعيد (status, request_id):
    disabled | invalid | user_not_found | duplicate | created
    """
    if not await feat_on("dep_bridge"):
        return "disabled", None

    value = parse_amount(amount)

    if value is None or value <= 0 or not (txid or "").strip():
        return "invalid", None

    user = await get_user(int(telegram_id))

    if not user or user["is_banned"]:
        return "user_not_found", None

    if await txid_duplicate(txid.strip(), method):
        return "duplicate", None

    note = f"method={method};txid={txid.strip()};bridge=1"

    if sender:
        note += f";sender={sender[:40]}"

    rid = await create_finance_request(
        int(telegram_id), "deposit", value, note=note,
    )

    raw_line = ""

    if raw:
        raw_line = "\n📄 التفاصيل: " + esc(str(raw)[:200])

    await notify_finance_staff(
        "🌉 <b>طلب شحن من الجسر</b> (إشعار آلي)\n\n"
        f"👤 المستخدم: <code>{int(telegram_id)}</code>\n"
        f"💳 الطريقة: <b>{esc(method)}</b>\n"
        f"💵 المبلغ: <b>{money(value)}</b>\n"
        f"🆔 رقم العملية: <code>{esc(txid.strip())}</code>\n"
        + (f"👤 المرسل: {esc(sender[:40])}\n" if sender else "")
        + f"🧾 الطلب: #{rid}" + raw_line,
        rid,
    )

    return "created", rid


async def panel_recon_if_due():
    """[R6-PLUS13] المطابقة الليلية: محفظة الوكيل ↔ مجموع أرصدة اللاعبين.

    تقرير قراءة فقط للأدمن — لا أي تعديل على اللوحة.
    """
    if not await feat_on("panel_recon"):
        return None

    last = await get_setting("last_panel_recon_at") or ""
    now = datetime.now(timezone.utc)

    if last:
        try:
            if (now - datetime.fromisoformat(last)).total_seconds() < 86400:
                return None
        except ValueError:
            pass

    if not panel_ready():
        return None  # بلا بيانات بيئة — لا تقارير ولا قفل توقيت

    await set_setting("last_panel_recon_at", now.isoformat())

    client = ipanel.get_panel()
    info, err = await panel_call(client.agent_info)

    if err:
        report = (
            "🌙 <b>المطابقة الليلية للوحة</b> — فشلت\n\n"
            f"❌ {esc(str(err))}"
        )
    else:
        players, perr = await panel_call(client.players)

        if perr:
            report = (
                "🌙 <b>المطابقة الليلية للوحة</b> — فشل جلب اللاعبين\n\n"
                f"❌ {esc(str(perr))}"
            )
        else:
            total_sum = 0.0
            nonzero = []

            for p in (players or [])[:100]:
                bal, berr = await panel_call(
                    client.player_balance, p.get("playerId"),
                )

                if berr or bal is None:
                    continue

                total_sum += bal

                if bal > 0:
                    nonzero.append((bal, p.get("username")))

            nonzero.sort(reverse=True)
            cur = esc(str(info["currency"]))
            lines = [
                f"• <code>{esc(str(u))}</code> — {b:.2f} {cur}"
                for b, u in nonzero[:8]
            ]

            report = (
                "🌙 <b>المطابقة الليلية للوحة</b>\n\n"
                f"💰 محفظة الوكيل: <b>{info['wallet']:.2f}</b> {cur}\n"
                f"💳 المتاح: <b>{info['available']:.2f}</b> {cur}\n"
                f"👥 اللاعبون: {len(players or [])}\n"
                f"Σ مجموع أرصدة اللاعبين: <b>{total_sum:.2f}</b> {cur}\n"
            )

            if nonzero:
                report += "\n⚠️ لاعبون بأرصدة:\n" + "\n".join(lines)
            else:
                report += "\n✅ لا يوجد لاعب برصيد غير صفري"

    try:
        await bot.send_message(ADMIN_USER_ID, report)
    except Exception as exc:
        logger.warning("تعذر إرسال تقرير المطابقة: %s", exc)

    return report


# ============================================================
# PANEL ADMIN SCREENS [R6-PLUS12]
# ============================================================

async def panel_home(cb: types.CallbackQuery, state: FSMContext):
    """الشاشة الرئيسية للوحة: محفظة الوكيل + أزرار العمليات."""
    if not await is_admin_or_supervisor(cb.from_user.id):
        await cb.answer("غير مصرّح.", show_alert=True)
        return

    await cb.answer()

    if not panel_ready():
        await safe_edit(
            cb.message,
            "🎰 <b>لوحة الوكيل</b>\n\n"
            "❌ غير مربوطة — عيّن BETS55_PANEL_URL و"
            "BETS55_AGENT_USER و BETS55_AGENT_PASS بالبيئة.",
            InlineKeyboardBuilder().button(
                text="🔙 رجوع", callback_data="admin_tools_menu",
            ).adjust(1).as_markup(),
        )
        return

    await state.clear()
    info, err = await panel_call(ipanel.get_panel().agent_info)

    if err:
        txt = f"🎰 <b>لوحة الوكيل</b>\n\n❌ {esc(str(err))}"
    else:
        txt = (
            "🎰 <b>لوحة الوكيل</b>\n\n"
            f"👤 الوكيل: <code>{esc(str(info['username']))}</code>"
            f" (#{info['affiliate_id']})\n"
            f"💰 المحفظة: <b>{info['wallet']:.2f}</b> {esc(info['currency'])}\n"
            f"💳 المتاح: <b>{info['available']:.2f}</b> {esc(info['currency'])}"
        )

        # [AGENT-FULL] الرصيد المتاح للسحب من محافظ الوكيل الحقيقية
        if await feat_on("panel_wallets"):
            wallets, werr = await panel_call(ipanel.get_panel().all_wallets)

            if not werr and wallets:
                w0 = wallets[0]
                avail = ipanel.parse_wallet(w0.get("availableWallet"))
                txt += (f"\n💼 متاح للسحب: <b>{avail:,.2f}</b> "
                        f"{esc(str(w0.get('currencyCode') or info['currency']))}")

    kb = InlineKeyboardBuilder()
    kb.button(text="📋 اللاعبون", callback_data="panel_players")
    kb.button(text="➕ إنشاء لاعب", callback_data="panel_create")
    kb.button(text="💸 إيداع للاعب", callback_data="panel_deposit")
    kb.button(text="🏦 سحب من لاعب", callback_data="panel_withdraw")

    if await feat_on("panel_wallets"):  # [AGENT-FULL]
        kb.button(text="💼 المحافظ والحركات",
                  callback_data="panel_wallets")

    kb.button(text="🔄 تحديث", callback_data="panel_home")
    kb.button(text="🔙 رجوع", callback_data="admin_home")  # [MENU-ORG]
    kb.adjust(2)
    await safe_edit(cb.message, txt, kb.as_markup())


@dp.callback_query(F.data == "panel_home")
async def panel_home_cb(cb: types.CallbackQuery, state: FSMContext):
    if await panel_hidden_on():  # [PHIDE 5.18.2] بوابة الإخفاء
        await cb.answer(
            "🙈 لوحة الوكيل مخفية حالياً — أظهرها من الإعدادات.",
            show_alert=True,
        )
        return

    await panel_home(cb, state)


@dp.callback_query(F.data == "panel_wallets")
async def panel_wallets_cb(cb: types.CallbackQuery, state: FSMContext):
    """[AGENT-FULL] محافظ الوكيل بكل العملات + العملات المتاحة + آخر حركة."""

    if not await is_admin_or_supervisor(cb.from_user.id):
        await cb.answer("غير مصرّح.", show_alert=True)
        return

    await cb.answer()

    if not panel_ready():
        await cb.answer("اللوحة غير مربوطة.", show_alert=True)
        return

    await state.clear()
    cli = ipanel.get_panel()
    wallets, werr = await panel_call(cli.all_wallets)
    curs, cerr = await panel_call(cli.available_currencies)
    last, lerr = await panel_call(cli.last_wallet_tx)

    if werr:
        txt = f"💼 <b>محافظ الوكيل</b>\n\n❌ {esc(str(werr))}"
    else:
        lines = ["💼 <b>محافظ الوكيل</b>\n"]

        for w in (wallets or []):
            lines.append(
                f"💱 <b>{esc(str(w.get('currencyCode') or '?'))}</b>"
                + (f" ({esc(str(w.get('currencyName')))})"
                   if w.get("currencyName") else "") + "\n"
                f"   💰 متاح للسحب: "
                f"<b>{ipanel.parse_wallet(w.get('availableWallet')):,.2f}</b>"
                f"\n   💳 رصيد: "
                f"{ipanel.parse_wallet(w.get('balance')):,.2f} | "
                f"🎁 مكافآت: "
                f"{ipanel.parse_wallet(w.get('bonus')):,.2f} | "
                f"🧊 مجمّد: "
                f"{ipanel.parse_wallet(w.get('frozenBalance')):,.2f}"
            )

        if not wallets:
            lines.append("لا محافظ ظاهرة للحساب.")

        if not cerr and curs:
            names = "، ".join(
                esc(str(v.get("iso") or k))
                for k, v in list(curs.items())[:6]
            )
            lines.append(f"\n💱 العملات المتاحة: {names}")

        if not lerr and last and last.get("transactionId"):
            lines.append(
                "\n🧾 آخر حركة على المحفظة:\n"
                f"   #{esc(str(last.get('transactionId')))} | "
                f"{esc(str(last.get('date') or ''))}\n"
                f"   الرصيد بعدها: "
                f"{ipanel.parse_wallet(last.get('balance')):,.2f}"
            )

        txt = "\n".join(lines)

    kb = InlineKeyboardBuilder()
    kb.button(text="🧾 سجل الحركات", callback_data="panel_txlist")
    kb.button(text="🔄 تحديث", callback_data="panel_wallets")
    kb.button(text="🔙 رجوع", callback_data="panel_home")
    kb.adjust(2, 1)
    await safe_edit(cb.message, txt, kb.as_markup())


@dp.callback_query(F.data == "panel_txlist")
async def panel_txlist_cb(cb: types.CallbackQuery, state: FSMContext):
    """[AGENT-FULL] سجل حركات محفظة الوكيل."""

    if not await is_admin_or_supervisor(cb.from_user.id):
        await cb.answer("غير مصرّح.", show_alert=True)
        return

    await cb.answer()

    if not panel_ready():
        await cb.answer("اللوحة غير مربوطة.", show_alert=True)
        return

    await state.clear()
    txs, err = await panel_call(
        ipanel.get_panel().wallet_transactions, 1, 10,
    )

    if err:
        txt = f"🧾 <b>سجل حركات المحفظة</b>\n\n❌ {esc(str(err))}"
    elif not txs:
        txt = ("🧾 <b>سجل حركات المحفظة</b>\n\n"
               "السجل فارغ — لا حركات مسجلة بعد.")
    else:
        rows = []

        for t in txs[:10]:
            rows.append(
                f"#{esc(str(t.get('transactionId') or '—'))} | "
                f"{esc(str(t.get('date') or '—'))} | "
                f"الرصيد: {ipanel.parse_wallet(t.get('balance')):,.2f}"
            )

        txt = ("🧾 <b>سجل حركات المحفظة</b> (الأحدث)\n\n"
               + "\n".join(rows))

    kb = InlineKeyboardBuilder()
    kb.button(text="🔄 تحديث", callback_data="panel_txlist")
    kb.button(text="🔙 رجوع", callback_data="panel_wallets")
    kb.adjust(2)
    await safe_edit(cb.message, txt, kb.as_markup())


@dp.callback_query(F.data == "panel_players")
async def panel_players(cb: types.CallbackQuery, state: FSMContext):
    if not await is_admin_or_supervisor(cb.from_user.id):
        await cb.answer("غير مصرّح.", show_alert=True)
        return

    await cb.answer()

    rows, err = await panel_call(ipanel.get_panel().players)

    if err:
        await safe_edit(
            cb.message,
            f"📋 <b>اللاعبون</b>\n\n❌ {esc(str(err))}",
            InlineKeyboardBuilder().button(
                text="🔙 رجوع", callback_data="panel_home",
            ).adjust(1).as_markup(),
        )
        return

    lines = []

    for p in (rows or [])[:12]:
        lines.append(
            f"• <code>{esc(str(p.get('username')))}</code>"
            f" — #{p.get('playerId')} ({esc(str(p.get('currency') or ''))})",
        )

    total = len(rows or [])
    txt = f"📋 <b>لاعبو الوكيل</b> ({total})\n\n" + "\n".join(lines)

    if total > 12:
        txt += f"\n… و{total - 12} آخرين"

    kb = InlineKeyboardBuilder()
    kb.button(text="🔄 تحديث", callback_data="panel_players")
    kb.button(text="🔙 رجوع", callback_data="panel_home")
    kb.adjust(2)
    await safe_edit(cb.message, txt, kb.as_markup())


@dp.callback_query(F.data == "panel_create")
async def panel_create_start(cb: types.CallbackQuery, state: FSMContext):
    if not await is_admin_or_supervisor(cb.from_user.id):
        await cb.answer("غير مصرّح.", show_alert=True)
        return

    await cb.answer()
    await state.set_state(PanelCreateFSM.username)
    await safe_edit(
        cb.message,
        "➕ <b>إنشاء لاعب باللوحة</b>\n\n"
        "أرسل اسم المستخدم الجديد (3-32 حرفاً بلا مسافات):",
        InlineKeyboardBuilder().button(
            text="❌ إلغاء", callback_data="panel_home",
        ).adjust(1).as_markup(),
    )


@dp.message(PanelCreateFSM.username)
async def panel_create_username(message: types.Message, state: FSMContext):
    if not await is_admin_or_supervisor(message.from_user.id, message):
        return

    username = (message.text or "").strip()

    if not (3 <= len(username) <= 32) or any(c.isspace() for c in username):
        await message.answer("❌ الاسم 3-32 حرفاً بلا مسافات. أعد المحاولة:")
        return

    await state.update_data(p_username=username)
    await state.set_state(PanelCreateFSM.password)
    await message.answer(
        f"✅ الاسم: <code>{esc(username)}</code>\n"
        "الآن أرسل كلمة المرور (6+ أحرف):",
    )


@dp.message(PanelCreateFSM.password)
async def panel_create_password(message: types.Message, state: FSMContext):
    if not await is_admin_or_supervisor(message.from_user.id, message):
        return

    password = (message.text or "").strip()

    if len(password) < 6 or any(c.isspace() for c in password):
        await message.answer("❌ كلمة المرور 6+ أحرف بلا مسافات. أعد:")
        return

    data = await state.get_data()
    username = data.get("p_username") or ""
    await state.clear()

    client = ipanel.get_panel()
    res, err = await panel_call(
        client.register_player, username, password,
    )

    if err:
        await message.answer(
            f"❌ فشل إنشاء اللاعب <code>{esc(username)}</code>:\n"
            f"{esc(str(err))}",
        )
        return

    await audit(message.from_user.id, "panel_player_create",
                details=f"player={username} id={res.get('playerId')}")

    # [PANEL-V2.1] المعرف قد يتأخر بتزامن قائمة اللوحة — رسالة صادقة
    pid = res.get("playerId")
    id_line = f" (#{pid})" if pid else ""
    sync_line = ("\n⏳ أنشئ على الخادم — المعرف سيظهر بقائمة"
                 " «📋 اللاعبون» خلال لحظات.") if res.get("unconfirmed") else ""

    await message.answer(
        "✅ <b>تم إنشاء اللاعب باللوحة</b>\n\n"
        f"👤 <code>{esc(username)}</code>{id_line}\n"
        f"🔑 <code>{esc(password)}</code>" + sync_line,
    )


async def _panel_money_start(cb: types.CallbackQuery, state: FSMContext, kind: str):
    if not await is_admin_or_supervisor(cb.from_user.id):
        await cb.answer("غير مصرّح.", show_alert=True)
        return

    await cb.answer()
    await state_set_panel_kind(cb.bot, cb.from_user.id, kind)
    # [PMLINK 5.18.17] نمط aiogram 3 — .set() (نمط v2) كان ينهار
    await state.set_state(PanelMoneyFSM.username)


@dp.callback_query(F.data == "panel_deposit")
async def panel_deposit_start(cb: types.CallbackQuery, state: FSMContext):
    await _panel_money_start(cb, state, "deposit")


@dp.callback_query(F.data == "panel_withdraw")
async def panel_withdraw_start(cb: types.CallbackQuery, state: FSMContext):
    await _panel_money_start(cb, state, "withdraw")


PANEL_KIND_KEY = f"panel_kind_"


async def state_set_panel_kind(bot, admin_id: int, kind: str):
    """تخزين نوع العملية بالمستخدم (بدون FSM إضافي)."""
    _PANEL_KINDS[admin_id] = kind


_PANEL_KINDS: dict = {}


@dp.message(PanelMoneyFSM.username)
async def panel_money_username(message: types.Message, state: FSMContext):
    if not await is_admin_or_supervisor(message.from_user.id, message):
        return

    username = (message.text or "").strip()

    client = ipanel.get_panel()
    player, err = await panel_call(client.find_player, username)

    if err or not player:
        await message.answer(
            "❌ لم أجد اللاعب باللوحة. أعد إرسال الاسم أو /cancel",
        )
        return

    await state.update_data(
        p_player_id=player.get("playerId"),
        p_player_name=player.get("username"),
    )
    await state.set_state(PanelMoneyFSM.amount)

    kind = _PANEL_KINDS.get(message.from_user.id, "deposit")
    title = "💸 إيداع للاعب" if kind == "deposit" else "🏦 سحب من لاعب"

    bal, berr = await panel_call(
        client.player_balance, player.get("playerId"),
    )

    bal_txt = f"\n💰 رصيده الحالي: {bal:.2f}" if not berr else ""
    await message.answer(
        f"{title}\n\n👤 <code>{esc(str(player.get('username')))}</code>"
        f" (#{player.get('playerId')}){bal_txt}\n\n"
        "أرسل المبلغ:",
    )


@dp.message(PanelMoneyFSM.amount)
async def panel_money_amount(message: types.Message, state: FSMContext):
    if not await is_admin_or_supervisor(message.from_user.id, message):
        return

    amount = parse_amount(message.text or "")

    if amount is None or amount <= 0:
        await message.answer("❌ مبلغ غير صالح. أعد الإرسال:")
        return

    data = await state.get_data()
    player_id = data.get("p_player_id")
    player_name = data.get("p_player_name")
    kind = _PANEL_KINDS.get(message.from_user.id, "deposit")

    if not player_id:
        await state.clear()
        await message.answer("❌ انتهت الجلسة — ابدأ من جديد.")
        return

    # تأكيد قبل التنفيذ (مال حقيقي)
    kb = InlineKeyboardBuilder()
    # [PMLINK 5.18.17] الاسم معقّم من ":" وقصير — حد تلجرام 64 بايت
    _pn = str(player_name or "").replace(":", " ").strip()[:12] or "player"
    cb_yes = f"panel_money_go:{kind}:{player_id}:{_pn}:{amount}"
    if len(cb_yes.encode()) > 64:
        cb_yes = f"panel_money_go:{kind}:{player_id}:{_pn[:8]}:{amount}"
        assert len(cb_yes.encode()) <= 64
    kb.button(text="✅ تنفيذ", callback_data=cb_yes)
    kb.button(text="❌ إلغاء", callback_data="panel_home")
    kb.adjust(2)
    await state.clear()

    title = "💸 إيداع" if kind == "deposit" else "🏦 سحب"
    await message.answer(
        f"⚠️ <b>تأكيد {title}</b>\n\n"
        f"👤 <code>{esc(str(player_name))}</code> (#{player_id})\n"
        f"💵 المبلغ: <b>{amount:.2f}</b>\n\n"
        "هذه عملية رصيد حقيقية على اللوحة.",
        reply_markup=kb.as_markup(),
    )


@dp.callback_query(F.data.startswith("panel_money_go:"))
async def panel_money_go(cb: types.CallbackQuery):
    if not await is_admin_or_supervisor(cb.from_user.id):
        await cb.answer("غير مصرّح.", show_alert=True)
        return

    try:
        _, kind, player_id, player_name, amount_s = cb.data.split(":", 4)
        amount = float(amount_s)
    except ValueError:
        await cb.answer("بيانات تالفة.", show_alert=True)
        return

    if kind not in ("deposit", "withdraw"):
        await cb.answer("نوع غير معروف.", show_alert=True)
        return

    await cb.answer("⏳ جارٍ التنفيذ…")
    client = ipanel.get_panel()
    comment = f"bot:tg={cb.from_user.id}"

    if kind == "deposit":
        res, err = await panel_call(
            client.deposit_to_player, player_id, amount, comment,
        )
    else:
        res, err = await panel_call(
            client.withdraw_from_player, player_id, amount, comment,
        )

    verb = "إيداع" if kind == "deposit" else "سحب"

    if err:
        await cb.message.answer(
            f"❌ فشل {verb} {amount:.2f} لـ"
            f"<code>{esc(player_name)}</code>:\n{esc(str(err))}",
        )
        return

    await audit(
        cb.from_user.id, f"panel_{kind}",
        details=f"player={player_name}({player_id}) amount={amount:.2f}",
    )
    await cb.message.answer(
        f"✅ <b>تم {verb} {amount:.2f}</b> "
        f"للاعب <code>{esc(player_name)}</code> (#{player_id})",
    )

    try:
        bal, _ = await panel_call(client.player_balance, player_id)

        if bal is not None:
            await cb.message.answer(f"💰 رصيده الآن: {bal:.2f}")
    except Exception:
        pass


# ============================================================
# SHAM CASH LINK SCREENS [R6-PLUS14]
# ============================================================

SHAM_DEVICE = sham.DEFAULT_DEVICE if sham else "Redmi Note 11 Pro"

SHAM_POLL_SECONDS = 2.2   # إيقاع الاستطلاع
SHAM_POLL_TOTAL = 600     # نافذة الانتظار (ثانية)
SHAM_STATUS_EVERY = 30    # تحديث حالة كل N ثانية

_SHAM_TASKS: dict = {}  # admin_id -> asyncio.Task
_SHAM_LINKS: dict = {}  # admin_id -> جلسة ربط قيد الانتظار (لـ«فحص الآن»)


def _sham_feature_ok() -> bool:
    return sham is not None


async def _sham_load() -> dict | None:
    """قراءة الجلسة المحفوظة (مشفرة Fernet) — None إن لم توجد."""
    raw = await get_setting("sham_session")

    if not raw:
        return None

    try:
        data = json.loads(decrypt_password(raw))
        return data if data.get("token") else None
    except Exception:
        return None


async def _sham_save(sess: dict):
    await set_setting("sham_session",
                      encrypt_password(json.dumps(sess, ensure_ascii=False)))


async def _sham_clear():
    await set_setting("sham_session", "")


def _sham_wait_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text="🔄 فحص الآن", callback_data="sham_check_now")
    kb.button(text="❌ إلغاء", callback_data="sham_cancel_wait")
    kb.adjust(2)
    return kb.as_markup()


def _sham_wait_end_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text="🔄 فحص الآن", callback_data="sham_check_now")
    kb.button(text="🔗 ربط من جديد", callback_data="sham_link_start")
    kb.adjust(2)
    return kb.as_markup()


def _sham_home_kb(linked: bool):
    kb = InlineKeyboardBuilder()

    if linked:
        kb.button(text="💰 الأرصدة الحية", callback_data="sham_balances")
        kb.button(text="🧪 فحص وتشخيص", callback_data="sham_diag")
        kb.button(text="🔁 إعادة ربط", callback_data="sham_link_start")
        kb.button(text="🗑 إلغاء الربط", callback_data="sham_unlink")
    else:
        kb.button(text="🔗 ربط حساب الآن", callback_data="sham_link_start")

    kb.button(text="🔙 رجوع", callback_data="admin_manage_sham")  # [MENU-ORG]
    kb.adjust(2, 2, 1, 1)
    return kb.as_markup()


async def sham_home(cb: types.CallbackQuery, state: FSMContext):
    """شاشة حالة شام كاش."""
    if not await is_admin_or_supervisor(cb.from_user.id):
        await cb.answer("غير مصرّح.", show_alert=True)
        return

    await cb.answer()

    if not _sham_feature_ok():
        await safe_edit(cb.message,
                        "💵 <b>شام كاش</b>\n\n❌ وحدة sham_link غير متوفرة.",
                        InlineKeyboardBuilder().button(
                            text="🔙 رجوع", callback_data="admin_manage_sham",
                        ).adjust(1).as_markup())
        return

    if not await feat_on("sham_link"):
        await safe_edit(cb.message,
                        "💵 <b>شام كاش</b>\n\n⛔ الميزة معطلة من لوحة الميزات.",
                        InlineKeyboardBuilder().button(
                            text="🔙 رجوع", callback_data="admin_manage_sham",
                        ).adjust(1).as_markup())
        return

    await state.clear()
    sess = await _sham_load()

    if sess:
        txt = (
            "💵 <b>شام كاش — مرتبط ✅</b>\n\n"
            f"📱 الجهاز: <code>{esc(sess.get('device') or SHAM_DEVICE)}</code>\n"
            f"🕒 منذ: {esc(str(sess.get('linked_at') or '—'))}"
        )

        if sess.get("name"):
            txt += f"\n👤 {esc(str(sess['name']))}"

        txt += "\n\nاختر عملية:"
    else:
        txt = (
            "💵 <b>شام كاش — غير مرتبط</b>\n\n"
            "اضغط «ربط حساب الآن» وامسح الرمز من التطبيق:\n"
            "حسابي ← الأجهزة المرتبطة ← إنشاء جلسة جديدة"
        )

    await safe_edit(cb.message, txt, _sham_home_kb(bool(sess)))


@dp.callback_query(F.data == "sham_home")
async def sham_home_cb(cb: types.CallbackQuery, state: FSMContext):
    await sham_home(cb, state)


@dp.callback_query(F.data == "sham_link_start")
async def sham_link_start(cb: types.CallbackQuery, state: FSMContext):
    """توليد QR ربط جديد وإرساله داخل تلجرام + تشغيل المستطلع."""
    if not await is_admin_or_supervisor(cb.from_user.id):
        await cb.answer("غير مصرّح.", show_alert=True)
        return

    await cb.answer()

    if not _sham_feature_ok() or not await feat_on("sham_link"):
        await cb.answer("الميزة غير متاحة.", show_alert=True)
        return

    sess = await _sham_load()

    if sess:
        kb = InlineKeyboardBuilder()
        kb.button(text="✅ نعم، استبدل",
                  callback_data="sham_link_confirm")
        kb.button(text="❌ تراجع", callback_data="sham_home")
        kb.adjust(2)
        await safe_edit(
            cb.message,
            "⚠️ <b>يوجد حساب مرتبط حالياً</b>\n"
            f"({esc(str(sess.get('device') or ''))}"
            f"{(' — ' + esc(str(sess.get('name')))) if sess.get('name') else ''})\n\n"
            "الربط الجديد <b>سيستبدله</b>. متابعة؟",
            kb.as_markup(),
        )
        return

    await _sham_link_go(cb)


@dp.callback_query(F.data == "sham_link_confirm")
async def sham_link_confirm(cb: types.CallbackQuery, state: FSMContext):
    if not await is_admin_or_supervisor(cb.from_user.id):
        await cb.answer("غير مصرّح.", show_alert=True)
        return

    await cb.answer()
    await _sham_link_go(cb)


async def _sham_reach() -> tuple[bool, str]:
    """فحص وصول سريع لخادم شام كاش — أي رد من الخادم = الوصول سليم."""
    probe = sham.gen_link(SHAM_DEVICE)

    try:
        _data, note = await asyncio.wait_for(
            sham.check_session_ex(probe), timeout=8,
        )
        return True, note
    except asyncio.TimeoutError:
        return False, "بلا رد من الخادم (مهلة 8 ثوانٍ)"
    except asyncio.CancelledError:
        raise
    except Exception as exc:
        return False, f"{type(exc).__name__}: {exc}"[:150]


async def _sham_link_go(cb: types.CallbackQuery):
    admin_id = cb.from_user.id

    reachable, note = await _sham_reach()

    if not reachable:
        await safe_edit(
            cb.message,
            "❌ <b>لا يمكن الوصول إلى خادم شام كاش من هذا الجهاز</b>\n\n"
            f"السبب: <code>{esc(note)}</code>\n\n"
            "لن يُلتقط الاعتماد ما دام الوصول مقطوعاً. الأسباب الشائعة:\n"
            "• انقطاع/ضعف إنترنت الجهاز المشغّل للبوت\n"
            "• جدار حماية أو مضاد فيروسات يحجب البرنامج\n"
            "• مزوّد الإنترنت يحجب الخادم — جرب نقطة اتصال الهاتف\n\n"
            "صلح الوصول ثم أعد المحاولة.",
            InlineKeyboardBuilder().button(
                text="🔄 إعادة المحاولة",
                callback_data="sham_link_start",
            ).button(
                text="🔙 رجوع", callback_data="sham_home",
            ).adjust(1).as_markup(),
        )
        return

    link = sham.gen_link()  # [RAND-DEV 5.17] اسم جهاز عشوائي لكل ربط
    png = sham.qr_png(link["payload"])

    if png is None:
        await safe_edit(
            cb.message,
            "❌ مكتبة qrcode غير مثبتة — أضفها للمتطلبات: qrcode[pil]",
            InlineKeyboardBuilder().button(
                text="🔙 رجوع", callback_data="sham_home",
            ).adjust(1).as_markup(),
        )
        return

    old = _SHAM_TASKS.pop(admin_id, None)

    if old and not old.done():
        old.cancel()

    _SHAM_LINKS[admin_id] = link

    photo = BufferedInputFile(png, filename="sham_link.png")
    await cb.message.answer_photo(
        photo,
        caption=(
            "🔗 <b>ربط حساب شام كاش</b>\n\n"
            "من التطبيق: حسابي ← <b>الأجهزة المرتبطة</b> ← "
            "<b>إنشاء جلسة جديدة</b>\n"
            "ثم امسح <b>رمز هذه الرسالة</b> واعتمد.\n"
            "⚠️ الرموز القديمة من محادثات سابقة منتهية الصلاحية.\n\n"
            f"📱 سيظهر باسم: "
            f"<code>{esc(link.get('device') or SHAM_DEVICE)}</code>\n"
            "✅ فحص الوصول للخادم: سليم\n"
            "⏳ الصلاحية ~10 دقائق"
        ),
    )

    status = await cb.message.answer(
        "⏳ <b>بانتظار الاعتماد…</b>\n"
        "أستطلع الخادم كل ثانيتين حتى 10 دقائق.\n"
        "ستتحدث هذه الرسالة تلقائياً.",
        reply_markup=_sham_wait_kb(),
    )

    await audit(admin_id, "sham_link_start",
                details=f"sid={link['raw_sid'][:8]}…")

    task = asyncio.create_task(_sham_poll_task(admin_id, link, status))
    _SHAM_TASKS[admin_id] = task


async def _sham_finalize(admin_id: int, link: dict, data: dict,
                         status: types.Message) -> bool:
    """حفظ الجلسة بعد الالتقاط + التدقيق + تحديث رسالة الحالة."""
    sess = {
        "token": data.get("token") or "",
        "access_token": data.get("accessToken") or "",
        "inner_key": link["inner_key"],
        "raw_sid": link["raw_sid"],
        "device": link.get("device") or SHAM_DEVICE,
        "linked_at": now_iso()[:16],
        "role": data.get("role") or "",
    }

    try:
        prof = await sham.profile(sess)

        if isinstance(prof, list) and prof:
            sess["name"] = prof[0].get("name") or ""
            sess["contact"] = (prof[0].get("email")
                               or prof[0].get("phone_number") or "")
    except Exception:
        pass

    await _sham_save(sess)
    await audit(admin_id, "sham_link_linked",
                details=f"device={sess['device']}")
    _SHAM_TASKS.pop(admin_id, None)
    _SHAM_LINKS.pop(admin_id, None)

    try:
        await status.edit_text(
            "✅ <b>تم ربط حساب شام كاش بنجاح</b>\n\n"
            f"📱 الجهاز: <code>{esc(sess['device'])}</code>\n"
            + (f"👤 {esc(str(sess.get('name')))}\n"
               if sess.get("name") else "")
            + "افتح 💵 شام كاش للأرصدة والعمليات.",
            reply_markup=_sham_home_kb(True),
        )
    except Exception:
        logger.warning("[sham] تعذر تحديث رسالة الحالة")

    return True


async def _sham_poll_task(admin_id: int, link: dict, status: types.Message):
    """استطلاع خلفي بحالة حية — يعرض رد الخادم والمحاولات لحظة بلحظة."""
    loop = asyncio.get_running_loop()
    deadline = loop.time() + SHAM_POLL_TOTAL
    attempts = 0
    net_fails = 0
    last_detail = "—"
    last_status_edit = 0.0

    while loop.time() < deadline:
        attempts += 1
        data = None

        try:
            data, detail = await sham.check_session_ex(link)
            net_fails = 0
            last_detail = detail
        except asyncio.CancelledError:
            raise
        except Exception as exc:
            net_fails += 1
            last_detail = f"تعذر الاتصال ({type(exc).__name__})"

        if data:
            await _sham_finalize(admin_id, link, data, status)
            return

        now = loop.time()

        if now - last_status_edit >= SHAM_STATUS_EVERY:
            last_status_edit = now
            net_note = (
                f"\n⚠️ {net_fails} محاولة بلا اتصال — "
                "تحقق من إنترنت جهاز البوت/VPN"
                if net_fails >= 10 else ""
            )

            try:
                await status.edit_text(
                    "⏳ <b>بانتظار الاعتماد…</b>\n"
                    f"المحاولات: {attempts} | "
                    f"آخر رد: {esc(last_detail)}{net_note}\n\n"
                    "تأكد أنك امسحت <b>رمز هذه المحادثة</b> تحديداً "
                    "وأن الاعتماد تم من هاتف صاحب الحساب.",
                    reply_markup=_sham_wait_kb(),
                )
            except Exception:
                pass

        await asyncio.sleep(SHAM_POLL_SECONDS)

    _SHAM_TASKS.pop(admin_id, None)

    try:
        await status.edit_text(
            "⏰ <b>انتهت مهلة الاعتماد</b>\n"
            f"المحاولات: {attempts} | آخر رد: {esc(last_detail)}\n\n"
            "⚠️ الأسباب الشائعة:\n"
            "• مسح رمز قديم من محادثة سابقة — امسح رمز رسالة الربط "
            "الجديدة فقط\n"
            "• الاعتماد تم بعد انتهاء صلاحية الرمز\n"
            "• انقطاع اتصال الجهاز المشغّل للبوت\n\n"
            "ابدأ ربطاً جديداً.",
            reply_markup=_sham_wait_end_kb(),
        )
    except Exception:
        pass


@dp.callback_query(F.data == "sham_check_now")
async def sham_check_now(cb: types.CallbackQuery, state: FSMContext):
    """فحص فوري عند الطلب — يعرض رد الخادم الحقيقي."""
    if not await is_admin_or_supervisor(cb.from_user.id):
        await cb.answer("غير مصرّح.", show_alert=True)
        return

    admin_id = cb.from_user.id
    link = _SHAM_LINKS.get(admin_id)

    if not link:
        await cb.answer("لا توجد جلسة ربط قيد الانتظار.", show_alert=True)
        return

    await cb.answer("⏳ فحص…")

    try:
        data, detail = await asyncio.wait_for(
            sham.check_session_ex(link), timeout=12,
        )
    except asyncio.TimeoutError:
        data, detail = None, "تعذر الاتصال (مهلة 12 ثوانٍ بلا رد)"
    except asyncio.CancelledError:
        raise
    except Exception as exc:
        data, detail = None, f"تعذر الاتصال ({type(exc).__name__})"

    if data:
        old = _SHAM_TASKS.get(admin_id)

        if old and not old.done():
            old.cancel()

        await _sham_finalize(admin_id, link, data, cb.message)
        return

    # رسالة جديدة — الجواب الثاني على نفس الضغطة يرفضه تلجرام
    try:
        await cb.message.answer(
            f"🔍 <b>فحص فوري</b> — آخر رد الخادم:\n"
            f"<code>{detail[:350]}</code>",
        )
    except Exception:
        pass


@dp.callback_query(F.data == "sham_cancel_wait")
async def sham_cancel_wait(cb: types.CallbackQuery, state: FSMContext):
    if not await is_admin_or_supervisor(cb.from_user.id):
        await cb.answer("غير مصرّح.", show_alert=True)
        return

    await cb.answer()
    admin_id = cb.from_user.id
    old = _SHAM_TASKS.pop(admin_id, None)

    if old and not old.done():
        old.cancel()

    _SHAM_LINKS.pop(admin_id, None)

    try:
        await cb.message.edit_text(
            "🚫 أُلغي انتظار الربط.",
            reply_markup=InlineKeyboardBuilder().button(
                text="🔗 ربط من جديد", callback_data="sham_link_start",
            ).adjust(1).as_markup(),
        )
    except Exception:
        pass


# ============================================================
# [AUTO-DEP] الشحن الآلي: مراقبة الوارد (tranKind=1) ومطابقة strTranId
# ============================================================

SHAM_DEP_KEEP = 400            # أقصى عدد معرفات محفوظة (مستهلك/مرصود)


class ShamDepFSM(StatesGroup):  # [AUTO-DEP] إدخال العتبات
    value = State()


def _sham_dep_split(raw: str) -> set:
    return {x.strip() for x in (raw or "").split(",") if x.strip()}


def _txid_norm(v) -> str:
    """[AUTO-FIX 5.18.18] توحيد رقم العملية للمقارنة المرنة.

    يتجاهل الفراغات/الشرطات/الشرط السفلي وحالة الأحرف — فالمستخدم
    قد ينسخ الرقم بفراغ أو بحروف صغيرة من إشعار شام كاش.
    """
    return re.sub(r"[\s\-–—_]", "", str(v or "")).strip().upper()


class _ShamRejectedError(Exception):
    """[AUTO-FIX 5.18.18] رد رفض صريح من خادم شام كاش.

    يميز انتهاء الجلسة/رفض الخادم عن أخطاء الشبكة العابرة: الأول
    يوقف نافذة التحقق فوراً (لا جدوى من إعادة المحاولة)، والثاني
    تُعاود نبضة لاحقة محاولتها كالمعتاد.
    """


def _sham_dep_join(items: set) -> str:
    lst = sorted(items)[-SHAM_DEP_KEEP:]
    return ",".join(lst)


async def _sham_auto_notify(text: str):
    """إشعار الأدمن بأحداث الشحن الآلي."""
    try:
        await bot.send_message(ADMIN_USER_ID, text)
    except Exception:
        pass


# ─── [EVDEP 5.18] الشحن الآلي حدثي: نافذة 10 نبضات لكل طلب ───
# لا دوران زمني إطلاقاً: الطلب المسجل هو الذي يستدعي الفحص،
# ومسح أمان واحد يومياً بإزاحة عشوائية. صفر نبضات بلا طلبات.

_SHAM_WIN_DELTAS = (0, 60, 60, 120, 120, 180, 180, 180, 300, 300)
# نبضات متراكمة: 0, 1, 2, 4, 6, 9, 12, 15, 20, 25 دقيقة (~25د نافذة)

_sham_verify_lock = asyncio.Lock()


async def _notify_once(key: str, text: str):
    """إشعار الأدمن مرة واحدة لكل مفتاح (حرس ضد إزعاج النوافذ)."""
    seen = _sham_dep_split(await get_setting("shamdep_seen"))

    if key in seen:
        return

    seen.add(key)
    await set_setting("shamdep_seen", _sham_dep_join(seen))
    await _sham_auto_notify(text)


async def _sham_fetch_incoming(sess: dict, pages: int = 2) -> list:
    """جلب الوارد (tranKind=1) من صفحات السجل."""
    rows = []

    for page in range(1, max(1, pages) + 1):
        try:
            data = await sham.history(sess, page)
        except Exception:
            break  # خطأ عابر (شبكة/مهلة) — تُحاول النبضة التالية

        # [AUTO-FIX 5.18.18] رد رفض صريح (جلسة منتهية غالباً) —
        # كان يُعالج كأنه سجل فارغ فتموت نافذة التحقق بصمت
        if isinstance(data, dict) and data.get("succeeded") is False:
            raise _ShamRejectedError(
                str(data.get("message") or data.get("result")
                    or "رفض من خادم شام كاش"),
            )

        batch = []

        if isinstance(data, list):
            batch = data
        elif isinstance(data, dict):
            for k in ("items", "logs", "records", "data", "transactions"):
                v = data.get(k)

                if isinstance(v, list):
                    batch = v
                    break

        rows += [tx for tx in batch if isinstance(tx, dict)
                 and str(tx.get("tranKind") or "") == "1"]

        # [AUTO-FIX 5.18.18] تابع الصفحة التالية ما دامت الحالية غير
        # فارغة — كان الرد القائمة يوقف الترقيم بعد الصفحة الأولى
        # فتفلت عمليات موجودة بالصفحة 2+
        if not batch:
            break

        if isinstance(data, dict) and "haveNext" in data \
                and not data.get("haveNext"):
            break

    return rows


async def _sham_attempt(request_id: int) -> str:
    """محاولة اعتماد واحدة: مطابقة رقم العملية + المبلغ بالسجل.

    يعيد: approved | no_match | out_of_range | cap | consumed |
    not_pending | no_txid | no_session | disabled | fail_<سبب>
    """
    if not await feat_on("sham_auto_dep"):
        return "disabled"

    sess = await _sham_load()

    if not sess:
        # [AUTO-FIX 5.18.18] كان السكوت هنا يدفن فشل الشحن الآلي بلا
        # أي أثر — إشعار يومي واحد بدل الصمت التام
        await _notify_once(
            f"nosess:{datetime.now(timezone.utc):%Y-%m-%d}",
            "⚠️ <b>الشحن الآلي متوقف فعلياً</b> — جلسة شام كاش غير "
            "موجودة أو منتهية، فلا يمكن التحقق من أي عملية.\n"
            "أعد الربط من: الإدارة ← شام كاش ← 🔁 إعادة ربط،"
            " ثم جرّب الطلب من جديد.",
        )
        return "no_session"

    async with _sham_verify_lock:
        db = await get_db()

        try:
            cur = await db.execute(
                "SELECT * FROM finance_requests WHERE id = ?",
                (request_id,),
            )
            req = await cur.fetchone()
        finally:
            await db.close()

        if not req or req["type"] != "deposit" \
                or req["status"] != "pending":
            return "not_pending"

        m = re.search(r"txid=([^;]+)", req["note"] or "")

        if not m:
            return "no_txid"

        txid = m.group(1).strip()
        req_amt = round2(float(req["amount"]))
        consumed = _sham_dep_split(await get_setting("shamdep_consumed"))

        if txid in consumed:
            return "consumed"

        min_a = await get_float_setting("shamdep_min", 1.0)
        max_a = await get_float_setting("shamdep_max", 0.0)
        cap = await get_float_setting("shamdep_daily_cap", 0.0)
        like_today = f"{datetime.now(timezone.utc):%Y-%m-%d}%"

        db2 = await get_db()

        try:
            cur2 = await db2.execute(
                "SELECT COALESCE(SUM(amount), 0) AS s FROM finance_requests"
                " WHERE type = 'deposit' AND status = 'approved'"
                " AND processed_by = ? AND processed_at LIKE ?"
                " AND note LIKE '%auto=1%'",
                (ADMIN_USER_ID, like_today),
            )
            auto_today = round2(float((await cur2.fetchone())["s"]))
        finally:
            await db2.close()

        try:
            incoming = await _sham_fetch_incoming(sess, 2)
        except _ShamRejectedError as exc:
            # [AUTO-FIX 5.18.18] فشل صريح من الخادم (جلسة منتهية غالباً)
            # — كان يُبلَع كأنه "لا مطابقة" فتُهدر 25 دقيقة بلا سبب
            await _notify_once(
                f"histfail:{datetime.now(timezone.utc):%Y-%m-%d}",
                "⚠️ <b>تعذر قراءة سجل شام كاش</b> أثناء التحقق الآلي:\n"
                f"<code>{esc(str(exc))}</code>\n\n"
                "غالباً الجلسة منتهية — أعد الربط من شاشة شام كاش"
                " ثم أعد المحاولة.",
            )
            return "no_session"
        except Exception as exc:
            logger.warning("[evdep] تعذر جلب السجل: %s", exc)
            return "no_match"

        match = None
        mismatch = False

        for tx in incoming:
            # [AUTO-FIX 5.18.18] مقارنة موحدة تتحمل فراغات/شرطات/حالة
            if _txid_norm(tx.get("strTranId")) != _txid_norm(txid):
                continue

            amt = round2(float(tx.get("amount") or 0))

            if amt != req_amt:
                mismatch = True
                continue

            match = tx
            break

        # ── [WGT] فحص حارس المحفظة ضمن هذه النبضة (بلا نبضة جديدة) ──
        try:
            if await wgt_on() and await _wgt_quota_take():
                out = await _wgt_check_wallet(sess)

                if not out.get("ok") or out.get("kind") == "mismatch":
                    await _wgt_alert(out)
        except Exception:
            logger.exception("[wgt] خطأ بالفحص")

        if not match:
            if mismatch:
                await _notify_once(
                    txid,
                    "⚠️ <b>عدم تطابق المبالغ</b> — العملية "
                    f"<code>{esc(txid)}</code> مبلغها بالسجل ≠ الطلب "
                    f"#{request_id} ({req_amt:,.2f}). الطلب يبقى "
                    "معلقاً للمعالجة اليدوية.",
                )

            return "no_match"

        amt = round2(float(match.get("amount") or 0))

        if amt < min_a or (max_a > 0 and amt > max_a):
            await _notify_once(
                f"rng#{request_id}",
                f"⚖️ الطلب #{request_id} ({amt:,.2f}) خارج عتبات "
                "الشحن الآلي — يُعالج يدوياً.",
            )
            return "out_of_range"

        if cap > 0 and round2(auto_today + amt) > round2(cap):
            await _notify_once(
                f"cap#{request_id}",
                f"🛑 السقف اليومي للشحن الآلي يمنع #{request_id} "
                f"({amt:,.2f}) — المستهلك اليوم {auto_today:,.2f}/"
                f"{cap:,.2f}.",
            )
            return "cap"

        _req, status, _p = await process_finance_request(
            request_id, ADMIN_USER_ID, True,
        )

        if status != "approved":
            return f"fail_{status}"

        db3 = await get_db()

        try:
            await db3.execute(
                "UPDATE finance_requests SET note = note || ';auto=1'"
                " WHERE id = ? AND note NOT LIKE '%auto=1%'",
                (request_id,),
            )
            await db3.commit()
        finally:
            await db3.close()

        consumed.add(txid)
        await set_setting("shamdep_consumed", _sham_dep_join(consumed))
        await audit(
            ADMIN_USER_ID, "sham_auto_dep", f"request={request_id}",
            f"txid={txid};amount={amt};auto=1",
        )

        # [WGT] حدّث المرجع: الوارد المؤكد يرفع المتوقع
        try:
            if await wgt_on():
                stamp = await get_setting("shamwd_last_balance") or ""

                if "|" in stamp:
                    bal_raw, _ts = stamp.split("|", 1)
                    await set_setting(
                        "shamwd_last_balance",
                        f"{round2(float(bal_raw) + amt)}|"
                        f"{datetime.now(timezone.utc).isoformat()}",
                    )
        except Exception:
            pass

        try:
            await bot.send_message(
                int(req["telegram_id"]),
                "🤖 <b>تم اعتماد شحنك آلياً</b>\n"
                f"الطلب #{request_id} بمبلغ "
                f"<b>{round2(float(req['amount'])):,.2f}</b>\n"
                "تحقق من رصيدك من القائمة الرئيسية.",
            )
        except Exception:
            pass

        await _sham_auto_notify(
            f"✅ <b>شحن آلي</b> — طلب #{request_id} | {amt:,.2f} | "
            f"العملية <code>{esc(txid)}</code>",
        )
        return "approved"


async def _sham_verify_window(request_id: int):
    """نافذة التحقق: 10 نبضات متباعدة لطلب واحد ثم سكوت تام.

    أي نتيجة غير «لا مطابقة» توقف النافذة فوراً — وعند انتهائها
    بلا مطابقة يبقى الطلب للفحص اليدوي أو ينقذه المسح اليومي.
    """
    try:
        for delta in _SHAM_WIN_DELTAS:

            if delta:
                await asyncio.sleep(delta)

            st = await _sham_attempt(request_id)

            if st != "no_match":
                return

        # [AUTO-FIX 5.18.18] انتهت النافذة بلا مطابقة — إشعار بدل
        # السكوت، حتى يعرف الأدمن أن الآلي حاول وفشل ولماذا يراجع يدوياً
        await _notify_once(
            f"winend:{request_id}",
            "⌛ <b>انتهت نافذة التحقق الآلي</b> (~25 دقيقة) للطلب "
            f"#{request_id} دون العثور على عملية مطابقة بسجل شام كاش.\n"
            "الطلب بانتظار المعالجة اليدوية.\n\n"
            "تأكد من: رقم العملية صحيح، المبلغ المُحوَّل = مبلغ الطلب"
            " تماماً، وأن التحويل وصل لحساب البوت المرتبط."
            " استخدم زر 🧪 من شاشة شام كاش لرؤية السجل الفعلي.",
        )

    except asyncio.CancelledError:
        raise
    except Exception:
        logger.exception("[evdep] خطأ بنافذة التحقق #%s", request_id)


async def _sham_sweep() -> dict:
    """المسح اليومي للأمان: ينقذ ما فاتت نوافذه + يرصد الوارد الشارد."""
    stats = {"approved": 0, "seen": 0, "unmatched": 0}

    if not await feat_on("sham_auto_dep"):
        return stats

    sess = await _sham_load()

    if not sess:
        return stats

    first = not (await get_setting("shamdep_last_sweep") or "")
    consumed = _sham_dep_split(await get_setting("shamdep_consumed"))
    seen = _sham_dep_split(await get_setting("shamdep_seen"))
    events = []

    try:
        incoming = await _sham_fetch_incoming(sess, 3)
    except Exception as exc:
        logger.warning("[evdep] فشل المسح اليومي: %s", exc)
        return stats

    for tx in incoming:
        tid = str(tx.get("strTranId") or "").strip()

        if not tid or tid in consumed or tid in seen:
            continue

        seen.add(tid)
        stats["seen"] += 1
        amt = round2(float(tx.get("amount") or 0))

        db = await get_db()

        try:
            cur = await db.execute(
                "SELECT id FROM finance_requests WHERE type = 'deposit'"
                " AND status = 'pending'"
                " AND instr(note || ';', 'txid=' || ? || ';') > 0"
                " ORDER BY id LIMIT 1",
                (tid,),
            )
            row = await cur.fetchone()
        finally:
            await db.close()

        if row:
            st = await _sham_attempt(int(row["id"]))

            if st == "approved":
                stats["approved"] += 1
                events.append(
                    f"✅ مسح يومي: طلب #{row['id']} | {amt:,.2f} | "
                    f"العملية <code>{esc(tid)}</code>",
                )
                continue

        if first:
            continue  # أول مسح: رصد فقط بلا إزعاج

        stats["unmatched"] += 1
        events.append(
            "🟡 <b>وارد بلا طلب معلق</b>\n"
            f"رقم العملية: <code>{esc(tid)}</code> | "
            f"المبلغ: <b>{amt:,.2f}</b>\n"
            f"من: <code>{esc(str(tx.get('peerAccountNumber') or '?'))}"
            f"</code>\nعلّم الطلب أو تجاهل — لن يُعتمد آلياً.",
        )

    await set_setting("shamdep_seen", _sham_dep_join(seen))
    await set_setting("shamdep_consumed", _sham_dep_join(consumed))
    await set_setting(
        "shamdep_last_sweep", datetime.now(timezone.utc).isoformat(),
    )

    if events:
        await _sham_auto_notify(
            "🧹 <b>المسح اليومي للشحن الآلي</b>\n\n"
            + "\n\n".join(events[:5]),
        )

    return stats


# ═══ [WGT 5.18.1] حارس المحفظة: مقارنة الرصيد + إنذار موت الجلسة ═══
# نبضات محدودة بالكامل بموجب EVDEP: تُنفَّذ ضمن نوافذ _sham_attempt
# والمسح اليومي — ولا تضيف أي نبضة جديدة إطلاقاً.

_WGT_MIN_INTERVAL = 3600 * 2  # حدا أدنى بين تبليغين من نفس النوع
_wgt_last_alert: dict = {}    # {type: ts} — ذاكرة تنبيهات العملية


def _wgt_should_alert(kind: str) -> bool:
    import time as _time

    last = _wgt_last_alert.get(kind, 0)

    if _time.time() - last < _WGT_MIN_INTERVAL:
        return False

    _wgt_last_alert[kind] = _time.time()
    return True


async def wgt_on() -> bool:
    """هل حارس المحفظة مفعّل؟ (الميزة الجديدة default=0)."""
    return await feat_on("sham_wallet_guard")


async def _wgt_expected_balance() -> float | None:
    """المتوفر المتوقع = آخر رصيد معروف + صادر متوقع − وارد مؤكد.

    آخر رصيد معروف: قيمة آخر مسح/نبضة ناجحة (shamwd_last_balance).
    الصادر المتوقع: أوامر دفع شام «مدفوعة» بالكامل (تحويلات خرجت).
    الوارد المؤكد: شحنات auto=1 المعتمدة بعد طابع آخر رصيد معروف.
    """
    stamp = await get_setting("shamwd_last_balance") or ""

    if not stamp or "|" not in stamp:
        return None  # لا مرجع بعد — أول نجاح يبنيه

    bal_raw, last_ts = stamp.split("|", 1)
    expected = float(bal_raw)

    # [WGTWIN 5.18.17] now_iso بدقة ثوانٍ — نزح الطابع ثانية للخلف
    # حتى لا تُفلت مدفوعات نفس الثانية (شمولية النافذة)
    try:
        _dt = datetime.fromisoformat(last_ts)
        _dt = _dt - timedelta(seconds=1)
        last_ts_cmp = _dt.isoformat(timespec="seconds")
    except Exception:
        last_ts_cmp = last_ts

    db = await get_db()

    try:
        cur = await db.execute(
            "SELECT COALESCE(SUM(amount), 0) AS s FROM payouts"
            " WHERE status = 'paid' AND external_id LIKE 'sham:%'"
            " AND processed_at >= ?",
            (last_ts_cmp,),  # [WGTWIN 5.18.17] نافذة الطابع (بإزاحة أمان)
        )
        expected -= float((await cur.fetchone())["s"])

        cur = await db.execute(
            "SELECT COALESCE(SUM(fr.amount), 0) AS s"
            " FROM finance_requests fr"
            " WHERE fr.type = 'deposit' AND fr.status = 'approved'"
            " AND fr.processed_by = ? AND fr.note LIKE '%auto=1%'"
            " AND fr.processed_at >= ?",
            (ADMIN_USER_ID, last_ts_cmp),
        )
        dep_after = float((await cur.fetchone())["s"])
    finally:
        await db.close()

    return round2(expected + dep_after)


async def _wgt_quota_take() -> bool:
    """اسحب نبضة حارس من حصة اليوم (wgt_day_quota). True إن سُمحت."""
    quota = int(float(await get_setting("wgt_day_quota") or 1) or 1)
    quota = max(1, min(6, quota))
    today = f"{datetime.now(timezone.utc):%Y-%m-%d}"
    raw = await get_setting("wgt_day_used") or ""

    used_date, used_n = today, 0

    if ":" in raw:
        d, n = raw.split(":", 1)

        if d == today:
            used_n = int(n or 0)

    if used_n >= quota:
        return False

    await set_setting("wgt_day_used", f"{today}:{used_n + 1}")
    return True


async def _wgt_check_wallet(sess: dict) -> dict:
    """فحص واحد: رصيد فعلي مقابل متوقع + صحة الجلسة. بلا أي إرسال."""
    out = {"ok": False, "kind": "", "actual": 0.0, "expected": None,
           "currency": ""}

    try:
        bal = await sham.balances(sess)
    except sham.ShamError as exc:
        out["kind"] = f"session:{exc}"
        return out

    if not isinstance(bal, dict) or not bal.get("balances"):
        out["kind"] = "bad_payload"
        return out

    primary = None

    for b_row in bal["balances"]:
        if primary is None or float(b_row.get("balance") or 0) \
                > float(primary.get("balance") or 0):
            primary = b_row

    if primary is None:
        out["kind"] = "bad_payload"
        return out

    actual = round2(float(primary.get("balance") or 0))
    out["ok"] = True
    out["actual"] = actual
    out["currency"] = str(primary.get("currencyName") or "")
    stamp = f"{actual}|{datetime.now(timezone.utc).isoformat()}"
    await set_setting("shamwd_last_balance", stamp)

    expected = await _wgt_expected_balance()

    if expected is not None and abs(actual - expected) > 0.01:
        out["kind"] = "mismatch"
        out["expected"] = expected

    return out


async def _wgt_alert(out: dict):
    if out.get("kind") == "mismatch" and _wgt_should_alert("mismatch"):
        await _sham_auto_notify(
            "🛡 <b>حارس المحفظة: عدم تطابق رصيد!</b>\n"
            f"الفعلي: <b>{out['actual']:,.2f}</b> "
            f"{esc(out.get('currency') or '')}\n"
            f"المتوقع: <b>{float(out['expected']):,.2f}</b>\n"
            "راجع المحفظة وسجلها فوراً — قد يكون وارد غير مُعتمد أو"
            " خروج غير مُسجّل.",
        )
    elif str(out.get("kind", "")).startswith("session:") \
            and _wgt_should_alert("session"):
        await _sham_auto_notify(
            "🚨 <b>حارس المحفظة: الجلسة لا تستجيب!</b>\n"
            f"السبب: <code>{esc(str(out['kind'])[:150])}</code>\n"
            "الشحن/السحب الآليان لن يعملا حتى إعادة الربط —"
            " افتح 💵 شام كاش ← ربط QR جديد.",
        )


async def _sham_sweep_loop():
    """مسح واحد يومياً بإزاحة عشوائية — لا نبض دوري إطلاقاً.

    [WGT 5.18.1] إن فُعّل حارس المحفظة فحصه يُنفَّذ ضمن نبضة
    المسح نفسها (بلا أي نبضة إضافية).
    """
    try:
        await asyncio.sleep(3600 * 6 + secrets.randbelow(3600 * 6))
    except asyncio.CancelledError:
        raise

    while True:
        try:
            await _sham_sweep()

            if await wgt_on():
                sess = await _sham_load()

                if sess:
                    out = await _wgt_check_wallet(sess)
                    await _wgt_alert(out)
        except asyncio.CancelledError:
            raise
        except Exception:
            logger.exception("[evdep] خطأ بالمسح اليومي")

        try:
            await asyncio.sleep(3600 * 22 + secrets.randbelow(3600 * 4))
        except asyncio.CancelledError:
            raise


@dp.callback_query(F.data == "sham_auto_screen")
async def sham_auto_screen(cb: types.CallbackQuery, state: FSMContext):
    """شاشة الشحن الآلي: الحالة + العتبات + التفعيل."""
    if not await is_admin_or_supervisor(cb.from_user.id, "finance"):
        await cb.answer("⚠️ للأدمن فقط!", show_alert=True)
        return

    await cb.answer()
    await state.clear()

    on = await feat_on("sham_auto_dep")
    min_a = await get_float_setting("shamdep_min", 1.0)
    max_a = await get_float_setting("shamdep_max", 0.0)
    cap = await get_float_setting("shamdep_daily_cap", 0.0)
    linked = bool(await _sham_load())
    last = (await get_setting("shamdep_last_check") or "")[:16]

    like_today = f"{datetime.now(timezone.utc):%Y-%m-%d}%"
    db = await get_db()

    try:
        cur = await db.execute(
            "SELECT COALESCE(SUM(amount), 0) AS s FROM finance_requests"
            " WHERE type = 'deposit' AND status = 'approved'"
            " AND processed_by = ? AND processed_at LIKE ?"
            " AND note LIKE '%auto=1%'",
            (ADMIN_USER_ID, like_today),
        )
        auto_today = round2(float((await cur.fetchone())["s"]))
    finally:
        await db.close()

    b = InlineKeyboardBuilder()
    b.button(
        text=("⏹ إيقاف الشحن الآلي" if on else "▶️ تفعيل الشحن الآلي"),
        callback_data="sham_auto_toggle",
    )
    b.button(text=f"1️⃣ الحد الأدنى: {min_a:,.2f}",
             callback_data="shamdep_set_min")
    b.button(text=f"2️⃣ الحد الأقصى: "
             + (f"{max_a:,.2f}" if max_a > 0 else "بلا حد"),
             callback_data="shamdep_set_max")
    b.button(text=f"3️⃣ السقف اليومي: "
             + (f"{cap:,.2f}" if cap > 0 else "بلا سقف"),
             callback_data="shamdep_set_cap")
    b.button(text="🔙 رجوع", callback_data="admin_manage_sham")
    b.adjust(1)

    await safe_edit(
        cb.message,
        "🤖 <b>الشحن الآلي — شام كاش</b>\n\n"
        f"الحالة: {'🟢 مفعّل' if on else '🔴 متوقف'}\n"
        f"🔗 الجلسة: {'✅ مرتبطة' if linked else '❌ غير مرتبطة'}\n"
        f"🕒 آخر فحص: {esc(last or '—')}\n"
        f"📅 اعتمادات آلية اليوم: <b>{auto_today:,.2f}</b>\n\n"
        "⚙️ <b>العتبات</b> (اطلبه يدوياً خارجها):\n"
        f"• الحد الأدنى: {min_a:,.2f}\n"
        f"• الحد الأقصى: "
        + (f"{max_a:,.2f}" if max_a > 0 else "بلا حد") + "\n"
        f"• السقف اليومي: "
        + (f"{cap:,.2f}" if cap > 0 else "بلا سقف") + "\n\n"
        "🛡 يُعتمد فقط ما تطابق: رقم العملية + المبلغ + طلب معلق،"
        " وكل عملية تُستهلك مرة واحدة، وأول تشغيل يرصد فقط بلا اعتماد.",
        b.as_markup(),
    )


@dp.callback_query(F.data == "sham_auto_toggle")
async def sham_auto_toggle(cb: types.CallbackQuery, state: FSMContext):
    if not await is_admin_or_supervisor(cb.from_user.id, "finance"):
        await cb.answer("⚠️ للأدمن فقط!", show_alert=True)
        return

    await cb.answer()
    on = await feat_on("sham_auto_dep")

    if not on:
        # قبل التفعيل: يجب جلسة مرتبطة + حد أدنى > 0
        if not await _sham_load():
            await cb.answer("اربط حساب شام كاش أولاً.", show_alert=True)
            return

        min_a = await get_float_setting("shamdep_min", 1.0)

        if min_a <= 0:
            await cb.answer(
                "اضبط الحد الأدنى أولاً (قيمة أكبر من صفر).",
                show_alert=True,
            )
            return

        await set_setting("feat_sham_auto_dep", "1")
        await audit(cb.from_user.id, "sham_auto_dep", "", "enabled")
        await cb.answer("🟢 فُعّل الشحن الآلي — أول دورة رصد فقط.",
                        show_alert=True)
    else:
        await set_setting("feat_sham_auto_dep", "0")
        await audit(cb.from_user.id, "sham_auto_dep", "", "disabled")
        await cb.answer("⏹ أُوقف الشحن الآلي.", show_alert=True)

    await sham_auto_screen(cb, state)


@dp.callback_query(F.data.startswith("shamdep_set_"))
async def shamdep_set_start(cb: types.CallbackQuery, state: FSMContext):
    if not await is_admin_or_supervisor(cb.from_user.id, "finance"):
        await cb.answer("⚠️ للأدمن فقط!", show_alert=True)
        return

    await cb.answer()
    field = cb.data.rsplit("_", 1)[-1]  # min / max / cap
    await state.update_data(shamdep_field=field)
    await state.set_state(ShamDepFSM.value)

    labels = {"min": "الحد الأدنى", "max": "الحد الأقصى (0 = بلا حد)",
              "cap": "السقف اليومي (0 = بلا سقف)"}
    await cb.message.answer(
        f"⚙️ أرسل قيمة <b>{labels.get(field, field)}</b> (رقم):\n"
        "للإلغاء أرسل /cancel",
        reply_markup=back_kb("sham_auto_screen"),
    )


@dp.message(ShamDepFSM.value)
async def shamdep_set_save(message: types.Message, state: FSMContext):
    if not await is_admin_or_supervisor(message.from_user.id, "finance"):
        await state.clear()
        return

    raw = (message.text or "").strip().replace(",", ".")

    try:
        val = float(raw)
        assert val >= 0
    except Exception:
        await message.answer("❌ أرسل رقماً صحيحاً (≥ 0).")
        return

    data = await state.get_data()
    field = data.get("shamdep_field") or "min"
    await state.clear()
    await set_setting(f"shamdep_{field}", str(val))
    await audit(message.from_user.id, "shamdep_limit", field, str(val))
    await message.answer(f"✅ حُفظت القيمة: {val:,.2f}")


# ═══════════════════════════════════════════════════════════════
# [AUTO-WD] السحب الآلي: تنفيذ مدفوعات شام كاش لطلبات السحب المعلقة
# الحواجز (إلزامية كلها):
#   1) تفعيل للأدمن الرئيسي فقط وبـPIN (موافقة مزدوجة).
#   2) عتبات: أدنى/أقصى للعملية + سقف يومي للمنظومة + سقف لكل مستخدم.
#   3) كل طلب يُلمس مرة واحدة فقط (وسم wdauto=…) — لا إعادة إرسال أبداً.
#   4) لا يُعلَّم أمر الدفع «مدفوعاً» إلا بمرجع شام مُتحقق (من الرد
#      أو من السجل الصادر) — وأي غموض = تجميد فوري + إشعار.
# ═══════════════════════════════════════════════════════════════

class ShamWdFSM(StatesGroup):  # [AUTO-WD] إدخال العتبات وPIN
    value = State()   # قيمة عتبة رقمية
    pin_set = State()  # تعيين PIN
    pin_chk = State()  # إدخال PIN للتفعيل


SHAMWD_PERIOD = 60  # ثانية بين دورات السحب الآلي


def _sha256_hex(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


async def _wd_mark(request_id: int, tag: str):
    """وسم الطلب كي يُلمس مرة واحدة فقط — لا إعادة محاولة آلية أبداً."""
    db = await get_db()

    try:
        await db.execute(
            "UPDATE finance_requests SET note = note || ?"
            " WHERE id = ? AND note NOT LIKE '%wdauto=%'",
            (f";wdauto={tag}", request_id),
        )
        await db.commit()
    finally:
        await db.close()


async def _sham_wd_freeze(reason: str):
    """تجميد فوري: إيقاف الميزة + سبب يظهر بالشاشة حتى يفحصه الأدمن."""
    await set_setting("feat_sham_auto_wd", "0")
    await set_setting("shamwd_freeze_note", reason[:300])
    await audit(
        ADMIN_USER_ID, "sham_auto_wd", "",
        f"frozen:{reason[:80]}",
    )
    await _sham_auto_notify(
        "🧊 <b>تجميد السحب الآلي!</b>\n" + esc(reason)
        + "\n\nافحص محفظة شام كاش وأوامر الدفع المعلقة، ثم أعد"
        " التفعيل من الشاشة بعد التأكد فقط.",
    )


async def _sham_wd_tick() -> dict:
    """دورة واحدة: طلبات سحب مؤهلة → اعتماد → تحويل شام → تحقق → تعليم.

    الترتيب مقصود: الاعتماد أولاً (خصم رصيد البوت + أمر دفع معلق) ثم
    الإرسال — فإذا فشل الإرسال يبقى أمر الدفع معلقاً (مسترد يدوياً)
    بدل إرسال مال بلا قيد محاسبي.
    """
    stats = {"executed": 0, "skipped": 0, "failed": 0}

    if not await feat_on("sham_auto_wd"):
        return stats

    if await get_setting("shamwd_freeze_note"):
        return stats  # مجمد بانتظار فحص الأدمن

    sess = await _sham_load()

    if not sess:
        # [AUTO-FIX 5.18.18] إشعار يومي واحد بدل السكوت التام
        await _notify_once(
            f"wdnosess:{datetime.now(timezone.utc):%Y-%m-%d}",
            "⚠️ <b>السحب الآلي متوقف فعلياً</b> — جلسة شام كاش غير "
            "موجودة أو منتهية، فلا تُنفَّذ أي سحوبات آلية.\n"
            "أعد الربط من: الإدارة ← شام كاش ← 🔁 إعادة ربط.",
        )
        return stats

    min_a = await get_float_setting("shamwd_min", 1.0)
    max_a = await get_float_setting("shamwd_max", 200.0)   # 0 = بلا حد
    cap = await get_float_setting("shamwd_daily_cap", 200.0)  # 0 = بلا سقف
    ucap = await get_float_setting("shamwd_user_cap", 100.0)  # 0 = بلا سقف

    like_today = f"{datetime.now(timezone.utc):%Y-%m-%d}%"
    # عمر ≥ 60ث: فرصة لمهام ما بعد الإنشاء (شذوذ/احتجاز) ولا سباق معها
    cutoff = (
        datetime.now(timezone.utc) - timedelta(seconds=60)
    ).isoformat()

    db = await get_db()

    try:
        cur = await db.execute(
            "SELECT user_tid, COALESCE(SUM(amount), 0) AS s FROM payouts"
            " WHERE status = 'paid' AND external_id LIKE 'sham:%'"
            " AND processed_at LIKE ? GROUP BY user_tid",
            (like_today,),
        )
        used_by_user = {}

        for r in await cur.fetchall():
            used_by_user[int(r["user_tid"])] = round2(float(r["s"]))

        used_total = round2(sum(used_by_user.values()))

        cur = await db.execute(
            "SELECT * FROM finance_requests WHERE type = 'withdraw'"
            " AND status = 'pending' AND created_at <= ?"
            " AND note NOT LIKE '%wdauto=%' ORDER BY id LIMIT 5",
            (cutoff,),
        )
        rows = await cur.fetchall()
    finally:
        await db.close()

    events = []
    today_short = like_today[:10]
    cap_noted_day = await get_setting("shamwd_last_cap_note") or ""

    for req in rows:
        amount = round2(float(req["amount"]))
        m = re.search(r"dest=([^;]+)", req["note"] or "")
        dest = m.group(1).strip() if m else ""

        if not dest:
            await _wd_mark(req["id"], "manual")
            stats["skipped"] += 1
            events.append(f"↩️ طلب #{req['id']} بلا وجهة — يُعالج يدوياً.")
            continue

        if amount < min_a or (max_a > 0 and amount > max_a):
            await _wd_mark(req["id"], "range")
            stats["skipped"] += 1
            events.append(
                f"⚖️ طلب #{req['id']} خارج النطاق ({amount:,.2f})"
                " — يُعالج يدوياً.",
            )
            continue

        if cap > 0 and round2(used_total + amount) > round2(cap):
            stats["skipped"] += 1  # يبقى معلقاً بلا وسم — قد يمر غداً

            if cap_noted_day != today_short:
                events.append(
                    f"🛑 السقف اليومي للسحب الآلي يمنع #{req['id']}"
                    f" ({amount:,.2f}) — المستهلك اليوم "
                    f"{used_total:,.2f}/{cap:,.2f}.",
                )
                await set_setting("shamwd_last_cap_note", today_short)
                cap_noted_day = today_short

            continue

        u_used = used_by_user.get(int(req["telegram_id"]), 0.0)

        if ucap > 0 and round2(u_used + amount) > round2(ucap):
            stats["skipped"] += 1

            if cap_noted_day != today_short:
                events.append(
                    f"🛑 سقف المستخدم اليومي يمنع #{req['id']}"
                    f" ({amount:,.2f}) — استهلاكه "
                    f"{u_used:,.2f}/{ucap:,.2f}.",
                )
                await set_setting("shamwd_last_cap_note", today_short)
                cap_noted_day = today_short

            continue

        # ---- الاعتماد: خصم رصيد البوت + أمر دفع معلق (نفس معاملة) ----
        _req, status, payout_id = await process_finance_request(
            req["id"], ADMIN_USER_ID, True,
        )

        if status != "approved":
            if status in ("insufficient_balance", "user_not_found"):
                await _wd_mark(req["id"], "manual")

            stats["skipped"] += 1
            events.append(
                f"⚠️ الطلب #{req['id']} لم يُعتمد ({esc(status)}).",
            )
            continue

        # ---- [WD-BREATH] تنفّس بشري بين التحويلات المتتالية ----
        if stats["executed"] > 0:
            gap = 20 + (secrets.randbelow(41))  # 20-60 ثانية
            await _sham_auto_notify(
                f"⏳ تنفّس {gap}ث قبل السحب التالي (إيقاع بشري).",
            )
            await asyncio.sleep(gap)

        # ---- إرسال شام كاش + تحقق مستقل بالمرجع ----
        try:
            res = await sham.send_transfer(
                sess, dest, amount, note=f"WD{req['id']}",
            )
        except Exception as exc:
            await _wd_mark(req["id"], "sendfail")
            stats["failed"] += 1
            await _sham_wd_freeze(
                f"فشل إرسال السحب #{req['id']} ({amount:,.2f} ← {dest}):"
                f" {exc}. رصيد المستخدم خُصص وأمر الدفع معلق — نفّذه"
                " يدوياً أو علّمه فاشلاً (باسترداد) من إدارة الأوامر.",
            )
            break

        if sham.res_failed(res):
            await _wd_mark(req["id"], "sendfail")
            stats["failed"] += 1
            await _sham_wd_freeze(
                f"رفض شام كاش السحب #{req['id']}: "
                f"{esc(str(res.get('message') or res.get('result') or '?'))}."
                f"\n📄 <b>الرد الخام</b> (أرسله للأدمن التقني لتصحيح"
                " صيغة الإرسال):\n"
                f"<code>{esc(str(res)[:400])}</code>"
                "\n\nأمر الدفع معلق — عالجه يدوياً.",
            )
            break

        ref = sham.tx_ref_from_res(res)

        if not ref:
            # لا مرجع بالرد → تحقق مستقل من السجل الصادر (3 محاولات)
            for _ in range(3):
                try:
                    tx = await sham.find_outgoing(sess, amount, dest)
                except Exception:
                    tx = None

                if tx:
                    ref = str(tx.get("strTranId")
                              or tx.get("tranId") or "")
                    break

                await asyncio.sleep(2)

        if not ref:
            await _wd_mark(req["id"], "ambig")
            stats["failed"] += 1
            await _sham_wd_freeze(
                f"نتيجة غير مؤكدة للسحب #{req['id']} "
                f"({amount:,.2f} ← {dest}) — لا مرجع بالإرسال ولا"
                " بالسجل."
                f"\n📄 <b>الرد الخام</b> (أرسله للأدمن التقني):"
                f"\n<code>{esc(str(res)[:400])}</code>"
                "\n\nتحقق من محفظة شام قبل أي إجراء.",
            )
            break

        paid = bool(payout_id) and await mark_payout_paid(
            payout_id, external_id=f"sham:{ref}",
            admin_id=ADMIN_USER_ID,
        )

        if not paid:
            await _wd_mark(req["id"], "ambig")
            stats["failed"] += 1
            await _sham_wd_freeze(
                f"السحب #{req['id']} أُرسل (مرجع {ref}) لكن تعليم"
                " أمر الدفع فشل — راجع الأوامر يدوياً فوراً.",
            )
            break

        used_by_user[int(req["telegram_id"])] = round2(u_used + amount)
        used_total = round2(used_total + amount)
        stats["executed"] += 1
        await _wd_mark(req["id"], "done")
        await audit(
            ADMIN_USER_ID, "sham_auto_wd", f"request={req['id']}",
            f"ref={ref};amount={amount};dest={dest}",
        )

        try:
            await bot.send_message(
                int(req["telegram_id"]),
                "🤖 <b>تم تنفيذ سحبك آلياً</b>\n"
                f"الطلب #{req['id']} — <b>{amount:,.2f}</b> إلى\n"
                f"<code>{esc(dest)}</code>\n"
                f"مرجع شام كاش: <code>{esc(ref)}</code>",
            )
        except Exception:
            pass

        events.append(
            f"✅ سحب آلي #{req['id']} | {amount:,.2f} ← "
            f"<code>{esc(dest)}</code> | مرجع <code>{esc(ref)}</code>",
        )

    if events:
        await _sham_auto_notify(
            "🤖 <b>السحب الآلي — أحداث الدورة</b>\n\n"
            + "\n\n".join(events[:5]),
        )

    if stats["executed"]:
        logger.info("[auto-wd] %s", stats)

    return stats


async def _sham_wd_loop():
    while True:
        try:
            await _sham_wd_tick()
        except asyncio.CancelledError:
            raise
        except Exception:
            logger.exception("[auto-wd] خطأ بالدورة")

        await asyncio.sleep(SHAMWD_PERIOD)


@dp.callback_query(F.data == "sham_wd_screen")
async def sham_wd_screen(cb: types.CallbackQuery, state: FSMContext):
    """شاشة السحب الآلي: الحالة + الحواجز + التفعيل."""
    if not await is_admin_or_supervisor(cb.from_user.id, "finance"):
        await cb.answer("⚠️ للأدمن فقط!", show_alert=True)
        return

    await cb.answer()
    await state.clear()

    on = await feat_on("sham_auto_wd")
    frozen = await get_setting("shamwd_freeze_note") or ""
    pin_on = bool(await get_setting("shamwd_pin_sha"))
    linked = bool(await _sham_load())
    min_a = await get_float_setting("shamwd_min", 1.0)
    max_a = await get_float_setting("shamwd_max", 200.0)
    cap = await get_float_setting("shamwd_daily_cap", 200.0)
    ucap = await get_float_setting("shamwd_user_cap", 100.0)

    like_today = f"{datetime.now(timezone.utc):%Y-%m-%d}%"
    db = await get_db()

    try:
        cur = await db.execute(
            "SELECT COUNT(*) AS c, COALESCE(SUM(amount), 0) AS s"
            " FROM payouts WHERE status = 'paid'"
            " AND external_id LIKE 'sham:%' AND processed_at LIKE ?",
            (like_today,),
        )
        row = await cur.fetchone()
        wd_today_n, wd_today_s = row["c"], round2(float(row["s"]))
    finally:
        await db.close()

    old_wd = (await get_setting("auto_wd_enabled") or "0") == "1"

    b = InlineKeyboardBuilder()
    b.button(
        text=("⏹ إيقاف السحب الآلي" if on else "▶️ تفعيل السحب الآلي"),
        callback_data="sham_wd_toggle",
    )
    b.button(
        text=("🔑 تغيير PIN التفعيل" if pin_on else "🔑 تعيين PIN التفعيل"),
        callback_data="sham_wd_pin",
    )
    b.button(text=f"1️⃣ أدنى سحب: {min_a:,.2f}",
             callback_data="shamwd_set_min")
    b.button(text=f"2️⃣ أقصى سحب: "
             + (f"{max_a:,.2f}" if max_a > 0 else "بلا حد"),
             callback_data="shamwd_set_max")
    b.button(text=f"3️⃣ سقف المنظومة اليومي: "
             + (f"{cap:,.2f}" if cap > 0 else "بلا سقف"),
             callback_data="shamwd_set_cap")
    b.button(text=f"4️⃣ سقف المستخدم اليومي: "
             + (f"{ucap:,.2f}" if ucap > 0 else "بلا سقف"),
             callback_data="shamwd_set_ucap")
    b.button(text="🔙 رجوع", callback_data="admin_manage_sham")
    b.adjust(1)

    txt = (
        "🤖 <b>السحب الآلي — شام كاش</b>\n\n"
        f"الحالة: {'🟢 مفعّل' if on else '🔴 متوقف'}\n"
        f"🔗 الجلسة: {'✅ مرتبطة' if linked else '❌ غير مرتبطة'}\n"
        f"🔐 PIN: {'✅ معيّن' if pin_on else '❌ غير معيّن (المطلوب للتفعيل)'}\n"
        f"📅 تحويلات آلية اليوم: <b>{wd_today_n}</b> بمجموع "
        f"<b>{wd_today_s:,.2f}</b>\n\n"
    )

    if frozen:
        txt += f"🧊 <b>مجممد حالياً:</b>\n{esc(frozen)}\n\n"

    if old_wd:
        txt += ("⚠️ <b>تنبيه:</b> نظام قائمة الثقة القديم (auto_wd)"
                " مفعّل — يعلّم أوامر الدفع «مدفوعة» دون إرسال فعلي!"
                " عطّله لتفادي الالتباس.\n\n")

    txt += (
        "⚙️ <b>العتبات</b> (خارجها يُعاد للمعالجة اليدوية):\n"
        f"• أدنى سحب: {min_a:,.2f}\n"
        f"• أقصى سحب: "
        + (f"{max_a:,.2f}" if max_a > 0 else "بلا حد") + "\n"
        f"• سقف المنظومة اليومي: "
        + (f"{cap:,.2f}" if cap > 0 else "بلا سقف") + "\n"
        f"• سقف المستخدم اليومي: "
        + (f"{ucap:,.2f}" if ucap > 0 else "بلا سقف") + "\n\n"
        "🛡 التنفيذ: اعتماد الطلب ← تحويل شام ← تحقق بمرجع من الرد أو"
        " السجل الصادر ← تعليم أمر الدفع. أي غموض = تجميد فوري،"
        " وكل طلب يُلمس مرة واحدة فقط."
    )

    await safe_edit(cb.message, txt, b.as_markup())


@dp.callback_query(F.data == "sham_wd_toggle")
async def sham_wd_toggle(cb: types.CallbackQuery, state: FSMContext):
    """تفعيل/إيقاف — للأدمن الرئيسي فقط (موافقة مزدوجة: أدمن + PIN)."""
    if cb.from_user.id != ADMIN_USER_ID:
        await cb.answer(
            "التفعيل/الإيقاف للأدمن الرئيسي فقط (موافقة مزدوجة).",
            show_alert=True,
        )
        return

    await cb.answer()
    on = await feat_on("sham_auto_wd")

    if on:
        await set_setting("feat_sham_auto_wd", "0")
        await audit(cb.from_user.id, "sham_auto_wd", "", "disabled")
        await cb.answer("⏹ أُوقف السحب الآلي.", show_alert=True)
        await sham_wd_screen(cb, state)
        return

    if not await _sham_load():
        await cb.answer("اربط حساب شام كاش أولاً.", show_alert=True)
        return

    if not await get_setting("shamwd_pin_sha"):
        await cb.answer(
            "عيّن PIN التفعيل أولاً (زر 🔑).", show_alert=True,
        )
        return

    if await get_float_setting("shamwd_min", 1.0) <= 0:
        await cb.answer(
            "اضبط أدنى سحب أولاً (قيمة أكبر من صفر).", show_alert=True,
        )
        return

    await state.set_state(ShamWdFSM.pin_chk)
    await cb.message.answer(
        "🔐 أرسل <b>PIN التفعيل</b> لتشغيل السحب الآلي:\n"
        "للإلغاء أرسل /cancel",
        reply_markup=back_kb("sham_wd_screen"),
    )


@dp.message(ShamWdFSM.pin_chk)
async def sham_wd_pin_chk(message: types.Message, state: FSMContext):
    if message.from_user.id != ADMIN_USER_ID:
        await state.clear()
        return

    pin = (message.text or "").strip()
    stored = await get_setting("shamwd_pin_sha") or ""
    await state.clear()

    if not pin or _sha256_hex(pin) != stored:
        await message.answer("❌ PIN خاطئ — لم يُفعَّل شيء.")
        return

    await set_setting("feat_sham_auto_wd", "1")
    await set_setting("shamwd_freeze_note", "")
    await set_setting("shamwd_last_cap_note", "")
    await audit(message.from_user.id, "sham_auto_wd", "", "enabled")
    await message.answer(
        "🟢 <b>فُعّل السحب الآلي.</b>\n"
        "كل تنفيذ يتطلب مرجع شام مُتحققاً — وأي نتيجة غير مؤكدة"
        " تُجمّد الميزة فوراً حتى مراجعتك.",
    )


@dp.callback_query(F.data == "sham_wd_pin")
async def sham_wd_pin_start(cb: types.CallbackQuery, state: FSMContext):
    if cb.from_user.id != ADMIN_USER_ID:
        await cb.answer("للأدمن الرئيسي فقط.", show_alert=True)
        return

    await cb.answer()
    await state.set_state(ShamWdFSM.pin_set)
    await cb.message.answer(
        "🔑 أرسل <b>PIN جديداً</b> (4-8 أرقام):\n"
        "يُخزَّن بصيغة hash ولا يُعرض مجدداً — يُطلب عند كل تفعيل.\n"
        "للإلغاء أرسل /cancel",
        reply_markup=back_kb("sham_wd_screen"),
    )


@dp.message(ShamWdFSM.pin_set)
async def sham_wd_pin_save(message: types.Message, state: FSMContext):
    if message.from_user.id != ADMIN_USER_ID:
        await state.clear()
        return

    pin = (message.text or "").strip()

    if not (pin.isdigit() and 4 <= len(pin) <= 8):
        await message.answer("❌ أرسل 4-8 أرقام فقط.")
        return

    await state.clear()
    await set_setting("shamwd_pin_sha", _sha256_hex(pin))
    await audit(message.from_user.id, "sham_auto_wd", "", "pin_set")
    await message.answer("✅ حُفظ PIN. لا تشاركه مع أحد.")


@dp.callback_query(F.data.startswith("shamwd_set_"))
async def shamwd_set_start(cb: types.CallbackQuery, state: FSMContext):
    if not await is_admin_or_supervisor(cb.from_user.id, "finance"):
        await cb.answer("⚠️ للأدمن فقط!", show_alert=True)
        return

    await cb.answer()
    field = cb.data.rsplit("_", 1)[-1]  # min / max / cap / ucap
    await state.update_data(shamwd_field=field)
    await state.set_state(ShamWdFSM.value)

    labels = {
        "min": "أدنى سحب",
        "max": "أقصى سحب (0 = بلا حد)",
        "cap": "سقف المنظومة اليومي (0 = بلا سقف)",
        "ucap": "سقف المستخدم اليومي (0 = بلا سقف)",
    }
    await cb.message.answer(
        f"⚙️ أرسل قيمة <b>{labels.get(field, field)}</b> (رقم):\n"
        "للإلغاء أرسل /cancel",
        reply_markup=back_kb("sham_wd_screen"),
    )


@dp.message(ShamWdFSM.value)
async def shamwd_set_save(message: types.Message, state: FSMContext):
    if not await is_admin_or_supervisor(message.from_user.id, "finance"):
        await state.clear()
        return

    raw = (message.text or "").strip().replace(",", ".")

    try:
        val = float(raw)
        assert val >= 0
    except Exception:
        await message.answer("❌ أرسل رقماً صحيحاً (≥ 0).")
        return

    data = await state.get_data()
    field = data.get("shamwd_field") or "min"
    await state.clear()
    await set_setting(f"shamwd_{field}", str(val))
    await audit(message.from_user.id, "shamwd_limit", field, str(val))
    await message.answer(f"✅ حُفظت القيمة: {val:,.2f}")


# ─── [WGT 5.18.1] شاشة حارس المحفظة (مقارنة الرصيد مع البوت) ───

_WGT_PULSE_LABELS = {
    1: "1 فحص/يوم (المسح اليومي فقط)",
    2: "2 فحص/يوم",
    3: "3 فحوص/يوم",
    4: "4 فحوص/يوم",
    5: "5 فحوص/يوم",
    6: "6 فحوص/يوم (الأقصى)",
}


@dp.callback_query(F.data == "wgt_screen")
async def wgt_screen(cb: types.CallbackQuery, state: FSMContext):
    """شاشة حارس المحفظة: الحالة + نبضات اليوم + آخر قراءة."""
    if not await is_admin_or_supervisor(cb.from_user.id, "finance"):
        await cb.answer("⚠️ للأدمن فقط!", show_alert=True)
        return

    await cb.answer()
    await state.clear()

    on = await wgt_on()
    quota = max(1, min(6, int(float(
        await get_setting("wgt_day_quota") or 1,
    ) or 1)))
    raw_used = await get_setting("wgt_day_used") or ""
    today = f"{datetime.now(timezone.utc):%Y-%m-%d}"
    used = 0

    if ":" in raw_used and raw_used.split(":", 1)[0] == today:
        used = int(raw_used.split(":", 1)[1] or 0)

    stamp = await get_setting("shamwd_last_balance") or ""
    last_line = "— لا قراءة بعد (أول فحص ناجح يبني المرجع)"

    if "|" in stamp:
        try:
            bal_raw, ts = stamp.split("|", 1)
            expected = await _wgt_expected_balance()
            exp_line = (
                f"{float(expected):,.2f}"
                if expected is not None else "— بعد أول اعتماد آلي"
            )
            last_line = (
                f"آخر قراءة: <b>{float(bal_raw):,.2f}</b> "
                f"({esc(ts[:16])})\n"
                f"المتوقع حالياً: <b>{exp_line}</b>"
            )
        except Exception:
            pass

    linked = bool(await _sham_load())

    b = InlineKeyboardBuilder()
    b.button(
        text=("⏹ إيقاف الحارس" if on else "▶️ تشغيل الحارس"),
        callback_data="wgt_toggle",
    )
    b.button(
        text=f"⚡ نبضات اليوم: "
             f"{_WGT_PULSE_LABELS[quota]}",
        callback_data="wgt_pulses",
    )
    b.button(text="🔄 تحديث", callback_data="wgt_screen")
    b.button(text="🔙 رجوع", callback_data="admin_manage_sham")
    b.adjust(1)

    txt = (
        "🛡 <b>مقارنة رصيد المحفظة مع البوت — حارس المحفظة</b>\n\n"
        f"الحالة: {'🟢 يعمل' if on else '🔴 متوقف'}\n"
        f"🔗 الجلسة: {'✅ مرتبطة' if linked else '❌ غير مرتبطة'}\n"
        f"⚡ استهلاك اليوم: <b>{used}</b> من <b>{quota}</b>\n\n"
        f"{last_line}\n\n"
        "🧭 متى يفحص؟ ضمن نبضات موجودة أصلاً: نافذة أول طلب شحن بعد "
        "التفعيل + المسح اليومي — <b>بلا أي نبضة جديدة</b>.\n"
        "🔔 ينبّهك فوراً عند: عدم تطابق الرصيد المتوقع، أو موت الجلسة."
    )

    await safe_edit(cb.message, txt, b.as_markup())


@dp.callback_query(F.data == "wgt_toggle")
async def wgt_toggle(cb: types.CallbackQuery, state: FSMContext):
    """تشغيل/إيقاف حارس المحفظة."""
    if not await is_admin_or_supervisor(cb.from_user.id, "finance"):
        await cb.answer("⚠️ للأدمن فقط!", show_alert=True)
        return

    await cb.answer()
    on = await wgt_on()
    await set_setting("feat_sham_wallet_guard", "0" if on else "1")
    await audit(
        cb.from_user.id, "sham_wallet_guard", "",
        "disabled" if on else "enabled",
    )

    if not on and not await _sham_load():
        await cb.answer(
            "🟢 فُعّل الحارس — يبدأ الفحص الفعلي بعد ربط جلسة شام كاش.",
            show_alert=True,
        )
    else:
        await cb.answer(
            "⏹ أُوقف الحارس." if on else "🟢 فُعّل الحارس.",
            show_alert=True,
        )

    await wgt_screen(cb, state)


@dp.callback_query(F.data == "wgt_pulses")
async def wgt_pulses(cb: types.CallbackQuery, state: FSMContext):
    """تدوير عدد فحوص الحارس اليومية: 1 → 6 → 1."""
    if not await is_admin_or_supervisor(cb.from_user.id, "finance"):
        await cb.answer("⚠️ للأدمن فقط!", show_alert=True)
        return

    await cb.answer()
    quota = max(1, min(6, int(float(
        await get_setting("wgt_day_quota") or 1,
    ) or 1)))
    quota = 1 if quota >= 6 else quota + 1
    await set_setting("wgt_day_quota", str(quota))
    await audit(cb.from_user.id, "wgt_pulses", "", str(quota))
    await wgt_screen(cb, state)



@dp.callback_query(F.data == "phide_on")
async def phide_on_cb(cb: types.CallbackQuery, state: FSMContext):
    """[PHIDE 5.18.2] إخفاء لوحة الوكيل: إخفاء الزر + قفل الوصول."""
    if cb.from_user.id != ADMIN_USER_ID:
        await cb.answer("للأدمن الرئيسي فقط.", show_alert=True)
        return

    await cb.answer()
    await set_setting("feat_panel_hidden", "1")
    await audit(cb.from_user.id, "panel_hidden", "", "hidden")
    await cb.message.edit_text(
        "🙈 <b>أُخفيت لوحة الوكيل.</b>\n\n"
        "• الزر اختفى من القائمة الرئيسية\n"
        "• أي محاولة فتح تُرفض\n"
        "• إعادة التشغيل غير مطلوبة\n\n"
        "لإعادتها: الإعدادات ← 🎰 إظهار لوحة الوكيل",
        reply_markup=InlineKeyboardBuilder().button(
            text="🎰 إظهار لوحة الوكيل",
            callback_data="phide_off",
        ).button(
            text="🔙 رجوع للإعدادات",
            callback_data="admin_tools_menu",
        ).adjust(1).as_markup(),
    )


@dp.callback_query(F.data == "phide_off")
async def phide_off_cb(cb: types.CallbackQuery, state: FSMContext):
    """[PHIDE 5.18.2] إظهار لوحة الوكيل: عودة كاملة للعمل الطبيعي."""
    if cb.from_user.id != ADMIN_USER_ID:
        await cb.answer("للأدمن الرئيسي فقط.", show_alert=True)
        return

    await cb.answer()
    await set_setting("feat_panel_hidden", "0")
    await audit(cb.from_user.id, "panel_hidden", "", "shown")
    await cb.message.edit_text(
        "🎰 <b>عادت لوحة الوكيل للعمل بشكل طبيعي.</b>\n\n"
        "• الزر ظهر في القائمة الرئيسية\n"
        "• كل الشاشات والعمليات متاحة فوراً\n"
        "• إعادة التشغيل غير مطلوبة",
        reply_markup=InlineKeyboardBuilder().button(
            text="🙈 إخفاء لوحة الوكيل",
            callback_data="phide_on",
        ).button(
            text="🎰 فتح لوحة الوكيل الآن",
            callback_data="panel_home",
        ).button(
            text="🔙 رجوع للإعدادات",
            callback_data="admin_tools_menu",
        ).adjust(1).as_markup(),
    )


@dp.callback_query(F.data == "sham_balances")
async def sham_balances(cb: types.CallbackQuery, state: FSMContext):
    if not await is_admin_or_supervisor(cb.from_user.id):
        await cb.answer("غير مصرّح.", show_alert=True)
        return

    await cb.answer("⏳ جارٍ الجلب…")
    sess = await _sham_load()

    if not sess:
        await cb.answer("لا توجد جلسة — اربط الحساب أولاً.", show_alert=True)
        return

    try:
        bal = await sham.balances(sess)
        txt = sham.format_balances(bal)
    except sham.ShamError as exc:
        txt = f"❌ {esc(str(exc))}\n\nإن كانت الجلسة منتهية أعد الربط."

    kb = InlineKeyboardBuilder()
    kb.button(text="🔄 تحديث", callback_data="sham_balances")
    kb.button(text="🔙 رجوع", callback_data="sham_home")
    kb.adjust(2)

    try:
        await cb.message.edit_text(txt, reply_markup=kb.as_markup())
    except Exception:
        await cb.message.answer(txt, reply_markup=kb.as_markup())


@dp.callback_query(F.data == "sham_diag")
async def sham_diag_cb(cb: types.CallbackQuery, state: FSMContext):
    """[AUTO-FIX 5.18.18] فحص تشخيصي حي لربط شام كاش.

    يجيب عن أسئلة فشل الشحن/السحب الآلي فوراً:
    1) هل الجلسة حية أصلاً؟ (profile)
    2) هل الأرصدة تُقرأ؟
    3) كيف يبدو السجل فعلياً؟ (عينة خام بالحقول الحقيقية —
       strTranId/tranKind/...) لتقارنها بما يدخله المستخدمون.

    ملاحظة: العينة الخام تظهر بنية ردود الخادم كما هي — وهي المفتاح
    لتصحيح صيغة التحويل الصادر عند أول فشل سحب آلي.
    """
    if not await is_admin_or_supervisor(cb.from_user.id):
        await cb.answer("غير مصرّح.", show_alert=True)
        return

    await cb.answer("🧪 جارٍ الفحص…")

    if not _sham_feature_ok():
        await cb.message.answer("❌ وحدة sham_link غير متوفرة.")
        return

    sess = await _sham_load()

    if not sess:
        await cb.message.answer(
            "🧪 <b>تشخيص شام كاش</b>\n\n"
            "❌ لا توجد جلسة محفوظة — الحساب غير مرتبط.\n"
            "هذا سبب توقف الشحن/السحب الآلي إن كانا مفعّلين.\n"
            "اربطه من «🔗 ربط حساب الآن» ثم أعد الفحص.",
        )
        return

    lines = ["🧪 <b>تشخيص شام كاش</b>\n"]
    alive = False

    # 1) صلاحية الجلسة
    try:
        prof = await sham.profile(sess)
        alive = True
        name = ""

        if isinstance(prof, dict):
            name = str(prof.get("fullName") or prof.get("name")
                       or prof.get("accountNumber") or "")

        lines.append(
            "1️⃣ الجلسة: ✅ حية"
            + (f" — <code>{esc(name[:60])}</code>" if name else ""),
        )
    except sham.ShamError as exc:
        lines.append(f"1️⃣ الجلسة: ❌ <code>{esc(str(exc))}</code>")
        lines.append("→ الجلسة منتهية على الأرجح: 🔁 إعادة ربط ثم أعد الفحص.")

    # 2) الأرصدة
    if alive:
        try:
            bal = await sham.balances(sess)
            lines.append("\n2️⃣ الأرصدة: ✅")
            lines.append(sham.format_balances(bal))
        except sham.ShamError as exc:
            lines.append(f"\n2️⃣ الأرصدة: ❌ <code>{esc(str(exc))}</code>")

        # 3) عينة خام من السجل — البنية الفعلية للحقول
        try:
            data = await sham.history(sess, 1)
            rows = []

            if isinstance(data, list):
                rows = [r for r in data if isinstance(r, dict)]
            elif isinstance(data, dict):
                for k in ("items", "logs", "records", "data",
                          "transactions"):
                    v = data.get(k)

                    if isinstance(v, list):
                        rows = [r for r in v if isinstance(r, dict)]
                        break

            lines.append(f"\n3️⃣ السجل (صفحة 1): {len(rows)} حركة")

            for i, tx in enumerate(rows[:3], 1):
                raw = json.dumps(tx, ensure_ascii=False, default=str)
                lines.append(
                    f"\n📄 حركة {i} (خام):"
                    f"\n<code>{esc(raw[:550])}</code>",
                )

            inc = [t for t in rows if str(t.get("tranKind") or "") == "1"]
            outg = [t for t in rows if str(t.get("tranKind") or "") == "2"]

            lines.append(
                f"\n📊 صفحة السجل: {len(rows)} حركة"
                f" | وارد {len(inc)} | صادر {len(outg)}",
            )

            if inc:
                keys = ", ".join(list(inc[0].keys())[:14])
                lines.append(
                    "🔍 حقول أول عملية واردة:"
                    f"\n<code>{esc(keys)}</code>",
                )
                lines.append(
                    "🔢 رقمها (strTranId): <code>"
                    + esc(str(inc[0].get("strTranId") or "غير موجود!"))
                    + "</code> — هذا ما يجب أن يرسله المستخدم"
                    " كرقم العملية.",
                )
            elif rows:
                lines.append(
                    "ℹ️ لا توجد عمليات واردة بهذه الصفحة — إن كان لديك"
                    " تحويل جديد فجرّب لاحقاً أو أرسل واحداً الآن ثم"
                    " أعد الفحص.",
                )
            else:
                lines.append(
                    "⚠️ السجل عاد فارغاً — إن كان يجب أن يحوي حركات"
                    " فالبنية تغيرت (راسل الأدمن التقني بالرد الخام).",
                )
        except sham.ShamError as exc:
            lines.append(
                f"\n3️⃣ السجل: ❌ <code>{esc(str(exc))}</code>",
            )

    lines.append(
        "\n💡 إن كان الشحن الآلي لا يعمل: قارن رقم العملية أعلاه مع"
        " ما يدخله المستخدم، وتأكد أن المبلغ المطابق وصل لحساب البوت.",
    )

    txt = "\n".join(lines)

    if len(txt) > 3900:
        txt = txt[:3900] + "\n…"

    kb = InlineKeyboardBuilder()
    kb.button(text="🔄 إعادة الفحص", callback_data="sham_diag")
    kb.button(text="🔙 رجوع", callback_data="sham_home")
    kb.adjust(2)

    try:
        await cb.message.answer(txt, reply_markup=kb.as_markup())
    except Exception:
        await cb.message.answer("🧪 الفحص اكتمل — لكن تعذر عرض التفاصيل.")


@dp.callback_query(F.data == "sham_unlink")
async def sham_unlink(cb: types.CallbackQuery, state: FSMContext):
    if not await is_admin_or_supervisor(cb.from_user.id):
        await cb.answer("غير مصرّح.", show_alert=True)
        return

    await cb.answer()
    kb = InlineKeyboardBuilder()
    kb.button(text="🗑 نعم، ألغِ الربط", callback_data="sham_unlink_go")
    kb.button(text="❌ تراجع", callback_data="sham_home")
    kb.adjust(2)
    await safe_edit(cb.message,
                    "⚠️ إلغاء الربط سيحذف الجلسة من البوت.\n"
                    "(يمكنك أيضاً إنهاء الجلسة من التطبيق)\n\nمتابعة؟",
                    kb.as_markup())


@dp.callback_query(F.data == "sham_unlink_go")
async def sham_unlink_go(cb: types.CallbackQuery, state: FSMContext):
    if not await is_admin_or_supervisor(cb.from_user.id):
        await cb.answer("غير مصرّح.", show_alert=True)
        return

    await cb.answer()
    sess = await _sham_load()

    if sess:
        try:
            await sham.logout(sess)
        except Exception:
            pass

    await _sham_clear()
    old = _SHAM_TASKS.pop(cb.from_user.id, None)

    if old and not old.done():
        old.cancel()

    await audit(cb.from_user.id, "sham_unlink")

    await safe_edit(cb.message, "✅ تم إلغاء الربط.",
                    InlineKeyboardBuilder().button(
                        text="🔙 رجوع", callback_data="sham_home",
                    ).adjust(1).as_markup())


# ============================================================
# START + COMMANDS
# [FIX 1] الأوامر مسجّلة قبل أي معالج FSM
# ============================================================

@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):

    await state.clear()

    # [NEW 29] التقاط رابط الإحالة /start ref_<id>
    ref_id = None
    if message.text:
        parts = message.text.split()
        if len(parts) > 1 and parts[1].startswith("ref_"):
            try:
                ref_id = int(parts[1][4:])
            except ValueError:
                ref_id = None

    was_new = await get_user(message.from_user.id) is None
    await ensure_user(message)

    if was_new and ref_id and ref_id != message.from_user.id:
        ref_user = await get_user(ref_id)

        if ref_user and not ref_user["is_banned"]:
            db = await get_db()
            try:
                cur = await db.execute(
                    "UPDATE users SET referrer_id = ?"
                    " WHERE telegram_id = ? AND referrer_id IS NULL",
                    (ref_id, message.from_user.id),
                )
                registered = cur.rowcount == 1
                await db.commit()
            finally:
                await db.close()

            if registered:
                bonus = await get_float_setting("referral_bonus", 0.0)
                bonus_line = ""
                if bonus > 0:
                    new_bal = round2(
                        float(ref_user["balance"] or 0) + bonus
                    )
                    await update_user(ref_id, balance=new_bal)
                    await add_transaction(
                        ref_user["id"], "referral", bonus,
                        f"from={message.from_user.id}",
                    )
                    bonus_line = f"💰 المكافأة: {money(bonus)}"

                try:
                    await bot.send_message(
                        ref_id,
                        "🤝 <b>صديق جديد انضم عبر رابطك!</b>\n"
                        f"👤 {esc(message.from_user.full_name or '')}\n"
                        f"{bonus_line}",
                    )
                except Exception:
                    pass

    if not await user_allowed(message.from_user.id, message):
        return

    # [R6-PLUS9 V8] ترحيب بصورة (مرفوعة من اللوحة) إن توفّرت
    photo_id = ""
    if await feat_on("welcome_photo"):
        photo_id = (await get_setting("welcome_photo_file_id") or "").strip()

    if photo_id:
        try:
            text, kb = await main_menu_content(message.from_user.id)
            await message.answer_photo(
                photo_id, caption=text, reply_markup=kb,
            )
        except Exception:
            await send_55bets_main(
                message, message.from_user.id, edit=False,
            )
    else:
        await send_55bets_main(
            message, message.from_user.id, edit=False,
        )  # [R6]

    # [R6-PLUS9 V4] الجولة التعريفية لأول استخدام
    if was_new and await feat_on("onboarding"):
        tour_key = f"tour_done_{message.from_user.id}"

        if not (await get_setting(tour_key) or "").strip():
            await send_tour_slide(message, 1)


TOUR_SLIDES = {  # [R6-PLUS9 V4]
    1: {
        "ar": "🛒 <b>كيف أشحن رصيدي؟</b>\n\n"
              "1️⃣ اضغط «شحن رصيد» من القائمة\n"
              "2️⃣ اختر شام كاش أو سيرياتيل كاش\n"
              "3️⃣ حوّل المبلغ وأرسل رقم العملية\n\n"
              "✅ يراجع الفريق طلبك ويُضاف رصيدك فوراً.",
        "en": "🛒 <b>How to deposit?</b>\n\n"
              "1️⃣ Tap “Deposit” from the menu\n"
              "2️⃣ Pick Sham Cash or Syriatel Cash\n"
              "3️⃣ Send the amount, then the transaction ID\n\n"
              "✅ Our team approves it and your balance is added.",
    },
    2: {
        "ar": "🏦 <b>كيف أسحب أرباحي؟</b>\n\n"
              "1️⃣ اضغط «سحب رصيد» واختر الطريقة\n"
              "2️⃣ أرسل رقم حسابك ثم المبلغ\n"
              "3️⃣ أكّد الطلب وشاهد حاله من «سجل العمليات»\n\n"
              "⚡ السحب خلال ساعات الدعم.",
        "en": "🏦 <b>How to withdraw?</b>\n\n"
              "1️⃣ Tap “Withdraw” and pick a method\n"
              "2️⃣ Send your account number, then the amount\n"
              "3️⃣ Confirm and track it in “History”\n\n"
              "⚡ Processed within support hours.",
    },
    3: {
        "ar": "🤝 <b>نصائح سريعة</b>\n\n"
              "• اقرأ <b>الشروط</b> قبل اللعب\n"
              "• استخدم <b>حاسبة الشحن</b> لتقدير النقاط\n"
              "• شارك <b>رابط الإحالة</b> واربح من أصدقائك\n"
              "• أي مشكلة؟ الدعم بزر واحد\n\n"
              "🎉 جاهز — بالتوفيق!",
        "en": "🤝 <b>Quick tips</b>\n\n"
              "• Read the <b>Terms</b> before playing\n"
              "• Use the <b>calculator</b> to estimate points\n"
              "• Share your <b>referral link</b> to earn\n"
              "• Any issue? Support is one tap away\n\n"
              "🎉 You are ready — good luck!",
    },
}


async def send_tour_slide(message, n: int):
    """[R6-PLUS9 V4] إرسال شريحة الجولة بأزرار التنقل."""
    lang = await user_lang(message.from_user.id)

    b = InlineKeyboardBuilder()
    b.button(
        text=tr(lang, "tour_next"),
        callback_data=f"tour:{n + 1}",
    )
    b.button(text=tr(lang, "tour_skip"), callback_data="tour:done")
    b.adjust(2)

    slide = TOUR_SLIDES[n].get(lang) or TOUR_SLIDES[n]["ar"]

    await message.answer(
        tr(lang, "tour_title").format(n=n) + "\n\n" + slide,
        reply_markup=b.as_markup(),
    )


@dp.callback_query(F.data.startswith("tour:"))
async def tour_nav(cb: types.CallbackQuery, state: FSMContext):
    """[R6-PLUS9 V4] تنقل الجولة وإنهاؤها."""

    if not await user_allowed(cb.from_user.id):
        await cb.answer("غير مسموح.", show_alert=True)
        return

    await cb.answer()
    action = cb.data.split(":", 1)[1]

    if action == "done" or action == "4":
        await set_setting(f"tour_done_{cb.from_user.id}", now_iso())

        if action == "done":
            await send_55bets_main(cb.message, cb.from_user.id, edit=True)
        else:
            await send_tour_slide_msg(cb, 3)
        return

    await send_tour_slide_msg(cb, int(action))


async def send_tour_slide_msg(cb, n: int):
    """[V4] تحديث شريحة الجولة داخل نفس الرسالة."""
    lang = await user_lang(cb.from_user.id)

    b = InlineKeyboardBuilder()

    if n < 3:
        b.button(
            text=tr(lang, "tour_next"),
            callback_data=f"tour:{n + 1}",
        )
    else:
        b.button(
            text=tr(lang, "tour_start"),
            callback_data="tour:done",
        )

    b.button(text=tr(lang, "tour_skip"), callback_data="tour:done")
    b.adjust(2)

    await safe_edit(
        cb.message,
        tr(lang, "tour_title").format(n=n)
        + "\n\n" + TOUR_SLIDES[n][lang],
        b.as_markup(),
    )


@dp.callback_query(F.data == "flow_cancel")
async def flow_cancel(cb: types.CallbackQuery, state: FSMContext):
    """[R6-PLUS9 V7] زر إلغاء صريح في شاشات الإدخال."""

    if not await user_allowed(cb.from_user.id):
        await cb.answer("غير مسموح.", show_alert=True)
        return

    await cb.answer("أُلغيت الجلسة ✅")
    await state.clear()
    await send_55bets_main(cb.message, cb.from_user.id, edit=True)


@dp.callback_query(F.data == "toggle_lang")
async def toggle_lang(cb: types.CallbackQuery, state: FSMContext):
    """[NEW 33] تبديل لغة المستخدم."""

    await state.clear()

    if not await user_allowed(cb.from_user.id):
        await cb.answer("غير مسموح.", show_alert=True)
        return

    current = await user_lang(cb.from_user.id)
    new_lang = "en" if current == "ar" else "ar"  # [R6-PLUS4] لغتان

    await create_user(
        cb.from_user.id,
        cb.from_user.username or "",
        cb.from_user.full_name or "",
    )

    db = await get_db()
    try:
        await db.execute(
            "UPDATE users SET lang = ? WHERE telegram_id = ?",
            (new_lang, cb.from_user.id),
        )
        await db.commit()
    finally:
        await db.close()

    await cb.answer(tr(new_lang, "lang_saved"))
    await send_55bets_main(cb.message, cb.from_user.id, edit=True)  # [R6]


@dp.message(Command("my_info"))
async def my_info_cmd(message: types.Message, state: FSMContext):
    """[R6-CH] /my_info — يفتح صفحة معلومات ملفي مباشرة.
    مسجّل مبكراً حتى لا تلتقطه معالجات حالات الإدخال المعلقة."""

    await state.clear()

    if not await user_allowed(message.from_user.id, message):
        return

    await _render_my_info(message, message.from_user.id, edit=False)


@dp.message(Command("admin"))
async def admin_command(message: types.Message, state: FSMContext):

    if not await is_admin_or_supervisor(message.from_user.id):
        await message.answer("❌ ليس لديك صلاحية للوصول إلى لوحة الإدارة.")
        return

    await state.clear()

    await message.answer(
        "👑 <b>لوحة تحكم الأدمن:</b>",
        reply_markup=get_admin_home_kb(),
    )


_START_TS = datetime.now(timezone.utc)  # [R6-NEW] لقياس مدة التشغيل


async def profit_summary(days: int) -> dict:
    """[R6-PLUS3] لوحة الأرباح الصافية لآخر N يوم:
    عمولات الشحن + رسوم السحب − مكافآت الإيداع − قيمة النقاط."""
    since = (
        datetime.now(timezone.utc) - timedelta(days=days)
    ).isoformat(timespec="seconds")

    db = await get_db()

    try:
        cur = await db.execute(
            "SELECT type, note, amount FROM transactions"
            " WHERE (type = 'deposit' OR type = 'withdraw'"
            " OR type = 'points_redeem') AND created_at >= ?",
            (since,),
        )
        rows = await cur.fetchall()
    finally:
        await db.close()

    dep_comm = 0.0
    dep_bonus = 0.0
    wd_fee = 0.0
    points_cost = 0.0

    def _note_val(note: str, key: str) -> float:
        for part in (note or "").split(";"):
            if part.startswith(key + "="):
                try:
                    return float(part[len(key) + 1:])
                except ValueError:
                    return 0.0
        return 0.0

    for r in rows:
        note = r["note"] or ""

        if r["type"] == "deposit":
            dep_comm += _note_val(note, "commission")
            dep_bonus += _note_val(note, "bonus")
            dep_bonus += _note_val(note, "promo")
        elif r["type"] == "withdraw":
            wd_fee += _note_val(note, "fee")
        elif r["type"] == "points_redeem":
            points_cost += float(r["amount"] or 0)

    net = round2(dep_comm + wd_fee - dep_bonus - points_cost)

    return {
        "dep_comm": round2(dep_comm),
        "dep_bonus": round2(dep_bonus),
        "wd_fee": round2(wd_fee),
        "points_cost": round2(points_cost),
        "net": net,
    }


def _profit_note_val(note: str, key: str) -> float:
    """[R6-PLUS9 V12] قراءة قيمة مفتاح من ملاحظة العملية."""
    for part in (note or "").split(";"):
        if part.startswith(key + "="):
            try:
                return float(part[len(key) + 1:])
            except ValueError:
                return 0.0

    return 0.0


async def profit_series(days: int = 30) -> dict:
    """[R6-PLUS9 V12] صافي الربح لكل يوم (آخر N يوم) للرسم البياني."""
    since = (
        datetime.now(timezone.utc) - timedelta(days=days)
    ).isoformat(timespec="seconds")

    db = await get_db()

    try:
        cur = await db.execute(
            "SELECT substr(created_at, 1, 10) AS day, type, note,"
            " amount FROM transactions"
            " WHERE (type = 'deposit' OR type = 'withdraw'"
            " OR type = 'points_redeem') AND created_at >= ?",
            (since,),
        )
        rows = await cur.fetchall()
    finally:
        await db.close()

    series = {}

    for r in rows:
        day = r["day"]
        note = r["note"] or ""
        net_d = series.get(day, 0.0)

        if r["type"] == "deposit":
            net_d += _profit_note_val(note, "commission")
            net_d += _profit_note_val(note, "bonus")
            net_d += _profit_note_val(note, "promo")
        elif r["type"] == "withdraw":
            net_d += _profit_note_val(note, "fee")
        elif r["type"] == "points_redeem":
            net_d -= float(r["amount"] or 0)

        series[day] = net_d

    return series


async def avg_process_hours(days: int = 7) -> dict:
    """[R6-PLUS3] متوسط زمن اعتماد الشحن/السحب آخر N يوم (ساعات)."""
    since = (
        datetime.now(timezone.utc) - timedelta(days=days)
    ).isoformat(timespec="seconds")

    db = await get_db()

    try:
        cur = await db.execute(
            "SELECT type, created_at, processed_at FROM finance_requests"
            " WHERE status = 'approved' AND processed_at IS NOT NULL"
            " AND created_at >= ?",
            (since,),
        )
        rows = await cur.fetchall()
    finally:
        await db.close()

    sums = {"deposit": [], "withdraw": []}

    for r in rows:
        try:
            dt = (
                datetime.fromisoformat(r["processed_at"])
                - datetime.fromisoformat(r["created_at"])
            ).total_seconds() / 3600.0

            if 0 <= dt < 24 * 30:
                sums.setdefault(r["type"], []).append(dt)
        except (ValueError, TypeError):
            continue

    dep = round(sum(sums.get("deposit", [])) / len(sums["deposit"]), 1) \
        if sums["deposit"] else 0.0
    wd = round(sum(sums.get("withdraw", [])) / len(sums["withdraw"]), 1) \
        if sums["withdraw"] else 0.0

    return {"dep_h": dep, "wd_h": wd, "n": len(rows)}


@dp.message(Command("now"))
async def admin_now_command(message: types.Message, state: FSMContext):
    """[R6-NEW] /now — نبض لحظي للأدمن بلا قوائم."""

    if message.from_user.id != ADMIN_USER_ID:
        return

    await state.clear()

    db = await get_db()

    try:
        cur = await db.execute(
            "SELECT COALESCE(SUM(balance), 0) AS s FROM users"
        )
        total_bal = float((await cur.fetchone())["s"])

        cur = await db.execute(
            "SELECT COUNT(*) AS c FROM finance_requests"
            " WHERE status = 'pending'"
        )
        pending = (await cur.fetchone())["c"]

        today = now_iso()[:10]

        cur = await db.execute(
            "SELECT COUNT(*) AS c, COALESCE(SUM(amount), 0) AS s"
            " FROM transactions WHERE type = 'deposit'"
            " AND created_at LIKE ?",
            (today + "%",),
        )
        dep_row = await cur.fetchone()

        cur = await db.execute(
            "SELECT COUNT(*) AS c, COALESCE(SUM(amount), 0) AS s"
            " FROM transactions WHERE type = 'withdraw'"
            " AND created_at LIKE ?",
            (today + "%",),
        )
        wd_row = await cur.fetchone()

        # [R6-PLUS2] متوسط تقييم السحب الشهري
        cur = await db.execute(
            "SELECT COALESCE(AVG(stars), 0) AS a, COUNT(*) AS c"
            " FROM payout_ratings WHERE created_at LIKE ?",
            (today[:7] + "%",),
        )
        rate_row = await cur.fetchone()
    finally:
        await db.close()

    up = datetime.now(timezone.utc) - _START_TS
    up_min = int(up.total_seconds() // 60)
    up_str = (
        f"{up_min // 60}س {up_min % 60}د" if up_min >= 60
        else f"{up_min}د"
    )

    await message.answer(
        "⚡ <b>نبض البوت الآن</b>\n\n"
        f"💰 إجمالي أرصدة المستخدمين: <b>{money(total_bal)}</b>\n"
        f"🕓 طلبات معلقة: <b>{pending}</b>\n"
        f"📥 شحن اليوم: {money(dep_row['s'])} ({dep_row['c']})\n"
        f"📤 سحب اليوم: {money(wd_row['s'])} ({wd_row['c']})\n"
        + (
            f"⭐ تقييم السحب: {rate_row['a']:.1f}/5"
            f" ({rate_row['c']} تقييم)\n" if rate_row["c"] else ""
        )
        + f"⏱ مدة التشغيل: {up_str}"
    )

    # [R6-PLUS3] KPIs قابلة للتفعيل من مركز الميزات
    extra = ""

    if await feat_on("profit_kpi"):
        p1 = await profit_summary(1)
        p30 = await profit_summary(30)
        extra += (
            "\n\n💰 <b>الأرباح الصافية</b>"
            f" (عمولات + رسوم − مكافآت − نقاط)\n"
            f"• اليوم: <b>{money(p1['net'])}</b>"
            f" (عمولات {money(p1['dep_comm'] + p1['wd_fee'])})\n"
            f"• 30 يوماً: <b>{money(p30['net'])}</b>"
            f" (عمولات {money(p30['dep_comm'] + p30['wd_fee'])})"
        )

    if await feat_on("proc_kpi"):
        k = await avg_process_hours(7)

        if k["n"]:
            extra += (
                "\n\n⚡ <b>متوسط زمن المعالجة</b> (7 أيام)\n"
                f"• شحن: {k['dep_h']} ساعة | سحب: {k['wd_h']} ساعة"
            )

    if extra:
        await message.answer(extra)


@dp.message(Command("ops"))
async def admin_ops_command(message: types.Message, state: FSMContext):
    """[R6-PLUS3] تشخيص شامل للأدمن في رسالة واحدة."""

    if message.from_user.id != ADMIN_USER_ID:
        return

    await state.clear()

    try:
        size_mb = os.path.getsize(DB_PATH) / (1024 * 1024)
    except OSError:
        size_mb = 0.0

    conn = sqlite3.connect(DB_PATH)

    try:
        qrow = conn.execute("PRAGMA quick_check").fetchone()
        quick = (qrow[0] if qrow else "—") or "—"
    finally:
        conn.close()

    db = await get_db()

    try:
        cur = await db.execute(
            "SELECT COUNT(*) AS c FROM finance_requests"
            " WHERE status = 'pending'",
        )
        pending = (await cur.fetchone())["c"]

        cur = await db.execute(
            "SELECT COUNT(*) AS c FROM channel_posts WHERE enabled = 1",
        )
        posts = (await cur.fetchone())["c"]
    finally:
        await db.close()

    feats_on = 0

    for _k in FEATURES:
        if await feat_on(_k):
            feats_on += 1
    last_backup = (await get_setting("last_backup_at") or "—")[:16]

    up = datetime.now(timezone.utc) - _START_TS
    up_min = int(up.total_seconds() // 60)
    up_str = (
        f"{up_min // 60}س {up_min % 60}د" if up_min >= 60
        else f"{up_min}د"
    )

    ok_mark = "✅" if quick.lower() == "ok" else "⚠️"

    last_recon = (await get_setting("last_panel_recon_at") or "")[:16]
    panel_line = await panel_ops_line()

    await message.answer(
        "🧰 <b>تشخيص البوت</b>\n\n"
        f"📦 الإصدار: <code>{BOT_VERSION}</code>\n"
        f"💾 حجم القاعدة: {size_mb:.1f} MB\n"
        f"{ok_mark} سلامة القاعدة: <code>{esc(quick)}</code>\n"
        f"🗄 آخر نسخة احتياطية: {esc(last_backup)} UTC\n"
        f"📨 طلبات معلقة: {pending}\n"
        f"📣 منشورات مجدولة فعالة: {posts}\n"
        f"🎛 ميزات مفعّلة: {feats_on}/{len(FEATURES)}\n"
        f"⏱ مدة التشغيل: {up_str}\n"
        f"{panel_line}"
        + (f"\n🌙 آخر مطابقة: {esc(last_recon)} UTC"
           if last_recon else "")
    )


@dp.message(Command("cancel"))
async def cancel_command(message: types.Message, state: FSMContext):

    current_state = await state.get_state()

    if current_state is None:
        lang = await user_lang(message.from_user.id)
        await message.answer(
            tr(lang, "cancel_none"),
            reply_markup=await menu_with_links(
                lang, message.from_user.id
            ),
        )
        return

    await state.clear()

    lang = await user_lang(message.from_user.id)
    await message.answer(
        tr(lang, "cancel_done"),
        reply_markup=await menu_with_links(lang, message.from_user.id),
    )


# ============================================================
# MAIN MENU
# ============================================================

@dp.callback_query(F.data == "menu_back")
async def menu_back(cb: types.CallbackQuery, state: FSMContext):

    await state.clear()

    if not await user_allowed(cb.from_user.id):
        await cb.answer("البوت متوقف أو الحساب محظور.", show_alert=True)
        return

    await cb.answer()
    await send_55bets_main(cb.message, cb.from_user.id, edit=True)  # [R6]


@dp.callback_query(F.data == "menu_profile")
async def menu_profile(cb: types.CallbackQuery, state: FSMContext):

    await state.clear()  # [FIX 2]

    if not await user_allowed(cb.from_user.id):
        await cb.answer("غير مسموح باستخدام البوت.", show_alert=True)
        return

    user = await get_user(cb.from_user.id)

    if not user:
        await create_user(
            cb.from_user.id,
            cb.from_user.username or "",
            cb.from_user.full_name or "",
        )
        user = await get_user(cb.from_user.id)

    lang = await user_lang(cb.from_user.id)  # [NEW 33]

    # [NEW 29] إحصاء الدعوات ورابط الدعوة
    db = await get_db()
    try:
        cur = await db.execute(
            "SELECT COUNT(*) AS c FROM users WHERE referrer_id = ?",
            (cb.from_user.id,),
        )
        refs_count = (await cur.fetchone())["c"]
    finally:
        await db.close()

    if BOT_USERNAME:
        invite = f"https://t.me/{BOT_USERNAME}?start=ref_{cb.from_user.id}"
    else:
        invite = "—"

    text = (
        f"{tr(lang, 'profile_title')}\n\n"
        f"{tr(lang, 'profile_name')}: {esc(user['full_name'])}\n"
        f"{tr(lang, 'profile_tid')}: <code>{user['telegram_id']}</code>\n"
        f"{tr(lang, 'profile_site')}: "
        f"<code>{esc(user['site_username'] or tr(lang, 'not_linked'))}</code>\n"
        f"{tr(lang, 'profile_balance')}: <b>{money(user['balance'])}</b>\n"
        f"{tr(lang, 'profile_refs')}: {refs_count}\n"
        f"{tr(lang, 'profile_invite')}: {esc(invite)}"
    )

    loyal = await get_loyalty(cb.from_user.id)  # [USR4-1]

    if loyal["line"]:
        text += f"\n\n{loyal['line']}"

    await cb.answer()
    await safe_edit(cb.message, text, profile_kb(lang))


# ============================================================
# MY PASSWORD + MY HISTORY [NEW 20 / NEW 30]
# ============================================================

@dp.callback_query(F.data == "my_password")
async def my_password(cb: types.CallbackQuery, state: FSMContext):
    """[UI-2] كلمة السر مخفية + كشف مؤقت + حذف تلقائي بعد 30 ثانية."""

    await state.clear()

    if not await user_allowed(cb.from_user.id):
        await cb.answer("غير مسموح.", show_alert=True)
        return

    lang = await user_lang(cb.from_user.id)
    user = await get_user(cb.from_user.id)

    if not user or not user.get("site_password"):
        await cb.answer(tr(lang, "no_password"), show_alert=True)
        return

    await cb.answer()

    plain = decrypt_password(user["site_password"])

    try:
        msg = await cb.message.answer(
            tr(lang, "pw_mask", u=esc(user["site_username"] or "")),
            reply_markup=_pw_kb(lang),
        )
    except Exception as exc:
        logger.warning("تعذر إرسال كلمة المرور: %s", exc)
        return

    _pw_remember(msg.message_id, user["site_username"] or "", plain, lang)
    await _pw_autodelete(msg)


TX_ICONS = {
    "deposit": "💰",
    "withdraw": "🏦",
    "gift": "🎁",
    "register": "🆕",
    "referral": "🤝",
    "refund": "↩️",
    "admin_adjust": "🛠",
    "transfer_out": "💸",  # [USR-1]
    "transfer_in": "📥",  # [USR-1]
    "gift_out": "🎟",  # [USR-4]
}


@dp.callback_query(F.data.startswith("my_history:"))
async def my_history(cb: types.CallbackQuery, state: FSMContext):

    await state.clear()

    if not await user_allowed(cb.from_user.id):
        await cb.answer("غير مسموح.", show_alert=True)
        return

    # [USR2-6] الصيغة: my_history:{page}:{filter}
    parts = cb.data.split(":")
    try:
        page = max(0, int(parts[1]))
    except (ValueError, IndexError):
        page = 0

    filt = parts[2] if len(parts) > 2 else "all"  # [USR2-6]
    if filt not in _HIST_FILTERS:
        filt = "all"

    mode = parts[3] if len(parts) > 3 else "full"  # [V14]

    if mode not in ("full", "compact"):
        mode = "full"

    lang = await user_lang(cb.from_user.id)
    user = await get_user(cb.from_user.id)

    if not user:
        await cb.answer()
        await safe_edit(
            cb.message, tr(lang, "history_empty"),
            back_kb("menu_back", lang),
        )
        return

    page_size = 10

    db = await get_db()
    try:
        cur = await db.execute(
            "SELECT type, amount, note, created_at FROM transactions"
            " WHERE user_id = ?" + _hist_filter_sql(filt) + " ORDER BY id"
            " DESC LIMIT ? OFFSET ?",
            (user["id"], page_size + 1, page * page_size),
        )
        rows = await cur.fetchall()
    finally:
        await db.close()

    has_more = len(rows) > page_size
    rows = rows[:page_size]

    await cb.answer()

    if not rows:
        await safe_edit(
            cb.message, tr(lang, "history_empty"),
            back_kb("menu_back", lang),
        )
        return

    # [R6-REV] نمط العرض الأصلي بنسختي العربية والإنكليزية
    TYPE_AR = {
        "deposit": "إيداع", "withdraw": "سحب", "gift": "هدية",
        "register": "تسجيل", "referral": "إحالة", "refund": "استرداد",
        "admin_adjust": "تعديل إداري", "transfer_out": "تحويل صادر",
        "transfer_in": "تحويل وارد", "bonus": "مكافأة",
        "gift_out": "كود هدية",
    }
    TYPE_EN = {
        "deposit": "Deposit", "withdraw": "Withdraw", "gift": "Gift",
        "register": "Register", "referral": "Referral", "refund": "Refund",
        "admin_adjust": "Admin adjust", "transfer_out": "Transfer out",
        "transfer_in": "Transfer in", "bonus": "Bonus",
        "gift_out": "Gift code",
    }
    types_map = TYPE_EN if lang == "en" else TYPE_AR

    lines = [
        f"{r6t(lang, 'hist_title')} "
        + r6t(lang, "hist_page").format(p=page + 1) + "\n"
    ]

    for row in rows:
        disp = float(row["amount"] or 0)
        if row["type"] in ("withdraw", "transfer_out"):  # [USR-1]
            disp = -disp
        amount_str = f"+{money(disp)}" if disp > 0 else money(disp)

        note_raw = row["note"] or ""
        method = "-"
        details = note_raw

        if "method=" in note_raw:
            parts = note_raw.split(";")
            for part in parts:
                if part.startswith("method="):
                    method = part[7:]
            details = ";".join(
                p for p in parts if not p.startswith(("method=", "dest="))
            ) or note_raw

        if mode == "compact":  # [R6-PLUS9 V14]
            dt_short = await fmt_dt(row["created_at"])  # [V6]
            lines.append(
                f"📌 {types_map.get(row['type'], row['type'])}"
                f" — <code>{amount_str}</code>"
                f" <i>({dt_short})</i>"
            )
            continue

        lines.append(
            f"📌 <b>{types_map.get(row['type'], row['type'])}</b>"
            f" ({esc(method)})\n"
            f"{r6t(lang, 'hist_amount')} <code>{amount_str}</code> | "
            f"{r6t(lang, 'hist_details')} "
            f"<code>{esc(details[:40])}</code>\n"
            f"{r6t(lang, 'hist_date')} "
            f"<code>{await fmt_dt(row['created_at'])}</code>\n"  # [V6]
            "------------------------------"
        )

    await safe_edit(
        cb.message,
        "\n".join(lines),
        history_kb(
            page, has_more, lang, filt, mode,  # [V14]
            show_lastreq=await feat_on("last_request"),  # [U35]
        ),
    )


@dp.callback_query(F.data.startswith("hist_toggle:"))
async def hist_toggle(cb: types.CallbackQuery, state: FSMContext):
    """[AUDIT2] تبديل عرض السجل مختصر/مفصل — كان زراً بلا معالج."""

    if not await user_allowed(cb.from_user.id):
        await cb.answer("غير مسموح.", show_alert=True)
        return

    try:
        parts = cb.data.split(":")
        page = max(0, int(parts[1]))
        filt = parts[2]
        new_mode = parts[3]
    except (ValueError, IndexError):
        await cb.answer("طلب غير صالح.", show_alert=True)
        return

    if new_mode not in ("full", "compact"):
        new_mode = "full"

    await cb.answer()
    _with_data(cb, f"my_history:{page}:{filt}:{new_mode}")
    await my_history(cb, state)


@dp.callback_query(F.data == "lastreq")
async def lastreq_view(cb: types.CallbackQuery, state: FSMContext):
    """[R6-PLUS10 U35] حالة آخر طلب بضغطة واحدة."""

    if not await user_allowed(cb.from_user.id):
        await cb.answer("غير مسموح.", show_alert=True)
        return

    if not await feat_on("last_request"):
        await cb.answer()
        return

    await cb.answer()
    lang = await user_lang(cb.from_user.id)

    db = await get_db()

    try:
        cur = await db.execute(
            "SELECT id, type, amount, status, created_at, note"
            " FROM finance_requests WHERE telegram_id = ?"
            " ORDER BY id DESC LIMIT 1",
            (cb.from_user.id,),
        )
        req = await cur.fetchone()
    finally:
        await db.close()

    if not req:
        await safe_edit(
            cb.message,
            r6t(lang, "lastreq_none"),
            back_kb("menu_back", lang),
        )
        return

    st_map = {
        "pending": "req_st_pending", "approved": "req_st_approved",
        "rejected": "req_st_rejected", "expired": "req_st_expired",
    }
    st_txt = r6t(lang, st_map.get(req["status"], "req_st_pending"))
    type_txt = r6t(
        lang, "req_type_dep" if req["type"] == "deposit" else "req_type_wd",
    )

    hold_line = (
        "\n🔒 <i>رصيدك محتجز لحين القرار</i>"
        if req["type"] == "withdraw" and "held=1" in (req["note"] or "")
        else ""
    )

    await safe_edit(
        cb.message,
        r6t(lang, "lastreq_title")
        + f"🆔 #{req['id']}\n"
        f"📄 {type_txt}\n"
        f"💵 <b>{money(float(req['amount']))}</b>\n"
        f"📊 {st_txt}{hold_line}\n"
        f"🕐 <code>{await fmt_dt(req['created_at'])}</code>",
        back_kb("my_history:0", lang),
    )


@dp.callback_query(F.data == "retry_dep")
async def retry_dep(cb: types.CallbackQuery, state: FSMContext):
    """[R6-PLUS10 U38] إعادة فتح شاشة الشحن بعد الرفض بضغطة."""

    if not await user_allowed(cb.from_user.id):
        await cb.answer("غير مسموح.", show_alert=True)
        return

    await cb.answer()
    await state.clear()
    lang = await user_lang(cb.from_user.id)
    await safe_edit(
        cb.message,
        r6t(lang, "recharge_pick"),
        await recharge_kb_for(cb.from_user.id, lang),
    )


@dp.callback_query(F.data == "balalert_set")
async def balalert_set(cb: types.CallbackQuery, state: FSMContext):
    """[R6-PLUS10 U36] ضبط حد تنبيه الرصيد."""

    if not await user_allowed(cb.from_user.id):
        await cb.answer("غير مسموح.", show_alert=True)
        return

    if not await feat_on("bal_alert"):
        await cb.answer()
        return

    await cb.answer()
    await state.clear()
    await state.set_state(UserBalAlertFSM.value)

    lang = await user_lang(cb.from_user.id)
    cur = (await get_setting(f"bal_alert_{cb.from_user.id}") or "").strip()
    cur_txt = money(float(cur)) if cur else "غير مضبوط"

    await cb.message.answer(
        tr(lang, "balalert_prompt").format(cur=cur_txt),
        reply_markup=cancel_kb(lang, "back_to_main"),  # [V7]
    )


@dp.message(UserBalAlertFSM.value)
async def balalert_save(message: types.Message, state: FSMContext):
    """[R6-PLUS10 U36] حفظ/حذف حد التنبيه."""

    if not await user_allowed(message.from_user.id, message):
        return

    lang = await user_lang(message.from_user.id)

    try:  # [R6-PLUS10] الصفر مسموح هنا (إلغاء)
        amount = float((message.text or "").strip().replace(",", "."))
    except ValueError:
        amount = None

    if amount is None or not math.isfinite(amount) or amount < 0:
        await message.answer("❌ أرسل مبلغاً صحيحاً (أو 0 للإلغاء).")
        return

    await state.clear()

    if amount == 0:
        await set_setting(f"bal_alert_{message.from_user.id}", "")
        await message.answer(
            tr(lang, "balalert_cleared"),
            reply_markup=back_kb("back_to_main", lang),
        )
        return

    await set_setting(
        f"bal_alert_{message.from_user.id}", str(amount),
    )
    await message.answer(
        tr(lang, "balalert_saved").format(v=money(amount)),
        reply_markup=back_kb("back_to_main", lang),
    )


@dp.callback_query(F.data == "favamt_set")
async def favamt_set(cb: types.CallbackQuery, state: FSMContext):
    """[R6-PLUS10 U37] ضبط مبلغ الشحن المفضل."""

    if not await user_allowed(cb.from_user.id):
        await cb.answer("غير مسموح.", show_alert=True)
        return

    if not await feat_on("fav_amount"):
        await cb.answer()
        return

    await cb.answer()
    await state.clear()
    await state.set_state(UserFavAmtFSM.amount)

    lang = await user_lang(cb.from_user.id)
    await cb.message.answer(
        tr(lang, "favamt_prompt"),
        reply_markup=cancel_kb(lang, "back_to_recharge"),  # [V7]
    )


@dp.message(UserFavAmtFSM.amount)
async def favamt_save(message: types.Message, state: FSMContext):
    """[R6-PLUS10 U37] حفظ/حذف المبلغ المفضل."""

    if not await user_allowed(message.from_user.id, message):
        return

    lang = await user_lang(message.from_user.id)

    try:  # [R6-PLUS10] الصفر مسموح هنا (حذف)
        amount = float((message.text or "").strip().replace(",", "."))
    except ValueError:
        amount = None

    if amount is None or not math.isfinite(amount) or amount < 0:
        await message.answer("❌ أرسل مبلغاً صحيحاً (أو 0 للحذف).")
        return

    await state.clear()

    if amount == 0:
        await set_setting(f"fav_amount_{message.from_user.id}", "")
        await message.answer(
            tr(lang, "favamt_cleared"),
            reply_markup=back_kb("back_to_recharge", lang),
        )
        return

    # [AUDIT2] لا يُقبل مبلغ خارج حدود الشحن (صار زراً ميتاً وإلا)
    lim = await amount_limits("deposit")

    if not (lim["min"] <= amount <= lim["max"]):
        await message.answer(
            f"❌ المبلغ يجب أن يكون بين {money(lim['min'])}"
            f" و {money(lim['max'])}.\nأعد الإرسال أو أرسل 0 للحذف:",
        )
        await state.set_state(UserFavAmtFSM.amount)
        return

    await set_setting(
        f"fav_amount_{message.from_user.id}", str(amount),
    )
    await message.answer(
        tr(lang, "favamt_saved").format(v=money(amount)),
        reply_markup=back_kb("back_to_recharge", lang),
    )


@dp.callback_query(F.data == "menu_services")
async def menu_services(cb: types.CallbackQuery, state: FSMContext):

    await state.clear()  # [FIX 2]

    if not await user_allowed(cb.from_user.id):
        await cb.answer("غير مسموح باستخدام البوت.", show_alert=True)
        return

    lang = await user_lang(cb.from_user.id)
    await cb.answer()
    await safe_edit(
        cb.message,
        tr(lang, "services_title"),
        services_kb(
            lang,
            show_rates=await feat_on("rates_screen"),  # [AUDIT2]
        ),
    )


@dp.callback_query(F.data == "menu_stats")
async def menu_stats(cb: types.CallbackQuery, state: FSMContext):

    await state.clear()  # [FIX 2]

    if not await user_allowed(cb.from_user.id):
        await cb.answer("غير مسموح باستخدام البوت.", show_alert=True)
        return

    db = await get_db()

    try:
        cur = await db.execute("SELECT COUNT(*) AS count FROM users")
        total_users = (await cur.fetchone())["count"]

        # [FIX 9] إجمالي الأرصدة للإدارة فقط
        staff = await is_admin_or_supervisor(cb.from_user.id)

        if staff:
            cur = await db.execute(
                "SELECT COALESCE(SUM(balance), 0) AS total FROM users"
            )
            total_balance = (await cur.fetchone())["total"]
    finally:
        await db.close()

    if staff:
        text = (
            "📊 <b>الإحصائيات العامة</b>\n\n"
            f"👥 إجمالي المستخدمين: {total_users}\n"
            f"💰 إجمالي الأرصدة: {money(total_balance)}"
        )
    else:
        user = await get_user(cb.from_user.id)
        my_balance = float(user["balance"] or 0) if user else 0
        text = (
            "📊 <b>إحصائياتك</b>\n\n"
            f"👥 إجمالي مستخدمي البوت: {total_users}\n"
            f"💰 رصيدك: {money(my_balance)}"
        )

    kb = back_kb()

    if not staff:  # [USR2-2] زر الإحالات للمستخدم العادي
        skb = InlineKeyboardBuilder.from_markup(back_kb())
        skb.button(text=tr("ar", "ref_btn"), callback_data="my_refs")
        skb.adjust(1)
        kb = skb.as_markup()

    await cb.answer()
    await safe_edit(cb.message, text, kb)


# ============================================================
# INFO MENU [NEW 18]
# ============================================================

@dp.callback_query(F.data == "menu_info")
async def menu_info(cb: types.CallbackQuery, state: FSMContext):

    await state.clear()

    if not await user_allowed(cb.from_user.id):
        await cb.answer("غير مسموح باستخدام البوت.", show_alert=True)
        return

    lang = await user_lang(cb.from_user.id)
    await cb.answer()
    await safe_edit(cb.message, tr(lang, "info_title"), info_menu_kb())


@dp.callback_query(F.data.startswith("info_text:"))
async def info_text(cb: types.CallbackQuery, state: FSMContext):

    await state.clear()

    if not await user_allowed(cb.from_user.id):
        await cb.answer("غير مسموح باستخدام البوت.", show_alert=True)
        return

    key = cb.data.split(":", 1)[1]

    if key not in BOT_TEXTS:
        await cb.answer("خيار غير معروف.", show_alert=True)
        return

    await cb.answer()

    title = BOT_TEXTS[key]
    value = await get_text(key) or ""
    lang = await user_lang(cb.from_user.id)
    kb = back_kb("menu_info", lang)

    try:
        await cb.message.edit_text(
            f"<b>{title}</b>\n\n{value}",
            reply_markup=kb,
        )
        return
    except Exception as exc:
        if "message is not modified" in str(exc).lower():
            return

    try:
        await cb.message.edit_text(
            f"<b>{title}</b>\n\n{esc(value)}",
            reply_markup=kb,
        )
    except Exception as exc:
        logger.warning("تعذر عرض النص: %s", exc)


# ============================================================
# GIFT USER
# ============================================================

@dp.callback_query(F.data == "menu_gift")
async def menu_gift(cb: types.CallbackQuery, state: FSMContext):

    if not await user_allowed(cb.from_user.id):
        await cb.answer("غير مسموح باستخدام البوت.", show_alert=True)
        return

    await cb.answer()
    await state.clear()  # [FIX 2]
    await state.set_state(GiftFSM.code)

    lang = await user_lang(cb.from_user.id)
    gb = InlineKeyboardBuilder()
    gb.button(text=tr(lang, "gift_own_btn"), callback_data="gift_own")  # [USR-4]
    gb.button(text=tr(lang, "back"), callback_data="menu_back")
    gb.adjust(1)
    await cb.message.answer(
        tr(lang, "gift_prompt"),
        reply_markup=gb.as_markup(),
    )


@dp.message(GiftFSM.code)
async def gift_code_submit(message: types.Message, state: FSMContext):

    if not await user_allowed(message.from_user.id, message):
        return

    raw_code = (message.text or "").strip().upper()

    if (
        len(raw_code) != 8
        or not all(
            char in string.ascii_uppercase + string.digits
            for char in raw_code
        )
    ):
        await message.answer(
            "❌ الكود غير صالح.\nيجب أن يكون 8 أحرف أو أرقام.\n\n"
            "للإلغاء أرسل /cancel"
        )
        return

    success, status, amount = await redeem_gift_code(
        message.from_user.id,
        raw_code,
    )

    if not success:
        messages = {
            "invalid": "❌ كود غير صالح.",
            "used": "⚠️ هذا الكود مستخدم مسبقًا.",
            "user_not_found": "❌ المستخدم غير موجود.",
        }
        await message.answer(messages.get(status, "❌ تعذر استخدام الكود."))
        return

    user = await get_user(message.from_user.id)

    await message.answer(
        "🎉 <b>تم استخدام كود الهدية بنجاح!</b>\n\n"
        f"💰 المبلغ المضاف: {money(amount)}\n"
        f"💳 رصيدك الجديد: {money(user['balance'])}",
        reply_markup=await menu_with_links("ar", message.from_user.id),
    )

    await state.clear()


# ============================================================
# CREATE SITE ACCOUNT
# ============================================================

@dp.callback_query(F.data == "svc_create_account")
async def svc_create_account(cb: types.CallbackQuery, state: FSMContext):

    if not await user_allowed(cb.from_user.id):
        await cb.answer("غير مسموح باستخدام البوت.", show_alert=True)
        return

    await cb.answer()
    await state.clear()  # [FIX 2]
    await state.set_state(RegisterFSM.site_username)

    await cb.message.answer(
        tr(await user_lang(cb.from_user.id), "create_prompt")
    )


@dp.message(RegisterFSM.site_username)
async def reg_site_username(message: types.Message, state: FSMContext):

    if not await user_allowed(message.from_user.id, message):
        return

    username = (message.text or "").strip()

    if len(username) < 3 or len(username) > 32:
        await message.answer("❌ اسم المستخدم يجب أن يكون بين 3 و32 حرفًا.")
        return

    if any(char.isspace() for char in username):
        await message.answer("❌ اسم المستخدم لا يجب أن يحتوي على مسافات.")
        return

    existing = await get_user(message.from_user.id)

    if existing and existing["site_username"]:
        await message.answer(
            "⚠️ لديك حساب موقع مرتبط بالفعل.\n"
            f"اسم المستخدم: <code>{esc(existing['site_username'])}</code>\n\n"
            "لاستبداله، استخدم لوحة الإدارة."
        )
        await state.clear()
        return

    # [FIX 5] منع استخدام اسم محجوز من مستخدم آخر
    taken = await get_user_by_site_username(username)
    if taken and taken["telegram_id"] != message.from_user.id:
        await message.answer(
            "❌ اسم المستخدم محجوز مسبقًا من مستخدم آخر.\nاختر اسمًا مختلفًا."
        )
        return

    # [R6-REV] كلمة المرور يختارها المستخدم بدل التوليد العشوائي
    lang = await user_lang(message.from_user.id)
    await state.update_data(reg_username=username)
    await state.set_state(RegisterFSM.site_password)

    await message.answer(
        tr(lang, "create_pw_prompt"),
        reply_markup=back_kb("menu_back", lang),
    )


@dp.message(RegisterFSM.site_password)
async def reg_site_password(message: types.Message, state: FSMContext):
    """[R6-REV] استلام كلمة المرور من المستخدم وإنشاء الحساب بها."""

    if not await user_allowed(message.from_user.id, message):
        return

    lang = await user_lang(message.from_user.id)
    password = (message.text or "").strip()

    if password.startswith("/"):
        await state.clear()
        return

    if len(password) < 6 or any(char.isspace() for char in password):
        await message.answer(tr(lang, "create_pw_invalid"))
        return

    data = await state.get_data()
    username = data.get("reg_username")

    if not username:
        await state.clear()
        await state.set_state(RegisterFSM.site_username)
        await message.answer(tr(lang, "create_prompt"))
        return

    # [R6-PLUS12 auto_create] إنشاء اللاعب فعلياً باللوحة أولاً
    panel_note = ""

    if await feat_on("auto_create") and panel_ready():
        client = ipanel.get_panel()
        _, perr = await panel_call(
            client.register_player, username, password,
        )

        if perr:
            await message.answer(
                "⚠️ تعذر إنشاء الحساب بالموقع حالياً:\n"
                f"{esc(str(perr))}\n\n"
                "حاول لاحقاً أو تواصل مع الإدارة.",
                reply_markup=await menu_with_links(lang, message.from_user.id),
            )
            await state.clear()
            return

        panel_note = "🎰 تم إنشاء حسابك فعلياً بالموقع وجاهز للدخول.\n\n"
        await audit(message.from_user.id, "panel_auto_create",
                    details=f"player={username}")

    try:
        await update_user(
            message.from_user.id,
            site_username=username,
            site_password=encrypt_password(password),  # [NEW 20]
        )
    except sqlite3.IntegrityError:  # [FIX 5]
        await message.answer(tr(lang, "create_taken"))
        await state.clear()
        await state.set_state(RegisterFSM.site_username)
        await message.answer(tr(lang, "create_prompt"))
        return

    user = await get_user(message.from_user.id)

    await add_transaction(
        user["id"], "register", 0, f"site_user={username}",
    )

    await message.answer(
        panel_note
        + tr(lang, "create_done").format(u=esc(username), p=esc(password)),
        reply_markup=await menu_with_links(lang, message.from_user.id),
    )

    await state.clear()


# ============================================================
# DEPOSIT
# ============================================================

@dp.callback_query(F.data == "svc_deposit")
async def svc_deposit(cb: types.CallbackQuery, state: FSMContext):

    if not await user_allowed(cb.from_user.id):
        await cb.answer("غير مسموح باستخدام البوت.", show_alert=True)
        return

    # [ADM-3] إيقاف الإيداعات يدوياً
    if await get_setting("deposits_paused") == "1":
        lang = await user_lang(cb.from_user.id)
        reason = (await get_setting("pause_reason_dep") or "").strip()
        await cb.answer()
        await cb.message.answer(tr(
            lang, "pause_dep",
            reason=esc(reason) if reason else tr(lang, "pause_default"),
        ))
        return

    await cb.answer()
    await state.clear()  # [FIX 2]
    await state.set_state(DepositFSM.amount)

    lang = await user_lang(cb.from_user.id)
    limits = await amount_limits("deposit")  # [NEW 27]

    badge = ""
    bonus_pct = await get_float_setting("bonus_percent", 0.0)  # [USR2-3]

    if bonus_pct > 0:
        badge = tr(lang, "bonus_badge", pct=bonus_pct)

    dkb = InlineKeyboardBuilder.from_markup(quick_deposit_kb())
    dkb.button(  # [USR2-4]
        text=tr(lang, "promo_btn"), callback_data="dpromo",
    )
    dkb.adjust(4, 1)

    await cb.message.answer(
        tr(lang, "deposit_prompt",
           min=money(limits["min"]), max=money(limits["max"])) + badge,
        reply_markup=dkb.as_markup(),
    )


@dp.message(DepositFSM.amount)
async def deposit_amount(message: types.Message, state: FSMContext):

    if not await user_allowed(message.from_user.id, message):
        return

    lang = await user_lang(message.from_user.id)
    amount = parse_amount(message.text)  # [FIX 7]

    if amount is None:
        await message.answer(
            "❌ مبلغ غير صالح.\n"
            f"أرسل مبلغًا أكبر من 0 ولا يتجاوز {MAX_AMOUNT}\n"
            "وبمنزلتين عشريتين كحد أقصى.\n\nللإلغاء أرسل /cancel"
        )
        return

    limits = await amount_limits("deposit")  # [NEW 27]
    if not (limits["min"] <= amount <= limits["max"]):
        await message.answer(
            f"❌ المبلغ يجب أن يكون بين {money(limits['min'])}"
            f" و {money(limits['max'])}.\n\nللإلغاء أرسل /cancel"
        )
        return

    if await has_pending_finance_request(message.from_user.id, "deposit"):
        await message.answer("⚠️ لديك بالفعل طلب شحن معلق قيد المراجعة.")
        return

    # [R6] حفظ المبلغ ثم طلب رقم العملية (نمط الواجهة الأصلية)
    await state.update_data(dep_amount=amount)
    await state.set_state(DepositFSM.txid)

    data = await state.get_data()
    method = data.get("deposit_method") or "شام كاش"

    await message.answer(
        r6t(lang, "dep_txid_ask").format(m=esc(method))
        + await ui_step_bar(lang, 3, 4),  # [V1]
        reply_markup=cancel_kb(lang, "back_to_recharge"),  # [V7]
    )


@dp.callback_query(F.data.startswith("dep_quick:"))
async def dep_quick(cb: types.CallbackQuery, state: FSMContext):
    """[NEW 31 + R6] المبالغ السريعة تمر عبر رقم العملية."""

    if not await user_allowed(cb.from_user.id):
        await cb.answer("غير مسموح.", show_alert=True)
        return

    try:
        amount = float(cb.data.split(":", 1)[1])
    except (ValueError, IndexError):
        await cb.answer("مبلغ غير صالح.", show_alert=True)
        return

    limits = await amount_limits("deposit")

    if not (limits["min"] <= amount <= limits["max"]):
        await cb.answer(
            f"المبلغ مسموح بين {money(limits['min'])}"
            f" و {money(limits['max'])}.",
            show_alert=True,
        )
        return

    if await has_pending_finance_request(cb.from_user.id, "deposit"):
        await cb.answer("لديك طلب شحن معلق بالفعل.", show_alert=True)
        return

    await cb.answer()
    await state.update_data(dep_amount=amount)
    await state.set_state(DepositFSM.txid)

    lang = await user_lang(cb.from_user.id)
    method = (await state.get_data()).get("deposit_method") or "شام كاش"
    await cb.message.answer(
        f"💰 المبلغ: {money(amount)}\n"
        + r6t(lang, "dep_txid_ask").format(m=esc(method))
        + await ui_step_bar(lang, 3, 4),  # [V1]
        reply_markup=cancel_kb(lang, "back_to_recharge"),  # [V7]
    )


# ============================================================
# WITHDRAW
# ============================================================

@dp.callback_query(F.data == "svc_withdraw")
async def svc_withdraw(cb: types.CallbackQuery, state: FSMContext):

    if not await user_allowed(cb.from_user.id):
        await cb.answer("غير مسموح باستخدام البوت.", show_alert=True)
        return

    await cb.answer()
    await state.clear()  # [FIX 2]
    await state.set_state(WithdrawFSM.amount)

    lang = await user_lang(cb.from_user.id)
    limits = await amount_limits("withdraw")  # [NEW 27]

    # [USR2-5] آخر مبلغ سحب كزر سريع
    db = await get_db()
    try:
        cur = await db.execute(
            """
            SELECT amount FROM finance_requests
            WHERE telegram_id = ? AND type = 'withdraw'
            ORDER BY id DESC LIMIT 1
            """,
            (cb.from_user.id,),
        )
        last_row = await cur.fetchone()
    finally:
        await db.close()

    markup = None
    if last_row:
        qb = InlineKeyboardBuilder()
        qb.button(
            text=tr(lang, "wd_last", amt=money(last_row["amount"])),
            callback_data=f"qw:{round2(float(last_row['amount'])):g}",
        )
        qb.adjust(1)
        markup = qb.as_markup()

    await cb.message.answer(
        tr(lang, "withdraw_prompt",
           min=money(limits["min"]), max=money(limits["max"])),
        reply_markup=markup,
    )

    # [USR4-2] دفتر وجهات السحب المحفوظة
    accounts = await get_payout_accounts(cb.from_user.id)

    if accounts:
        ab = InlineKeyboardBuilder()

        for acct in accounts:
            ab.button(
                text=(f"📒 {acct['label']} "
                      f"{mask_acct(acct['destination'])}"),
                callback_data=f"wdacct:{acct['id']}",
            )

        ab.button(text="➕ حفظ وجهة", callback_data="wdacct_add")
        ab.button(text="🗑 حذف وجهة", callback_data="wdacct_del")
        ab.adjust(1)
        await cb.message.answer(
            "📒 <b>وجهات السحب المحفوظة</b>"
            "\nاختر واحدة لتُرفق بطلب السحب القادم:",
            reply_markup=ab.as_markup(),
        )


@dp.message(WithdrawFSM.amount)
async def withdraw_amount(message: types.Message, state: FSMContext):

    if not await user_allowed(message.from_user.id, message):
        return

    # [R6-PLUS7 E4] منع العمليات المالية خلال نافذة الصيانة
    if await _maint_fin_msg(message, state):
        return

    # [ADM-3] إيقاف السحوبات يدوياً
    if await get_setting("withdraws_paused") == "1":
        lang = await user_lang(message.from_user.id)
        reason = (await get_setting("pause_reason_wd") or "").strip()
        await message.answer(tr(
            lang, "pause_wd",
            reason=esc(reason) if reason else tr(lang, "pause_default"),
        ))
        await state.clear()
        return

    amount = parse_amount(message.text)  # [FIX 7]

    if amount is None:
        await message.answer(
            "❌ مبلغ غير صالح.\n"
            f"أرسل مبلغًا أكبر من 0 ولا يتجاوز {MAX_AMOUNT}\n"
            "وبمنزلتين عشريتين كحد أقصى.\n\nللإلغاء أرسل /cancel"
        )
        return

    limits = await amount_limits("withdraw")  # [NEW 27]
    if not (limits["min"] <= amount <= limits["max"]):
        await message.answer(
            f"❌ المبلغ يجب أن يكون بين {money(limits['min'])}"
            f" و {money(limits['max'])}.\n\nللإلغاء أرسل /cancel"
        )
        return

    # [NEW 41] سقوف السحب اليومية
    cap_error = await check_withdraw_caps(message.from_user.id, amount)
    if cap_error:
        await message.answer(f"🛑 {cap_error}\n\nللإلغاء أرسل /cancel")
        return

    # [R6-PLUS5] حد عدد طلبات السحب اليومي
    wd_count_lim = await get_float_setting("daily_wd_count", 0.0)

    if wd_count_lim > 0:
        today_d = f"{datetime.now(timezone.utc):%Y-%m-%d}%"
        db_c = await get_db()

        try:
            cur_c = await db_c.execute(
                "SELECT COUNT(*) AS c FROM finance_requests"
                " WHERE telegram_id = ? AND type = 'withdraw'"
                " AND created_at LIKE ?",
                (message.from_user.id, today_d),
            )
            wd_today = (await cur_c.fetchone())["c"]
        finally:
            await db_c.close()

        if wd_today >= int(wd_count_lim):
            wd_lang_c = await user_lang(message.from_user.id)
            await message.answer(
                r6t(wd_lang_c, "wd_count_limit").format(
                    n=int(wd_count_lim),
                )
                + "\n\nللإلغاء أرسل /cancel"
            )
            return

    user = await get_user(message.from_user.id)

    if not user:
        await message.answer("❌ تعذر العثور على حسابك.")
        await state.clear()
        return

    if round2(float(user["balance"] or 0)) < amount:  # [FIX 7]
        await message.answer(
            "❌ الرصيد غير كافٍ.\n"
            f"رصيدك الحالي: {money(user['balance'])}"
        )
        return

    if await has_pending_finance_request(message.from_user.id, "withdraw"):
        await message.answer("⚠️ لديك بالفعل طلب سحب معلق قيد المراجعة.")
        return

    # [R6] طريقة السحب وحساب الاستلام (الواجهة الأصلية + الدفتر)
    wd_lang = await user_lang(message.from_user.id)

    # [R6-NEW] فترة التهدئة بين طلبات السحب
    cd_min = await get_float_setting("withdraw_cooldown_min", 0.0)

    if cd_min > 0:
        urow = await get_user(message.from_user.id)

        if urow:
            db_cd = await get_db()

            try:
                cur_cd = await db_cd.execute(
                    "SELECT created_at FROM transactions"
                    " WHERE user_id = ? AND type = 'withdraw'"
                    " ORDER BY id DESC LIMIT 1",
                    (urow["id"],),
                )
                last_wd = await cur_cd.fetchone()
            finally:
                await db_cd.close()

            if last_wd and last_wd["created_at"]:
                try:
                    last_dt = datetime.fromisoformat(
                        last_wd["created_at"]
                    )
                    elapsed = (
                        datetime.now(timezone.utc) - last_dt
                    ).total_seconds() / 60.0
                except (ValueError, TypeError):
                    elapsed = None

                if elapsed is not None and elapsed < cd_min:
                    remain = max(1, int(round(cd_min - elapsed)))
                    wait_str = (
                        f"{remain // 60} ساعة و {remain % 60} دقيقة"
                        if remain >= 60
                        else f"{remain} دقيقة"
                    )
                    await message.answer(
                        r6t(wd_lang, "wd_cooldown").format(m=wait_str)
                    )
                    await state.clear()
                    return

    wd_data = await state.get_data()
    wd_method = wd_data.get("withdraw_method") or ""
    wd_dest_manual = wd_data.get("wd_dest") or ""
    acct_id = wd_data.get("wd_acct")
    acct_label = ""
    acct_dest = ""

    if acct_id:
        acct = await get_payout_account(int(acct_id), message.from_user.id)

        if acct:
            acct_label = acct["label"]
            acct_dest = acct["destination"]

    dest_str = acct_dest or wd_dest_manual

    # [R6-PLUS2] كشف تكرار وجهة السحب بين حسابات مختلفة
    if dest_str and await feat_on("dest_alert"):  # [R6-PLUS3]
        db_d = await get_db()

        try:
            cur_d = await db_d.execute(
                "SELECT user_tid FROM payouts"
                " WHERE destination = ? AND user_tid != ?"
                " ORDER BY id DESC LIMIT 1",
                (dest_str, message.from_user.id),
            )
            dup_row = await cur_d.fetchone()
        finally:
            await db_d.close()

        if dup_row:
            if (await get_setting("dest_block") or "0") == "1":
                await message.answer(
                    "⛔ هذه الوجهة مستخدمة من حساب آخر.\n"
                    "تواصل مع الدعم إن كانت ملكك."
                )
                await state.clear()
                return

            try:
                await bot.send_message(
                    ADMIN_USER_ID,
                    "🕵️ <b>تنبيه وجهة سحب مكررة</b>\n\n"
                    f"👤 المستخدم: <code>{message.from_user.id}</code>\n"
                    f"🏦 الوجهة: <code>{esc(dest_str)}</code>\n"
                    "↩️ سبق أن سُحب إليها من: "
                    f"<code>{dup_row['user_tid']}</code>",
                )
            except Exception:
                pass

    wd_note = ""

    if wd_method or dest_str:
        wd_note = f"method={wd_method}"

        if dest_str:
            wd_note += f";dest={dest_str}"

    # [R6-NEW] عمولة السحب (0 افتراضياً) — يصل المستخدم الصافي
    fee_pct = await get_float_setting("withdraw_fee_percent", 0.0)
    gross = amount
    fee = round2(amount * fee_pct / 100.0) if fee_pct > 0 else 0.0
    net = round2(gross - fee)

    if net <= 0:
        await message.answer("❌ المبلغ قليل جداً بعد عمولة السحب.")
        await state.clear()
        return

    if fee > 0:
        wd_note = (wd_note + ";" if wd_note else "") + \
            f"fee={fee:g};gross={gross:g}"

    # [R6-PLUS3] تجهيز بيانات الإتمام (مشترك بين المسارين)
    await state.update_data(
        wdc_amount=amount, wdc_fee=fee, wdc_net=net, wdc_gross=gross,
        wdc_note=wd_note, wdc_method=wd_method, wdc_dest=dest_str,
        wdc_label=acct_label, wdc_manual=wd_dest_manual,
    )

    # [R6-PLUS3] بطاقة تأكيد السحب بالصافي قبل الإرسال
    if await feat_on("wd_confirm"):
        await state.set_state(WithdrawFSM.confirm)

        b = InlineKeyboardBuilder()
        b.button(text="✅ تأكيد الإرسال", callback_data="wd_ok")
        b.button(
            text=r6t(wd_lang, "help_btn"),
            callback_data="flowhelp:wd",
        )  # [R6-PLUS5]
        b.button(text="❌ إلغاء", callback_data="back_to_main")
        b.adjust(1)

        bal_after = round2(float(user["balance"] or 0) - amount)
        card = (
            "🧾 <b>تأكيد طلب السحب</b>\n\n"
            f"💵 المبلغ: {money(gross)}\n"
            + (f"🏷 عمولة السحب: {money(fee)}\n" if fee > 0 else "")
            + f"✅ الصافي الواصل: <b>{money(net)}</b>\n"
            + (f"🏦 الوجهة: {esc(dest_str)}\n" if dest_str else "")
            + f"💼 رصيدك بعد السحب: {money(bal_after)}\n\n"
            "هل تريد إرسال الطلب؟"
        )

        await message.answer(
            card + await ui_step_bar(wd_lang, 4, 4),  # [V1]
            reply_markup=b.as_markup(),
        )
        return

    await _finalize_withdraw(message, state, wd_lang)


async def _finalize_withdraw(message: types.Message, state: FSMContext,
                             wd_lang: str = "ar"):
    """[R6-PLUS3] إنشاء طلب السحب فعلياً بعد التأكيد."""
    data = await state.get_data()

    net = float(data["wdc_net"])
    fee = float(data["wdc_fee"])
    gross = float(data["wdc_gross"])
    wd_note = data["wdc_note"] or ""
    wd_method = data["wdc_method"] or ""
    acct_dest = data["wdc_dest"] or ""
    acct_label = data["wdc_label"] or ""
    wd_dest_manual = data["wdc_manual"] or ""

    # [R6-PLUS5] احتجاز رصيد السحب المعلق (بميزة قابلة للتفعيل)
    held = await feat_on("wd_hold")

    if held:
        wd_note = (wd_note + ";" if wd_note else "") + "held=1"

    request_id = await create_finance_request(
        message.from_user.id, "withdraw", net,
        note=wd_note,
    )

    if held:
        u_h = await get_user(message.from_user.id)

        db_h = await get_db()

        try:
            # [AUDIT F1] حارس: لا احتجاز يصنع رصيداً سالباً
            # [WDFIX 5.18.16] الاحتجاز بالإجمالي — العمولة تُحجب فوراً
            # (كان يخصم الصافي فتبقى العمولة برصيد المستخدم أبداً)
            gross_h = float(data["wdc_gross"])

            cur_h = await db_h.execute(
                "UPDATE users SET balance = balance - ?"
                " WHERE telegram_id = ? AND balance >= ?",
                (gross_h, message.from_user.id, gross_h),
            )

            if cur_h.rowcount != 1:
                await db_h.rollback()
                await db_h.execute(
                    "UPDATE finance_requests"
                    " SET status = 'expired', processed_at = ?"
                    " WHERE id = ? AND status = 'pending'",
                    (now_iso(), request_id),
                )
                await db_h.commit()

                # [AUTO-FIX 5.18.18] سبب واضح بدل رسالة مربكة:
                # طلبات سحب معلقة سابقة تحتجز الرصيد هي السبب غالباً
                pend_ids: list = []
                db_p = await get_db()

                try:
                    cur_p = await db_p.execute(
                        "SELECT id, amount FROM finance_requests"
                        " WHERE telegram_id = ? AND type = 'withdraw'"
                        " AND status IN ('pending', 'awaiting_admin')"
                        " AND id != ?"
                        " ORDER BY id DESC LIMIT 5",
                        (message.from_user.id, request_id),
                    )
                    pend_ids = [
                        f"#{r['id']} ({money(round2(float(r['amount'])))})"
                        for r in await cur_p.fetchall()
                    ]
                except Exception:
                    pass
                finally:
                    await db_p.close()

                if pend_ids:
                    await message.answer(
                        "❌ رصيدك المتاح لا يكفي لهذا السحب.\n\n"
                        "🔒 لديك طلبات سحب قيد المعالجة تحتجز رصيدك:\n"
                        + "\n".join(pend_ids)
                        + "\n\nانتظر معالجتها أو تابعها من «طلباتي»،"
                        " ثم أعد المحاولة."
                    )
                else:
                    await message.answer(
                        "❌ تغيّر رصيدك منذ إعداد الطلب — لم يُخصم شيء"
                        " وأُلغي الطلب.\nأعد المحاولة من الشاشة السابقة."
                    )
                await state.clear()
                return

            await db_h.execute(
                "INSERT INTO transactions"
                " (user_id, type, amount, note, created_at)"
                " VALUES (?, 'wd_hold', ?, ?, ?)",
                (
                    u_h["id"] if u_h else 0, gross_h,
                    f"request={request_id}", now_iso(),
                ),
            )
            await db_h.commit()
        finally:
            await db_h.close()

    wd_line = ""

    if fee > 0:
        wd_line = r6t(wd_lang, "wd_fee_line").format(
            f=money(fee), g=money(gross),
        )

    if wd_method:
        wd_line += r6t(wd_lang, "wd_method_line").format(m=esc(wd_method))

    if acct_dest:
        wd_line += r6t(wd_lang, "wd_dest_line").format(
            l=esc(acct_label), d=esc(acct_dest),
        )
    elif wd_dest_manual:
        wd_line += r6t(wd_lang, "wd_manual_line").format(
            d=esc(wd_dest_manual),
        )

    receipt = (
        tr(wd_lang, "receipt_line")  # [V5]
        if await feat_on("clear_receipt") else ""
    )

    await message.answer(
        r6t(wd_lang, "wd_success").format(
            amt=money(net), rid=request_id, wd_line=wd_line,
        ) + receipt,
        reply_markup=await menu_with_links(wd_lang, message.from_user.id),
    )

    # [NEW 15] إشعار الفريق المالي كاملاً
    await notify_finance_staff(
        "🏦 <b>طلب سحب جديد</b>\n\n"
        f"👤 المستخدم: <code>{message.from_user.id}</code>\n"
        f"💵 الصافي: <b>{money(net)}</b>\n"
        f"🆔 الطلب: #{request_id}{wd_line}",
        request_id,
        exclude_id=message.from_user.id,
    )

    await state.clear()


@dp.callback_query(F.data == "wd_ok")
async def wd_ok(cb: types.CallbackQuery, state: FSMContext):
    """[R6-PLUS3] تأكيد إرسال طلب السحب."""

    if not await user_allowed(cb.from_user.id):
        await cb.answer("غير مسموح.", show_alert=True)
        return

    if await state.get_state() != WithdrawFSM.confirm.state:
        await cb.answer("انتهت جلسة التأكيد — أعد الطلب.", show_alert=True)
        return

    await cb.answer("✅ أُرسل الطلب")
    await _finalize_withdraw(cb.message, state,
                             await user_lang(cb.from_user.id))


# ============================================================
# ADMIN PANEL / TOGGLE
# ============================================================

@dp.callback_query(F.data == "admin_panel")
async def admin_panel(cb: types.CallbackQuery, state: FSMContext):
    """[PANELHUB 5.18.14] اللوحة الكاملة دُمجت في «إدارة البوت» — alias."""
    await admin_manage_bot(cb, state)


@dp.callback_query(F.data == "admin_toggle_bot")
async def admin_toggle_bot(cb: types.CallbackQuery):

    if not await is_admin_or_supervisor(cb.from_user.id, "all"):
        await cb.answer("غير مصرّح.", show_alert=True)
        return

    current = await is_bot_active()
    new_value = "0" if current else "1"

    await set_setting("bot_active", new_value)

    await cb.answer(
        "تم إيقاف البوت." if new_value == "0" else "تم تشغيل البوت.",
        show_alert=True,
    )


# ============================================================
# ADMIN USERS
# ============================================================

@dp.callback_query(F.data == "admin_users")
async def admin_users(cb: types.CallbackQuery, state: FSMContext):
    _last_admin_screen[cb.from_user.id] = "admin_users"  # [V11]

    if not await is_admin_or_supervisor(cb.from_user.id):
        await cb.answer("غير مصرّح.", show_alert=True)
        return

    await cb.answer()
    await state.clear()  # [FIX 2]
    await safe_edit(cb.message, "👥 <b>إدارة المستخدمين</b>", admin_users_kb())


@dp.callback_query(F.data == "admin_user_create")
async def admin_user_create(cb: types.CallbackQuery, state: FSMContext):

    if not await is_admin_or_supervisor(cb.from_user.id, "users"):
        await cb.answer("غير مصرّح.", show_alert=True)
        return

    await cb.answer()
    await state.clear()
    await state.set_state(AdminCreateUserFSM.telegram_id)

    await cb.message.answer(
        "أرسل معرف تلجرام للمستخدم (@username):\n\n"
        "ℹ️ يجب أن يكون المستخدم قد فتح البوت سابقاً (/start)"
        " حتى يكون مسجلاً لدينا."
    , reply_markup=back_kb("admin_users"))


@dp.message(AdminCreateUserFSM.telegram_id)
async def admin_create_user_tid(message: types.Message, state: FSMContext):

    if not await is_admin_or_supervisor(message.from_user.id, "users"):
        await state.clear()
        return

    # [R6-REV] الإدخال بمعرف تلجرام (@username) مع قبول الرقم احتياطياً
    raw = (message.text or "").strip().lstrip("@")

    if re.fullmatch(r"\d{1,15}", raw):
        target = await get_user(int(raw))
    else:
        target = await get_user_by_tg_username(raw)

    if not target:
        await message.answer(
            "❌ لا يوجد مستخدم بهذا المعرف — يجب أن يكون قد فتح البوت"
            " أولاً (/start).\n\nللإلغاء أرسل /cancel"
        )
        return

    telegram_id = target["telegram_id"]

    await state.update_data(telegram_id=telegram_id)
    await state.set_state(AdminCreateUserFSM.site_username)

    await message.answer(
        f"✅ المستخدم: {esc(target['full_name'] or '')}"
        f" (<code>{telegram_id}</code>)\n"
        "أرسل اسم المستخدم للموقع:"
    , reply_markup=back_kb("admin_users"))


@dp.message(AdminCreateUserFSM.site_username)
async def admin_create_user_uname(message: types.Message, state: FSMContext):

    if not await is_admin_or_supervisor(message.from_user.id, "users"):
        await state.clear()
        return

    site_username = (message.text or "").strip()

    if (
        len(site_username) < 3
        or len(site_username) > 32
        or any(char.isspace() for char in site_username)
    ):
        await message.answer(
            "❌ اسم المستخدم يجب أن يكون بين 3 و32 حرفًا وبدون مسافات."
        )
        return

    data = await state.get_data()
    telegram_id = data["telegram_id"]

    existing = await get_user(telegram_id)

    if existing and existing["site_username"]:
        await message.answer("⚠️ هذا المستخدم لديه حساب موقع بالفعل.")
        await state.clear()
        return

    # [FIX 5] منع استخدام اسم محجوز من مستخدم آخر
    taken = await get_user_by_site_username(site_username)
    if taken and taken["telegram_id"] != telegram_id:
        await message.answer(
            "❌ اسم المستخدم محجوز مسبقًا من مستخدم آخر.\nاختر اسمًا مختلفًا."
        )
        return

    await create_user(telegram_id, "", f"User-{telegram_id}")

    password = generate_password()

    try:
        await update_user(
            telegram_id,
            site_username=site_username,
            site_password=encrypt_password(password),  # [NEW 20]
        )
    except sqlite3.IntegrityError:  # [FIX 5]
        await message.answer(
            "❌ اسم المستخدم محجوز مسبقًا من مستخدم آخر.\nاختر اسمًا مختلفًا."
        )
        return

    user = await get_user(telegram_id)

    await add_transaction(
        user["id"], "register", 0,
        f"admin_created site_user={site_username}",
    )

    await message.answer(
        "✅ <b>تم إنشاء الحساب.</b>\n\n"
        f"🆔 Telegram ID: <code>{telegram_id}</code>\n"
        f"👤 Username: <code>{esc(site_username)}</code>\n"
        f"🔑 Password: <code>{esc(password)}</code>",
        reply_markup=admin_users_kb(),
    )

    await state.clear()


@dp.callback_query(F.data == "admin_user_ban")
async def admin_user_ban(cb: types.CallbackQuery, state: FSMContext):

    if not await is_admin_or_supervisor(cb.from_user.id, "users"):
        await cb.answer("غير مصرّح.", show_alert=True)
        return

    await cb.answer()
    await state.clear()
    await state.set_state(AdminBanFSM.telegram_id)

    await cb.message.answer(
        "أرسل اسم حساب المستخدم في البوت (الاسم الذي أنشأه عند التسجيل)"
        " للحظر أو فك الحظر:\n\nℹ️ يمكنك أيضاً إرسال Telegram ID رقمياً."
    , reply_markup=back_kb("admin_users"))


@dp.message(AdminBanFSM.telegram_id)
async def admin_ban_user(message: types.Message, state: FSMContext):

    if not await is_admin_or_supervisor(message.from_user.id, "users"):
        await state.clear()
        return

    # [R6-REV] البحث باسم حساب البوت، مع قبول الرقم احتياطياً
    raw = (message.text or "").strip().lstrip("@")

    if re.fullmatch(r"\d{1,15}", raw):
        user = await get_user(int(raw)) or \
            await get_user_by_site_username(raw)
    else:
        user = await get_user_by_site_username(raw)

    if not user:
        await message.answer(
            "❌ لا يوجد مستخدم بهذا الحساب.\n\nللإلغاء أرسل /cancel"
        )
        return

    telegram_id = user["telegram_id"]

    if telegram_id == ADMIN_USER_ID:
        await message.answer("❌ لا يمكن حظر الأدمن الرئيسي.")
        await state.clear()
        return

    new_status = 0 if user["is_banned"] else 1

    await update_user(telegram_id, is_banned=new_status)

    await audit(  # [NEW 22]
        message.from_user.id,
        "ban" if new_status else "unban",
        telegram_id,
    )

    status_text = (
        "تم حظر المستخدم 🚫" if new_status else "تم فك حظر المستخدم ✅"
    )

    await message.answer(
        f"{status_text}\nTelegram ID: <code>{telegram_id}</code>",
        reply_markup=admin_users_kb(),
    )

    await state.clear()


# ============================================================
# ADMIN FINANCE
# ============================================================

@dp.callback_query(F.data == "admin_finance")
async def admin_finance(cb: types.CallbackQuery, state: FSMContext):

    if not await is_admin_or_supervisor(cb.from_user.id):
        await cb.answer("غير مصرّح.", show_alert=True)
        return

    await cb.answer()
    await state.clear()  # [FIX 2]
    await safe_edit(cb.message, "💳 <b>الشحن والسحب</b>", admin_finance_kb())


@dp.callback_query(F.data == "admin_finance_adjust")
async def admin_finance_adjust(cb: types.CallbackQuery, state: FSMContext):
    """[R6-REV] تعديل رصيد مستخدم — قائمة المستخدمين مباشرة."""

    if not await is_admin_or_supervisor(cb.from_user.id, "finance"):
        await cb.answer("غير مصرّح.", show_alert=True)
        return

    await cb.answer()
    await state.clear()
    await _render_adj_picker(cb.message, 0)


async def _render_adj_picker(msg, page: int, viewer_id: int = None):
    """[R6-REV] قائمة المستخدمين: الاسم + حساب البوت + الرصيد الحالي."""
    viewer_id = viewer_id or ADMIN_USER_ID
    page_size = 6

    db = await get_db()

    try:
        cur = await db.execute("SELECT COUNT(*) AS c FROM users")
        total = (await cur.fetchone())["c"]
        cur = await db.execute(
            """
            SELECT telegram_id, full_name, username, site_username,
                   balance, is_banned
            FROM users
            ORDER BY id
            LIMIT ? OFFSET ?
            """,
            (page_size, page * page_size),
        )
        rows = await cur.fetchall()
    finally:
        await db.close()

    pages = max(1, math.ceil(total / page_size))
    page = max(0, min(page, pages - 1))

    lines = [
        "⚖️ <b>تعديل رصيد مستخدم</b>"
        f" — صفحة {page + 1}/{pages} (المجموع {total})\n"
    ]
    b = InlineKeyboardBuilder()

    for row in rows:
        uname = f"@{row['username']}" if row["username"] else "—"
        acc = row["site_username"] or "—"
        flag = " 🚫" if row["is_banned"] else ""
        lines.append(
            f"<code>{row['telegram_id']}</code> | "
            f"{esc((row['full_name'] or '—')[:16])} ({esc(uname)}) | "
            f"👤 {esc(acc)} | "
            f"💰 {await fmt_bal(viewer_id, row['balance'])}{flag}"
        )
        b.button(
            text=f"⚖️ {row['telegram_id']}",
            callback_data=f"adjpick:{row['telegram_id']}:{page}",
        )

    nav = 1
    b.button(text=f"📄 {page + 1}/{pages}", callback_data="noop")
    if page > 0:
        b.button(text="⬅️", callback_data=f"adjpickpg:{page - 1}")
        nav += 1
    if page < pages - 1:
        b.button(text="➡️", callback_data=f"adjpickpg:{page + 1}")
        nav += 1

    b.button(text="🔢 إدخال ID يدوياً", callback_data="admin_adj_manual")
    b.button(text="🔙 رجوع", callback_data="admin_finance")

    sizes = [3] * math.ceil(len(rows) / 3)
    if nav:
        sizes.append(nav)
    sizes.append(2)
    b.adjust(*sizes)

    await safe_edit(msg, "\n".join(lines), b.as_markup())


@dp.callback_query(F.data.startswith("adjpickpg:"))
async def admin_adj_pick_page(cb: types.CallbackQuery, state: FSMContext):

    if not await is_admin_or_supervisor(cb.from_user.id, "finance"):
        await cb.answer("غير مصرّح.", show_alert=True)
        return

    try:
        page = max(0, int(cb.data.split(":")[1]))
    except (ValueError, IndexError):
        page = 0

    await cb.answer()
    await _render_adj_picker(cb.message, page, cb.from_user.id)


@dp.callback_query(F.data == "admin_adj_manual")
async def admin_adj_manual(cb: types.CallbackQuery, state: FSMContext):

    if not await is_admin_or_supervisor(cb.from_user.id, "finance"):
        await cb.answer("غير مصرّح.", show_alert=True)
        return

    await cb.answer()
    await state.clear()
    await state.set_state(AdminAdjustBalanceFSM.telegram_id)

    await cb.message.answer("أرسل Telegram ID للمستخدم:", reply_markup=back_kb("admin_finance"))


@dp.callback_query(F.data.startswith("adjpick:"))
async def admin_adj_pick(cb: types.CallbackQuery, state: FSMContext):
    """[R6-REV] اختيار مستخدم من القائمة → خطوة المبلغ مباشرة."""

    if not await is_admin_or_supervisor(cb.from_user.id, "finance"):
        await cb.answer("غير مصرّح.", show_alert=True)
        return

    try:
        telegram_id = int(cb.data.split(":")[1])
    except (ValueError, IndexError):
        await cb.answer("اختيار غير صالح.", show_alert=True)
        return

    user = await get_user(telegram_id)

    if not user:
        await cb.answer("المستخدم غير موجود.", show_alert=True)
        return

    await cb.answer()
    await state.clear()
    await state.update_data(telegram_id=telegram_id)
    await state.set_state(AdminAdjustBalanceFSM.amount)

    uname = f"@{user['username']}" if user["username"] else "—"
    acc = user["site_username"] or "—"

    await cb.message.answer(
        f"👤 <b>{esc(user['full_name'] or '—')}</b> ({esc(uname)})\n"
        f"👤 حساب البوت: <code>{esc(acc)}</code>\n"
        f"💰 الرصيد الحالي: <b>{await fmt_bal(cb.from_user.id, user['balance'])}</b>\n\n"
        "أرسل مقدار التعديل.\n\n"
        "مثال:\n"
        "<code>+100</code> لإضافة 100\n"
        "<code>-50</code> لخصم 50",
        reply_markup=back_kb("admin_finance"),
    )


@dp.message(AdminAdjustBalanceFSM.telegram_id)
async def admin_adjust_tid(message: types.Message, state: FSMContext):

    if not await is_admin_or_supervisor(message.from_user.id, "finance"):
        await state.clear()
        return

    try:
        telegram_id = int((message.text or "").strip())
    except Exception:
        await message.answer("❌ ID غير صالح.\n\nللإلغاء أرسل /cancel")
        return

    user = await get_user(telegram_id)

    if not user:
        await message.answer("❌ المستخدم غير موجود.")
        return

    await state.update_data(telegram_id=telegram_id)
    await state.set_state(AdminAdjustBalanceFSM.amount)

    uname = f"@{user['username']}" if user["username"] else "—"
    acc = user["site_username"] or "—"

    await message.answer(
        f"👤 <b>{esc(user['full_name'] or '—')}</b> ({esc(uname)})\n"
        f"👤 حساب البوت: <code>{esc(acc)}</code>\n"
        f"💰 الرصيد الحالي: <b>{await fmt_bal(message.from_user.id, user['balance'])}</b>\n\n"
        "أرسل مقدار التعديل.\n\n"
        "مثال:\n"
        "<code>+100</code> لإضافة 100\n"
        "<code>-50</code> لخصم 50",
        reply_markup=back_kb("admin_finance"),
    )


@dp.message(AdminAdjustBalanceFSM.amount)
async def admin_adjust_amount(message: types.Message, state: FSMContext):

    if not await is_admin_or_supervisor(message.from_user.id, "finance"):
        await state.clear()
        return

    amount = parse_amount(message.text, allow_negative=True)  # [FIX 7]

    if amount is None:
        await message.answer(
            "❌ أرسل رقمًا صحيحًا غير صفري،\n"
            f"قيمته المطلقة لا تتجاوز {MAX_AMOUNT}\n"
            "وبمنزلتين عشريتين كحد أقصى.\n\nللإلغاء أرسل /cancel"
        )
        return

    data = await state.get_data()
    telegram_id = data["telegram_id"]

    # [NEW 24] تأكيد ثنائي للتعديلات المالية الكبيرة
    threshold = await get_float_setting(
        "confirm_threshold", CONFIRM_THRESHOLD_DEFAULT
    )

    if abs(amount) >= threshold:
        await state.update_data(pending_amount=amount)

        kb = InlineKeyboardBuilder()
        kb.button(text="✅ تأكيد التعديل", callback_data="admin_adjust_confirm")
        kb.button(text="❌ إلغاء", callback_data="admin_adjust_cancel")
        kb.adjust(2)

        await message.answer(
            "⚠️ <b>تعديل مالي كبير!</b>\n\n"
            f"👤 المستخدم: <code>{telegram_id}</code>\n"
            f"💵 المقدار: <b>{money(amount)}</b>\n\n"
            "هل تريد التنفيذ؟",
            reply_markup=kb.as_markup(),
        )
        return

    result = await apply_balance_adjust(
        telegram_id, amount, message.from_user.id
    )

    if result is None:
        await message.answer("❌ المستخدم غير موجود أو الرصيد سيصبح سالبًا.")
        await state.clear()
        return

    old_balance, new_balance = result

    await message.answer(
        "✅ <b>تم تعديل الرصيد.</b>\n\n"
        f"الرصيد السابق: {money(old_balance)}\n"
        f"التعديل: {money(amount)}\n"
        f"الرصيد الجديد: {money(new_balance)}",
        reply_markup=admin_finance_kb(),
    )

    try:
        await bot.send_message(
            telegram_id,
            "💳 <b>تم تعديل رصيدك من الإدارة.</b>\n\n"
            f"التعديل: {money(amount)}\n"
            f"الرصيد الجديد: {money(new_balance)}",
        )
    except Exception as exc:
        logger.warning("تعذر إرسال إشعار تعديل الرصيد: %s", exc)

    await send_adjust_receipt(
        telegram_id, amount, old_balance, new_balance,
        message.from_user.id,
    )

    await state.clear()


@dp.callback_query(F.data == "admin_adjust_confirm")
async def admin_adjust_confirm(cb: types.CallbackQuery, state: FSMContext):
    """[NEW 24] تنفيذ التعديل الكبير بعد التأكيد."""

    if not await is_admin_or_supervisor(cb.from_user.id, "finance"):
        await cb.answer("غير مصرّح.", show_alert=True)
        return

    data = await state.get_data()
    telegram_id = data.get("telegram_id")
    amount = data.get("pending_amount")

    if telegram_id is None or amount is None:
        await cb.answer("لا توجد عملية معلقة.", show_alert=True)
        return

    await cb.answer()

    result = await apply_balance_adjust(
        telegram_id, amount, cb.from_user.id
    )
    await state.clear()

    if result is None:
        await safe_edit(
            cb.message,
            "❌ المستخدم غير موجود أو الرصيد سيصبح سالبًا.",
            admin_finance_kb(),
        )
        return

    old_balance, new_balance = result

    await safe_edit(
        cb.message,
        "✅ <b>تم تنفيذ التعديل بعد التأكيد.</b>\n\n"
        f"👤 المستخدم: <code>{telegram_id}</code>\n"
        f"الرصيد السابق: {money(old_balance)}\n"
        f"التعديل: {money(amount)}\n"
        f"الرصيد الجديد: {money(new_balance)}",
        admin_finance_kb(),
    )

    try:
        await bot.send_message(
            telegram_id,
            "💳 <b>تم تعديل رصيدك من الإدارة.</b>\n\n"
            f"التعديل: {money(amount)}\n"
            f"الرصيد الجديد: {money(new_balance)}",
        )
    except Exception as exc:
        logger.warning("تعذر إرسال إشعار تعديل الرصيد: %s", exc)

    await send_adjust_receipt(
        telegram_id, amount, old_balance, new_balance,
        cb.from_user.id,
    )


@dp.callback_query(F.data == "admin_adjust_cancel")
async def admin_adjust_cancel(cb: types.CallbackQuery, state: FSMContext):
    """[NEW 24] إلغاء التعديل الكبير."""

    if not await is_admin_or_supervisor(cb.from_user.id, "finance"):
        await cb.answer("غير مصرّح.", show_alert=True)
        return

    await state.clear()
    await cb.answer("تم إلغاء التعديل.")
    await safe_edit(cb.message, "❌ تم إلغاء التعديل.", admin_finance_kb())


# ============================================================
# PENDING FINANCE
# ============================================================

@dp.callback_query(F.data == "admin_finance_pending")
async def admin_finance_pending(cb: types.CallbackQuery, state: FSMContext):

    if not await is_admin_or_supervisor(cb.from_user.id, "finance"):
        await cb.answer("غير مصرّح.", show_alert=True)
        return

    await state.clear()  # [FIX 2]

    db = await get_db()

    try:
        cur = await db.execute(
            """
            SELECT *
            FROM finance_requests
            WHERE status = 'pending'
            ORDER BY id DESC
            LIMIT 20
            """
        )
        rows = await cur.fetchall()
    finally:
        await db.close()

    if not rows:
        await cb.answer()
        await safe_edit(
            cb.message,
            "📭 لا توجد طلبات مالية معلقة.\n\n"
            f"ℹ️ تنتهي صلاحية الطلبات تلقائيًا بعد {REQUEST_EXPIRY_HOURS} ساعة.",
            back_kb("admin_finance"),
        )
        return

    await cb.answer()
    await safe_edit(cb.message, f"📋 <b>الطلبات المعلقة:</b> {len(rows)}")

    for row in rows:
        request_type = "💰 شحن" if row["type"] == "deposit" else "🏦 سحب"

        text = (
            f"{request_type}\n"
            f"🆔 الطلب: #{row['id']}\n"
            f"👤 User ID: <code>{row['telegram_id']}</code>\n"
            f"💵 المبلغ: <b>{money(row['amount'])}</b>\n"
            f"🕐 {esc(row['created_at'])}"
        )

        try:
            await cb.message.answer(
                text,
                reply_markup=finance_request_kb(row["id"]),
            )
        except Exception as exc:
            logger.warning("تعذر عرض طلب مالي: %s", exc)


# ============================================================
# APPROVE FINANCE
# ============================================================

@dp.callback_query(F.data.startswith("finance_approve:"))
async def finance_approve(cb: types.CallbackQuery, state: FSMContext):


    try:
        request_id = int(cb.data.split(":")[1])
    except Exception:
        await cb.answer("طلب غير صالح.", show_alert=True)
        return

    db_t = await get_db()

    try:
        cur_t = await db_t.execute(
            "SELECT type FROM finance_requests WHERE id = ?",
            (request_id,),
        )
        trow = await cur_t.fetchone()
    finally:
        await db_t.close()

    if not trow:
        await cb.answer("الطلب غير موجود.", show_alert=True)
        return

    needed = "deposits" if trow["type"] == "deposit" else "withdrawals"

    if not await has_fin_perm(cb.from_user.id, needed):
        await cb.answer("غير مصرّح.", show_alert=True)
        return

    request, status, payout_id = await process_finance_request(
        request_id,
        cb.from_user.id,
        True,
    )

    if status == "budget_exceeded":  # [ADM3-5]
        await cb.answer(
            "💸 هذا السحب يتجاوز ميزانية اليوم —\n"
            "ارفع الميزانية من ⚙️ الإعدادات أو عُد غداً.",
            show_alert=True,
        )

        try:
            await cb.message.edit_reply_markup(reply_markup=None)
        except Exception:
            pass
        return

    if status == "awaiting_admin":  # [ADM-2]
        await cb.answer(
            "مبلغ ضخم — أُحيل للأدمن الرئيسي للموافقة النهائية.",
            show_alert=True,
        )

        try:
            await cb.message.edit_reply_markup(reply_markup=None)
        except Exception:
            pass

        try:
            kb2 = InlineKeyboardBuilder()
            kb2.button(text="✅ موافقة نهائية",
                       callback_data=f"finance_approve:{request_id}")
            kb2.button(text="❌ رفض",
                       callback_data=f"finance_reject:{request_id}")
            kb2.adjust(2)
            await bot.send_message(
                ADMIN_USER_ID,
                "👁 <b>سحب ضخم بانتظار موافقتك</b>\n\n"
                f"👤 <code>{request['telegram_id']}</code>\n"
                f"💵 {money(round2(float(request['amount'])))}\n"
                f"🆔 الطلب: #{request_id}\n"
                f"🙌 أقرّه المشرف: <code>{cb.from_user.id}</code>",
                reply_markup=kb2.as_markup(),
            )
        except Exception as exc:
            logger.warning("تعذر إشعار الأدمن بالموافقة المزدوجة: %s", exc)
        return

    if status == "approved":

        await cb.answer("تمت الموافقة.", show_alert=True)

        try:
            await cb.message.edit_reply_markup(reply_markup=None)
        except Exception:
            pass

        request_type = "شحن" if request["type"] == "deposit" else "سحب"
        gross = round2(float(request["amount"]))

        text = (
            f"✅ تمت الموافقة على طلب {request_type}.\n"
            f"💵 المبلغ: {money(gross)}\n"
            f"🆔 الطلب: #{request_id}"
        )

        receipt_rows = [
            ("Type", request["type"]),
            ("Amount", money(gross)),
        ]

        if request["type"] == "deposit":
            pct = max(
                0.0,
                min(
                    50.0,
                    await get_float_setting("commission_percent", 0.0),
                ),
            )
            commission = round2(gross * pct / 100.0)
            credited = round2(gross - commission)
            if commission > 0:
                text += (
                    f"\n💳 أُضيف للرصيد: {money(credited)}"
                    f" (عمولة {money(commission)})"
                )
            receipt_rows.append(
                (f"Commission ({pct:g}%)", money(commission))
            )
            receipt_rows.append(("Credited", money(credited)))
        else:
            receipt_rows.append(("Withdrawn", money(gross)))

        receipt_rows.append(("Status", "Approved"))
        receipt_rows.append(("Date (UTC)", now_iso()))
        receipt_rows.append(("Request ID", f"#{request_id}"))

        try:
            await bot.send_message(request["telegram_id"], text)
        except Exception as exc:
            logger.warning("تعذر إرسال إشعار الموافقة: %s", exc)

        receipt = build_receipt_pdf(  # [NEW 32]
            f"Receipt #{request_id}", receipt_rows,
        )
        if receipt:
            try:
                await bot.send_document(
                    request["telegram_id"],
                    receipt,
                    caption="🧾 إيصال العملية",
                )
            except Exception as exc:
                logger.warning("تعذر إرسال الإيصال: %s", exc)

        # [NEW 36] أمر الدفع أُنشئ داخل معاملة الموافقة نفسها؛
        # هنا فقط نعرض أزرار المعالجة للإدارة.
        if request["type"] == "withdraw" and payout_id:
            await audit(
                cb.from_user.id, "payout_created",
                f"payout={payout_id}",
                f"user={request['telegram_id']};amount={gross}",
            )
            kb_po = InlineKeyboardBuilder()
            kb_po.button(
                text="✅ مدفوعة",
                callback_data=f"payout_pay:{payout_id}",
            )
            kb_po.button(
                text="❌ فشلت (إرجاع)",
                callback_data=f"payout_fail:{payout_id}",
            )
            kb_po.adjust(2)
            try:
                await cb.message.answer(
                    "🚀 <b>أمر دفع جديد (Payout)</b>\n\n"
                    f"🆔 Payout: #{payout_id}\n"
                    f"👤 المستخدم: <code>{request['telegram_id']}</code>\n"
                    f"💵 المبلغ: <b>{money(gross)}</b>\n\n"
                    "بعد تحويل المبلغ فعلياً اضغط «مدفوعة»،\n"
                    "أو «فشلت» لإرجاع المبلغ لرصيد المستخدم تلقائياً.",
                    reply_markup=kb_po.as_markup(),
                )
            except Exception as exc:
                logger.warning("تعذر عرض أمر الدفع: %s", exc)

    elif status == "already_processed":
        await cb.answer("تمت معالجة الطلب مسبقًا.", show_alert=True)

    elif status == "insufficient_balance":
        await cb.answer("رصيد المستخدم لم يعد كافيًا.", show_alert=True)

    else:
        await cb.answer("تعذر معالجة الطلب.", show_alert=True)


# ============================================================
# REJECT FINANCE
# ============================================================

class AdminRejReasonFSM(StatesGroup):
    text = State()


async def _do_reject(rid: int, admin_id: int, reason: str = "",
                     orig_msg=None):
    """[R6-PLUS2] تنفيذ الرفض مع سبب يصل للمستخدم."""
    request, status, _p = await process_finance_request(rid, admin_id, False)

    if status == "rejected":
        if orig_msg is not None:
            try:
                await orig_msg.edit_reply_markup(reply_markup=None)
            except Exception:
                pass

        reason_line = f"\n📝 السبب: {esc(reason)}" if reason else ""

        # [R6-PLUS10 U38] زر إعادة المحاولة للشحن المرفوض
        retry_kb = None

        if request["type"] == "deposit" and await feat_on("retry_btn"):
            kb_r = InlineKeyboardBuilder()
            kb_r.button(text="🔄 أعد المحاولة", callback_data="retry_dep")
            kb_r.adjust(1)
            retry_kb = kb_r.as_markup()

        try:
            await bot.send_message(
                request["telegram_id"],
                "❌ تم رفض طلبك المالي.\n"
                f"💵 المبلغ: {money(request['amount'])}\n"
                f"🆔 الطلب: #{rid}"
                f"{reason_line}",
                reply_markup=retry_kb,
            )
        except Exception as exc:
            logger.warning("تعذر إرسال إشعار الرفض: %s", exc)

        return True

    return False


@dp.callback_query(F.data.startswith("finance_reject:"))
async def finance_reject(cb: types.CallbackQuery, state: FSMContext):

    try:
        request_id = int(cb.data.split(":")[1])
    except Exception:
        await cb.answer("طلب غير صالح.", show_alert=True)
        return

    db_t = await get_db()

    try:
        cur_t = await db_t.execute(
            "SELECT type FROM finance_requests WHERE id = ?",
            (request_id,),
        )
        trow = await cur_t.fetchone()
    finally:
        await db_t.close()

    if not trow:
        await cb.answer("الطلب غير موجود.", show_alert=True)
        return

    needed = "deposits" if trow["type"] == "deposit" else "withdrawals"

    if not await has_fin_perm(cb.from_user.id, needed):
        await cb.answer("غير مصرّح.", show_alert=True)
        return

    await cb.answer()
    await state.set_state(AdminRejReasonFSM.text)
    await state.update_data(rej_rid=request_id)

    b = InlineKeyboardBuilder()

    if await feat_on("reject_reasons"):  # [R6-PLUS10 E12]
        b.button(
            text="🔢 رقم العملية غير صحيح",
            callback_data=f"rej_q:{request_id}:txid",
        )
        b.button(
            text="👤 الحساب غير مطابق",
            callback_data=f"rej_q:{request_id}:acct",
        )
        b.button(
            text="💰 المبلغ غير واصل",
            callback_data=f"rej_q:{request_id}:nomoney",
        )

    b.button(text="✏️ سبب آخر (اكتب)", callback_data=f"rej_txt:{request_id}")
    b.button(text="⏭ رفض بدون سبب", callback_data=f"rej_no:{request_id}")
    b.adjust(1)

    await cb.message.answer(
        f"📝 ما سبب رفض الطلب #{request_id}؟\n"
        "(سيصل للمستخدم مع إشعار الرفض)\n\nللإلغاء أرسل /cancel",
        reply_markup=b.as_markup(),
    )


REJECT_PRESETS = {  # [R6-PLUS10 E12] أسباب مهذبة جاهزة للمستخدم
    "txid": "🔢 رقم العملية غير صحيح أو غير مطابق — تأكد من الرقم"
            " وأعد الإرسال 🙏",
    "acct": "👤 حساب الاستلام غير مطابق — تأكد من الرقم"
            " وأعد المحاولة 🙏",
    "nomoney": "💰 لم يصلنا المبلغ — تأكد من إتمام التحويل"
               " ثم أعد الإرسال 🙏",
}


@dp.callback_query(F.data.startswith("rej_txt:"))
async def rej_txt_pick(cb: types.CallbackQuery, state: FSMContext):
    """[R6-PLUS10 E12] اختيار كتابة سبب مخصص (نفس المسار القديم)."""
    try:
        request_id = int(cb.data.split(":")[1])
    except (ValueError, IndexError):
        await cb.answer("طلب غير صالح.", show_alert=True)
        return

    await cb.answer()
    await state.set_state(AdminRejReasonFSM.text)
    await state.update_data(rej_rid=request_id)
    await cb.message.answer(
        f"📝 اكتب سبب رفض الطلب #{request_id}:"
        "\n\nللإلغاء أرسل /cancel",
    )


@dp.callback_query(F.data.startswith("rej_q:"))
async def rej_quick(cb: types.CallbackQuery, state: FSMContext):
    """[R6-PLUS10 E12] رفض بضغطة بسبب جاهز."""

    try:
        parts = cb.data.split(":")
        request_id = int(parts[1])
        rk = parts[2]
    except (ValueError, IndexError):
        await cb.answer("طلب غير صالح.", show_alert=True)
        return

    if rk not in REJECT_PRESETS:
        await cb.answer("سبب غير معروف.", show_alert=True)
        return

    db_t = await get_db()

    try:
        cur_t = await db_t.execute(
            "SELECT type FROM finance_requests WHERE id = ?",
            (request_id,),
        )
        trow = await cur_t.fetchone()
    finally:
        await db_t.close()

    if not trow:
        await cb.answer("الطلب غير موجود.", show_alert=True)
        return

    needed = "deposits" if trow["type"] == "deposit" else "withdrawals"

    if not await has_fin_perm(cb.from_user.id, needed):
        await cb.answer("غير مصرّح.", show_alert=True)
        return

    await cb.answer()
    await state.clear()

    ok = await _do_reject(
        request_id, cb.from_user.id, REJECT_PRESETS[rk],
        orig_msg=cb.message,
    )

    await cb.message.answer(
        "✅ تم الرفض وإشعار المستخدم بالسبب." if ok
        else "⚠️ لم تتم المعالجة — قد يكون الطلب معالجاً مسبقاً.",
    )


@dp.callback_query(F.data.startswith("rej_no:"))
async def rej_no_reason(cb: types.CallbackQuery, state: FSMContext):

    try:
        request_id = int(cb.data.split(":")[1])
    except (ValueError, IndexError):
        await cb.answer("طلب غير صالح.", show_alert=True)
        return

    db_t2 = await get_db()

    try:
        cur_t2 = await db_t2.execute(
            "SELECT type FROM finance_requests WHERE id = ?",
            (request_id,),
        )
        trow2 = await cur_t2.fetchone()
    finally:
        await db_t2.close()

    if not trow2:
        await cb.answer("الطلب غير موجود.", show_alert=True)
        return

    needed2 = "deposits" if trow2["type"] == "deposit" else "withdrawals"

    if not await has_fin_perm(cb.from_user.id, needed2):
        await cb.answer("غير مصرّح.", show_alert=True)
        return

    ok = await _do_reject(request_id, cb.from_user.id, "", cb.message)
    await state.clear()
    await cb.answer(
        "تم رفض الطلب." if ok else "تمت معالجته مسبقاً.", show_alert=True,
    )


@dp.message(AdminRejReasonFSM.text)
async def rej_reason_save(message: types.Message, state: FSMContext):
    """[R6-PLUS2] حفظ سبب الرفض وتنفيذه."""

    data0 = await state.get_data()
    rid0 = data0.get("rej_rid")

    if not rid0:
        await state.clear()
        return

    db_t3 = await get_db()

    try:
        cur_t3 = await db_t3.execute(
            "SELECT type FROM finance_requests WHERE id = ?", (rid0,),
        )
        trow3 = await cur_t3.fetchone()
    finally:
        await db_t3.close()

    if not trow3:
        await state.clear()
        return

    needed3 = "deposits" if trow3["type"] == "deposit" else "withdrawals"

    if not await has_fin_perm(message.from_user.id, needed3):
        await state.clear()
        return

    reason = (message.text or "").strip()[:300]

    if reason.startswith("/"):
        await state.clear()
        return

    await state.clear()

    ok = await _do_reject(rid0, message.from_user.id, reason)

    await message.answer(
        "✅ تم رفض الطلب وإشعار المستخدم بالسبب."
        if ok else "⚠️ تمت معالجة الطلب مسبقاً."
    )


# ============================================================
# FINANCE LOGS
# ============================================================

@dp.callback_query(F.data == "admin_finance_logs")
async def admin_finance_logs(cb: types.CallbackQuery, state: FSMContext):

    if not await is_admin_or_supervisor(cb.from_user.id, "finance"):
        await cb.answer("غير مصرّح.", show_alert=True)
        return

    await state.clear()  # [FIX 2]

    db = await get_db()

    try:
        cur = await db.execute(
            """
            SELECT t.*, u.telegram_id
            FROM transactions t
            JOIN users u ON u.id = t.user_id
            WHERE t.type IN ('deposit', 'withdraw', 'admin_adjust')
            ORDER BY t.id DESC
            LIMIT 30
            """
        )
        rows = await cur.fetchall()
    finally:
        await db.close()

    if not rows:
        text = "📭 لا توجد عمليات مالية."
    else:
        lines = ["📊 <b>آخر العمليات المالية</b>\n"]

        for row in rows:
            type_name = {
                "deposit": "💰 شحن",
                "withdraw": "🏦 سحب",
                "admin_adjust": "🛠 تعديل إداري",
            }.get(row["type"], row["type"])

            lines.append(
                f"{type_name} | <code>{row['telegram_id']}</code> | "
                f"{money(row['amount'])}\n"
                f"🕐 {esc(row['created_at'])}"
            )

        text = "\n\n".join(lines)

    await cb.answer()
    await safe_edit(cb.message, text, back_kb("admin_finance"))


# ============================================================
# ADMIN GIFTS
# ============================================================

@dp.callback_query(F.data == "admin_gifts")
async def admin_gifts(cb: types.CallbackQuery, state: FSMContext):

    if not await is_admin_or_supervisor(cb.from_user.id):
        await cb.answer("غير مصرّح.", show_alert=True)
        return

    await cb.answer()
    await state.clear()  # [FIX 2]
    await safe_edit(cb.message, "🎁 <b>أكواد الهدايا</b>", admin_gifts_kb())


@dp.callback_query(F.data == "admin_gift_create")
async def admin_gift_create(cb: types.CallbackQuery, state: FSMContext):

    if not await is_admin_or_supervisor(cb.from_user.id, "gifts"):
        await cb.answer("غير مصرّح.", show_alert=True)
        return

    await cb.answer()
    await state.clear()
    await state.set_state(AdminGiftCodeFSM.amount)

    await cb.message.answer("🎁 أرسل قيمة كود الهدية:", reply_markup=back_kb("admin_gifts"))


@dp.message(AdminGiftCodeFSM.amount)
async def admin_gift_create_amount(message: types.Message, state: FSMContext):

    if not await is_admin_or_supervisor(message.from_user.id, "gifts"):
        await state.clear()
        return

    amount = parse_amount(message.text)  # [FIX 7]

    if amount is None:
        await message.answer(
            "❌ مبلغ غير صالح.\n"
            f"أرسل مبلغًا أكبر من 0 ولا يتجاوز {MAX_AMOUNT}\n"
            "وبمنزلتين عشريتين كحد أقصى.\n\nللإلغاء أرسل /cancel"
        )
        return

    code = await generate_unique_gift_code(amount)

    await audit(  # [NEW 22]
        message.from_user.id, "gift_create", code, f"amount={amount}",
    )

    await message.answer(
        "🎁 <b>تم إنشاء كود الهدية.</b>\n\n"
        f"🔑 الكود: <code>{code}</code>\n"
        f"💰 القيمة: <b>{money(amount)}</b>",
        reply_markup=admin_gifts_kb(),
    )

    await state.clear()


async def render_gift_codes_page(page: int):
    """[FIX 12] بناء صفحة أكواد الهدايا (نص + كيبورد)."""

    db = await get_db()

    try:
        cur = await db.execute("SELECT COUNT(*) AS c FROM gift_codes")
        total = (await cur.fetchone())["c"]
    finally:
        await db.close()

    if total == 0:
        return "📭 لا توجد أكواد.", back_kb("admin_gifts")

    pages = max(1, math.ceil(total / GIFTS_PAGE_SIZE))
    page = min(max(page, 0), pages - 1)

    db = await get_db()

    try:
        cur = await db.execute(
            """
            SELECT *
            FROM gift_codes
            ORDER BY created_at DESC, code
            LIMIT ? OFFSET ?
            """,
            (GIFTS_PAGE_SIZE, page * GIFTS_PAGE_SIZE),
        )
        rows = await cur.fetchall()
    finally:
        await db.close()

    lines = [f"📋 <b>أكواد الهدايا</b> — صفحة {page + 1}/{pages}\n"]
    delete_buttons = []

    for row in rows:
        if row["used_by"] == -1:
            status = "🚫 ملغى"  # [ADM-1]
        elif row["used_by"]:
            status = f"❌ مستخدم بواسطة <code>{row['used_by']}</code>"
        else:
            status = "✅ غير مستخدم"

        lines.append(
            f"🎁 <code>{esc(row['code'])}</code> | "
            f"💰 {money(row['amount'])} | {status}\n"
            f"🕐 {esc(row['created_at'])}"
        )

        if not row["used_by"]:
            delete_buttons.append(row["code"])

    b = InlineKeyboardBuilder()

    for code in delete_buttons:
        b.button(text=f"🗑 {code}", callback_data=f"gift_del:{page}:{code}")

    nav_count = 0
    if page > 0:
        b.button(text="⬅️ السابق", callback_data=f"admin_gift_list:{page - 1}")
        nav_count += 1
    if page < pages - 1:
        b.button(text="التالي ➡️", callback_data=f"admin_gift_list:{page + 1}")
        nav_count += 1

    b.button(text="🔙 رجوع", callback_data="admin_gifts")

    sizes = [1] * len(delete_buttons)
    if nav_count:
        sizes.append(nav_count)
    sizes.append(1)
    b.adjust(*sizes)

    return "\n".join(lines), b.as_markup()


@dp.callback_query(F.data.startswith("admin_gift_list:"))
async def admin_gift_list(cb: types.CallbackQuery, state: FSMContext):

    if not await is_admin_or_supervisor(cb.from_user.id, "gifts"):
        await cb.answer("غير مصرّح.", show_alert=True)
        return

    await state.clear()  # [FIX 2]

    try:
        page = int(cb.data.split(":", 1)[1])
    except (ValueError, IndexError):
        page = 0

    await cb.answer()

    text, kb = await render_gift_codes_page(page)
    await safe_edit(cb.message, text, kb)


@dp.callback_query(F.data.startswith("gift_del:"))
async def gift_delete(cb: types.CallbackQuery, state: FSMContext):

    if not await is_admin_or_supervisor(cb.from_user.id, "gifts"):
        await cb.answer("غير مصرّح.", show_alert=True)
        return

    await state.clear()  # [FIX 2]

    try:
        _, page_raw, code = cb.data.split(":", 2)
        page = int(page_raw)
    except (ValueError, IndexError):
        await cb.answer("طلب غير صالح.", show_alert=True)
        return

    db = await get_db()

    try:
        cur = await db.execute(
            "SELECT used_by FROM gift_codes WHERE code = ?",
            (code,),
        )
        row = await cur.fetchone()

        if not row:
            await cb.answer("الكود غير موجود.", show_alert=True)
            return

        if row["used_by"]:
            await cb.answer("لا يمكن حذف كود مستخدم.", show_alert=True)
            return

        await db.execute(
            "DELETE FROM gift_codes WHERE code = ? AND used_by IS NULL",
            (code,),
        )
        await db.commit()
    finally:
        await db.close()

    await audit(cb.from_user.id, "gift_delete", code)  # [NEW 22]
    await cb.answer("تم حذف الكود.")

    text, kb = await render_gift_codes_page(page)
    await safe_edit(cb.message, text, kb)


# ============================================================
# ADMIN SUPERVISORS
# ============================================================

@dp.callback_query(F.data == "admin_supervisors")
async def admin_supervisors(cb: types.CallbackQuery, state: FSMContext):

    if cb.from_user.id != ADMIN_USER_ID:
        await cb.answer("هذه الخاصية للأدمن الرئيسي فقط.", show_alert=True)
        return

    await cb.answer()
    await state.clear()  # [FIX 2]
    await safe_edit(cb.message, "🛡 <b>إدارة المشرفين</b>", admin_supervisors_kb())


@dp.callback_query(F.data == "admin_sup_add")
async def admin_sup_add(cb: types.CallbackQuery, state: FSMContext):
    """[R6-REV] قائمة المستخدمين للإضافة المباشرة كمشرف."""

    if cb.from_user.id != ADMIN_USER_ID:
        await cb.answer("للأدمن الرئيسي فقط.", show_alert=True)
        return

    await cb.answer()
    await state.clear()
    await _render_sup_picker(cb.message, 0)


async def _render_sup_picker(msg, page: int):
    """[R6-REV] قائمة المستخدمين بمعلوماتهم لاختيار مشرف."""
    page_size = 6

    db = await get_db()

    try:
        cur = await db.execute("SELECT COUNT(*) AS c FROM users")
        total = (await cur.fetchone())["c"]
        cur = await db.execute(
            """
            SELECT telegram_id, full_name, username, site_username,
                   balance, is_banned
            FROM users
            ORDER BY id
            LIMIT ? OFFSET ?
            """,
            (page_size, page * page_size),
        )
        rows = await cur.fetchall()
    finally:
        await db.close()

    pages = max(1, math.ceil(total / page_size))
    page = max(0, min(page, pages - 1))

    lines = [
        f"🛡 <b>اختر مستخدماً لإضافته/تحديثه كمشرف</b>"
        f" — صفحة {page + 1}/{pages} (المجموع {total})\n"
    ]
    b = InlineKeyboardBuilder()

    for row in rows:
        uname = f"@{row['username']}" if row["username"] else "—"
        acc = row["site_username"] or "—"
        flag = " 🚫" if row["is_banned"] else ""
        lines.append(
            f"<code>{row['telegram_id']}</code> | "
            f"{esc((row['full_name'] or '—')[:16])} | "
            f"{esc(uname)} | 👤 {esc(acc)} | "
            f"{money(row['balance'])}{flag}"
        )
        b.button(
            text=f"🛡 {row['telegram_id']}",
            callback_data=f"suppick:{row['telegram_id']}:{page}",
        )

    nav = 1
    b.button(text=f"📄 {page + 1}/{pages}", callback_data="noop")
    if page > 0:
        b.button(text="⬅️", callback_data=f"suppickpg:{page - 1}")
        nav += 1
    if page < pages - 1:
        b.button(text="➡️", callback_data=f"suppickpg:{page + 1}")
        nav += 1

    b.button(text="🔢 إدخال ID يدوياً", callback_data="admin_sup_manual")
    b.button(text="🔙 رجوع", callback_data="admin_supervisors")

    sizes = [3] * math.ceil(len(rows) / 3)
    if nav:
        sizes.append(nav)
    sizes.append(2)
    b.adjust(*sizes)

    await safe_edit(msg, "\n".join(lines), b.as_markup())


@dp.callback_query(F.data.startswith("suppickpg:"))
async def admin_sup_pick_page(cb: types.CallbackQuery, state: FSMContext):

    if cb.from_user.id != ADMIN_USER_ID:
        await cb.answer("للأدمن الرئيسي فقط.", show_alert=True)
        return

    try:
        page = max(0, int(cb.data.split(":")[1]))
    except (ValueError, IndexError):
        page = 0

    await cb.answer()
    await _render_sup_picker(cb.message, page)


@dp.callback_query(F.data == "admin_sup_manual")
async def admin_sup_manual(cb: types.CallbackQuery, state: FSMContext):

    if cb.from_user.id != ADMIN_USER_ID:
        await cb.answer("للأدمن الرئيسي فقط.", show_alert=True)
        return

    await cb.answer()
    await state.clear()
    await state.set_state(AdminSupervisorFSM.telegram_id)

    await cb.message.answer("أرسل Telegram ID للمشرف:", reply_markup=back_kb("admin_supervisors"))


@dp.callback_query(F.data.startswith("suppick:"))
async def admin_sup_pick(cb: types.CallbackQuery, state: FSMContext):
    """[R6-REV] إضافة مشرف من القائمة مباشرة → خطوة الصلاحيات."""

    if cb.from_user.id != ADMIN_USER_ID:
        await cb.answer("للأدمن الرئيسي فقط.", show_alert=True)
        return

    try:
        telegram_id = int(cb.data.split(":")[1])
    except (ValueError, IndexError):
        await cb.answer("اختيار غير صالح.", show_alert=True)
        return

    if telegram_id == ADMIN_USER_ID:
        await cb.answer("ℹ️ هذا هو الأدمن الرئيسي بالفعل.", show_alert=True)
        return

    await cb.answer()
    await state.clear()
    await _sup_perms_prompt(state, telegram_id, cb.message.answer)


@dp.message(AdminSupervisorFSM.telegram_id)
async def admin_sup_tid(message: types.Message, state: FSMContext):

    if message.from_user.id != ADMIN_USER_ID:
        await state.clear()
        return

    try:
        telegram_id = int((message.text or "").strip())
        if telegram_id <= 0:
            raise ValueError
    except Exception:
        await message.answer("❌ ID غير صالح.\n\nللإلغاء أرسل /cancel")
        return

    if telegram_id == ADMIN_USER_ID:
        await message.answer("ℹ️ هذا هو الأدمن الرئيسي بالفعل.")
        await state.clear()
        return

    await _sup_perms_prompt(state, telegram_id, message.answer)


async def _sup_perms_prompt(state: FSMContext, telegram_id: int, send):
    """[R6-REV] خطوة الصلاحيات — مشتركة بين الإدخال اليدوي والقائمة."""
    await state.update_data(telegram_id=telegram_id)

    # [NEW 39] الصلاحيات الحالية إن كان المشرف موجوداً
    db = await get_db()
    try:
        cur = await db.execute(
            "SELECT permissions FROM supervisors WHERE telegram_id = ?",
            (telegram_id,),
        )
        row = await cur.fetchone()
    finally:
        await db.close()

    try:
        current_perms = json.loads(row["permissions"] or "[]") if row else []
    except Exception:
        current_perms = []

    await state.update_data(perms=list(current_perms))
    await state.set_state(AdminSupervisorFSM.permissions)

    await send(
        f"🛡 صلاحيات المشرف <code>{telegram_id}</code>\n"
        "اضغط على كل صلاحية للتبديل ثم احفظ:",
        reply_markup=render_sup_perms_kb(current_perms),
    )


SUP_PERM_LABELS = {
    "users": "👥 المستخدمون",
    "finance": "💳 المالية كاملة",
    "deposits": "📥 الشحنات فقط",
    "withdrawals": "📤 السحوبات فقط",
    "gifts": "🎁 الهدايا",
    "reports": "📥 التقارير",
    "all": "🌐 كل الصلاحيات",
}


# [R6-PLUS3] مركز تفعيل الميزات — كل ميزة بمفتاح feat_<key>
FEATURES = {
    "daily_summary": ("📨 الملخص اليومي", "1"),
    "weekly_report": ("📈 التقرير الأسبوعي", "1"),
    "stale_alerts": ("⏰ تذكير الطلبات العالقة", "1"),
    "winback": ("🎁 الرجوع للغائبين", "0"),
    "points": ("⭐ نقاط الولاء", "1"),
    "payout_rating": ("🌟 تقييم بعد السحب", "1"),
    "offers_badge": ("🔴 بادج العروض", "1"),
    "ann_push": ("🔔 بث مشتركي الجرس", "1"),
    "new_user_notify": ("🆕 إشعار مستخدم جديد", "0"),
    "profit_kpi": ("💰 KPI الأرباح", "1"),
    "proc_kpi": ("⚡ KPI زمن المعالجة", "1"),
    "digest": ("📭 الملخص الشخصي", "1"),
    "fav_method": ("⭐ تذكر الطريقة", "1"),
    "wd_confirm": ("✅ تأكيد السحب بالصافي", "1"),
    "rev_calc": ("🔄 الحاسبة العكسية", "1"),
    "dest_alert": ("🕵️ الوجهات المكررة", "1"),
    "db_maint": ("🧱 صيانة القاعدة", "1"),
    "anniv_gift": ("🎂 هدية ذكرى الانضمام", "1"),
    "wd_hold": ("🔒 احتجاز رصيد السحب", "1"),
    "inst_dep_alert": ("🚨 شحن ثم سحب فوري", "1"),
    "wd_dest_check": ("✅ تحقق وجهة السحب", "1"),  # [R6-PLUS7]
    "rates_screen": ("📊 الأسعار والحدود", "1"),  # [R6-PLUS7]
    "maint_announce": ("🔔 إعلان الصيانة", "1"),  # [R6-PLUS7]
    "mem_cleanup": ("🧹 تنظيف التنبيهات", "1"),  # [R6-PLUS7]
    "quiet_errors": ("🤫 إسكات الأخطاء البريئة", "1"),  # [R6-PLUS8]
    "step_bars": ("🧭 مؤشر الخطوات", "1"),  # [R6-PLUS9 V1]
    "bal_bar": ("💳 شريط الرصيد", "1"),  # [V2]
    "smart_welcome": ("👋 ترحيب ذكي", "1"),  # [V3]
    "onboarding": ("🎓 جولة تعريفية للجدد", "1"),  # [V4]
    "clear_receipt": ("✅ طمأنة بعد الطلب", "1"),  # [V5]
    "damascus_time": ("🕐 توقيت دمشق", "0"),  # [V6]
    "welcome_photo": ("🖼 ترحيب بصورة", "0"),  # [V8]
    "quick_card": ("👤 الملف بإشعارات الفريق", "1"),  # [V9]
    "live_counters": ("🔢 عدادات حية", "1"),  # [V10]
    "profit_chart": ("📈 رسم الأرباح", "1"),  # [V12]
    "txid_dedup": ("⛔ منع تكرار العملية", "1"),  # [R6-PLUS10 F8]
    "hold_stale": ("⏰ تنبيه الاحتجاز العالق", "1"),  # [F9]
    "retention": ("♻️ تقرير الاحتفاظ", "1"),  # [E7]
    "user_ltv": ("💎 إجمالي المستخدم", "1"),  # [E8]
    "peak_hours": ("🔥 ساعات الذروة", "1"),  # [E9]
    "last_request": ("📍 آخر طلبي", "1"),  # [U35]
    "bal_alert": ("🔔 تنبيه نزول الرصيد", "1"),  # [U36]
    "fav_amount": ("⭐ مبلغ شحن مفضل", "1"),  # [U37]
    "retry_btn": ("🔄 إعادة المحاولة", "1"),  # [U38]
    "reject_reasons": ("📝 أسباب رفض جاهزة", "1"),  # [E12]
    "weekly_now": ("👁 معاينة الأسبوعي", "1"),  # [E11]
    "panel_wallets": ("💼 محافظ الوكيل", "1"),  # [AGENT-FULL]
    "sham_auto_dep": ("🤖 الشحن الآلي (شام)", "0"),  # [AUTO-DEP] مطفأ افتراضياً
    "sham_auto_wd": ("🤖 السحب الآلي (شام)", "0"),  # [AUTO-WD] مطفأ افتراضياً
    "auto_create": ("⚡ إنشاء حساب آلي", "1"),  # [R6-PLUS12]
    "site_balance_live": ("🎮 رصيد الموقع الحي", "1"),  # [R6-PLUS12]
    "panel_recon": ("🌙 مطابقة اللوحة الليلية", "1"),  # [R6-PLUS13]
    "dep_bridge": ("🌉 جسر إشعارات شام", "0"),  # [R6-PLUS13]
    "sham_link": ("💵 ربط شام كاش (QR)", "1"),  # [R6-PLUS14]
    "sham_wallet_guard": ("🛡 حارس المحفظة", "0"),  # [WGT] مطفأ افتراضياً
    "panel_hidden": ("🙈 إخفاء لوحة الوكيل", "0"),  # [PHIDE 5.18.2] افتراضياً ظاهرة
}


async def feat_on(key: str) -> bool:
    """[R6-PLUS3] هل الميزة مفعلة؟ يقرأ feat_<key> ويرجع للافتراضي."""
    default = FEATURES.get(key, ("", "1"))[1]
    value = (await get_setting(f"feat_{key}") or "").strip()
    return (value or default) == "1"


async def has_fin_perm(telegram_id: int, kind: str) -> bool:
    """[R6-PLUS2] صلاحية مالية دقيقة: deposits أو withdrawals.
    «finance» الكاملة تمنحهما معاً."""
    if telegram_id == ADMIN_USER_ID:
        return True

    db = await get_db()

    try:
        cur = await db.execute(
            "SELECT permissions, suspended FROM supervisors"
            " WHERE telegram_id = ?",
            (telegram_id,),
        )
        row = await cur.fetchone()
    finally:
        await db.close()

    if not row or row["suspended"]:
        return False

    try:
        perms = json.loads(row["permissions"] or "[]")
    except Exception:
        perms = []

    return (
        "all" in perms or "finance" in perms or kind in perms
    )


def render_sup_perms_kb(perms: list):
    """[NEW 39] لوحة تبديل صلاحيات المشرف بالأزرار."""
    b = InlineKeyboardBuilder()

    for perm, label in SUP_PERM_LABELS.items():
        mark = "✅" if perm in perms else "❌"
        b.button(text=f"{mark} {label}", callback_data=f"supperm:{perm}")

    b.button(text="💾 حفظ", callback_data="supsave")
    b.button(text="❌ إلغاء", callback_data="supcancel")
    b.adjust(1)
    return b.as_markup()


@dp.callback_query(F.data.startswith("supperm:"))
async def admin_supperm(cb: types.CallbackQuery, state: FSMContext):
    """[NEW 39] تبديل صلاحية في الحالة المؤقتة."""

    if cb.from_user.id != ADMIN_USER_ID:
        await cb.answer("للأدمن الرئيسي فقط.", show_alert=True)
        return

    perm = cb.data.split(":", 1)[1]

    if perm not in SUP_PERM_LABELS:
        await cb.answer("صلاحية غير معروفة.", show_alert=True)
        return

    data = await state.get_data()
    perms = list(data.get("perms") or [])

    if perm in perms:
        perms.remove(perm)
    else:
        perms.append(perm)

    if perm == "all":
        perms = ["all"] if "all" in perms else []
    else:
        perms = [p for p in perms if p != "all"]

    await state.update_data(perms=perms)
    await cb.answer()

    try:
        await cb.message.edit_reply_markup(
            reply_markup=render_sup_perms_kb(perms),
        )
    except Exception as exc:
        if "message is not modified" not in str(exc).lower():
            logger.warning("تعذر تحديث لوحة الصلاحيات: %s", exc)


@dp.callback_query(F.data == "supsave")
async def admin_supsave(cb: types.CallbackQuery, state: FSMContext):
    """[NEW 39] حفظ صلاحيات المشرف من لوحة الأزرار."""

    if cb.from_user.id != ADMIN_USER_ID:
        await cb.answer("للأدمن الرئيسي فقط.", show_alert=True)
        return

    data = await state.get_data()
    telegram_id = data.get("telegram_id")
    permissions = list(data.get("perms") or [])

    if not telegram_id or not permissions:
        await cb.answer(
            "اختر صلاحية واحدة على الأقل قبل الحفظ.",
            show_alert=True,
        )
        return

    if "all" in permissions:
        permissions = ["all"]

    db = await get_db()

    try:
        cur = await db.execute(
            "SELECT telegram_id FROM supervisors WHERE telegram_id = ?",
            (telegram_id,),
        )
        exists = await cur.fetchone()

        if exists:
            await db.execute(
                "UPDATE supervisors SET permissions = ?"
                " WHERE telegram_id = ?",
                (json.dumps(permissions, ensure_ascii=False), telegram_id),
            )
        else:
            await db.execute(
                """
                INSERT INTO supervisors
                (telegram_id, permissions, created_at)
                VALUES (?, ?, ?)
                """,
                (
                    telegram_id,
                    json.dumps(permissions, ensure_ascii=False),
                    now_iso(),
                ),
            )

        await db.commit()
    finally:
        await db.close()

    await state.clear()
    await audit(  # [NEW 22]
        cb.from_user.id, "supervisor_set",
        telegram_id, ",".join(permissions),
    )

    await cb.answer("تم الحفظ ✅", show_alert=True)

    await safe_edit(
        cb.message,
        "✅ تم إضافة/تحديث المشرف.\n\n"
        f"🆔 ID: <code>{telegram_id}</code>\n"
        f"🛡 الصلاحيات: {esc(', '.join(permissions))}",
        admin_supervisors_kb(),
    )


@dp.callback_query(F.data == "supcancel")
async def admin_supcancel(cb: types.CallbackQuery, state: FSMContext):

    if cb.from_user.id != ADMIN_USER_ID:
        await cb.answer("للأدمن الرئيسي فقط.", show_alert=True)
        return

    await state.clear()
    await cb.answer("تم الإلغاء.")
    await safe_edit(cb.message, "❌ تم الإلغاء.", admin_supervisors_kb())


@dp.callback_query(F.data == "admin_sup_list")
async def admin_sup_list(cb: types.CallbackQuery, state: FSMContext):

    if cb.from_user.id != ADMIN_USER_ID:
        await cb.answer("للأدمن الرئيسي فقط.", show_alert=True)
        return

    await state.clear()  # [FIX 2]

    db = await get_db()

    try:
        cur = await db.execute(
            "SELECT * FROM supervisors ORDER BY created_at DESC LIMIT 50"
        )
        rows = await cur.fetchall()

        cur = await db.execute("SELECT COUNT(*) AS c FROM supervisors")
        total = (await cur.fetchone())["c"]

        cur = await db.execute(
            "SELECT processed_by, MAX(processed_at) last_at"
            " FROM finance_requests WHERE processed_by > 0"
            " GROUP BY processed_by"
        )
        last_active = {
            str(r["processed_by"]): (r["last_at"] or "")[:10]
            for r in await cur.fetchall()
        }  # [ADM3-4]
    finally:
        await db.close()

    if not rows:
        await cb.answer()
        await safe_edit(
            cb.message, "📭 لا يوجد مشرفون.", back_kb("admin_supervisors"),
        )
        return

    lines = ["🛡 <b>قائمة المشرفين</b>\n"]

    for row in rows:
        try:
            perms = json.loads(row["permissions"] or "[]")
        except Exception:
            perms = []

        flag = " ⏸" if row["suspended"] else ""  # [NEW 40]
        quota = float(row["daily_quota"] or 0) if row["daily_quota"] else 0

        if quota > 0:  # [ADM2-3]
            flag += f" 💼{quota:g}"

        lines.append(
            f"👤 <code>{row['telegram_id']}</code>{flag}\n"
            f"🔐 {esc(', '.join(perms))}\n"
            f"🕐 آخر نشاط: {last_active.get(str(row['telegram_id']), '—')}"
        )  # [ADM3-4]

    if total > len(rows):  # [FIX 4]
        lines.append(f"ℹ️ يوجد {total - len(rows)} مشرفًا آخر غير معروض.")

    await cb.answer()
    await safe_edit(
        cb.message, "\n\n".join(lines), back_kb("admin_supervisors"),
    )


@dp.callback_query(F.data == "admin_sup_delete")
async def admin_sup_delete(cb: types.CallbackQuery, state: FSMContext):

    if cb.from_user.id != ADMIN_USER_ID:
        await cb.answer("للأدمن الرئيسي فقط.", show_alert=True)
        return

    await cb.answer()
    await state.clear()
    await state.set_state(AdminDeleteSupervisorFSM.telegram_id)

    await cb.message.answer("أرسل Telegram ID للمشرف الذي تريد حذفه:", reply_markup=back_kb("admin_supervisors"))


@dp.message(AdminDeleteSupervisorFSM.telegram_id)
async def admin_delete_supervisor_by_id(
    message: types.Message,
    state: FSMContext,
):

    if message.from_user.id != ADMIN_USER_ID:
        await state.clear()
        return

    try:
        telegram_id = int((message.text or "").strip())
    except Exception:
        await message.answer("❌ ID غير صالح.\n\nللإلغاء أرسل /cancel")
        return

    if telegram_id == ADMIN_USER_ID:
        await message.answer("❌ لا يمكن حذف الأدمن الرئيسي.")
        await state.clear()
        return

    db = await get_db()

    try:
        cur = await db.execute(
            "SELECT telegram_id FROM supervisors WHERE telegram_id = ?",
            (telegram_id,),
        )
        row = await cur.fetchone()

        if not row:
            await message.answer("❌ لم يتم العثور على المشرف.")
            return

        await db.execute(
            "DELETE FROM supervisors WHERE telegram_id = ?",
            (telegram_id,),
        )
        await db.commit()
    finally:
        await db.close()

    await audit(  # [NEW 22]
        message.from_user.id, "supervisor_delete", telegram_id
    )

    await message.answer(
        f"✅ تم حذف المشرف:\n<code>{telegram_id}</code>",
        reply_markup=admin_supervisors_kb(),
    )

    await state.clear()


# ============================================================
# ADMIN STATISTICS
# ============================================================

@dp.callback_query(F.data == "admin_statistics")
async def admin_statistics(cb: types.CallbackQuery, state: FSMContext):
    _last_admin_screen[cb.from_user.id] = "admin_statistics"  # [V11]

    if not await is_admin_or_supervisor(cb.from_user.id):
        await cb.answer("غير مصرّح.", show_alert=True)
        return

    await state.clear()  # [FIX 2]

    db = await get_db()

    try:
        cur = await db.execute("SELECT COUNT(*) AS c FROM users")
        users_count = (await cur.fetchone())["c"]

        cur = await db.execute(
            "SELECT COALESCE(SUM(balance), 0) AS total FROM users"
        )
        total_balance = (await cur.fetchone())["total"]

        cur = await db.execute(
            "SELECT COUNT(*) AS c FROM finance_requests"
            " WHERE status = 'pending'"
        )
        pending = (await cur.fetchone())["c"]

        cur = await db.execute(
            "SELECT COUNT(*) AS c FROM gift_codes WHERE used_by IS NULL"
        )
        unused_gifts = (await cur.fetchone())["c"]

        cur = await db.execute(
            "SELECT COUNT(*) AS c FROM users WHERE is_banned = 1"
        )
        banned = (await cur.fetchone())["c"]

        cur = await db.execute(
            "SELECT COUNT(*) AS c FROM payouts"
            " WHERE status IN ('pending', 'processing')"
        )
        pending_payouts = (await cur.fetchone())["c"]
    finally:
        await db.close()

    text = (
        "📈 <b>إحصائيات الإدارة</b>\n\n"
        f"👥 المستخدمون: {users_count}\n"
        f"🚫 المحظورون: {banned}\n"
        f"💰 إجمالي الأرصدة: {money(total_balance)}\n"
        f"📨 طلبات مالية معلقة: {pending}\n"
        f"🚀 مدفوعات معلقة: {pending_payouts}\n"
        f"🎁 أكواد غير مستخدمة: {unused_gifts}"
    )

    await cb.answer()
    await safe_edit(cb.message, text, back_kb("admin_panel"))


# ============================================================
# ADMIN REPORTS [NEW 14]
# ============================================================

def build_csv_file(
    base_name: str,
    headers: list,
    rows: list,
) -> BufferedInputFile:
    """
    بناء ملف CSV بترميز UTF-8 مع BOM
    حتى تظهر العربية بشكل صحيح في Excel.
    """
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(headers)

    for row in rows:
        writer.writerow(["" if v is None else v for v in row])

    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    data = buf.getvalue().encode("utf-8-sig")

    return BufferedInputFile(
        data,
        filename=f"{base_name}_{stamp}.csv",
    )


@dp.callback_query(F.data == "admin_reports")
async def admin_reports(cb: types.CallbackQuery, state: FSMContext):

    if not await is_admin_or_supervisor(cb.from_user.id, "reports"):
        await cb.answer("غير مصرّح.", show_alert=True)
        return

    await cb.answer()
    await state.clear()
    await safe_edit(
        cb.message,
        "📥 <b>التقارير</b>\n\nاختر التقرير المطلوب:",
        admin_reports_kb(
            show_weekly=await feat_on("weekly_now"),  # [AUDIT2]
        ),
    )


@dp.callback_query(F.data == "weekly_now")
async def weekly_now(cb: types.CallbackQuery, state: FSMContext):
    """[R6-PLUS10 E11] معاينة التقرير الأسبوعي فوراً دون انتظار الأحد."""

    if not await is_admin_or_supervisor(cb.from_user.id, "reports"):
        await cb.answer("غير مصرّح.", show_alert=True)
        return

    await cb.answer()
    await state.clear()

    start = (
        datetime.now(timezone.utc) - timedelta(days=7)
    ).strftime("%Y-%m-%d")

    db = await get_db()

    try:
        async def one(sql, params):
            cur = await db.execute(sql, params)
            return await cur.fetchone()

        row = await one(
            "SELECT COUNT(*) c, COALESCE(SUM(amount), 0) s"
            " FROM transactions WHERE type='deposit' AND created_at >= ?",
            (start,),
        )
        dep_n, dep_s = row["c"], float(row["s"])

        row = await one(
            "SELECT COUNT(*) c, COALESCE(SUM(amount), 0) s"
            " FROM transactions WHERE type='withdraw' AND created_at >= ?",
            (start,),
        )
        wd_n, wd_s = row["c"], float(row["s"])

        row = await one(
            "SELECT COUNT(*) c FROM users WHERE created_at >= ?",
            (start,),
        )
        new_users = row["c"]

        row = await one(
            "SELECT COUNT(*) c FROM support_tickets"
            " WHERE created_at >= ?",
            (start,),
        )
        tickets = row["c"]

        row = await one(
            "SELECT COALESCE(AVG(rating), 0) a FROM support_tickets"
            " WHERE rating IS NOT NULL",
            (),
        )
        rating = float(row["a"])
    finally:
        await db.close()

    retention_txt = await _retention_text(7)  # [E7]

    text = (
        f"👁 <b>معاينة التقرير الأسبوعي</b> (آخر 7 أيام)\n\n"
        f"💰 شحن: {dep_n} عملية = {money(dep_s)}\n"
        f"🏦 سحب: {wd_n} عملية = {money(wd_s)}\n"
        f"👥 مستخدمون جدد: {new_users}\n"
        f"💬 تذاكر: {tickets}\n"
        f"⭐ متوسط الرضا: {rating:.1f}\n\n"
        "─────────────\n"
        f"{retention_txt}"
    )

    await safe_edit(cb.message, text, back_kb("admin_reports"))


@dp.callback_query(F.data.startswith("report:"))
async def admin_report_send(cb: types.CallbackQuery, state: FSMContext):

    if not await is_admin_or_supervisor(cb.from_user.id, "reports"):
        await cb.answer("غير مصرّح.", show_alert=True)
        return

    kind = cb.data.split(":", 1)[1]

    if kind not in ("users", "transactions", "requests"):
        await cb.answer("تقرير غير معروف.", show_alert=True)
        return

    await state.clear()
    await cb.answer("جاري تحضير التقرير...")

    db = await get_db()

    try:
        if kind == "users":
            cur = await db.execute(
                """
                SELECT telegram_id, username, full_name,
                       site_username, balance, is_banned, created_at
                FROM users
                ORDER BY id
                LIMIT ?
                """,
                (REPORT_ROW_LIMIT,),
            )
            rows = await cur.fetchall()
            doc = build_csv_file(
                "users",
                [
                    "telegram_id", "username", "full_name",
                    "site_username", "balance", "is_banned", "created_at",
                ],
                [tuple(r) for r in rows],
            )
            caption = f"👥 تقرير المستخدمين ({len(rows)} سجل)"

        elif kind == "transactions":
            cur = await db.execute(
                """
                SELECT t.id, u.telegram_id, t.type, t.amount,
                       t.note, t.created_at
                FROM transactions t
                JOIN users u ON u.id = t.user_id
                ORDER BY t.id DESC
                LIMIT ?
                """,
                (REPORT_ROW_LIMIT,),
            )
            rows = await cur.fetchall()
            doc = build_csv_file(
                "transactions",
                ["id", "telegram_id", "type", "amount", "note", "created_at"],
                [tuple(r) for r in rows],
            )
            caption = f"💳 تقرير العمليات المالية ({len(rows)} سجل)"

        else:
            cur = await db.execute(
                """
                SELECT id, telegram_id, type, amount, status,
                       created_at, processed_at, processed_by
                FROM finance_requests
                ORDER BY id DESC
                LIMIT ?
                """,
                (REPORT_ROW_LIMIT,),
            )
            rows = await cur.fetchall()
            doc = build_csv_file(
                "requests",
                [
                    "id", "telegram_id", "type", "amount",
                    "status", "created_at", "processed_at", "processed_by",
                ],
                [tuple(r) for r in rows],
            )
            caption = f"📋 تقرير الطلبات ({len(rows)} سجل)"

    finally:
        await db.close()

    if len(rows) >= REPORT_ROW_LIMIT:
        caption += f"\n⚠️ تم تقييد التقرير بـ {REPORT_ROW_LIMIT} سجل."

    try:
        await cb.message.answer_document(doc, caption=caption)
    except Exception as exc:
        logger.warning("تعذر إرسال التقرير: %s", exc)


# ============================================================
# ADMIN BROADCAST [NEW 16]
# ============================================================

@dp.callback_query(F.data == "admin_broadcast")
async def admin_broadcast(cb: types.CallbackQuery, state: FSMContext):

    if cb.from_user.id != ADMIN_USER_ID:
        await cb.answer("للأدمن الرئيسي فقط.", show_alert=True)
        return

    await cb.answer()
    await state.clear()
    await state.set_state(AdminBroadcastFSM.message)

    await cb.message.answer(
        "📣 أرسل الرسالة التي تريد بثها لجميع المستخدمين\n"
        "(نص، صورة، أو أي محتوى مدعوم):"
    , reply_markup=back_kb("admin_panel"))


@dp.message(AdminBroadcastFSM.message)
async def admin_broadcast_message(
    message: types.Message,
    state: FSMContext,
):

    if message.from_user.id != ADMIN_USER_ID:
        await state.clear()
        return

    await state.update_data(
        broadcast_chat_id=message.chat.id,
        broadcast_message_id=message.message_id,
    )

    # [ADM2-1] اختيار الشريحة المستهدفة
    sb = InlineKeyboardBuilder()
    sb.button(text="👥 الكل", callback_data="bseg:all")
    sb.button(text="🔥 نشطوا اليوم", callback_data="bseg:active")
    sb.button(text="💰 رصيد ≥ حد معين", callback_data="bseg:bal")
    sb.button(text="🇸🇦 العربي فقط", callback_data="bseg:ar")
    sb.button(text="🇬🇧 English only", callback_data="bseg:en")
    sb.button(text="🇷🇺 Русский", callback_data="bseg:ru")  # [R6-PLUS3]
    sb.button(  # [R6-PLUS3]
        text="💤 الغائبون 14+ يوماً", callback_data="bseg:inactive",
    )
    sb.button(text="❌ إلغاء", callback_data="admin_broadcast_cancel")
    sb.adjust(1)

    await message.answer(
        "📩 تم استلام الرسالة أعلاه ⬆️\n\n"
        "<b>من تريد بثها إليهم؟</b>",
        reply_markup=sb.as_markup(),
    )


@dp.callback_query(F.data == "admin_broadcast_cancel")
async def admin_broadcast_cancel(cb: types.CallbackQuery, state: FSMContext):

    if cb.from_user.id != ADMIN_USER_ID:
        await cb.answer("للأدمن الرئيسي فقط.", show_alert=True)
        return

    await state.clear()
    await cb.answer("تم إلغاء البث.")

    await safe_edit(cb.message, "❌ تم إلغاء البث.", back_kb("admin_panel"))


@dp.callback_query(F.data == "admin_broadcast_confirm")
async def admin_broadcast_confirm(cb: types.CallbackQuery, state: FSMContext):

    if cb.from_user.id != ADMIN_USER_ID:
        await cb.answer("للأدمن الرئيسي فقط.", show_alert=True)
        return

    if not await pin_gate(cb):  # [ADM3-1]
        return

    data = await state.get_data()
    chat_id = data.get("broadcast_chat_id")
    message_id = data.get("broadcast_message_id")

    if not chat_id or not message_id:
        await cb.answer("لا توجد رسالة محفوظة للبث.", show_alert=True)
        return

    await state.clear()
    await cb.answer()

    segment = data.get("broadcast_segment") or "all"  # [ADM2-1]
    min_balance = data.get("broadcast_min_balance")

    targets = await broadcast_targets(segment, min_balance)

    status_message = await cb.message.answer(
        f"📣 جاري البث ({_SEG_LABELS.get(segment, 'الكل')}) إلى "
        f"{len(targets)} مستخدم..."
    )

    sent, failed = await do_broadcast_copy(
        status_message, chat_id, message_id, targets,
    )
    total = len(targets)

    await status_message.edit_text(
        "✅ <b>انتهى البث</b>\n\n"
        f"📬 وصلت الرسالة: {sent}\n"
        f"🚫 فشل الإرسال: {failed}\n"
        f"👥 إجمالي المستهدفين: {total}"
    )

    await audit(  # [NEW 22]
        cb.from_user.id, "broadcast",
        f"targets={total}", f"sent={sent};failed={failed}",
    )


# ============================================================
# ADMIN TEXTS [NEW 17]
# ============================================================

@dp.callback_query(F.data == "admin_texts")
async def admin_texts(cb: types.CallbackQuery, state: FSMContext):

    if cb.from_user.id != ADMIN_USER_ID:
        await cb.answer("للأدمن الرئيسي فقط.", show_alert=True)
        return

    await cb.answer()
    await state.clear()
    await safe_edit(
        cb.message,
        "📝 <b>إدارة النصوص</b>\n\nاختر النص الذي تريد تعديله:",
        admin_texts_kb(),
    )


@dp.callback_query(F.data.startswith("admin_text_edit:"))
async def admin_text_edit(cb: types.CallbackQuery, state: FSMContext):

    if cb.from_user.id != ADMIN_USER_ID:
        await cb.answer("للأدمن الرئيسي فقط.", show_alert=True)
        return

    key = cb.data.split(":", 1)[1]

    if key not in BOT_TEXTS:
        await cb.answer("نص غير معروف.", show_alert=True)
        return

    await cb.answer()
    await state.clear()
    await state.update_data(text_key=key)
    await state.set_state(AdminEditTextFSM.value)

    title = BOT_TEXTS[key]
    current = await get_text(key) or ""

    if current:
        preview = current[:300] + ("..." if len(current) > 300 else "")
        preview_text = f"المحتوى الحالي:\n{esc(preview)}"
    else:
        preview_text = "لا يوجد محتوى حالياً."

    await cb.message.answer(
        f"✏️ <b>{title}</b>\n\n"
        f"{preview_text}\n\n"
        "أرسل النص الجديد.\n"
        "لحذف النص أرسل <code>/clear</code>\n"
        "للإلغاء أرسل <code>/cancel</code>"
    , reply_markup=back_kb("admin_settings_menu"))


@dp.message(AdminEditTextFSM.value)
async def admin_text_save(message: types.Message, state: FSMContext):

    if message.from_user.id != ADMIN_USER_ID:
        await state.clear()
        return

    data = await state.get_data()
    key = data.get("text_key")

    if key not in BOT_TEXTS:
        await state.clear()
        return

    raw = (message.text or "").strip()

    if not raw:
        await message.answer("❌ أرسل نصًا صالحًا.")
        return

    if raw.startswith("/clear"):
        await set_text(key, "")
        await state.clear()
        await message.answer(f"🗑 تم حذف محتوى: {BOT_TEXTS[key]}")
        return

    if raw.startswith("/"):
        await message.answer(
            "ℹ️ لإلغاء أرسل /cancel\nولحذف النص أرسل /clear"
        )
        return

    await set_text(key, raw)
    await state.clear()

    await audit(  # [NEW 22]
        message.from_user.id, "text_edit", key, f"len={len(raw)}",
    )

    await message.answer(
        f"✅ تم حفظ النص: <b>{BOT_TEXTS[key]}</b>\n\n"
        "أصبح متاحاً الآن للمستخدمين من زر «ℹ️ معلومات».",
        reply_markup=back_kb("admin_panel"),
    )


# ============================================================
# AUDIT VIEW + CHART + COMMISSION + LIMITS + REFERRAL
# [NEW 22/26/27/29/34]
# ============================================================

@dp.callback_query(F.data == "admin_audit")
async def admin_audit_view(cb: types.CallbackQuery, state: FSMContext):

    if not await is_admin_or_supervisor(cb.from_user.id):
        await cb.answer("غير مصرّح.", show_alert=True)
        return

    await state.clear()

    db = await get_db()

    try:
        cur = await db.execute(
            """
            SELECT admin_id, action, target, details, created_at
            FROM admin_audit
            ORDER BY id DESC
            LIMIT 30
            """
        )
        rows = await cur.fetchall()
    finally:
        await db.close()

    if not rows:
        text = "📭 سجل التدقيق فارغ."
    else:
        lines = ["📜 <b>آخر العمليات الإدارية</b>\n"]

        for row in rows:
            lines.append(
                f"🛠 <code>{row['admin_id']}</code> | "
                f"{esc(row['action'])} | {esc(row['target'])}\n"
                f"{esc(row['details'])}\n"
                f"🕐 {esc(row['created_at'])}"
            )

        text = "\n\n".join(lines)

    await cb.answer()
    await safe_edit(cb.message, text, back_kb("admin_panel"))


@dp.callback_query(F.data == "admin_chart")
async def admin_chart(cb: types.CallbackQuery, state: FSMContext):
    """[NEW 34] رسم بياني لنشاط آخر 14 يوماً."""

    if not await is_admin_or_supervisor(cb.from_user.id):
        await cb.answer("غير مصرّح.", show_alert=True)
        return

    await state.clear()
    await cb.answer("جاري بناء الرسم البياني...")

    days = 14
    today = datetime.now(timezone.utc).date()
    day_list = [
        (today - timedelta(days=i)).isoformat()
        for i in range(days - 1, -1, -1)
    ]

    db = await get_db()

    try:
        cur = await db.execute(
            """
            SELECT substr(created_at, 1, 10) AS day, type,
                   SUM(amount) AS total
            FROM transactions
            WHERE type IN ('deposit', 'withdraw')
              AND created_at >= ?
            GROUP BY day, type
            """,
            (day_list[0],),
        )
        tx_rows = await cur.fetchall()

        cur = await db.execute(
            """
            SELECT substr(created_at, 1, 10) AS day,
                   COUNT(*) AS c
            FROM users
            WHERE created_at >= ?
            GROUP BY day
            """,
            (day_list[0],),
        )
        user_rows = await cur.fetchall()
    finally:
        await db.close()

    deposits = {d: 0.0 for d in day_list}
    withdrawals = {d: 0.0 for d in day_list}
    new_users = {d: 0 for d in day_list}

    for row in tx_rows:
        if row["day"] in deposits:
            if row["type"] == "deposit":
                deposits[row["day"]] = float(row["total"] or 0)
            else:
                withdrawals[row["day"]] = float(row["total"] or 0)

    for row in user_rows:
        if row["day"] in new_users:
            new_users[row["day"]] = row["c"]

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        await cb.message.answer(
            "⚠️ مكتبة matplotlib غير مثبتة — لا يمكن إنشاء الرسم البياني.\n"
            "ثبّتها: pip install matplotlib"
        )
        return

    fig, (ax1, ax2) = plt.subplots(
        2, 1, figsize=(10, 7),
        gridspec_kw={"height_ratios": [2, 1]},
    )

    x = range(days)
    ax1.plot(
        x, [deposits[d] for d in day_list],
        marker="o", color="#2e7d32", label="Deposits",
    )
    ax1.plot(
        x, [withdrawals[d] for d in day_list],
        marker="s", color="#c62828", label="Withdrawals",
    )
    ax1.set_title("Financial activity - last 14 days (UTC)")
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    ax2.bar(x, [new_users[d] for d in day_list], color="#1565c0")
    ax2.set_title("New users per day")
    ax2.grid(True, alpha=0.3)

    step = max(1, days // 7)
    tick_pos = list(x)[::step]
    tick_labels = [day_list[i][5:] for i in tick_pos]
    for ax in (ax1, ax2):
        ax.set_xticks(tick_pos)
        ax.set_xticklabels(tick_labels)

    plt.tight_layout()

    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=110)
    plt.close(fig)
    buf.seek(0)

    photo = BufferedInputFile(buf.getvalue(), filename="activity.png")

    try:
        await cb.message.answer_photo(
            photo,
            caption=(
                "📊 نشاط آخر 14 يوماً\n"
                f"💰 شحن: {money(sum(deposits.values()))}\n"
                f"🏦 سحب: {money(sum(withdrawals.values()))}\n"
                f"👥 مستخدمون جدد: {sum(new_users.values())}"
            ),
        )
    except Exception as exc:
        logger.warning("تعذر إرسال الرسم البياني: %s", exc)


@dp.callback_query(F.data == "admin_commission")
async def admin_commission(cb: types.CallbackQuery, state: FSMContext):
    """[NEW 26] ضبط نسبة عمولة الشحن."""

    if cb.from_user.id != ADMIN_USER_ID:
        await cb.answer("للأدمن الرئيسي فقط.", show_alert=True)
        return

    await cb.answer()
    await state.clear()
    await state.set_state(AdminCommissionFSM.value)

    current = await get_float_setting("commission_percent", 0.0)

    await cb.message.answer(
        "٪ <b>عمولة الشحن</b>\n\n"
        f"النسبة الحالية: <b>{current:g}%</b>\n\n"
        "أرسل النسبة الجديدة (0 إلى 50):\n"
        "مثال: <code>5</code> أو <code>2.5</code>\n"
        "للإلغاء أرسل /cancel"
    , reply_markup=back_kb("admin_settings_menu"))


@dp.message(AdminCommissionFSM.value)
async def admin_commission_save(message: types.Message, state: FSMContext):

    if message.from_user.id != ADMIN_USER_ID:
        await state.clear()
        return

    try:
        pct = float((message.text or "").strip().replace(",", "."))
        if not (0 <= pct <= 50) or not math.isfinite(pct):
            raise ValueError
    except Exception:
        await message.answer(
            "❌ أرسل نسبة صحيحة بين 0 و 50.\n\nللإلغاء أرسل /cancel"
        )
        return

    await set_setting("commission_percent", str(round(pct, 2)))
    await state.clear()

    await audit(message.from_user.id, "commission_set", f"{pct:g}%")

    await message.answer(
        f"✅ تم ضبط عمولة الشحن على <b>{pct:g}%</b>.",
        reply_markup=back_kb("admin_panel"),
    )


async def render_limits_text():
    """[NEW 27/41] نص عرض الحدود والسقوف الحالية."""
    dl = await amount_limits("deposit")
    wl = await amount_limits("withdraw")
    cap_user = await get_float_setting("daily_withdraw_per_user", 0.0)
    cap_total = await get_float_setting("daily_withdraw_total", 0.0)

    cap_user_txt = money(cap_user) if cap_user > 0 else "معطّل"
    cap_total_txt = money(cap_total) if cap_total > 0 else "معطّل"

    return (
        "⚙️ <b>الحدود والسقوف</b>\n\n"
        f"💰 الشحن: من {money(dl['min'])} إلى {money(dl['max'])}\n"
        f"🏦 السحب: من {money(wl['min'])} إلى {money(wl['max'])}\n"
        f"🛑 سقف سحب يومي/مستخدم: {cap_user_txt}\n"
        f"🛑 سقف سحب يومي/إجمالي: {cap_total_txt}\n\n"
        "اختر الحد الذي تريد تعديله:"
    )


@dp.callback_query(F.data == "admin_limits")
async def admin_limits(cb: types.CallbackQuery, state: FSMContext):
    """[NEW 27] إدارة حدود الشحن والسحب."""

    if cb.from_user.id != ADMIN_USER_ID:
        await cb.answer("للأدمن الرئيسي فقط.", show_alert=True)
        return

    await cb.answer()
    await state.clear()

    text = await render_limits_text()
    await safe_edit(cb.message, text, admin_limits_kb())


@dp.callback_query(F.data.startswith("lim:"))
async def admin_limits_pick(cb: types.CallbackQuery, state: FSMContext):

    if cb.from_user.id != ADMIN_USER_ID:
        await cb.answer("للأدمن الرئيسي فقط.", show_alert=True)
        return

    field = cb.data.split(":", 1)[1]

    if field not in LIM_FIELDS:
        await cb.answer("حد غير معروف.", show_alert=True)
        return

    await cb.answer()
    await state.clear()
    await state.update_data(limit_field=field)
    await state.set_state(AdminLimitsFSM.value)

    await cb.message.answer(
        f"أرسل القيمة الجديدة لـ <code>{field}</code>\n"
        f"(بين 0.01 و {MAX_AMOUNT})\n\nللإلغاء أرسل /cancel"
    , reply_markup=back_kb("admin_limits"))


@dp.message(AdminLimitsFSM.value)
async def admin_limits_save(message: types.Message, state: FSMContext):

    if message.from_user.id != ADMIN_USER_ID:
        await state.clear()
        return

    data = await state.get_data()
    field = data.get("limit_field")

    if field not in LIM_FIELDS:
        await state.clear()
        return

    value = parse_amount(message.text)

    # [NEW 41] السقوف اليومية تقبل 0 (تعطيل)
    if value is None and field not in DEFAULT_LIMITS:
        try:
            if float((message.text or "").strip()) == 0:
                value = 0.0
        except Exception:
            value = None

    if value is None:
        await message.answer(
            f"❌ أرسل قيمة صحيحة (0 لتعطيل السقف،"
            f" وإلا بين 0.01 و {MAX_AMOUNT})."
            "\n\nللإلغاء أرسل /cancel"
        )
        return

    await set_setting(field, str(value))
    await state.clear()

    await audit(  # [NEW 22]
        message.from_user.id, "limits_set", field, str(value)
    )

    text = await render_limits_text()

    await message.answer(
        f"✅ تم تحديث {field}.\n\n{text}",
        reply_markup=admin_limits_kb(),
    )


@dp.callback_query(F.data == "admin_refbonus")
async def admin_refbonus(cb: types.CallbackQuery, state: FSMContext):
    """[NEW 29] ضبط مكافأة الإحالة."""

    if cb.from_user.id != ADMIN_USER_ID:
        await cb.answer("للأدمن الرئيسي فقط.", show_alert=True)
        return

    await cb.answer()
    await state.clear()
    await state.set_state(AdminRefBonusFSM.value)

    current = await get_float_setting("referral_bonus", 0.0)

    await cb.message.answer(
        "🤝 <b>مكافأة الإحالة</b>\n\n"
        f"المكافأة الحالية: <b>{money(current)}</b>\n\n"
        "أرسل المبلغ الذي يحصل عليه الداعي عند انضمام صديق جديد.\n"
        "أرسل <code>0</code> لتعطيل المكافأة.\n"
        "للإلغاء أرسل /cancel"
    , reply_markup=back_kb("admin_refbonus"))


@dp.message(AdminRefBonusFSM.value)
async def admin_refbonus_save(message: types.Message, state: FSMContext):

    if message.from_user.id != ADMIN_USER_ID:
        await state.clear()
        return

    value = parse_amount(message.text, allow_negative=False)

    if value is None:
        try:  # السماح بالصفر للتعطيل
            if float((message.text or "").strip()) == 0:
                value = 0.0
        except Exception:
            value = None

    if value is None:
        await message.answer(
            f"❌ أرسل مبلغًا صحيحًا (0 إلى {MAX_AMOUNT})."
            "\n\nللإلغاء أرسل /cancel"
        )
        return

    await set_setting("referral_bonus", str(value))
    await state.clear()

    await audit(  # [NEW 22]
        message.from_user.id, "referral_bonus_set", money(value)
    )

    note = "معطلة." if value == 0 else f"{money(value)} لكل صديق جديد."

    await message.answer(
        f"✅ تم ضبط مكافأة الإحالة: {note}",
        reply_markup=back_kb("admin_panel"),
    )


# ============================================================
# PERIODIC TASKS [NEW 23 / NEW 25 / NEW 28]
# ============================================================

async def expire_old_requests():
    """[NEW 25] إنهاء الطلبات المعلقة الأقدم من 24 ساعة مع إشعار أصحابها."""
    cutoff = (
        datetime.now(timezone.utc) - timedelta(hours=REQUEST_EXPIRY_HOURS)
    ).isoformat(timespec="seconds")

    db = await get_db()

    try:
        cur = await db.execute(
            """
            SELECT id, telegram_id, type, note, amount
            FROM finance_requests
            WHERE status = 'pending'
              AND created_at < ?
            """,
            (cutoff,),
        )
        rows = await cur.fetchall()

        if not rows:
            return 0

        for row in rows:
            await db.execute(
                """
                UPDATE finance_requests
                SET status = 'expired',
                    processed_at = ?
                WHERE id = ?
                  AND status = 'pending'
                """,
                (now_iso(), row["id"]),
            )

            # [R6-PLUS5] إعادة رصيد السحب المحتجز عند الانتهاء
            if row["type"] == "withdraw" and \
                    "held=1" in (row["note"] or ""):
                cur_u = await db.execute(
                    "SELECT id FROM users WHERE telegram_id = ?",
                    (row["telegram_id"],),
                )
                urow = await cur_u.fetchone()

                if urow:
                    amt = float(row["amount"])

                    await db.execute(
                        "UPDATE users SET balance = balance + ?"
                        " WHERE id = ?",
                        (amt, urow["id"]),
                    )
                    await db.execute(
                        "INSERT INTO transactions"
                        " (user_id, type, amount, note, created_at)"
                        " VALUES (?, 'wd_refund', ?, ?, ?)",
                        (urow["id"], amt, f"request={row['id']}",
                         now_iso()),
                    )

        await db.commit()
    finally:
        await db.close()

    for row in rows:
        try:
            await bot.send_message(
                row["telegram_id"],
                f"⌛ انتهت صلاحية طلبك المالي #{row['id']}"
                " ولم تتم معالجته.\n"
                "يمكنك إعادة إرسال طلب جديد في أي وقت.",
            )
        except Exception:
            pass

    return len(rows)


async def auto_backup_if_due():
    """[NEW 23] نسخة احتياطية يومية من قاعدة البيانات إلى خاص الأدمن."""
    last = await get_setting("last_backup_at") or ""
    now = datetime.now(timezone.utc)

    if last:
        try:
            if (now - datetime.fromisoformat(last)).total_seconds() < 86400:
                return False
        except ValueError:
            pass

    backup_path = DB_PATH + ".backup"

    src = sqlite3.connect(DB_PATH)
    dst = sqlite3.connect(backup_path)
    with dst:
        src.backup(dst)
    dst.close()
    src.close()

    with open(backup_path, "rb") as fh:
        doc = BufferedInputFile(
            fh.read(),
            filename=f"backup_{now:%Y%m%d_%H%M%S}.db",
        )

    try:
        await bot.send_document(
            ADMIN_USER_ID,
            doc,
            caption="🗄 نسخة احتياطية تلقائية يومية",
        )
    except Exception as exc:
        logger.warning("تعذر إرسال النسخة الاحتياطية: %s", exc)
        return False

    # [R6-PLUS2] نسخة إضافية لغرفة المراقبة (حماية من فقدان الجهاز)
    mirror_chat = (await get_setting("mirror_chat_id") or "").strip()

    if mirror_chat.lstrip("-").isdigit() and int(mirror_chat) != ADMIN_USER_ID:
        try:
            with open(backup_path, "rb") as fh2:
                doc2 = BufferedInputFile(
                    fh2.read(),
                    filename=f"backup_{now:%Y%m%d_%H%M%S}.db",
                )
            await bot.send_document(
                int(mirror_chat),
                doc2,
                caption="🗄 نسخة احتياطية (نسخة ثانية)",
            )
        except Exception:
            pass

    await set_setting("last_backup_at", now.isoformat(timespec="seconds"))
    return True


async def send_daily_summary_if_due():
    """[NEW 28] ملخص يومي تلقائي يُرسل للأدمن مرة واحدة كل يوم."""
    if not await feat_on("daily_summary"):  # [R6-PLUS3]
        return False

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    if (await get_setting("last_summary_date") or "") == today:
        return False

    like = f"{today}%"

    db = await get_db()

    try:
        cur = await db.execute(
            "SELECT COUNT(*) AS c FROM users WHERE created_at LIKE ?",
            (like,),
        )
        new_users = (await cur.fetchone())["c"]

        cur = await db.execute(
            "SELECT COUNT(*) AS c, COALESCE(SUM(amount), 0) AS total"
            " FROM transactions WHERE type='deposit' AND created_at LIKE ?",
            (like,),
        )
        row = await cur.fetchone()
        dep_count, dep_total = row["c"], float(row["total"])

        cur = await db.execute(
            "SELECT COUNT(*) AS c, COALESCE(SUM(amount), 0) AS total"
            " FROM transactions WHERE type='withdraw' AND created_at LIKE ?",
            (like,),
        )
        row = await cur.fetchone()
        wd_count, wd_total = row["c"], float(row["total"])

        cur = await db.execute(
            "SELECT COUNT(*) AS c FROM finance_requests"
            " WHERE status = 'pending'",
        )
        pending = (await cur.fetchone())["c"]

        cur = await db.execute(
            "SELECT COUNT(*) AS c, COALESCE(SUM(amount), 0) AS total"
            " FROM transactions WHERE type='gift' AND created_at LIKE ?",
            (like,),
        )
        row = await cur.fetchone()
        gift_count, gift_total = row["c"], float(row["total"])
    finally:
        await db.close()

    # [R6-PLUS2] تفصيل شحن اليوم بحسب طريقة الدفع
    db_m = await get_db()

    try:
        cur_m = await db_m.execute(
            "SELECT note FROM finance_requests WHERE type = 'deposit'"
            " AND status = 'approved' AND processed_at LIKE ?",
            (like,),
        )
        mrows = await cur_m.fetchall()
    finally:
        await db_m.close()

    by_method = {}

    for r in mrows:
        m = "أخرى"

        if "method=" in (r["note"] or ""):
            for part in r["note"].split(";"):
                if part.startswith("method="):
                    m = part[7:]

        by_method[m] = by_method.get(m, 0) + 1

    method_lines = "".join(
        f"\n   • {esc(k)}: {v}"
        for k, v in sorted(by_method.items(), key=lambda x: -x[1])
    )

    text = (
        f"📅 <b>الملخص اليومي</b> — {today}\n\n"
        f"👥 مستخدمون جدد: {new_users}\n"
        f"💰 عمليات شحن: {dep_count} بقيمة {money(dep_total)}"
        f"{method_lines}\n"
        f"🏦 عمليات سحب: {wd_count} بقيمة {money(wd_total)}\n"
        f"🎁 أكواد مستخدمة: {gift_count} بقيمة {money(gift_total)}\n"
        f"📨 طلبات معلقة الآن: {pending}"
    )

    # [R6-PLUS3] متوسط تقييم السحب لآخر 24 ساعة
    db_r = await get_db()

    try:
        cur_r = await db_r.execute(
            "SELECT COALESCE(AVG(stars), 0) AS a, COUNT(*) AS c"
            " FROM payout_ratings WHERE created_at LIKE ?",
            (f"{today}%",),
        )
        rate_row = await cur_r.fetchone()
    finally:
        await db_r.close()

    if rate_row["c"]:
        text += (
            f"\n⭐ تقييم السحب اليوم: {rate_row['a']:.1f}/5"
            f" ({rate_row['c']})"
        )

    try:
        await bot.send_message(ADMIN_USER_ID, text)
    except Exception as exc:
        logger.warning("تعذر إرسال الملخص اليومي: %s", exc)
        return False

    await set_setting("last_summary_date", today)
    return True


def _chp_kind_label(kind: str) -> str:
    """[R6-CH] تسمية نوع النشر."""
    return {
        "announcement": "📣 آخر إعلان فعّال",
        "custom": "📝 نص مخصص",
        "daily_report": "📊 تقرير يومي",
    }.get(kind, kind)


_CHP_URL_RE = re.compile(
    r"^(?:https?://)?(?:www\.)?(?:t\.me|telegram\.me)/(.+)$", re.I,
)
_CHP_NAME_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_]{2,64}$")


def _chp_normalize(raw: str):
    """[CHPOST-5.16.3] تطبيع أي صيغة يرسلها الأدمن إلى (نوع، قيمة).

    الأنواع: num (رقمي صالح) / user (@اسم عام) / invite (رابط دعوة
    خاص لا يكفي للعنونة — يلزم الرقم) / raw (كما هو) / empty.
    """
    s = (raw or "").strip()

    # إزالة علامات ترقيم/اقتباس ملتصقة وأحرف غير مرئية
    s = s.strip("«»\"'`.,؛")
    s = re.sub(r"[\u200b-\u200f\u202a-\u202e\ufeff]", "", s)

    if not s:
        return "empty", ""

    if s.lstrip("-").isdigit():
        return "num", int(s)

    m = _CHP_URL_RE.match(s)

    if m:
        rest = m.group(1).strip().rstrip("/")

        if rest.startswith("+") or rest.lower().startswith("joinchat/"):
            return "invite", rest

        cm = re.match(r"^c/(\d+)(?:/\d+)?/?$", rest)

        if cm:  # t.me/c/1234567/2 → الرقم -1001234567
            return "num", int("-100" + cm.group(1))

        name = rest.split("/", 1)[0]  # t.me/name/25 → الاسم فقط

        if _CHP_NAME_RE.match(name):
            return "user", "@" + name

        return "invite", rest

    if s.startswith("@"):
        return "user", s

    if _CHP_NAME_RE.match(s):
        return "user", "@" + s

    return "raw", s


async def _chp_target(chat_id: str):
    """[R6-CH] تحويل معرف القناة إلى هدف إرسال صالح — أو None."""
    kind, val = _chp_normalize(chat_id)

    if kind in ("num", "user"):
        return val

    return None  # raw/invite/empty غير قابلة للعنونة



async def _chp_ann_photo():
    """[R6-PLUS2] file_id صورة آخر إعلان فعّال ('' إن لا صورة)."""
    db = await get_db()

    try:
        cur = await db.execute(
            "SELECT photo_file_id FROM announcements"
            " WHERE expires_at > ? AND photo_file_id != ''"
            " ORDER BY id DESC LIMIT 1",
            (now_iso(),),
        )
        row = await cur.fetchone()
        return row["photo_file_id"] if row else ""
    finally:
        await db.close()


async def _send_chp(target: int, text: str, photo: str = ""):
    """[R6-PLUS2] إرسال منشور القناة: صورة + نص أو نص فقط."""
    if photo:
        try:
            await bot.send_photo(target, photo=photo, caption=text[:1024])
            return True
        except Exception:
            pass

    await bot.send_message(target, text)
    return True


async def _chp_text(kind: str, custom_text: str) -> str:
    """[R6-CH] بناء نص المنشور بحسب النوع."""
    if kind == "custom":
        return custom_text or ""

    if kind == "daily_report":
        db = await get_db()

        try:
            today = now_iso()[:10]
            cur = await db.execute(
                "SELECT COALESCE(SUM(amount), 0) AS s, COUNT(*) AS c"
                " FROM transactions WHERE type = 'deposit'"
                " AND created_at LIKE ?",
                (today + "%",),
            )
            dep = await cur.fetchone()
            cur = await db.execute(
                "SELECT COALESCE(SUM(amount), 0) AS s, COUNT(*) AS c"
                " FROM transactions WHERE type = 'withdraw'"
                " AND created_at LIKE ?",
                (today + "%",),
            )
            wd = await cur.fetchone()
            cur = await db.execute(
                "SELECT COUNT(*) AS c FROM finance_requests"
                " WHERE status = 'pending'"
            )
            pend = (await cur.fetchone())["c"]
        finally:
            await db.close()

        return (
            "📊 <b>التقرير اليومي</b>\n\n"
            f"📥 الشحن: {money(dep['s'])} ({dep['c']})\n"
            f"📤 السحب: {money(wd['s'])} ({wd['c']})\n"
            f"🕓 طلبات معلقة: {pend}"
        )

    # announcement — آخر إعلان فعّال
    db = await get_db()

    try:
        cur = await db.execute(
            "SELECT text FROM announcements WHERE expires_at > ?"
            " ORDER BY id DESC LIMIT 1",
            (now_iso(),),
        )
        row = await cur.fetchone()
    finally:
        await db.close()

    if row:
        return f"🍀 <b>عرضنا الحالي:</b>\n\n{row['text']}"

    return ""


async def channel_posts_if_due():
    """[R6-CH] النشر المجدول الدوري على القناة/المجموعات المعيّنة."""
    db = await get_db()

    try:
        cur = await db.execute(
            "SELECT * FROM channel_posts WHERE enabled = 1"
        )
        rows = await cur.fetchall()
    finally:
        await db.close()

    now = datetime.now(timezone.utc)

    for row in rows:
        due = False

        if row["interval_hours"] and row["interval_hours"] > 0:
            if not row["last_sent"]:
                due = True
            else:
                try:
                    last_dt = datetime.fromisoformat(row["last_sent"])
                    due = (now - last_dt).total_seconds() >= (
                        row["interval_hours"] * 3600
                    )
                except (ValueError, TypeError):
                    due = True
        elif row["at_time"]:
            hhmm = now.strftime("%H:%M")
            due = bool(
                hhmm >= row["at_time"]
                and (row["last_sent"] or "")[:10] != now_iso()[:10]
            )

        if not due:
            continue

        text = await _chp_text(row["kind"], row["custom_text"])

        if not text:
            continue

        target = await _chp_target(row["chat_id"])

        photo = (
            await _chp_ann_photo()
            if row["kind"] == "announcement" else ""
        )  # [R6-PLUS2]

        try:
            await _send_chp(target, text, photo)
        except Exception as exc:
            logger.warning(
                "فشل النشر المجدول إلى %s: %s", row["chat_id"], exc,
            )
            continue

        db2 = await get_db()

        try:
            await db2.execute(
                "UPDATE channel_posts SET last_sent = ? WHERE id = ?",
                (now_iso(), row["id"]),
            )
            await db2.commit()
        finally:
            await db2.close()


async def stale_requests_if_due():
    """[R6-PLUS2] تذكير متكرر بالطلبات المعلقة الطويلة."""
    if not await feat_on("stale_alerts"):  # [R6-PLUS3]
        return

    hours = await get_float_setting("pending_alert_hours", 6.0)

    if hours <= 0:
        return

    now = datetime.now(timezone.utc)
    cutoff = (now - timedelta(hours=hours)).isoformat(timespec="seconds")
    rem_cut = (now - timedelta(hours=12)).isoformat(timespec="seconds")

    db = await get_db()

    try:
        cur = await db.execute(
            "SELECT id, telegram_id, type, amount, created_at"
            " FROM finance_requests WHERE status = 'pending'"
            " AND created_at <= ? AND COALESCE(remind_at, '') <= ?",
            (cutoff, rem_cut),
        )
        rows = await cur.fetchall()

        for row in rows:
            try:
                old_dt = datetime.fromisoformat(row["created_at"])
                hours_old = int((now - old_dt).total_seconds() // 3600)
            except (ValueError, TypeError):
                hours_old = hours

            try:
                icon = "📥" if row["type"] == "deposit" else "🏦"

                await notify_finance_staff(
                    "⏰ <b>طلب معلق منذ مدة طويلة</b>\n\n"
                    f"🆔 #{row['id']} | {icon} {row['type']}\n"
                    f"💵 {money(row['amount'])} | "
                    f"👤 <code>{row['telegram_id']}</code>\n"
                    f"🕐 عمر الطلب: ~{hours_old} ساعة",
                    row["id"],
                )
            except Exception:
                pass

            await db.execute(
                "UPDATE finance_requests SET remind_at = ? WHERE id = ?",
                (now_iso(), row["id"]),
            )

            # [R6-PLUS6] U24: طمأنة صاحب الطلب المعلق
            try:
                await bot.send_message(
                    row["telegram_id"],
                    r6t(
                        await user_lang(row["telegram_id"]),
                        "pending_reassure",
                    ).format(rid=row["id"]),
                )
            except Exception:
                pass

        await db.commit()
    finally:
        await db.close()


async def winback_if_due():
    """[R6-PLUS2] رسالة استرجاع لمن غاب عن الشحن مدة طويلة."""
    _old = (await get_setting("winback_enabled") or "0") == "1"

    if not (_old or await feat_on("winback")):  # [R6-PLUS3]
        return

    days = await get_float_setting("winback_days", 14.0)

    if days <= 0:
        return

    cutoff = (
        datetime.now(timezone.utc) - timedelta(days=days)
    ).isoformat(timespec="seconds")

    db = await get_db()

    try:
        cur = await db.execute(
            "SELECT telegram_id, full_name FROM users"
            " WHERE created_at <= ? AND COALESCE(last_winback, '') = ''"
            " AND is_banned = 0 AND NOT EXISTS ("
            " SELECT 1 FROM transactions t WHERE t.user_id = users.id"
            " AND t.type = 'deposit' AND t.created_at > ?)"
            " LIMIT 40",
            (cutoff, cutoff),
        )
        rows = await cur.fetchall()
    finally:
        await db.close()

    msg = (await get_setting("winback_msg") or "").strip() or (
        "نشتاق لك! 🎁\n"
        "لديك خصم عمولة على طلب الشحن القادم — عود الآن!"
    )

    for row in rows:
        # [R6-PLUS6] مراقبة انسداد البوت لدى المستخدم (D8)
        await notify_user_guarded(row["telegram_id"], msg)

        db2 = await get_db()

        try:
            await db2.execute(
                "UPDATE users SET last_winback = ? WHERE telegram_id = ?",
                (now_iso(), row["telegram_id"]),
            )
            await db2.commit()
        finally:
            await db2.close()


async def anniv_gifts_if_due():
    """[R6-PLUS5] هدية نقاط عند ذكرى الانضمام (شهر + كل سنة)."""
    if not await feat_on("anniv_gift"):
        return

    today = f"{datetime.now(timezone.utc):%Y-%m-%d}"

    if (await get_setting("last_anniv_check") or "") == today:
        return

    m_pts = await get_float_setting("anniv_month_points", 100.0)
    y_pts = await get_float_setting("anniv_year_points", 1000.0)
    now = datetime.now(timezone.utc)

    db = await get_db()

    try:
        given = 0
        last_id = 0  # [AUDIT F3] تمرير على الكل بدفعات (بلا سقف 500)

        while True:
            cur = await db.execute(
                "SELECT id, telegram_id, lang, created_at,"
                " COALESCE(anniv_gifts, '') AS gifts FROM users"
                " WHERE created_at IS NOT NULL AND created_at != ''"
                " AND id > ? ORDER BY id LIMIT 500",
                (last_id,),
            )
            rows = await cur.fetchall()

            if not rows:
                break

            for u in rows:
                last_id = u["id"]

                try:
                    created = datetime.fromisoformat(u["created_at"])
                except (ValueError, TypeError):
                    continue

                if created.tzinfo is None:
                    created = created.replace(tzinfo=timezone.utc)

                days = (now - created).days
                milestones = []

                if days >= 30 and "m30" not in (u["gifts"] or ""):
                    milestones.append("m30")

                years = days // 365

                for y in range(1, years + 1):
                    tag = f"y{y}"

                    if tag not in (u["gifts"] or ""):
                        milestones.append(tag)

                if not milestones:
                    continue

                awarded = 0

                for tag in milestones:
                    if tag == "m30":
                        awarded += m_pts
                    else:
                        awarded += y_pts

                awarded = int(round(awarded))
                new_tags = (
                    (u["gifts"] + "," if u["gifts"] else "")
                    + ",".join(milestones)
                )

                await db.execute(
                    "UPDATE users SET points = COALESCE(points, 0) + ?,"
                    " anniv_gifts = ? WHERE id = ?",
                    (awarded, new_tags, u["id"]),
                )
                await db.execute(
                    "INSERT INTO transactions"
                    " (user_id, type, amount, note, created_at)"
                    " VALUES (?, 'points_earn', ?, ?, ?)",
                    (u["id"], float(awarded),
                     f"anniversary={'+'.join(milestones)}", now_iso()),
                )
                given += 1

                msg = r6t(
                    u["lang"] or "ar",
                    "anniv_month" if milestones == ["m30"]
                    else "anniv_year",
                ).format(p=awarded)

                # [R6-PLUS6] مراقبة انسداد البوت (D8)
                await notify_user_guarded(u["telegram_id"], msg)

        await db.commit()
    finally:
        await db.close()

    await set_setting("last_anniv_check", today)

    if given:
        logger.info("هدية الذكرى: مُنحت لـ %s مستخدماً.", given)


async def db_maint_if_due():
    """[R6-PLUS3] صيانة دورية: optimize يومي + VACUUM وفحص أسبوعي."""
    if not await feat_on("db_maint"):
        return

    now = datetime.now(timezone.utc)
    today = f"{now:%Y-%m-%d}"

    if (await get_setting("last_db_opt") or "") == today:
        return

    integrity = ""
    vacuum_done = False

    conn = sqlite3.connect(DB_PATH)

    try:
        conn.execute("PRAGMA optimize")

        if now.weekday() == 5 and (
            (await get_setting("last_db_vac") or "") != today
        ):  # السبت: أسبوعياً
            conn.execute("VACUUM")
            row = conn.execute("PRAGMA quick_check").fetchone()
            integrity = (row[0] if row else "") or ""
            await set_setting("last_db_vac", today)
            vacuum_done = True
    finally:
        conn.close()

    await set_setting("last_db_opt", today)

    if vacuum_done:
        logger.info("صيانة القاعدة: VACUUM ✓ | فحص: %s", integrity)

        if integrity and integrity.lower() != "ok":
            try:
                await bot.send_message(
                    ADMIN_USER_ID,
                    "⚠️ <b>فحص سلامة قاعدة البيانات</b>\n"
                    f"<code>{esc(integrity[:300])}</code>",
                )
            except Exception:
                pass


def _cleanup_preupgrade_backups(keep: int = 3) -> int:
    """[R6-PLUS10 E10] إبقاء أحدث نسخ الترقية فقط وإرجاع المحذوف."""
    d = os.path.dirname(os.path.abspath(DB_PATH)) or "."
    files = []

    try:
        names = os.listdir(d)
    except OSError:
        return 0

    for name in names:
        if name.startswith("bot_preupgrade_") and name.endswith(".db"):
            p = os.path.join(d, name)

            try:
                files.append((os.path.getmtime(p), p))
            except OSError:
                continue

    files.sort()

    removed = 0

    for _m, p in files[:-keep] if keep > 0 and len(files) > keep else []:
        try:
            os.remove(p)
            removed += 1
        except OSError:
            pass

    return removed


async def pre_upgrade_backup_if_due():
    """[R6-PLUS6] عند إقلاع إصدار أحدث من المحفوظ: نسخة أمان أولاً."""
    db = await get_db()

    try:
        cur = await db.execute(
            "SELECT value FROM admin_settings WHERE key = 'schema_version'",
        )
        row = await cur.fetchone()
    finally:
        await db.close()

    try:
        stored = int((row["value"] if row else "0") or 0)
    except (ValueError, TypeError):
        stored = 0

    if stored >= SCHEMA_VERSION:
        return

    # [AUDIT F7] تثبيت جديد فارغ — لا داعي لنسخة أمان
    db_c = await get_db()

    try:
        cur_c = await db_c.execute("SELECT COUNT(*) AS c FROM users")
        users_n = (await cur_c.fetchone())["c"]
    finally:
        await db_c.close()

    if users_n == 0:
        db2 = await get_db()

        try:
            await db2.execute(
                "UPDATE admin_settings SET value = ?"
                " WHERE key = 'schema_version'",
                (str(SCHEMA_VERSION),),
            )
            await db2.execute(
                "INSERT INTO admin_settings (key, value)"
                " SELECT 'schema_version', ?"
                " WHERE NOT EXISTS (SELECT 1 FROM admin_settings"
                " WHERE key = 'schema_version')",
                (str(SCHEMA_VERSION),),
            )
            await db2.commit()
        finally:
            await db2.close()

        return

    logger.info(
        "ترقية إصدار القاعدة %s → %s — نسخة أمان أولاً.",
        stored, SCHEMA_VERSION,
    )

    try:
        src = sqlite3.connect(DB_PATH)
        stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        safe_path = (
            os.path.join(
                os.path.dirname(os.path.abspath(DB_PATH)) or ".",
                f"bot_preupgrade_{stamp}.db",
            )
        )
        dst = sqlite3.connect(safe_path)

        with dst:
            src.backup(dst)

        dst.close()
        src.close()
        logger.info("نسخة ما قبل الترقية: %s", safe_path)

        if ADMIN_USER_ID:
            try:
                with open(safe_path, "rb") as fh:
                    doc = BufferedInputFile(
                        fh.read(),
                        filename=os.path.basename(safe_path),
                    )
                await bot.send_document(
                    ADMIN_USER_ID,
                    doc,
                    caption=(
                        "🛟 <b>نسخة أمان قبل ترقية الإصدار</b>\n"
                        f"📦 {stored} → {SCHEMA_VERSION}\n"
                        "احتفظ بها — تسمح بالرجوع للإصدار السابق."
                    ),
                )
                await mirror(
                    "🛟 نسخة أمان قبل ترقية الإصدار: "
                    + os.path.basename(safe_path),
                )
            except Exception as exc:
                logger.warning(
                    "تعذر إرسال نسخة ما قبل الترقية: %s", exc,
                )
        removed = _cleanup_preupgrade_backups()  # [R6-PLUS10 E10]

        if removed:
            logger.info("[E10] حُذفت %s نسخة ترقية قديمة.", removed)

    except Exception as exc:
        logger.error("فشل إنشاء نسخة ما قبل الترقية: %s", exc)

    db2 = await get_db()

    try:
        await db2.execute(
            "UPDATE admin_settings SET value = ?"
            " WHERE key = 'schema_version'",
            (str(SCHEMA_VERSION),),
        )
        await db2.execute(
            "INSERT INTO admin_settings (key, value)"
            " SELECT 'schema_version', ?"
            " WHERE NOT EXISTS (SELECT 1 FROM admin_settings"
            " WHERE key = 'schema_version')",
            (str(SCHEMA_VERSION),),
        )
        await db2.commit()
    finally:
        await db2.close()


async def mem_cleanup_if_due():
    """[R6-PLUS7 T1] تنظيف دوري لذاكرة التنبيهات (كل 24 ساعة).

    يفرّغ مفاتيح منع التكرار وعدادات الفشل الصفرية حتى لا تنمو
    بذاكرة العملية مع الأيام. المفاتيح اليومية تستهلك ذاتياً
    والتنظيف يعيد التنبيه فقط لنمط جديد فعلي بعد مرور يوم كامل.
    """
    if not await feat_on("mem_cleanup"):
        return

    today = f"{datetime.now(timezone.utc):%Y-%m-%d}"

    if (await get_setting("last_mem_cleanup") or "") == today:
        return

    n_alerts = len(_alerted_ids)
    _alerted_ids.clear()

    n_streaks = sum(
        1 for v in list(_FAIL_STREAK.values()) if not v
    )

    for k in [k for k, v in _FAIL_STREAK.items() if not v]:
        _FAIL_STREAK.pop(k, None)

    await set_setting("last_mem_cleanup", today)
    logger.info(
        "[T1] تنظيف الذاكرة: %s مفتاح تنبيه، %s عداد فشل صفري.",
        n_alerts, n_streaks,
    )


async def maint_announce_if_due():
    """[R6-PLUS7 E4] إعلان مسبق مجدول لنافذة الصيانة (مرة يومياً)."""
    if not await feat_on("maint_announce"):
        return

    window = (await get_setting("maintenance_window") or "").strip()
    parsed = _parse_maintenance_window(window)

    if not parsed:
        return

    lead = await get_float_setting("maint_announce_min", 60.0)

    if lead <= 0:
        return

    now = datetime.now(timezone.utc)
    today = f"{now:%Y-%m-%d}"

    if (await get_setting("last_maint_announce") or "") == today:
        return

    s_min, _ = parsed
    cur_min = now.hour * 60 + now.minute
    delta = s_min - cur_min

    if delta < 0:
        delta += 1440  # النافذة قد تبدأ غداً

    if delta > lead:
        return

    s_txt, e_txt = window.split("-", 1)
    db = await get_db()

    try:
        cur = await db.execute(
            "SELECT telegram_id, lang FROM users WHERE is_banned = 0",
        )
        rows = await cur.fetchall()
    finally:
        await db.close()

    sent = 0

    for u in rows:
        msg = tr(
            u["lang"] or "ar", "maint_announce", s=s_txt, e=e_txt,
        )
        await notify_user_guarded(u["telegram_id"], msg)
        sent += 1

    await set_setting("last_maint_announce", today)
    await audit(0, "maint_announce", window, f"sent={sent}")
    logger.info(
        "[E4] إعلان الصيانة أُرسل لـ %s مستخدماً (النافذة %s).",
        sent, window,
    )


async def hold_stale_if_due():
    """[R6-PLUS10 F9] تنبيه الفريق المالي عند احتجاز عالق دون قرار."""
    if not await feat_on("hold_stale"):
        return

    hours = await get_float_setting("hold_stale_hours", 12.0)

    if hours <= 0:
        return

    since = (
        datetime.now(timezone.utc) - timedelta(hours=hours)
    ).isoformat(timespec="seconds")

    db = await get_db()

    try:
        cur = await db.execute(
            "SELECT id, telegram_id, amount, created_at"
            " FROM finance_requests"
            " WHERE type = 'withdraw' AND status = 'pending'"
            " AND note LIKE '%held=1%' AND created_at <= ?",
            (since,),
        )
        rows = await cur.fetchall()
    finally:
        await db.close()

    for r in rows:
        key = f"holdstale_{r['id']}"

        if key in _alerted_ids:
            continue

        _alerted_ids.add(key)

        hrs = max(1, int(
            (datetime.now(timezone.utc)
             - datetime.fromisoformat(r["created_at"])).total_seconds()
            // 3600,
        ))

        for sid in await get_finance_staff_ids():
            try:
                await bot.send_message(
                    sid,
                    "⏰ <b>احتجاز عالق دون قرار</b>\n\n"
                    f"🆔 الطلب: #{r['id']}\n"
                    f"👤 المستخدم: <code>{r['telegram_id']}</code>\n"
                    f"💵 المحتجز: <b>{money(float(r['amount']))}</b>\n"
                    f"⏱ عمر الطلب: ~{hrs} ساعة\n\n"
                    "اعتمده أو ارفضه — رصيد المستخدم محتجز انتظاراً.",
                )
            except Exception:
                pass

        logger.info(
            "[F9] احتجاز عالق #%s عمره ~%s ساعة.", r["id"], hrs,
        )


async def _retention_text(days: int = 7) -> str:
    """[R6-PLUS10 E7] بناء نص الاحتفاظ — مشترك بين المجدول والمعاينة."""
    start = (
        datetime.now(timezone.utc) - timedelta(days=days)
    ).strftime("%Y-%m-%d")

    db = await get_db()

    try:
        cur = await db.execute(
            "SELECT COUNT(DISTINCT telegram_id) AS c"
            " FROM finance_requests"
            " WHERE type = 'deposit' AND status = 'approved'"
            " AND created_at >= ?",
            (start,),
        )
        total = (await cur.fetchone())["c"]

        cur = await db.execute(
            "SELECT COUNT(DISTINCT telegram_id) AS c"
            " FROM finance_requests fr"
            " WHERE fr.type = 'deposit' AND fr.status = 'approved'"
            " AND fr.created_at >= ?"
            " AND NOT EXISTS (SELECT 1 FROM finance_requests fr2"
            " WHERE fr2.telegram_id = fr.telegram_id"
            " AND fr2.type = 'deposit' AND fr2.status = 'approved'"
            " AND fr2.created_at < ?)",
            (start, start),
        )
        new = (await cur.fetchone())["c"]
    finally:
        await db.close()

    if total == 0:
        return (
            f"♻️ <b>الاحتفاظ — آخر {days} يوماً</b>\n\n"
            "لا شحنات معتمدة بعد."
        )

    returning = total - new
    rate = returning * 100.0 / total

    return (
        f"♻️ <b>الاحتفاظ — آخر {days} يوماً</b>\n\n"
        f"🛒 من شحن: <b>{total}</b>\n"
        f"🆕 جدد: {new} | 🔁 عائدون: {returning}\n"
        f"📊 نسبة العودة: <b>{rate:.0f}%</b>"
    )


async def retention_if_due(now: datetime | None = None):
    """[R6-PLUS10 E7] تقرير الاحتفاظ الأسبوعي (أحد بعد 9 UTC)."""
    if not await feat_on("retention"):
        return

    now = now or datetime.now(timezone.utc)
    today = f"{now:%Y-%m-%d}"

    if (await get_setting("last_retention_week") or "") == today:
        return

    if now.weekday() != 6 or now.hour < 9:  # الأحد
        return

    text = await _retention_text(7)

    try:
        await bot.send_message(ADMIN_USER_ID, text)
        await mirror(text)
    except Exception as exc:
        logger.warning("تعذر إرسال تقرير الاحتفاظ: %s", exc)
        return

    await set_setting("last_retention_week", today)


async def bal_alerts_if_due():
    """[R6-PLUS10 U36] إشعار المستخدم حين ينخفض رصيده عن حدّه."""
    if not await feat_on("bal_alert"):
        return

    db = await get_db()

    try:
        cur = await db.execute(
            "SELECT key, value FROM admin_settings"
            " WHERE key LIKE 'bal_alert_%' LIMIT 200",
        )
        rows = await cur.fetchall()
    finally:
        await db.close()

    for r in rows:
        try:
            tid = int(r["key"].rsplit("_", 1)[1])
            thr = float(r["value"])
        except (ValueError, IndexError):
            continue

        if thr <= 0:
            continue

        u = await get_user(tid)

        if not u or u["is_banned"]:
            continue

        bal = float(u["balance"] or 0)
        marker = f"balalert_fired_{tid}"

        if bal < thr:
            if marker in _alerted_ids:
                continue

            _alerted_ids.add(marker)
            lang = await user_lang(tid)
            await notify_user_guarded(
                tid,
                tr(lang, "balalert_fired", bal=money(bal), thr=money(thr)),
            )
        elif marker in _alerted_ids:
            _alerted_ids.discard(marker)  # ارتفع مجدداً — يمكن إعادة التنبيه


async def _periodic_tasks():
    """حلقة المهام الدورية (كل 10 دقائق)."""
    while True:
        try:
            await auto_backup_if_due()
            await send_daily_summary_if_due()
            expired = await expire_old_requests()
            if expired:
                logger.info("انتهت صلاحية %s طلبًا معلقًا.", expired)
            await check_smart_alerts()  # [NEW 46]
            await scheduled_zip_if_due()  # [ADM-4]
            await expire_user_gifts()  # [USR-4]
            await monthly_pl_if_due()  # [ADM2-4]
            await auto_protect_if_needed()  # [ADM2-6]
            await weekly_report_if_due()  # [ADM3-12]
            await scheduled_broadcast_if_due()  # [ADM3-10]
            await contest_if_due()  # [ADM4-2]
            await channel_posts_if_due()  # [R6-CH] نشر القنوات
            await stale_requests_if_due()  # [R6-PLUS2] تذكير العالق
            await winback_if_due()  # [R6-PLUS2] رسالة الرجوع
            await digest_if_due()  # [R6-PLUS3] الملخص الشخصي
            await anniv_gifts_if_due()  # [R6-PLUS5] هدية الذكرى
            await db_maint_if_due()  # [R6-PLUS3] صيانة القاعدة
            await mem_cleanup_if_due()  # [R6-PLUS7 T1] تنظيف الذاكرة
            await maint_announce_if_due()  # [R6-PLUS7 E4] إعلان مسبق
            await hold_stale_if_due()  # [R6-PLUS10 F9] احتجاز عالق
            await retention_if_due()  # [R6-PLUS10 E7] الاحتفاظ
            await bal_alerts_if_due()  # [R6-PLUS10 U36] تنبيه الرصيد
            await panel_recon_if_due()  # [R6-PLUS13] مطابقة اللوحة
        except Exception:
            logger.exception("خطأ في المهام الدورية")
        await asyncio.sleep(600)


# ============================================================
# ADMIN PAYOUTS UI [NEW 36]
# ============================================================

@dp.callback_query(F.data == "admin_payouts")
async def admin_payouts(cb: types.CallbackQuery, state: FSMContext):

    if not await is_admin_or_supervisor(cb.from_user.id, "finance"):
        await cb.answer("غير مصرّح.", show_alert=True)
        return

    await state.clear()
    await cb.answer()

    text, kb = await render_payouts_view()
    await safe_edit(cb.message, text, kb)


@dp.callback_query(F.data.startswith("payout_pay:"))
async def payout_pay(cb: types.CallbackQuery, state: FSMContext):

    if not await is_admin_or_supervisor(cb.from_user.id, "finance"):
        await cb.answer("غير مصرّح.", show_alert=True)
        return

    if not await pin_gate(cb):  # [ADM3-1]
        return

    try:
        payout_id = int(cb.data.split(":", 1)[1])
    except (ValueError, IndexError):
        await cb.answer("أمر غير صالح.", show_alert=True)
        return

    ok = await mark_payout_paid(
        payout_id, admin_id=cb.from_user.id,
    )

    if not ok:
        await cb.answer("تمت معالجتها مسبقًا.", show_alert=True)
        return

    await audit(  # [NEW 22]
        cb.from_user.id, "payout_paid", f"payout={payout_id}"
    )
    await cb.answer("تم التعليم كمدفوعة ✅", show_alert=True)

    payout = await get_payout(payout_id)
    if payout:
        try:
            await bot.send_message(
                payout["user_tid"],
                "✅ <b>تمت تسوية أمر السحب</b>\n\n"
                f"💵 المبلغ: {money(payout['amount'])}\n"
                f"🆔 Payout: #{payout_id}\n\n"
                "إذا وصلك المبلغ فلا تحتاج لأي إجراء.",
            )
        except Exception as exc:
            logger.warning("تعذر إشعار المستخدم بالدفع: %s", exc)

        # [R6-PLUS2] طلب تقييم ⭐ لتجربة السحب
        if await feat_on("payout_rating"):  # [R6-PLUS3]
            await _ask_payout_rating(payout["user_tid"], payout_id)

    text, kb = await render_payouts_view()
    await safe_edit(cb.message, text, kb)


@dp.callback_query(F.data.startswith("payout_fail:"))
async def payout_fail(cb: types.CallbackQuery, state: FSMContext):

    if not await is_admin_or_supervisor(cb.from_user.id, "finance"):
        await cb.answer("غير مصرّح.", show_alert=True)
        return

    if not await pin_gate(cb):  # [ADM3-1]
        return

    try:
        payout_id = int(cb.data.split(":", 1)[1])
    except (ValueError, IndexError):
        await cb.answer("أمر غير صالح.", show_alert=True)
        return

    changed, refunded = await mark_payout_failed_and_refund(
        payout_id,
        error=f"by_admin_{cb.from_user.id}",
        admin_id=cb.from_user.id,
    )

    if not changed:
        await cb.answer("تمت معالجتها مسبقًا.", show_alert=True)
        return

    await cb.answer("تم الإرجاع للمستخدم ↩️", show_alert=True)

    payout = await get_payout(payout_id)
    if payout:
        try:
            text = (
                "↩️ <b>تعذر إتمام تحويل السحب</b>\n\n"
                f"💵 المبلغ: {money(payout['amount'])}\n"
                f"🆔 Payout: #{payout_id}"
            )
            if refunded:
                text += "\n✅ أُعيد المبلغ كاملاً إلى رصيدك."
            await bot.send_message(payout["user_tid"], text)
        except Exception as exc:
            logger.warning("تعذر إشعار المستخدم بالفشل: %s", exc)

    text, kb = await render_payouts_view()
    await safe_edit(cb.message, text, kb)



# ============================================================
# WITHDRAW DAILY CAPS [NEW 41]
# ============================================================

async def _withdraw_sum(telegram_id: int) -> float:
    """مجموع سحوبات اليوم (المعتمدة + المعلقة) لمستخدم محدد."""
    like = f"{datetime.now(timezone.utc):%Y-%m-%d}%"

    db = await get_db()

    try:
        cur = await db.execute(
            """
            SELECT COALESCE(SUM(t.amount), 0) AS total
            FROM transactions t
            JOIN users u ON u.id = t.user_id
            WHERE t.type = 'withdraw'
              AND t.created_at LIKE ?
              AND u.telegram_id = ?
            """,
            (like, telegram_id),
        )
        approved = float((await cur.fetchone())["total"])

        cur = await db.execute(
            """
            SELECT COALESCE(SUM(amount), 0) AS total
            FROM finance_requests
            WHERE type = 'withdraw'
              AND status = 'pending'
              AND created_at LIKE ?
              AND telegram_id = ?
            """,
            (like, telegram_id),
        )
        pending = float((await cur.fetchone())["total"])
    finally:
        await db.close()

    return approved + pending


async def _withdraw_sum_all() -> float:
    """مجموع سحوبات اليوم لكل المستخدمين (معتمدة + معلقة)."""
    like = f"{datetime.now(timezone.utc):%Y-%m-%d}%"

    db = await get_db()

    try:
        cur = await db.execute(
            """
            SELECT COALESCE(SUM(amount), 0) AS total
            FROM transactions
            WHERE type = 'withdraw'
              AND created_at LIKE ?
            """,
            (like,),
        )
        approved = float((await cur.fetchone())["total"])

        cur = await db.execute(
            """
            SELECT COALESCE(SUM(amount), 0) AS total
            FROM finance_requests
            WHERE type = 'withdraw'
              AND status = 'pending'
              AND created_at LIKE ?
            """,
            (like,),
        )
        pending = float((await cur.fetchone())["total"])
    finally:
        await db.close()

    return approved + pending


async def check_withdraw_caps(telegram_id: int, amount: float):
    """
    [NEW 41] التحقق من السقوف اليومية للسحب قبل قبول الطلب.
    يعيد نص الخطأ أو None إذا كان الطلب مسموحاً.
    """
    cap_user = await get_float_setting("daily_withdraw_per_user", 0.0)

    # [R6-PLUS2] سقف خاص بالمستخدم يتجاوز العام إن وُجد
    db_uc = await get_db()

    try:
        cur_uc = await db_uc.execute(
            "SELECT wd_daily_cap FROM users WHERE telegram_id = ?",
            (telegram_id,),
        )
        _urow = await cur_uc.fetchone()
    finally:
        await db_uc.close()

    if _urow and _urow["wd_daily_cap"] and _urow["wd_daily_cap"] > 0:
        cap_user = float(_urow["wd_daily_cap"])

    if cap_user > 0:
        used = await _withdraw_sum(telegram_id)

        if round2(used + amount) > round2(cap_user):
            remaining = max(0.0, round2(cap_user - used))
            return (
                f"تجاوزت سقف السحب اليومي ({money(cap_user)}).\n"
                f"سحبت اليوم: {money(used)} | المتباح الآن: "
                f"{money(remaining)}"
            )

    cap_total = await get_float_setting("daily_withdraw_total", 0.0)

    if cap_total > 0:
        used_all = await _withdraw_sum_all()

        if round2(used_all + amount) > round2(cap_total):
            return (
                "تم بلوغ السقف الإجمالي اليومي للسحوبات"
                f" ({money(cap_total)}).\nحاول مجدداً غداً."
            )

    return None


# ============================================================
# ADMIN SUBMENUS [NEW 44]
# ============================================================

@dp.callback_query(F.data == "sup_reply_stats")
async def sup_reply_stats(cb: types.CallbackQuery, state: FSMContext):
    """[R6-PLUS5] إحصاء ردود التذاكر لكل مشرف (30 يوماً)."""

    if not await is_admin_or_supervisor(cb.from_user.id, "reports"):
        await cb.answer("غير مصرّح.", show_alert=True)
        return

    await cb.answer()
    await state.clear()

    since = (
        datetime.now(timezone.utc) - timedelta(days=30)
    ).isoformat(timespec="seconds")

    db = await get_db()

    try:
        cur = await db.execute(
            "SELECT answered_by, COUNT(*) AS c FROM support_tickets"
            " WHERE answered_by IS NOT NULL AND answered_at >= ?"
            " GROUP BY answered_by ORDER BY c DESC",
            (since,),
        )
        rows = await cur.fetchall()
    finally:
        await db.close()

    lines = ["📊 <b>ردود الدعم — آخر 30 يوماً</b>\n"]
    total = 0

    for r in rows:
        u = await get_user(r["answered_by"])
        name = (u["full_name"] or str(r["answered_by"])) if u \
            else str(r["answered_by"])
        total += r["c"]
        lines.append(f"👤 {esc(name[:24])} — <b>{r['c']}</b> رد")

    if not rows:
        lines.append("لا ردود مسجلة بعد.")

    lines.append(f"\nالإجمالي: <b>{total}</b> رد")

    b = InlineKeyboardBuilder()
    b.button(text="🔙 رجوع", callback_data="admin_inbox")
    b.adjust(1)

    await safe_edit(cb.message, "\n".join(lines), b.as_markup())


# [AUDIT F5] مفاتيح رقمية/نصية بلا واجهة سابقاً
VALUE_SETTINGS = {
    "points_per_unit": ("⭐ نقاط لكل 1$ شحن", "float"),
    "winback_days": ("💤 أيام الغياب للرحوع", "float"),
    "winback_msg": ("💬 نص رسالة الرجوع", "text"),
    "anniv_month_points": ("🎂 نقاط ذكرى الشهر", "float"),
    "anniv_year_points": ("🎉 نقاط الذكرى السنوية", "float"),
    "inst_dep_window_min": ("🚨 نافذة الشحن/السحب (دقائق)", "float"),
    "maint_announce_min": ("🚧 دقائق الإعلان المسبق للصيانة", "float"),
    "hold_stale_hours": ("⏰ ساعات التنبيه للاحتجاز العالق", "float"),
}


@dp.callback_query(F.data == "welcome_photo_set")
async def welcome_photo_set(cb: types.CallbackQuery, state: FSMContext):
    """[R6-PLUS9 V8] رفع/مسح صورة الترحيب."""

    if cb.from_user.id != ADMIN_USER_ID:
        await cb.answer("للأدمن الرئيسي فقط.", show_alert=True)
        return

    await cb.answer()
    await state.clear()
    await state.set_state(AdminPhotoFSM.photo)

    cur = (await get_setting("welcome_photo_file_id") or "").strip()
    status_txt = "موجودة ✅" if cur else "غير مضبوطة"

    await cb.message.answer(
        "🖼 <b>صورة الترحيب</b>\n\n"
        f"الحالة: {status_txt}\n\n"
        "أرسل صورة الآن لتصبح شعار الترحيب عند /start\n"
        "أو أرسل <code>مسح</code> لإزالتها.\n"
        "للإلغاء أرسل /cancel",
        reply_markup=back_kb("admin_settings_menu"),
    )


@dp.message(AdminPhotoFSM.photo)
async def welcome_photo_save(message: types.Message, state: FSMContext):
    """[R6-PLUS9 V8] حفظ/مسح صورة الترحيب."""

    if message.from_user.id != ADMIN_USER_ID:
        await state.clear()
        return

    raw = (message.text or "").strip()

    if raw.startswith("/"):
        await state.clear()
        return

    if message.photo:
        await set_setting(
            "welcome_photo_file_id", message.photo[-1].file_id,
        )
        await state.clear()
        await audit(message.from_user.id, "welcome_photo", "", "set")

        await message.answer(
            "✅ صارت صورة الترحيب مفعّلة — تظهر مع /start للجميع"
            " (بميزة 🖼 ترحيب بصورة).",
            reply_markup=back_kb("admin_settings_menu"),
        )
        return

    if raw in ("مسح", "clear"):
        await set_setting("welcome_photo_file_id", "")
        await state.clear()
        await audit(message.from_user.id, "welcome_photo", "", "cleared")

        await message.answer(
            "🗑 أُزيلت صورة الترحيب — عاد الترحيب النصي.",
            reply_markup=back_kb("admin_settings_menu"),
        )
        return

    await message.answer(
        "❌ أرسل <b>صورة</b> أو <code>مسح</code>.\nللإلغاء أرسل /cancel",
    )


@dp.callback_query(F.data == "value_settings")
async def value_settings(cb: types.CallbackQuery, state: FSMContext):
    """[AUDIT F5] شاشة ضبط قيم الميزات المتقدمة."""

    if not await is_admin_or_supervisor(cb.from_user.id, "all"):
        await cb.answer("غير مصرّح.", show_alert=True)
        return

    await cb.answer()
    await state.clear()

    b = InlineKeyboardBuilder()
    lines = ["🔢 <b>إعدادات القيم</b>\n"]

    for key, (label, kind) in VALUE_SETTINGS.items():
        cur = (await get_setting(key) or "").strip()

        if not cur:
            defaults = {
                "points_per_unit": "1", "winback_days": "14",
                "anniv_month_points": "100",
                "anniv_year_points": "1000",
                "inst_dep_window_min": "30",
            }
            cur = defaults.get(key, "—")

        lines.append(f"• {label}: <code>{esc(cur)}</code>")
        b.button(text=label, callback_data=f"valset:{key}")

    b.button(text="🔙 رجوع", callback_data="admin_settings_menu")
    b.adjust(1)

    await safe_edit(
        cb.message,
        "\n".join(lines)
        + "\n\nاضغط على أي بند لتعديل قيمته:",
        b.as_markup(),
    )


@dp.callback_query(F.data.startswith("valset:"))
async def valset_pick(cb: types.CallbackQuery, state: FSMContext):
    """[AUDIT F5] اختيار مفتاح للتعديل."""

    if not await is_admin_or_supervisor(cb.from_user.id, "all"):
        await cb.answer("غير مصرّح.", show_alert=True)
        return

    key = cb.data.split(":", 1)[1]

    if key not in VALUE_SETTINGS:
        await cb.answer("مفتاح غير معروف.", show_alert=True)
        return

    label, kind = VALUE_SETTINGS[key]
    current = (await get_setting(key) or "").strip()

    await cb.answer()
    await state.clear()
    await state.update_data(val_key=key)
    await state.set_state(AdminValSetFSM.value)

    prompt = (
        f"✏️ <b>{label}</b>\n"
        f"الحالي: <code>{esc(current or '—')}</code>\n\n"
    )

    if kind == "float":
        prompt += "أرسل الرقم الجديد:"
    else:
        prompt += "أرسل النص الجديد (أو «مسح» لاستخدام الافتراضي):"

    await cb.message.answer(
        prompt + "\n\nللإلغاء أرسل /cancel",
        reply_markup=back_kb("admin_settings_menu"),
    )


@dp.message(AdminValSetFSM.value)
async def valset_save(message: types.Message, state: FSMContext):
    """[AUDIT F5] حفظ القيمة الجديدة."""

    if not await is_admin_or_supervisor(message.from_user.id, "all"):
        await state.clear()
        return

    raw = (message.text or "").strip()

    if not raw or raw.startswith("/"):
        await state.clear()
        return

    data = await state.get_data()
    key = data.get("val_key")

    if key not in VALUE_SETTINGS:
        await state.clear()
        return

    label, kind = VALUE_SETTINGS[key]

    if kind == "float":
        try:
            value = float(raw)

            if value < 0:
                raise ValueError
        except ValueError:
            await message.answer("❌ أرسل رقماً صحيحاً (≥ 0).")
            return

        await set_setting(key, str(value))
    else:
        if raw in ("مسح", "clear"):
            await set_setting(key, "")
        else:
            await set_setting(key, raw[:1000])

    await state.clear()
    await audit(message.from_user.id, "value_set", key, raw[:100])

    await message.answer(f"✅ حُفظ: {label} = <code>{esc(raw)}</code>")


@dp.callback_query(F.data == "support_hours_set")
async def support_hours_set(cb: types.CallbackQuery, state: FSMContext):
    """[R6-PLUS5] ضبط ساعات عمل الدعم (فارغ = دائماً متاح)."""

    if not await is_admin_or_supervisor(cb.from_user.id, "all"):
        await cb.answer("غير مصرّح.", show_alert=True)
        return

    await cb.answer()
    await state.clear()
    await state.set_state(SupportHoursFSM.value)

    current = (await get_setting("support_hours") or "").strip()

    await cb.message.answer(
        "🕐 <b>ساعات عمل الدعم</b>\n\n"
        "أرسل الفترة بصيغة <code>09:00-23:00</code>"
        " (بتوقيت UTC)\n"
        "خارجها يُنبه البوت صاحب التذكرة تلقائياً.\n"
        "أو أرسل «مسح» ليكون الدعم متاحاً دائماً:\n"
        f"الحالي: <code>{esc(current or 'دائماً')}</code>\n"
        "للإلغاء أرسل /cancel",
        reply_markup=back_kb("admin_settings_menu"),
    )


@dp.message(SupportHoursFSM.value)
async def support_hours_save(message: types.Message, state: FSMContext):
    """[R6-PLUS5] حفظ ساعات الدعم."""

    if not await is_admin_or_supervisor(message.from_user.id, "all"):
        await state.clear()
        return

    raw = (message.text or "").strip()

    if not raw or raw.startswith("/"):
        await state.clear()
        return

    if raw in ("مسح", "clear"):
        await set_setting("support_hours", "")
        await state.clear()
        await message.answer("✅ الدعم متاح دائماً الآن.")
        return

    if not _support_hours_str(raw):
        await message.answer(
            "❌ صيغة غير صحيحة — مثال: <code>09:00-23:00</code>"
        )
        return

    await set_setting("support_hours", raw)
    await state.clear()
    await audit(message.from_user.id, "support_hours", "", raw)
    await message.answer(f"✅ حُفظت ساعات الدعم: <code>{raw}</code> UTC")


@dp.callback_query(F.data == "features_hub")
async def features_hub(cb: types.CallbackQuery, state: FSMContext):
    """[R6-PLUS3] مركز تفعيل/تعطيل ميزات البوت."""

    if not await is_admin_or_supervisor(cb.from_user.id, "all"):
        await cb.answer("غير مصرّح.", show_alert=True)
        return

    await cb.answer()
    await state.clear()

    b = InlineKeyboardBuilder()
    on_count = 0

    for key, (label, default) in FEATURES.items():
        on = await feat_on(key)

        if on:
            on_count += 1

        b.button(
            text=f"{'✅' if on else '❌'} {label}",
            callback_data=f"togfeat:{key}",
        )

    b.button(text="↩️ رجوع", callback_data="admin_home")  # [PANELHUB 5.18.14]
    b.adjust(2)  # [UI-TABS 5.18.4] زرين بالسطر

    await safe_edit(
        cb.message,
        "🎛 <b>مركز تفعيل الميزات</b>\n\n"
        f"المفعّل: <b>{on_count}</b> من {len(FEATURES)}\n"
        "اضغط على أي ميزة للتبديل بين التفعيل والإيقاف:",
        b.as_markup(),
    )


@dp.callback_query(F.data.startswith("togfeat:"))
async def togfeat(cb: types.CallbackQuery, state: FSMContext):
    """[R6-PLUS3] تبديل حالة ميزة."""

    if not await is_admin_or_supervisor(cb.from_user.id, "all"):
        await cb.answer("غير مصرّح.", show_alert=True)
        return

    key = cb.data.split(":", 1)[1]

    if key not in FEATURES:
        await cb.answer("ميزة غير معروفة.", show_alert=True)
        return

    new_val = "0" if await feat_on(key) else "1"
    await set_setting(f"feat_{key}", new_val)
    await audit(cb.from_user.id, "feature_toggle", key, new_val)

    label = FEATURES[key][0]
    await cb.answer(
        f"{'✅ فُعّلت' if new_val == '1' else '❌ أوقفت'}: {label}",
        show_alert=True,
    )

    # إعادة رسم الشاشة
    b = InlineKeyboardBuilder()

    for k2, (label2, _d2) in FEATURES.items():
        on2 = await feat_on(k2)
        b.button(
            text=f"{'✅' if on2 else '❌'} {label2}",
            callback_data=f"togfeat:{k2}",
        )

    b.button(text="↩️ رجوع", callback_data="admin_home")  # [PANELHUB 5.18.14]
    b.adjust(2)  # [UI-TABS 5.18.4] زرين بالسطر

    await safe_edit(
        cb.message,
        "🎛 <b>مركز تفعيل الميزات</b>\n\n"
        "اضغط على أي ميزة للتبديل بين التفعيل والإيقاف:",
        b.as_markup(),
    )


@dp.callback_query(F.data == "admin_settings_menu")
async def admin_settings_menu(cb: types.CallbackQuery, state: FSMContext):

    if not await is_admin_or_supervisor(cb.from_user.id):
        await cb.answer("غير مصرّح.", show_alert=True)
        return

    await cb.answer()
    await state.clear()
    status = await admin_status_line()  # [UI-1]
    await safe_edit(
        cb.message,
        f"⚙️ <b>الإعدادات والأدوات</b>\n{status}\n\nاختر ما تريد ضبطه:",
        await admin_settings_kb(),
    )


@dp.callback_query(F.data == "admin_tools_menu")
async def admin_tools_menu(cb: types.CallbackQuery, state: FSMContext):
    """[SETTOOLS 5.18.13] الأدوات دُمجت في الإعدادات — يفتح الجذر الموحد."""
    await admin_settings_menu(cb, state)


# ============================================================
# KPI LIVE DASHBOARD [NEW 42]
# ============================================================

async def gather_kpi() -> dict:
    """[NEW 42] جمع مؤشرات الأداء الرئيسية."""
    today = f"{datetime.now(timezone.utc):%Y-%m-%d}%"

    db = await get_db()

    try:
        async def one(sql, params=()):
            cur = await db.execute(sql, params)
            return await cur.fetchone()

        k = {}
        k["users_total"] = (
            await one("SELECT COUNT(*) c FROM users")
        )["c"]
        k["users_new"] = (
            await one(
                "SELECT COUNT(*) c FROM users WHERE created_at LIKE ?",
                (today,),
            )
        )["c"]
        k["banned"] = (
            await one(
                "SELECT COUNT(*) c FROM users WHERE is_banned = 1"
            )
        )["c"]
        k["active_today"] = (
            await one(
                "SELECT COUNT(DISTINCT user_id) c FROM transactions"
                " WHERE created_at LIKE ?",
                (today,),
            )
        )["c"]

        row = await one(
            "SELECT COUNT(*) c, COALESCE(SUM(amount), 0) s"
            " FROM transactions WHERE type='deposit'"
            " AND created_at LIKE ?",
            (today,),
        )
        k["dep_count"], k["dep_sum"] = row["c"], float(row["s"])

        row = await one(
            "SELECT COUNT(*) c, COALESCE(SUM(amount), 0) s"
            " FROM transactions WHERE type='withdraw'"
            " AND created_at LIKE ?",
            (today,),
        )
        k["wd_count"], k["wd_sum"] = row["c"], float(row["s"])

        k["pending_finance"] = (
            await one(
                "SELECT COUNT(*) c FROM finance_requests"
                " WHERE status='pending'"
            )
        )["c"]
        k["pending_payouts"] = (
            await one(
                "SELECT COUNT(*) c FROM payouts"
                " WHERE status IN ('pending','processing')"
            )
        )["c"]
        k["open_tickets"] = (
            await one(
                "SELECT COUNT(*) c FROM support_tickets"
                " WHERE status='open'"
            )
        )["c"]

        # [USR2-7] متوسط رضا العملاء
        row = await one(
            "SELECT COALESCE(AVG(rating), 0) a, COUNT(rating) n"
            " FROM support_tickets WHERE rating IS NOT NULL"
        )
        k["rating_avg"], k["rating_n"] = float(row["a"]), row["n"]
    finally:
        await db.close()

    return k


@dp.callback_query(F.data == "admin_kpi")
async def admin_kpi(cb: types.CallbackQuery, state: FSMContext):
    """[NEW 42] لوحة المؤشرات الحية مع زر تحديث."""

    if not await is_admin_or_supervisor(cb.from_user.id):
        await cb.answer("غير مصرّح.", show_alert=True)
        return

    await state.clear()
    await cb.answer()
    _last_admin_screen[cb.from_user.id] = "admin_kpi"  # [V11]

    k = await gather_kpi()

    # [R6-PLUS10 E9] أعلى ساعات النشاط آخر 7 أيام
    peak_txt = ""

    if await feat_on("peak_hours"):
        since_p = (
            datetime.now(timezone.utc) - timedelta(days=7)
        ).isoformat(timespec="seconds")
        db_p = await get_db()

        try:
            cur_p = await db_p.execute(
                "SELECT substr(created_at, 12, 2) AS h, COUNT(*) AS c"
                " FROM transactions WHERE created_at >= ?"
                " GROUP BY h ORDER BY c DESC LIMIT 5",
                (since_p,),
            )
            prows = await cur_p.fetchall()
        finally:
            await db_p.close()

        if prows:
            peak_txt = "\n\n🔥 <b>ساعات الذروة</b> (7 أيام):\n" + "\n".join(
                f"• {int(r['h']):02d}:00 — {r['c']} عملية" for r in prows
            )

    text = (
        "📊 <b>KPI — مباشر</b>\n\n"
        f"👥 المستخدمون: {k['users_total']}"
        f" (جدد اليوم: {k['users_new']})\n"
        f"🔥 نشطوا اليوم: {k['active_today']}\n"
        f"🚫 المحظورون: {k['banned']}\n\n"
        f"💰 شحن اليوم: {k['dep_count']} عملية = {money(k['dep_sum'])}\n"
        f"🏦 سحب اليوم: {k['wd_count']} عملية = {money(k['wd_sum'])}\n\n"
        f"📨 طلبات معلقة: {k['pending_finance']}\n"
        f"🚀 مدفوعات معلقة: {k['pending_payouts']}\n"
        f"💬 تذاكر مفتوحة: {k['open_tickets']}\n"
        f"⭐ رضا العملاء: {k['rating_avg']:.1f}"
        f" ({k['rating_n']} تقييماً)"  # [USR2-7]
        + peak_txt  # [R6-PLUS10 E9]
    )

    b = InlineKeyboardBuilder()

    if await feat_on("profit_chart"):  # [V12]
        b.button(text="💰 رسم الأرباح (30ي)", callback_data="profit_chart")

    b.button(text="🔄 تحديث", callback_data="admin_kpi")
    b.button(text="🔙 رجوع", callback_data="admin_panel")
    b.adjust(2)

    await safe_edit(cb.message, text, b.as_markup())


@dp.callback_query(F.data == "profit_chart")
async def profit_chart(cb: types.CallbackQuery, state: FSMContext):
    """[R6-PLUS9 V12] رسم صافي الأرباح لآخر 30 يوماً (PNG)."""

    if not await is_admin_or_supervisor(cb.from_user.id, "reports"):
        await cb.answer("غير مصرّح.", show_alert=True)
        return

    await cb.answer()

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        await cb.message.answer(
            "⚠️ مكتبة matplotlib غير مثبتة — لا يمكن إنشاء الرسم.\n"
            "ثبّتها: pip install matplotlib",
        )
        return

    days = 30
    series = await profit_series(days)
    total = round2(sum(series.values()))

    day_list = [
        (
            datetime.now(timezone.utc) - timedelta(days=i)
        ).strftime("%Y-%m-%d")
        for i in range(days - 1, -1, -1)
    ]
    vals = [series.get(d, 0.0) for d in day_list]

    fig, ax = plt.subplots(figsize=(10, 4.5))
    colors = ["#2e7d32" if v >= 0 else "#c62828" for v in vals]
    ax.bar(range(days), vals, color=colors)
    ax.axhline(0, color="#666", linewidth=0.8)
    ax.set_title("Net profit - last 30 days (UTC)")
    ax.grid(True, axis="y", alpha=0.3)

    step = max(1, days // 7)
    ax.set_xticks(list(range(days))[::step])
    ax.set_xticklabels([day_list[i][5:] for i in range(0, days, step)])

    plt.tight_layout()

    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=110)
    plt.close(fig)
    buf.seek(0)

    photo = BufferedInputFile(buf.getvalue(), filename="profit_30d.png")

    try:
        await cb.message.answer_photo(
            photo,
            caption=(
                "💰 <b>صافي الأرباح — آخر 30 يوماً</b>\n\n"
                f"الإجمالي: <b>{money(total)}</b>\n"
                "(عمولات + رسوم − مكافآت − نقاط)"
            ),
        )
    except Exception:
        await cb.message.answer(f"💰 صافي 30 يوماً: {money(total)}")


# ============================================================
# FULL ZIP EXPORT [NEW 43]
# ============================================================

def build_csv_bytes(headers: list, rows: list) -> bytes:
    """CSV بترميز Excel-صديق كبايتات جاهزة للأرشفة."""
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(headers)

    for row in rows:
        writer.writerow(["" if v is None else v for v in row])

    return buf.getvalue().encode("utf-8-sig")


# ============================================================
# USER SEARCH + CARD + LIST + DM [NEW 37 / NEW 38]
# ============================================================

async def fmt_bal(viewer_id: int, balance) -> str:
    """[ADM3-8] إخفاء الأرصدة عن المشرفين إن فُعّل."""
    if viewer_id != ADMIN_USER_ID and (
        await get_setting("staff_hide_balance") == "1"
    ):
        return "•••"

    return money(balance)


async def render_user_card(user: dict, viewer_id: int):
    """[NEW 37] كارت مستخدم شامل مع أزرار إجراءات سريعة."""
    tid = user["telegram_id"]

    db = await get_db()

    try:
        cur = await db.execute(
            "SELECT COUNT(*) AS c FROM users WHERE referrer_id = ?",
            (tid,),
        )
        refs = (await cur.fetchone())["c"]

        cur = await db.execute(
            "SELECT suspended FROM supervisors WHERE telegram_id = ?",
            (tid,),
        )
        sup_row = await cur.fetchone()

        # [ADM2-2] آخر 3 ملاحظات إدارية
        cur = await db.execute(
            """
            SELECT note, created_at FROM user_notes
            WHERE target_tid = ?
            ORDER BY id DESC LIMIT 3
            """,
            (tid,),
        )
        note_rows = await cur.fetchall()

        # [ADM4-1] وسوم المستخدم
        cur = await db.execute(
            "SELECT id, tag FROM user_tags WHERE telegram_id = ?"
            " ORDER BY id",
            (tid,),
        )
        tag_rows = await cur.fetchall()
    finally:
        await db.close()

    # [R6-PLUS10 E8] إجماليات المستخدم منذ التسجيل (LTV)
    ltv_line = ""

    if await feat_on("user_ltv"):
        db_l = await get_db()

        try:
            cur_l = await db_l.execute(
                "SELECT"
                " COALESCE(SUM(CASE WHEN type = 'deposit' THEN amount"
                " END), 0) AS dep,"
                " COALESCE(SUM(CASE WHEN type = 'withdraw' THEN amount"
                " END), 0) AS wd"
                " FROM transactions WHERE user_id = ?",
                (user["id"],),
            )
            ltv = await cur_l.fetchone()
        finally:
            await db_l.close()

        dep_s, wd_s = float(ltv["dep"]), float(ltv["wd"])
        ltv_line = (
            f"\n💎 شحناته: {money(dep_s)} | سحبه: {money(wd_s)}"
            f" | صافيه: {money(dep_s - wd_s)}"
        )

    is_suspended = bool(sup_row and sup_row["suspended"])

    status = "🚫 محظور" if user["is_banned"] else "✅ نشط"

    # [R6-PLUS3] عرض الحظر المؤقت النشط
    tban_line = ""
    _bu = user["ban_until"] if "ban_until" in user.keys() else ""

    if _bu:
        try:
            _bud = datetime.fromisoformat(_bu)

            if _bud > datetime.now(timezone.utc):
                tban_line = (
                    f"\n⏳ حظر مؤقت حتى {esc(_bu[:16])} UTC"
                )
        except (ValueError, TypeError):
            pass

    sup_line = ""
    if sup_row:
        sup_line = (
            "\n⏸ مشرف موقوف مؤقتاً" if is_suspended else "\n🛡 مشرف"
        )

    uname_line = (
        f"\nاليوزر: @{user['username']}" if user["username"] else ""
    )

    text = (
        "👤 <b>كارت المستخدم</b>\n\n"
        f"الاسم: {esc(user['full_name'])}\n"
        f"Telegram: <code>{tid}</code>"
        f"{uname_line}\n"
        f"الموقع: {esc(user['site_username'] or '—')}\n"
        f"الرصيد: <b>{await fmt_bal(viewer_id, user['balance'])}</b>"
        f"{ltv_line}\n"  # [R6-PLUS10 E8]
        f"الحالة: {status}{sup_line}{tban_line}\n"
        f"إحالات: {refs}\n"
        f"انضم: {esc(await fmt_dt(user['created_at']))}"  # [V6]
    )

    if tag_rows:  # [ADM4-1]
        text += "\n🏷 الوسوم: " + "، ".join(
            esc(x["tag"]) for x in tag_rows
        )

    if note_rows:  # [ADM2-2]
        text += "\n🗒 <b>ملاحظات الإدارة:</b>"
        for nr in note_rows:
            text += f"\n• {esc(nr['note'])} ({esc(nr['created_at'])[:10]})"

    ban_label = (
        "✅ فك الحظر" if user["is_banned"] else "🚫 حظر"
    )

    b = InlineKeyboardBuilder()
    b.button(text="💰 ±رصيد", callback_data=f"ucard_adj:{tid}")
    b.button(text=ban_label, callback_data=f"ucard_ban:{tid}")
    b.button(text="💬 رسالة خاصة", callback_data=f"ucard_msg:{tid}")
    b.button(text="🗒 ملاحظة", callback_data=f"ucard_note:{tid}")  # [ADM2-2]
    b.button(text="♻️ تراجع عن تعديل", callback_data=f"adjlist:{tid}")  # [ADM3-6]
    b.button(
        text="⏳ حظر مؤقت",
        callback_data=f"tban:{tid}",
    )  # [R6-PLUS3]
    b.button(text="🎚 سقف سحب خاص",
             callback_data=f"ucap:{tid}")  # [R6-PLUS2]
    b.button(text="🏷 الوسوم", callback_data=f"ucard_tag:{tid}")  # [ADM4-1]
    b.button(text="📒 وجهاته", callback_data=f"ucard_accts:{tid}")  # [USR4-2]
    b.button(text="🔙 قائمة المستخدمين", callback_data="admin_users")
    b.adjust(2, 2, 2, 2, 2)

    return text, b.as_markup()


@dp.callback_query(F.data == "admin_user_search")
async def admin_user_search(cb: types.CallbackQuery, state: FSMContext):
    """[NEW 37] بدء البحث عن مستخدم."""

    if not await is_admin_or_supervisor(cb.from_user.id, "users"):
        await cb.answer("غير مصرّح.", show_alert=True)
        return

    await cb.answer()
    await state.clear()
    await state.set_state(AdminSearchFSM.query)

    await cb.message.answer(
        "🔍 أرسل Telegram ID أو اسم حساب الموقع:\n\nللإلغاء أرسل /cancel"
    , reply_markup=back_kb("admin_users"))


@dp.message(AdminSearchFSM.query)
async def admin_search_query(message: types.Message, state: FSMContext):
    """[NEW 37] تنفيذ البحث وعرض الكارت."""

    if not await is_admin_or_supervisor(message.from_user.id, "users"):
        await state.clear()
        return

    q = (message.text or "").strip()

    if not q or q.startswith("/"):
        await state.clear()
        return

    user = None

    if q.isdigit():
        user = await get_user(int(q))

    if not user:
        user = await get_user_by_site_username(q)

    if not user:
        await message.answer(
            "❌ لم يُعثر على مستخدم بهذا المعرف.\n"
            "حاول معرفاً آخر أو أرسل /cancel للإلغاء."
        )
        return

    text, kb = await render_user_card(user, message.from_user.id)
    await message.answer(text, reply_markup=kb)
    await state.clear()


@dp.callback_query(F.data.startswith("admin_user_card:"))
async def admin_user_card(cb: types.CallbackQuery, state: FSMContext):
    """[NEW 37] إعادة عرض الكارت من زر."""

    if not await is_admin_or_supervisor(cb.from_user.id, "users"):
        await cb.answer("غير مصرّح.", show_alert=True)
        return

    await state.clear()

    try:
        tid = int(cb.data.split(":", 1)[1])
    except (ValueError, IndexError):
        await cb.answer("معرف غير صالح.", show_alert=True)
        return

    user = await get_user(tid)

    if not user:
        await cb.answer("المستخدم غير موجود.", show_alert=True)
        return

    await cb.answer()
    text, kb = await render_user_card(user, cb.from_user.id)

    # [R6-PLUS9 V11] زر رجوع للشاشة الإدارية السابقة إن وُجدت
    prev = _last_admin_screen.get(cb.from_user.id)

    if prev:
        nb = InlineKeyboardBuilder()
        nb.button(text="🔙 رجوع للسابقة", callback_data="admin_back_last")

        for row in kb.inline_keyboard:
            nb.row(*row)

        kb = nb.as_markup()

    await safe_edit(cb.message, text, kb)


@dp.callback_query(F.data.startswith("admin_user_list:"))
async def admin_user_list(cb: types.CallbackQuery, state: FSMContext):
    """[NEW 37] قائمة المستخدمين بترقيم صفحات."""
    _last_admin_screen[cb.from_user.id] = cb.data  # [V11]

    if not await is_admin_or_supervisor(cb.from_user.id, "users"):
        await cb.answer("غير مصرّح.", show_alert=True)
        return

    await state.clear()

    try:
        page = max(0, int(cb.data.split(":", 1)[1]))
    except (ValueError, IndexError):
        page = 0

    page_size = 8

    db = await get_db()

    try:
        cur = await db.execute("SELECT COUNT(*) AS c FROM users")
        total = (await cur.fetchone())["c"]

        cur = await db.execute(
            """
            SELECT telegram_id, full_name, site_username, balance,
                   is_banned
            FROM users
            ORDER BY id
            LIMIT ? OFFSET ?
            """,
            (page_size, page * page_size),
        )
        rows = await cur.fetchall()
    finally:
        await db.close()

    if not rows:
        await cb.answer()
        await safe_edit(
            cb.message, "📭 لا يوجد مستخدمون.", back_kb("admin_users"),
        )
        return

    pages = max(1, math.ceil(total / page_size))

    lines = [f"📂 <b>المستخدمون</b> — صفحة {page + 1}/{pages} (المجموع {total})\n"]
    b = InlineKeyboardBuilder()

    for row in rows:
        flag = " 🚫" if row["is_banned"] else ""
        acc = f"👤 {esc(row['site_username'])}" \
            if row["site_username"] else "👤 —"
        lines.append(
            f"<code>{row['telegram_id']}</code> | "
            f"{esc((row['full_name'] or '—')[:18])} | "
            f"{acc} | "
            f"{await fmt_bal(cb.from_user.id, row['balance'])}{flag}"
        )
        b.button(
            text=f"👤 {row['telegram_id']}",
            callback_data=f"admin_user_card:{row['telegram_id']}",
        )

    nav = 1
    b.button(text=f"📄 {page + 1}/{pages}", callback_data="noop")  # [UI-5]
    if page > 0:
        b.button(text="⬅️", callback_data=f"admin_user_list:{page - 1}")
        nav += 1
    if page < pages - 1:
        b.button(text="➡️", callback_data=f"admin_user_list:{page + 1}")
        nav += 1

    b.button(text="🔙 رجوع", callback_data="admin_users")

    sizes = [3] * math.ceil(len(rows) / 3)
    if nav:
        sizes.append(nav)
    sizes.append(1)
    b.adjust(*sizes)

    await cb.answer()
    await safe_edit(cb.message, "\n".join(lines), b.as_markup())


@dp.callback_query(F.data.startswith("ucard_ban:"))
async def ucard_ban(cb: types.CallbackQuery, state: FSMContext):
    """[NEW 37] حظر/فك حظر من الكارت مباشرة."""

    if not await is_admin_or_supervisor(cb.from_user.id, "users"):
        await cb.answer("غير مصرّح.", show_alert=True)
        return

    await state.clear()

    try:
        tid = int(cb.data.split(":", 1)[1])
    except (ValueError, IndexError):
        await cb.answer("معرف غير صالح.", show_alert=True)
        return

    if tid == ADMIN_USER_ID:
        await cb.answer("لا يمكن حظر الأدمن الرئيسي.", show_alert=True)
        return

    user = await get_user(tid)

    if not user:
        await cb.answer("المستخدم غير موجود.", show_alert=True)
        return

    new_status = 0 if user["is_banned"] else 1
    await update_user(tid, is_banned=new_status)
    await audit(
        cb.from_user.id,
        "ban" if new_status else "unban",
        tid,
    )

    await cb.answer(
        "تم الحظر 🚫" if new_status else "تم فك الحظر ✅",
        show_alert=True,
    )

    user = await get_user(tid)
    text, kb = await render_user_card(user, cb.from_user.id)
    await safe_edit(cb.message, text, kb)


@dp.callback_query(F.data.startswith("ucard_adj:"))
async def ucard_adj(cb: types.CallbackQuery, state: FSMContext):
    """[NEW 37] اختصار تعديل الرصيد من الكارت (تعبئة مسبقة)."""

    if not await is_admin_or_supervisor(cb.from_user.id, "finance"):
        await cb.answer("غير مصرّح.", show_alert=True)
        return

    if not await pin_gate(cb):  # [ADM3-1]
        return

    await cb.answer()

    try:
        tid = int(cb.data.split(":", 1)[1])
    except (ValueError, IndexError):
        await cb.answer("معرف غير صالح.", show_alert=True)
        return

    await state.clear()
    await state.update_data(telegram_id=tid)
    await state.set_state(AdminAdjustBalanceFSM.amount)

    await cb.message.answer(
        f"💰 تعديل رصيد <code>{tid}</code>\n\n"
        "أرسل مقدار التعديل:\n"
        "<code>+100</code> لإضافة | <code>-50</code> لخصم\n\n"
        "للإلغاء أرسل /cancel"
    , reply_markup=back_kb(f"admin_user_card:{tid}"))


@dp.callback_query(F.data.startswith("ucard_msg:"))
async def ucard_msg(cb: types.CallbackQuery, state: FSMContext):
    """[NEW 38] بدء مراسلة مستخدم من الإدارة."""

    if not await is_admin_or_supervisor(cb.from_user.id, "users"):
        await cb.answer("غير مصرّح.", show_alert=True)
        return

    await cb.answer()

    try:
        tid = int(cb.data.split(":", 1)[1])
    except (ValueError, IndexError):
        await cb.answer("معرف غير صالح.", show_alert=True)
        return

    await state.clear()
    await state.update_data(dm_target=tid)
    await state.set_state(AdminMessageFSM.text)

    await cb.message.answer(
        f"💬 أرسل نص الرسالة إلى <code>{tid}</code>:\n\nللإلغاء أرسل /cancel"
    , reply_markup=back_kb(f"admin_user_card:{tid}"))


@dp.message(AdminMessageFSM.text)
async def admin_dm(message: types.Message, state: FSMContext):
    """[NEW 38] إرسال رسالة الإدارة إلى المستخدم."""

    if not await is_admin_or_supervisor(message.from_user.id, "users"):
        await state.clear()
        return

    raw = (message.text or "").strip()

    if not raw or raw.startswith("/"):
        await state.clear()
        return

    data = await state.get_data()
    tid = data.get("dm_target")

    if not tid:
        await state.clear()
        return

    try:
        await bot.send_message(
            tid,
            f"📩 <b>رسالة من الإدارة:</b>\n\n{esc(raw)}",
        )
    except Exception as exc:
        logger.warning("تعذر إرسال رسالة الإدارة: %s", exc)
        await message.answer(
            "❌ تعذر الإرسال — قد يكون المستخدم لم يبدأ البوت."
        )
        await state.clear()
        return

    await state.clear()
    await audit(  # [NEW 22]
        message.from_user.id, "admin_dm", tid, f"len={len(raw)}",
    )

    await message.answer(
        f"✅ وصلت الرسالة إلى <code>{tid}</code>.",
        reply_markup=back_kb("admin_users"),
    )


# ============================================================
# SUPPORT TICKETS + UNIFIED INBOX [NEW 38]
# ============================================================

def _support_hours_str(raw: str):
    """[R6-PLUS5] تحليل نص الساعات «09:00-23:00» → (from, to)."""
    raw = (raw or "").strip()

    m = re.fullmatch(r"(\d{1,2}):(\d{2})\s*-\s*(\d{1,2}):(\d{2})", raw)

    if not m:
        return None

    h1, m1, h2, m2 = map(int, m.groups())

    if not (0 <= h1 <= 23 and 0 <= h2 <= 23
            and 0 <= m1 <= 59 and 0 <= m2 <= 59):
        return None

    return (h1 * 60 + m1, h2 * 60 + m2, raw)


async def support_open_now():
    """[R6-PLUS5] هل الدعم متاح الآن؟ (بلا إعدادات = دائماً)."""
    raw = await get_setting("support_hours") or ""

    if not raw.strip():
        return True

    parsed = _support_hours_str(raw)

    if not parsed:
        return True

    start, end, _ = parsed
    now_m = datetime.now(timezone.utc).hour * 60 + \
        datetime.now(timezone.utc).minute

    if start <= end:
        return start <= now_m < end

    return now_m >= start or now_m < end  # فترة تعبر منتصف الليل


@dp.callback_query(F.data == "support_start")
async def support_start(cb: types.CallbackQuery, state: FSMContext):
    """[NEW 38] بدء محادثة دعم للمستخدم."""

    if not await user_allowed(cb.from_user.id):
        await cb.answer("غير مسموح.", show_alert=True)
        return

    lang = await user_lang(cb.from_user.id)
    await cb.answer()
    await state.clear()
    await state.set_state(SupportFSM.message)

    await cb.message.answer(tr(lang, "support_prompt"))


@dp.message(SupportFSM.message)
async def support_message(message: types.Message, state: FSMContext):
    """[NEW 38] استلام رسالة الدعم وتحويلها للإدارة كتذكرة."""

    if not await user_allowed(message.from_user.id, message):
        return

    raw = (message.text or "").strip()

    if not raw or raw.startswith("/"):
        await state.clear()
        return

    # [AUDIT F6] إلحاق سياق المساعدة (شحن/سحب) بالتذكرة
    flow_ctx = (await state.get_data()).get("flow_ctx") or ""
    prefix = {
        "dep": "🛒 [استفسار شحن] ",
        "wd": "🏦 [استفسار سحب] ",
    }.get(flow_ctx, "")

    db = await get_db()

    try:
        cur = await db.execute(
            """
            INSERT INTO support_tickets
            (user_tid, message, status, created_at)
            VALUES (?, ?, 'open', ?)
            """,
            (message.from_user.id, (prefix + raw)[:2000], now_iso()),
        )
        ticket_id = cur.lastrowid
        await db.commit()
    finally:
        await db.close()

    lang = await user_lang(message.from_user.id)

    kb = InlineKeyboardBuilder()
    kb.button(text="✉️ رد", callback_data=f"ticket_reply:{ticket_id}")
    kb.button(text="✖ إغلاق", callback_data=f"ticket_close:{ticket_id}")
    kb.adjust(2)

    try:
        await bot.send_message(
            ADMIN_USER_ID,
            f"💬 <b>تذكرة دعم جديدة</b> #{ticket_id}\n"
            f"👤 <code>{message.from_user.id}</code>\n\n"
            f"{esc(raw)}",
            reply_markup=kb.as_markup(),
        )
        await mirror(  # [ADM3-2]
            f"💬 <b>تذكرة دعم جديدة</b> #{ticket_id}\n"
            f"👤 <code>{message.from_user.id}</code>\n\n"
            f"{esc(raw)}"
        )
    except Exception as exc:
        logger.warning("تعذر إرسال التذكرة للأدمن: %s", exc)

    await message.answer(tr(lang, "support_sent"))

    # [R6-PLUS5] ساعات عمل الدعم: تنويه لطيف خارج الأوقات
    if not await support_open_now():
        hours_raw = (await get_setting("support_hours") or "").strip()

        try:
            await bot.send_message(
                message.from_user.id,
                r6t(lang, "support_closed").format(h=hours_raw),
            )
        except Exception:
            pass
    await state.clear()


async def render_tickets_page(page: int):
    """[NEW 38] صفحة التذاكر المفتوحة مع أزرار الرد والإغلاق."""
    page_size = 5

    db = await get_db()

    try:
        cur = await db.execute(
            "SELECT COUNT(*) AS c FROM support_tickets WHERE status='open'"
        )
        total = (await cur.fetchone())["c"]

        cur = await db.execute(
            """
            SELECT id, user_tid, message, created_at
            FROM support_tickets
            WHERE status = 'open'
            ORDER BY id DESC
            LIMIT ? OFFSET ?
            """,
            (page_size, page * page_size),
        )
        rows = await cur.fetchall()
    finally:
        await db.close()

    if not rows:
        return (
            "📭 لا توجد تذاكر مفتوحة.",
            back_kb("admin_inbox"),
        )

    pages = max(1, math.ceil(total / page_size))
    page = min(page, pages - 1)

    lines = [
        f"💬 <b>التذاكر المفتوحة</b> — صفحة {page + 1}/{pages}"
        f" (المجموع {total})\n"
    ]
    b = InlineKeyboardBuilder()

    for row in rows:
        preview = esc((row["message"] or "")[:60])
        lines.append(
            f"#{row['id']} | 👤 <code>{row['user_tid']}</code>\n"
            f"{preview}\n"
            f"🕐 {esc(row['created_at'])}"
        )
        b.button(text=f"✉️ #{row['id']}",
                 callback_data=f"ticket_reply:{row['id']}")
        b.button(text=f"✖ #{row['id']}",
                 callback_data=f"ticket_close:{row['id']}")

    nav = 1
    b.button(text=f"📄 {page + 1}/{pages}", callback_data="noop")  # [UI-5]
    if page > 0:
        b.button(text="⬅️", callback_data=f"admin_tickets:{page - 1}")
        nav += 1
    if page < pages - 1:
        b.button(text="➡️", callback_data=f"admin_tickets:{page + 1}")
        nav += 1

    b.button(text="💬 قوالب الرد", callback_data="admin_canned")  # [ADM3-9]
    b.button(text="🔙 رجوع", callback_data="admin_inbox")

    sizes = [2] * len(rows)
    if nav:
        sizes.append(nav)
    sizes.append(1)
    b.adjust(*sizes)

    return "\n\n".join(lines), b.as_markup()


@dp.callback_query(F.data.startswith("admin_tickets:"))
async def admin_tickets(cb: types.CallbackQuery, state: FSMContext):
    """[NEW 38] عرض التذاكر المفتوحة."""

    if not await is_admin_or_supervisor(cb.from_user.id):
        await cb.answer("غير مصرّح.", show_alert=True)
        return

    await state.clear()

    try:
        page = max(0, int(cb.data.split(":", 1)[1]))
    except (ValueError, IndexError):
        page = 0

    await cb.answer()
    text, kb = await render_tickets_page(page)
    await safe_edit(cb.message, text, kb)


@dp.callback_query(F.data == "admin_inbox")
async def admin_inbox(cb: types.CallbackQuery, state: FSMContext):
    _last_admin_screen[cb.from_user.id] = "admin_inbox"  # [V11]
    """[NEW 38] الطابور الموحد لكل ما يحتاج قراراً."""

    if not await is_admin_or_supervisor(cb.from_user.id):
        await cb.answer("غير مصرّح.", show_alert=True)
        return

    await state.clear()

    db = await get_db()

    try:
        cur = await db.execute(
            "SELECT COUNT(*) AS c FROM finance_requests"
            " WHERE status = 'pending'"
        )
        finance_n = (await cur.fetchone())["c"]

        cur = await db.execute(
            "SELECT COUNT(*) AS c FROM payouts"
            " WHERE status IN ('pending','processing')"
        )
        payouts_n = (await cur.fetchone())["c"]

        cur = await db.execute(
            "SELECT COUNT(*) AS c FROM support_tickets"
            " WHERE status = 'open'"
        )
        tickets_n = (await cur.fetchone())["c"]

        cur = await db.execute(
            "SELECT COUNT(*) AS c FROM finance_requests"
            " WHERE status = 'awaiting_admin'"
        )
        awaiting_n = (await cur.fetchone())["c"]  # [ADM-2]
    finally:
        await db.close()

    status = await admin_status_line()  # [UI-1]
    text = (
        f"🧾 <b>الطابور الموحد</b>\n{status}\n\n"
        f"📋 طلبات مالية معلقة: {finance_n}\n"
        f"🚀 مدفوعات معلقة: {payouts_n}\n"
        f"💬 تذاكر دعم مفتوحة: {tickets_n}\n"
        f"👁 بانتظار موافقتك: {awaiting_n}"  # [ADM-2]
    )

    b = InlineKeyboardBuilder()
    b.button(
        text=f"📋 الطلبات ({finance_n})",
        callback_data="admin_finance_pending",
    )
    b.button(
        text=f"🚀 المدفوعات ({payouts_n})",
        callback_data="admin_payouts",
    )
    b.button(
        text=f"💬 التذاكر ({tickets_n})",
        callback_data="admin_tickets:0",
    )
    b.button(
        text="📊 ردود الدعم",
        callback_data="sup_reply_stats",
    )  # [R6-PLUS5]
    b.button(text="🔙 رجوع", callback_data="admin_panel")
    b.adjust(1)

    await cb.answer()
    await safe_edit(cb.message, text, b.as_markup())


@dp.callback_query(F.data.startswith("ticket_reply:"))
async def ticket_reply(cb: types.CallbackQuery, state: FSMContext):
    """[NEW 38] بدء الرد على تذكرة."""

    if not await is_admin_or_supervisor(cb.from_user.id):
        await cb.answer("غير مصرّح.", show_alert=True)
        return

    try:
        ticket_id = int(cb.data.split(":", 1)[1])
    except (ValueError, IndexError):
        await cb.answer("تذكرة غير صالحة.", show_alert=True)
        return

    db = await get_db()

    try:
        cur = await db.execute(
            "SELECT user_tid, status FROM support_tickets WHERE id = ?",
            (ticket_id,),
        )
        row = await cur.fetchone()
    finally:
        await db.close()

    if not row or row["status"] != "open":
        await cb.answer("التذكرة مغلقة أو غير موجودة.", show_alert=True)
        return

    await cb.answer()
    await state.clear()
    await state.update_data(ticket_id=ticket_id, ticket_user=row["user_tid"])
    await state.set_state(AdminTicketReplyFSM.text)

    await cb.message.answer(
        f"✉️ أرسل نص الرد على التذكرة #{ticket_id}\n"
        f"للمستخدم <code>{row['user_tid']}</code>:\n\nللإلغاء أرسل /cancel"
    , reply_markup=back_kb("admin_inbox"))

    # [ADM3-9] أزرار الردود الجاهزة (إن وجدت)
    db2 = await get_db()

    try:
        cur2 = await db2.execute(
            "SELECT id, title FROM canned_replies ORDER BY id LIMIT 8"
        )
        canned_rows = await cur2.fetchall()
    finally:
        await db2.close()

    if canned_rows:
        ckb = InlineKeyboardBuilder()

        for crow in canned_rows:
            ckb.button(
                text=f"💬 {crow['title']}",
                callback_data=f"cuse:{ticket_id}:{crow['id']}",
            )

        ckb.adjust(2)
        await cb.message.answer(
            "أو اختر رداً جاهزاً:",
            reply_markup=ckb.as_markup(),
        )


@dp.message(AdminTicketReplyFSM.text)
async def ticket_reply_send(message: types.Message, state: FSMContext):
    """[NEW 38] إرسال رد الإدارة على التذكرة."""

    if not await is_admin_or_supervisor(message.from_user.id):
        await state.clear()
        return

    raw = (message.text or "").strip()

    if not raw or raw.startswith("/"):
        await state.clear()
        return

    data = await state.get_data()
    ticket_id = data.get("ticket_id")
    user_tid = data.get("ticket_user")

    if not ticket_id:
        await state.clear()
        return

    lang = await user_lang(user_tid)

    # [R6-PLUS5] توقيع مشرف الدعم على الرد (الاسم من تلجرام)
    staff_name = (
        getattr(message.from_user, "full_name", "") or ""
    ).strip()

    if staff_name:
        raw = f"{raw}\n\n— دعم {staff_name}"

    try:
        await bot.send_message(
            user_tid,
            tr(lang, "support_reply", msg=esc(raw)),
            reply_markup=_ticket_rate_kb(ticket_id),  # [USR2-7]
        )
    except Exception as exc:
        logger.warning("تعذر إرسال رد التذكرة: %s", exc)
        await message.answer(
            "❌ تعذر الوصول للمستخدم (ربما لم يبدأ البوت)."
        )
        await state.clear()
        return

    db = await get_db()

    try:
        await db.execute(
            """
            UPDATE support_tickets
            SET status = 'answered',
                answered_at = ?,
                answered_by = ?
            WHERE id = ?
              AND status = 'open'
            """,
            (now_iso(), message.from_user.id, ticket_id),
        )
        await db.commit()
    finally:
        await db.close()

    await state.clear()
    await audit(  # [NEW 22]
        message.from_user.id, "ticket_reply", f"ticket={ticket_id}",
        f"user={user_tid}",
    )

    await message.answer(
        f"✅ تم الرد على التذكرة #{ticket_id}.",
        reply_markup=back_kb("admin_inbox"),
    )


@dp.callback_query(F.data.startswith("ticket_close:"))
async def ticket_close(cb: types.CallbackQuery, state: FSMContext):
    """[NEW 38] إغلاق تذكرة بدون رد."""

    if not await is_admin_or_supervisor(cb.from_user.id):
        await cb.answer("غير مصرّح.", show_alert=True)
        return

    try:
        ticket_id = int(cb.data.split(":", 1)[1])
    except (ValueError, IndexError):
        await cb.answer("تذكرة غير صالحة.", show_alert=True)
        return

    db = await get_db()

    try:
        cur = await db.execute(
            """
            UPDATE support_tickets
            SET status = 'closed',
                answered_at = ?,
                answered_by = ?
            WHERE id = ?
              AND status = 'open'
            """,
            (now_iso(), cb.from_user.id, ticket_id),
        )
        changed = cur.rowcount
        await db.commit()
    finally:
        await db.close()

    if not changed:
        await cb.answer("التذكرة مغلقة أو غير موجودة.", show_alert=True)
        return

    await audit(  # [NEW 22]
        cb.from_user.id, "ticket_close", f"ticket={ticket_id}",
    )
    await cb.answer("تم إغلاق التذكرة ✅", show_alert=True)

    text, kb = await render_tickets_page(0)
    await safe_edit(cb.message, text, kb)


# ============================================================
# SUPERVISOR SUSPEND [NEW 40]
# ============================================================

@dp.callback_query(F.data == "admin_sup_suspend")
async def admin_sup_suspend(cb: types.CallbackQuery, state: FSMContext):
    """[NEW 40] إيقاف/تشغيل مشرف مؤقتاً."""

    if cb.from_user.id != ADMIN_USER_ID:
        await cb.answer("للأدمن الرئيسي فقط.", show_alert=True)
        return

    await cb.answer()
    await state.clear()
    await state.set_state(AdminSuspendFSM.telegram_id)

    await cb.message.answer(
        "أرسل Telegram ID للمشرف لإيقافه أو تشغيله:\n\nللإلغاء أرسل /cancel"
    , reply_markup=back_kb("admin_supervisors"))


@dp.message(AdminSuspendFSM.telegram_id)
async def admin_suspend_tid(message: types.Message, state: FSMContext):
    """[NEW 40] تنفيذ الإيقاف/التشغيل."""

    if message.from_user.id != ADMIN_USER_ID:
        await state.clear()
        return

    try:
        telegram_id = int((message.text or "").strip())
    except Exception:
        await message.answer("❌ ID غير صالح.\n\nللإلغاء أرسل /cancel")
        return

    if telegram_id == ADMIN_USER_ID:
        await message.answer("❌ لا يمكن إيقاف الأدمن الرئيسي.")
        await state.clear()
        return

    db = await get_db()

    try:
        cur = await db.execute(
            "SELECT suspended FROM supervisors WHERE telegram_id = ?",
            (telegram_id,),
        )
        row = await cur.fetchone()

        if not row:
            await message.answer("❌ المشرف غير موجود.")
            await state.clear()
            return

        new_status = 0 if row["suspended"] else 1

        await db.execute(
            "UPDATE supervisors SET suspended = ? WHERE telegram_id = ?",
            (new_status, telegram_id),
        )
        await db.commit()
    finally:
        await db.close()

    await audit(  # [NEW 22]
        message.from_user.id,
        "supervisor_suspend" if new_status else "supervisor_resume",
        telegram_id,
    )

    state_text = (
        "⏸ تم إيقاف المشرف مؤقتاً (الصلاحيات مجمّدة)."
        if new_status
        else "▶️ تم تشغيل المشرف من جديد."
    )

    await message.answer(
        f"{state_text}\nTelegram ID: <code>{telegram_id}</code>",
        reply_markup=admin_supervisors_kb(),
    )

    await state.clear()


# ============================================================
# SCHEDULED MAINTENANCE [NEW 45]
# ============================================================

@dp.callback_query(F.data == "admin_maintenance")
async def admin_maintenance(cb: types.CallbackQuery, state: FSMContext):
    """[NEW 45] ضبط نافذة الصيانة المجدولة."""

    if cb.from_user.id != ADMIN_USER_ID:
        await cb.answer("للأدمن الرئيسي فقط.", show_alert=True)
        return

    await cb.answer()
    await state.clear()
    await state.set_state(AdminMaintenanceFSM.value)

    current = (await get_setting("maintenance_window") or "").strip()

    current_txt = current if current else "معطّلة"

    await cb.message.answer(
        "🕐 <b>الصيانة المجدولة</b>\n\n"
        f"النافذة الحالية: <b>{esc(current_txt)}</b>\n\n"
        "أرسل النافذة بصيغة:\n"
        "<code>HH:MM-HH:MM</code> (بتوقيت UTC)\n"
        "مثال: <code>01:00-02:30</code>\n\n"
        "أرسل <code>0</code> لتعطيل الجدولة.\n"
        "للإلغاء أرسل /cancel"
    , reply_markup=back_kb("admin_settings_menu"))


@dp.message(AdminMaintenanceFSM.value)
async def admin_maintenance_save(message: types.Message, state: FSMContext):
    """[NEW 45] حفظ/تعطيل نافذة الصيانة."""

    if message.from_user.id != ADMIN_USER_ID:
        await state.clear()
        return

    raw = (message.text or "").strip()

    if not raw or raw.startswith("/"):
        await state.clear()
        return

    if raw == "0":
        await set_setting("maintenance_window", "")
        await state.clear()
        await audit(message.from_user.id, "maintenance_off")

        await message.answer(
            "✅ تم تعطيل الصيانة المجدولة.",
            reply_markup=back_kb("admin_panel"),
        )
        return

    match = re.fullmatch(r"(\d{1,2}):(\d{2})-(\d{1,2}):(\d{2})", raw)

    if not match:
        await message.answer(
            "❌ صيغة غير صحيحة.\n"
            "المثال الصحيح: <code>01:00-02:30</code>\n\n"
            "للإلغاء أرسل /cancel"
        )
        return

    sh, sm, eh, em = map(int, match.groups())

    if not (sh < 24 and eh < 24 and sm < 60 and em < 60):
        await message.answer(
            "❌ وقت غير منطقي.\n"
            "الساعات 0-23 والدقائق 0-59.\n\nللإلغاء أرسل /cancel"
        )
        return

    window = f"{sh:02d}:{sm:02d}-{eh:02d}:{em:02d}"

    await set_setting("maintenance_window", window)
    await state.clear()
    await audit(  # [NEW 22]
        message.from_user.id, "maintenance_set", window,
    )

    await message.answer(
        f"✅ تم ضبط نافذة الصيانة: <code>{window}</code> (UTC).\n\n"
        "سيعتبر البوت نفسه متوقفاً تلقائياً خلال هذه النافذة يومياً.",
        reply_markup=back_kb("admin_panel"),
    )


# ============================================================
# SMART ALERTS [NEW 46]
# ============================================================

_alerted_ids: set = set()
_last_congestion_ts: float = -1e12  # يسمح بأول تنبيه فوراً


async def check_smart_alerts():
    """
    [NEW 46] تنبيهات ذكية تُفحص مع كل دورة مهام (كل 10 دقائق):
    - مدفوعات معلقة أقدم من 12 ساعة
    - طلبات سحب ضخمة معلقة
    - تراكم الطلبات (ازدحام)
    كل تنبيه يُرسل مرة واحدة فقط لكل عنصر.
    """
    global _last_congestion_ts

    if len(_alerted_ids) > 5000:
        _alerted_ids.clear()

    alerts = []
    now = datetime.now(timezone.utc)
    cutoff12 = (now - timedelta(hours=12)).isoformat(timespec="seconds")

    db = await get_db()

    try:
        cur = await db.execute(
            """
            SELECT id, user_tid, amount
            FROM payouts
            WHERE status IN ('pending', 'processing')
              AND created_at < ?
            """,
            (cutoff12,),
        )
        stale_payouts = await cur.fetchall()

        threshold = await get_float_setting(
            "confirm_threshold", CONFIRM_THRESHOLD_DEFAULT
        )

        cur = await db.execute(
            """
            SELECT id, telegram_id, amount
            FROM finance_requests
            WHERE status = 'pending'
              AND type = 'withdraw'
              AND amount >= ?
            """,
            (threshold,),
        )
        big_reqs = await cur.fetchall()

        cur = await db.execute(
            "SELECT COUNT(*) AS c FROM finance_requests"
            " WHERE status = 'pending'"
        )
        pending_total = (await cur.fetchone())["c"]
    finally:
        await db.close()

    for p in stale_payouts:
        key = f"po_{p['id']}"

        if key in _alerted_ids:
            continue

        _alerted_ids.add(key)
        alerts.append(
            f"⏰ <b>أمر دفع معلق منذ +12 ساعة</b>\n"
            f"🆔 #{p['id']} | 👤 <code>{p['user_tid']}</code>"
            f" | 💵 {money(p['amount'])}"
        )

    for r in big_reqs:
        key = f"req_{r['id']}"

        if key in _alerted_ids:
            continue

        _alerted_ids.add(key)
        alerts.append(
            f"🚨 <b>طلب سحب ضخم معلق</b>\n"
            f"🆔 #{r['id']} | 👤 <code>{r['telegram_id']}</code>"
            f" | 💵 {money(r['amount'])}"
        )

    if pending_total > 20 and time.monotonic() - _last_congestion_ts > 3600:
        _last_congestion_ts = time.monotonic()
        alerts.append(
            f"📉 <b>تراكم طلبات</b>\n{pending_total} طلباً مالياً معلق"
            " — راجع الطابور الموحد."
        )

    # [R6-PLUS6] نمط «شحن ثم سحب فوري» — رقابة AML بسيطة
    if await feat_on("inst_dep_alert"):
        window_min = await get_float_setting(
            "inst_dep_window_min", 30.0,
        )

        if window_min > 0:
            db_f = await get_db()

            try:
                cur_f = await db_f.execute(
                    """
                    SELECT d.user_id AS uid, u.telegram_id AS tid
                    FROM transactions d
                    JOIN transactions w ON w.user_id = d.user_id
                      AND w.type IN ('withdraw', 'wd_hold')
                      AND (w.created_at > d.created_at
                           OR w.id > d.id)  -- نفس الثانية
                    JOIN users u ON u.id = d.user_id
                    WHERE d.type = 'deposit'
                      AND julianday(d.created_at) IS NOT NULL
                      AND (julianday(w.created_at)
                           - julianday(d.created_at)) * 1440 <= ?
                      AND d.created_at >= ?
                    GROUP BY d.user_id
                    """,
                    (
                        window_min,
                        (
                            now - timedelta(days=2)
                        ).isoformat(timespec="seconds"),
                    ),
                )
                instant_rows = await cur_f.fetchall()
            finally:
                await db_f.close()

            for r in instant_rows:
                key = f"inst_{r['uid']}"  # [AUDIT F2] مرة واحدة

                if key in _alerted_ids:
                    continue

                _alerted_ids.add(key)
                alerts.append(
                    "🚨 <b>شحن ثم سحب فوري</b>\n"
                    f"👤 <code>{r['tid']}</code> | "
                    f"خلال آخر {int(window_min)} دقيقة\n"
                    "راجع النمط — قد يكون تجربة أو غسلاً."
                )

    for text in alerts:
        try:
            await bot.send_message(
                ADMIN_USER_ID,
                f"🔔 <b>تنبيه إداري</b>\n\n{text}",
            )
            await mirror(f"🔔 <b>تنبيه إداري</b>\n\n{text}")  # [ADM3-2]
        except Exception as exc:
            logger.warning("تعذر إرسال التنبيه: %s", exc)


# [R6-PLUS6] D8 — عدّاد فشل الإرسال المتتالي (انسداد البوت)
_FAIL_STREAK: dict = {}


async def notify_user_guarded(telegram_id: int, text: str) -> bool:
    """[R6-PLUS6] إرسال مع رصد الانسداد: 3 إخفاقات متتالية → تنبيه.

    يعيد True إذا وصلت الرسالة. يُستخدم في الإشعارات الدورية
    (الملخص الأسبوعي، هدية الذكرى، الرجوع للغائبين).
    """
    ok = True

    try:
        await bot.send_message(telegram_id, text)
        _FAIL_STREAK.pop(telegram_id, None)
    except Exception as exc:
        ok = False
        n = _FAIL_STREAK.get(telegram_id, 0) + 1
        _FAIL_STREAK[telegram_id] = n

        if n >= 3:
            _FAIL_STREAK.pop(telegram_id, None)

            try:
                await bot.send_message(
                    ADMIN_USER_ID,
                    "📵 <b>مستخدم يبدو أنه حظر البوت</b>\n\n"
                    f"👤 <code>{telegram_id}</code>\n"
                    f"فشل الإرسال {n} مرات متتالية"
                    " (آخر خطأ: "
                    f"{str(exc)[:60]})\n"
                    "اعرض كارته — إن أكد انسداده يُنصح بالحظر"
                    " أو الحذف لتخفيف القاعدة.",
                )
            except Exception:
                pass

    return ok



# ============================================================
# [UI-1..5] APPEARANCE & UX HELPERS
# ============================================================

async def admin_status_line() -> str:
    """[UI-1] شريط حالة حي يظهر أعلى شاشات الإدارة."""
    active = await is_bot_active()
    dot = "🟢 يعمل" if active else "🔴 متوقف"

    window = (await get_setting("maintenance_window") or "").strip()
    maint = ""
    if not active and _parse_maintenance_window(window):
        maint = f" | ⏸ {esc(window)}"

    db = await get_db()

    try:
        cur = await db.execute(
            "SELECT COUNT(*) AS c FROM finance_requests"
            " WHERE status = 'pending'"
        )
        fin = (await cur.fetchone())["c"]

        cur = await db.execute(
            "SELECT COUNT(*) AS c FROM support_tickets WHERE status='open'"
        )
        tkt = (await cur.fetchone())["c"]
    finally:
        await db.close()

    return f"{dot}{maint} | 📨 {fin} | 💬 {tkt}"


def _pw_kb(lang: str):
    """[UI-2] أزرار كشف/إخفاء كلمة السر."""
    b = InlineKeyboardBuilder()
    b.button(text=tr(lang, "btn_reveal"), callback_data="pw_reveal")
    b.button(text=tr(lang, "btn_del_now"), callback_data="pw_hide")
    b.adjust(2)
    return b.as_markup()


PW_CACHE: dict = {}


def _pw_remember(message_id, username, plain, lang):
    """[UI-2] تخزين مؤقت لكلمة السر المرتبطة برسالة محددة."""
    if len(PW_CACHE) > 50:
        PW_CACHE.clear()

    PW_CACHE[str(message_id)] = {
        "u": username,
        "p": plain,
        "lang": lang,
    }


async def _pw_autodelete(msg, delay: int = 30):
    """[UI-2] حذف رسالة كلمة السر تلقائياً بعد 30 ثانية."""

    async def _later():
        await asyncio.sleep(delay)
        PW_CACHE.pop(str(msg.message_id), None)
        try:
            await msg.delete()
        except Exception:
            pass

    asyncio.create_task(_later())


@dp.callback_query(F.data == "pw_reveal")
async def pw_reveal(cb: types.CallbackQuery, state: FSMContext):
    """[UI-2] كشف كلمة السر خلف Spoiler."""

    data = PW_CACHE.get(str(cb.message.message_id))

    if not data:
        await cb.answer("انتهت صلاحية الرسالة.", show_alert=True)
        return

    await cb.answer()

    try:
        await cb.message.edit_text(
            tr(data["lang"], "pw_revealed",
               u=esc(data["u"]), p=esc(data["p"])),
        )
    except Exception as exc:
        if "message is not modified" not in str(exc).lower():
            logger.warning("تعذر كشف كلمة السر: %s", exc)

    await _pw_autodelete(cb.message)


@dp.callback_query(F.data == "pw_hide")
async def pw_hide(cb: types.CallbackQuery, state: FSMContext):
    """[UI-2] إخفاء فوري عند الطلب."""

    await cb.answer("تم الإخفاء 🗑")
    PW_CACHE.pop(str(cb.message.message_id), None)

    try:
        await cb.message.delete()
    except Exception as exc:
        logger.warning("تعذر حذف رسالة كلمة السر: %s", exc)


async def menu_with_links(lang: str = "ar", user_id: int = None):
    """[UI-3 + R6] القائمة الرئيسية بواجهة 55bets + صف روابط قابل للضبط."""
    url = f"{BETS55_LOGIN_BASE}?accounts=%2A&login=%2A"
    is_admin = False

    if user_id:
        url = await _user_login_url(user_id)
        # [R6-PLUS4F] زر اللوحة يظهر للمشرف المصرّح له أيضاً
        is_admin = await is_admin_or_supervisor(user_id)

    badge = await _unread_announcements(user_id) > 0 \
        if user_id and await feat_on("offers_badge") \
        else False  # [R6-PLUS2 + R6-PLUS3]
    kb = await get_55bets_main_menu(url, is_admin, lang, offers_badge=badge)
    rows = [list(row) for row in kb.inline_keyboard]

    link_row = []

    for key, label_key in (
        ("link_channel", "lnk_channel"),
        ("link_site", "lnk_site"),
        ("link_support", "lnk_support"),
    ):
        u = (await get_setting(key) or "").strip()

        if u.startswith("http://") or u.startswith("https://"):
            link_row.append(
                types.InlineKeyboardButton(text=tr(lang, label_key), url=u)
            )

    if link_row:
        rows.append(link_row)

    return types.InlineKeyboardMarkup(inline_keyboard=rows)


def admin_links_kb():
    b = InlineKeyboardBuilder()
    b.button(text="🔙 رجوع", callback_data="admin_settings_menu")
    b.adjust(1)
    return b.as_markup()


@dp.callback_query(F.data == "admin_links")
async def admin_links(cb: types.CallbackQuery, state: FSMContext):
    """[UI-3] ضبط روابط القائمة الرئيسية (قناة/موقع/دعم)."""

    if cb.from_user.id != ADMIN_USER_ID:
        await cb.answer("للأدمن الرئيسي فقط.", show_alert=True)
        return

    await cb.answer()
    await state.clear()
    await state.set_state(AdminLinksFSM.value)

    cur = []
    for key in ("link_channel", "link_site", "link_support"):
        val = (await get_setting(key) or "").strip()
        cur.append(esc(val) if val else "—")

    await cb.message.answer(
        "🔗 <b>روابط القائمة الرئيسية</b>\n\n"
        f"الحالية:\n📢 {cur[0]}\n🌐 {cur[1]}\n💬 {cur[2]}\n\n"
        "أرسل ثلاثة روابط مفصولة بـ <code>|</code> بالترتيب:\n"
        "<code>قناة | موقع | دعم</code>\n"
        "مثال:\n"
        "<code>https://t.me/chan | https://site.com | https://t.me/help</code>\n\n"
        "أرسل <code>0</code> لإزالة كل الروابط.\n"
        "للإلغاء أرسل /cancel",
        reply_markup=admin_links_kb(),
    )


@dp.message(AdminLinksFSM.value)
async def admin_links_save(message: types.Message, state: FSMContext):
    """[UI-3] حفظ الروابط (الروابط غير الصالحة تُتجاهل)."""

    if message.from_user.id != ADMIN_USER_ID:
        await state.clear()
        return

    raw = (message.text or "").strip()

    if not raw or raw.startswith("/"):
        await state.clear()
        return

    if raw == "0":
        for key in ("link_channel", "link_site", "link_support"):
            await set_setting(key, "")

        await state.clear()
        await audit(message.from_user.id, "links_clear")

        await message.answer(
            "✅ أُزيلت كل الروابط من القائمة.",
            reply_markup=back_kb("admin_settings_menu"),
        )
        return

    parts = [p.strip() for p in raw.split("|")]

    if len(parts) != 3:
        await message.answer(
            "❌ أرسل ثلاثة روابط مفصولة بـ <code>|</code> بالضبط.\n\n"
            "للإلغاء أرسل /cancel"
        )
        return

    saved = skipped = 0

    for key, val in zip(
        ("link_channel", "link_site", "link_support"), parts,
    ):
        if val.startswith("http://") or val.startswith("https://"):
            await set_setting(key, val)
            saved += 1
        else:
            await set_setting(key, "")
            skipped += 1

    await state.clear()
    await audit(  # [NEW 22]
        message.from_user.id, "links_set", f"saved={saved}",
    )

    note = f" (تجاهل {skipped} غير صالح)" if skipped else ""
    await message.answer(
        f"✅ حُفظت {saved} رابطاً{note}.",
        reply_markup=back_kb("admin_settings_menu"),
    )


@dp.callback_query(F.data == "noop")
async def noop_cb(cb: types.CallbackQuery, state: FSMContext):
    """[UI-5] زر رقم الصفحة (غير تفاعلي)."""
    await cb.answer()



# ============================================================
# [ADM-1..6] ADMIN POWER TOOLS
# ============================================================

async def build_export_zip():
    """[NEW 43 + ADM-4] بناء الأرشيف الشامل — مشترك بين الزر والمجدول."""
    db = await get_db()

    try:
        cur = await db.execute(
            """
            SELECT telegram_id, username, full_name, site_username,
                   balance, is_banned, created_at
            FROM users ORDER BY id
            """
        )
        users_rows = [tuple(r) for r in await cur.fetchall()]

        cur = await db.execute(
            """
            SELECT t.id, u.telegram_id, t.type, t.amount, t.note,
                   t.created_at
            FROM transactions t
            JOIN users u ON u.id = t.user_id
            ORDER BY t.id DESC LIMIT ?
            """,
            (REPORT_ROW_LIMIT,),
        )
        tx_rows = [tuple(r) for r in await cur.fetchall()]

        cur = await db.execute(
            """
            SELECT id, telegram_id, type, amount, status,
                   created_at, processed_at, processed_by
            FROM finance_requests ORDER BY id DESC LIMIT ?
            """,
            (REPORT_ROW_LIMIT,),
        )
        req_rows = [tuple(r) for r in await cur.fetchall()]

        cur = await db.execute(
            """
            SELECT id, admin_id, action, target, details, created_at
            FROM admin_audit ORDER BY id DESC LIMIT ?
            """,
            (REPORT_ROW_LIMIT,),
        )
        audit_rows = [tuple(r) for r in await cur.fetchall()]
    finally:
        await db.close()

    tmp_path = DB_PATH + ".ziptmp"

    try:
        src_conn = sqlite3.connect(DB_PATH)
        dst_conn = sqlite3.connect(tmp_path)
        with dst_conn:
            src_conn.backup(dst_conn)
        dst_conn.close()
        src_conn.close()

        with open(tmp_path, "rb") as fh:
            db_bytes = fh.read()
    except Exception as exc:
        logger.warning("فشل نسخ القاعدة للأرشيف: %s", exc)
        return None, ""

    finally:
        try:
            os.remove(tmp_path)
        except OSError:
            pass

    zbuf = io.BytesIO()

    with zipfile.ZipFile(zbuf, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("users.csv", build_csv_bytes(
            ["telegram_id", "username", "full_name", "site_username",
             "balance", "is_banned", "created_at"],
            users_rows,
        ))
        zf.writestr("transactions.csv", build_csv_bytes(
            ["id", "telegram_id", "type", "amount", "note", "created_at"],
            tx_rows,
        ))
        zf.writestr("finance_requests.csv", build_csv_bytes(
            ["id", "telegram_id", "type", "amount", "status",
             "created_at", "processed_at", "processed_by"],
            req_rows,
        ))
        zf.writestr("admin_audit.csv", build_csv_bytes(
            ["id", "admin_id", "action", "target", "details", "created_at"],
            audit_rows,
        ))
        zf.writestr("database.db", db_bytes)

    zbuf.seek(0)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    doc = BufferedInputFile(
        zbuf.getvalue(),
        filename=f"export_{stamp}.zip",
    )
    caption = (
        "📦 الأرشيف الشامل\n"
        f"👥 {len(users_rows)} مستخدم | "
        f"💳 {len(tx_rows)} عملية | "
        f"📋 {len(req_rows)} طلب | "
        f"📜 {len(audit_rows)} تدقيق"
    )
    return doc, caption


@dp.callback_query(F.data == "admin_export_zip")
async def admin_export_zip(cb: types.CallbackQuery, state: FSMContext):
    """[NEW 43 + ADM-4] أرشيف شامل عند الطلب."""

    if cb.from_user.id != ADMIN_USER_ID:
        await cb.answer("للأدمن الرئيسي فقط.", show_alert=True)
        return

    if not await pin_gate(cb):  # [ADM3-1]
        return

    await state.clear()
    await cb.answer("جاري بناء الأرشيف...")

    doc, caption = await build_export_zip()

    if doc is None:
        await cb.message.answer("❌ تعذر بناء الأرشيف.")
        return

    try:
        await cb.message.answer_document(doc, caption=caption)
    except Exception as exc:
        logger.warning("تعذر إرسال الأرشيف: %s", exc)
        return

    await audit(cb.from_user.id, "export_zip")


async def scheduled_zip_if_due() -> bool:
    """[ADM-4] أرشيف ZIP يومي تلقائي بعد 09:00 UTC (تفعيل اختياري)."""
    if (await get_setting("export_zip_daily") or "0") != "1":
        return False

    now = datetime.now(timezone.utc)
    today = now.strftime("%Y-%m-%d")

    if (await get_setting("last_zip_export_date") or "") == today:
        return False

    if now.hour < 9:
        return False

    doc, caption = await build_export_zip()

    if doc is None:
        return False

    try:
        await bot.send_document(ADMIN_USER_ID, doc, caption=caption)
    except Exception as exc:
        logger.warning("تعذر إرسال الأرشيف المجدول: %s", exc)
        return False

    await set_setting("last_zip_export_date", today)
    return True


@dp.callback_query(F.data == "admin_ziptgl")
async def admin_ziptgl(cb: types.CallbackQuery, state: FSMContext):
    """[ADM-4] تفعيل/تعطيل التصدير اليومي."""

    if cb.from_user.id != ADMIN_USER_ID:
        await cb.answer("للأدمن الرئيسي فقط.", show_alert=True)
        return

    current = (await get_setting("export_zip_daily") or "0") == "1"
    new_value = "0" if current else "1"
    await set_setting("export_zip_daily", new_value)
    await audit(  # [NEW 22]
        cb.from_user.id, "zip_daily_toggle", new_value,
    )

    await cb.answer(
        "✅ التصدير اليومي مفعّل — يصلك كل يوم بعد 09:00 UTC"
        if new_value == "1"
        else "⛔ التصدير اليومي معطّل",
        show_alert=True,
    )


@dp.callback_query(F.data == "admin_backup_now")
async def admin_backup_now(cb: types.CallbackQuery, state: FSMContext):
    """[ADM-6] نسخة احتياطية فورية + فحص سلامة سريع."""

    if cb.from_user.id != ADMIN_USER_ID:
        await cb.answer("للأدمن الرئيسي فقط.", show_alert=True)
        return

    await state.clear()
    await cb.answer("جاري إنشاء النسخة...")

    now = datetime.now(timezone.utc)
    backup_path = DB_PATH + ".backup"

    try:
        src = sqlite3.connect(DB_PATH)
        dst = sqlite3.connect(backup_path)
        with dst:
            src.backup(dst)
        dst.close()
        src.close()
    except Exception as exc:
        logger.warning("فشل النسخ الاحتياطي: %s", exc)
        await cb.message.answer("❌ فشل إنشاء النسخة الاحتياطية.")
        return

    with open(backup_path, "rb") as fh:
        doc = BufferedInputFile(
            fh.read(),
            filename=f"backup_{now:%Y%m%d_%H%M%S}.db",
        )

    db = await get_db()

    try:
        cur = await db.execute("SELECT COUNT(*) AS c FROM users")
        users_n = (await cur.fetchone())["c"]
        cur = await db.execute("SELECT COUNT(*) AS c FROM transactions")
        tx_n = (await cur.fetchone())["c"]
        cur = await db.execute(
            "SELECT COUNT(*) AS c FROM finance_requests"
            " WHERE status = 'pending'"
        )
        pend_n = (await cur.fetchone())["c"]
    finally:
        await db.close()

    size_kb = os.path.getsize(DB_PATH) / 1024
    last = (await get_setting("last_backup_at") or "").strip() or "—"

    caption = (
        "🗄 <b>نسخة احتياطية فورية</b>\n\n"
        f"👥 المستخدمون: {users_n}\n"
        f"💳 العمليات: {tx_n}\n"
        f"📨 الطلبات المعلقة: {pend_n}\n"
        f"💾 حجم القاعدة: {size_kb:.0f} KB\n"
        f"🕐 آخر نسخة تلقائية: {esc(last)}"
    )

    try:
        await cb.message.answer_document(doc, caption=caption)
    except Exception as exc:
        logger.warning("تعذر إرسال النسخة: %s", exc)
        return

    await set_setting("last_backup_at", now.isoformat(timespec="seconds"))
    await audit(cb.from_user.id, "backup_now")


def render_pause_kb(dep: bool, wd: bool, auto: bool = False):
    """[ADM-3 + ADM2-6] أزرار إيقاف الخدمات."""
    b = InlineKeyboardBuilder()
    b.button(  # [ADM2-6]
        text="🤖 الحماية التلقائية: ✅" if auto else "🤖 الحماية التلقائية: ⛔",
        callback_data="admin_autoprotect",
    )
    b.button(
        text="🛑 الإيداعات موقوفة" if dep else "🟢 الإيداعات تعمل",
        callback_data="admin_pause_tgl:dep",
    )
    b.button(
        text="🛑 السحوبات موقوفة" if wd else "🟢 السحوبات تعمل",
        callback_data="admin_pause_tgl:wd",
    )
    b.button(text="✏️ سبب الإيداعات", callback_data="admin_pause_rs:dep")
    b.button(text="✏️ سبب السحوبات", callback_data="admin_pause_rs:wd")
    b.button(text="🔙 رجوع", callback_data="admin_settings_menu")
    b.adjust(1)
    return b.as_markup()


async def render_pause_text():
    """[ADM-3 + ADM2-6] نص لوحة إيقاف الخدمات."""
    dep = (await get_setting("deposits_paused") or "0") == "1"
    wd = (await get_setting("withdraws_paused") or "0") == "1"
    rdep = (await get_setting("pause_reason_dep") or "").strip()
    rwd = (await get_setting("pause_reason_wd") or "").strip()
    auto = (await get_setting("auto_protect") or "0") == "1"  # [ADM2-6]

    text = (
        "⏸️ <b>إيقاف الخدمات</b>\n\n"
        f"💰 الإيداعات: {'🛑 موقوفة' if dep else '🟢 تعمل'}\n"
        f"🏦 السحوبات: {'🛑 موقوفة' if wd else '🟢 تعمل'}\n"
        f"🤖 الحماية التلقائية: {'✅ مفعّلة' if auto else '⛔ معطّلة'}\n\n"
        f"✏️ سبب الإيداعات: {esc(rdep) if rdep else '—'}\n"
        f"✏️ سبب السحوبات: {esc(rwd) if rwd else '—'}\n\n"
        "الإيقاف يمنع بدء طلب جديد فقط — الطلبات المعلقة تبقى كما هي."
    )
    return text, render_pause_kb(dep, wd, auto)


@dp.callback_query(F.data == "admin_pause")
async def admin_pause(cb: types.CallbackQuery, state: FSMContext):
    """[ADM-3] لوحة إيقاف/تشغيل الإيداعات والسحوبات منفرداً."""

    if cb.from_user.id != ADMIN_USER_ID:
        await cb.answer("للأدمن الرئيسي فقط.", show_alert=True)
        return

    await cb.answer()
    await state.clear()
    text, kb = await render_pause_text()
    await safe_edit(cb.message, text, kb)


@dp.callback_query(F.data.startswith("admin_pause_tgl:"))
async def admin_pause_tgl(cb: types.CallbackQuery, state: FSMContext):
    """[ADM-3] تبديل حالة خدمة."""

    if cb.from_user.id != ADMIN_USER_ID:
        await cb.answer("للأدمن الرئيسي فقط.", show_alert=True)
        return

    which = cb.data.split(":", 1)[1]
    key = "deposits_paused" if which == "dep" else "withdraws_paused"

    current = (await get_setting(key) or "0") == "1"
    await set_setting(key, "0" if current else "1")
    await audit(  # [NEW 22]
        cb.from_user.id, "pause_toggle", which,
        "paused" if not current else "resumed",
    )
    await cb.answer("تم ✅")

    text, kb = await render_pause_text()
    await safe_edit(cb.message, text, kb)


@dp.callback_query(F.data.startswith("admin_pause_rs:"))
async def admin_pause_rs(cb: types.CallbackQuery, state: FSMContext):
    """[ADM-3] إدخال سبب الإيقاف (يظهر للمستخدمين)."""

    if cb.from_user.id != ADMIN_USER_ID:
        await cb.answer("للأدمن الرئيسي فقط.", show_alert=True)
        return

    which = cb.data.split(":", 1)[1]
    await cb.answer()
    await state.clear()

    if which == "dep":
        await state.set_state(AdminPauseFSM.reason_dep)
    else:
        await state.set_state(AdminPauseFSM.reason_wd)

    await cb.message.answer(
        "✏️ أرسل نص السبب الذي سيراه المستخدمون"
        " (أرسل <code>0</code> لمسحه):"
    , reply_markup=back_kb("admin_settings_menu"))


async def _save_pause_reason(message, state, key, audit_tag):
    if message.from_user.id != ADMIN_USER_ID:
        await state.clear()
        return

    raw = (message.text or "").strip()

    if not raw or raw.startswith("/"):
        await state.clear()
        return

    value = "" if raw == "0" else raw[:300]
    await set_setting(key, value)
    await state.clear()
    await audit(message.from_user.id, audit_tag, value[:50])

    note = "مُسح" if not value else f"«{esc(value[:80])}»"
    await message.answer(
        f"✅ السبب {note}.",
        reply_markup=back_kb("admin_settings_menu"),
    )


@dp.message(AdminPauseFSM.reason_dep)
async def pause_reason_dep_save(message: types.Message, state: FSMContext):
    """[ADM-3] حفظ سبب إيقاف الإيداعات."""
    await _save_pause_reason(message, state, "pause_reason_dep", "pause_reason_dep")


@dp.message(AdminPauseFSM.reason_wd)
async def pause_reason_wd_save(message: types.Message, state: FSMContext):
    """[ADM-3] حفظ سبب إيقاف السحوبات."""
    await _save_pause_reason(message, state, "pause_reason_wd", "pause_reason_wd")


@dp.callback_query(F.data == "admin_dual")
async def admin_dual(cb: types.CallbackQuery, state: FSMContext):
    """[ADM-2] ضبط عتبة الموافقة المزدوجة."""

    if cb.from_user.id != ADMIN_USER_ID:
        await cb.answer("للأدمن الرئيسي فقط.", show_alert=True)
        return

    await cb.answer()
    await state.clear()
    await state.set_state(AdminDualFSM.value)

    current = await get_float_setting("dual_approve_threshold", 0.0)
    current_txt = money(current) if current > 0 else "معطّلة (0)"

    await cb.message.answer(
        "👥 <b>الموافقة المزدوجة</b>\n\n"
        "أي سحب بمبلغ ≥ العتبة يعتمده مشرف يبقى معلقاً\n"
        "حتى تعتمده أنت شخصياً (العيون الأربع).\n\n"
        f"العتبة الحالية: <b>{current_txt}</b>\n\n"
        "أرسل المبلغ الجديد، أو <code>0</code> للتعطيل.\n"
        "للإلغاء أرسل /cancel"
    , reply_markup=back_kb("admin_settings_menu"))


@dp.message(AdminDualFSM.value)
async def admin_dual_save(message: types.Message, state: FSMContext):
    """[ADM-2] حفظ العتبة."""

    if message.from_user.id != ADMIN_USER_ID:
        await state.clear()
        return

    amount = parse_amount(message.text)  # [FIX 7]

    if amount is None:
        await message.answer(
            "❌ مبلغ غير صالح.\n\nللإلغاء أرسل /cancel"
        )
        return

    await set_setting("dual_approve_threshold", str(amount))
    await state.clear()
    await audit(  # [NEW 22]
        message.from_user.id, "dual_threshold_set", f"amount={amount}",
    )

    if amount > 0:
        await message.answer(
            f"✅ السحوبات ≥ {money(amount)} من المشرفين\n"
            "ستحتاج موافقتك النهائية.",
            reply_markup=back_kb("admin_settings_menu"),
        )
    else:
        await message.answer(
            "✅ أُوقفت الموافقة المزدوجة.",
            reply_markup=back_kb("admin_settings_menu"),
        )


@dp.callback_query(F.data == "admin_gift_batch")
async def admin_gift_batch(cb: types.CallbackQuery, state: FSMContext):
    """[ADM-1] بدء إنشاء دفعة أكواد."""

    if not await is_admin_or_supervisor(cb.from_user.id, "gifts"):
        await cb.answer("غير مصرّح.", show_alert=True)
        return

    await cb.answer()
    await state.clear()
    await state.set_state(AdminGiftBatchFSM.value)

    await cb.message.answer(
        "🎁 <b>دفعة أكواد</b>\n\n"
        "أرسل: <code>عدد مبلغ</code>\n"
        "مثال: <code>10 5</code> = عشرة أكواد بقيمة 5 لكل كود\n\n"
        "(العدد 1-50)\nللإلغاء أرسل /cancel"
    , reply_markup=back_kb("admin_gifts"))


@dp.message(AdminGiftBatchFSM.value)
async def admin_gift_batch_save(message: types.Message, state: FSMContext):
    """[ADM-1] توليد الدفعة وإرسال الأكواد."""

    if not await is_admin_or_supervisor(message.from_user.id, "gifts"):
        await state.clear()
        return

    parts = (message.text or "").strip().split()

    if len(parts) != 2 or not parts[0].isdigit():
        await message.answer(
            "❌ الصيغة: <code>عدد مبلغ</code>\n"
            "مثال: <code>10 5</code>\n\nللإلغاء أرسل /cancel"
        )
        return

    count = int(parts[0])

    if not (1 <= count <= 50):
        await message.answer("❌ العدد يجب أن يكون بين 1 و 50.")
        return

    amount = parse_amount(parts[1])  # [FIX 7]

    if amount is None:
        await message.answer("❌ مبلغ غير صالح.\n\nللإلغاء أرسل /cancel")
        return

    codes = []
    for _ in range(count):
        codes.append(await generate_unique_gift_code(amount))

    await audit(  # [NEW 22]
        message.from_user.id, "gift_batch",
        f"count={count}", f"amount={amount}",
    )

    lines = "\n".join(f"<code>{c}</code>" for c in codes)
    await message.answer(
        f"🎁 <b>أُنشئت {count} أكواد</b> بقيمة {money(amount)} للكود:\n\n"
        f"{lines}",
        reply_markup=admin_gifts_kb(),
    )
    await state.clear()



# ============================================================
# [USR-1..4] USER FEATURES
# ============================================================

@dp.callback_query(F.data == "my_tickets")
async def my_tickets(cb: types.CallbackQuery, state: FSMContext):
    """[USR-3] المستخدم يرى تذاكرة السابقة وحالتها."""

    if not await user_allowed(cb.from_user.id):
        await cb.answer("غير مسموح.", show_alert=True)
        return

    await cb.answer()
    await state.clear()
    lang = await user_lang(cb.from_user.id)

    db = await get_db()

    try:
        cur = await db.execute(
            """
            SELECT id, message, status, created_at, answered_at
            FROM support_tickets
            WHERE user_tid = ?
            ORDER BY id DESC
            LIMIT 10
            """,
            (cb.from_user.id,),
        )
        rows = await cur.fetchall()
    finally:
        await db.close()

    if not rows:
        await safe_edit(
            cb.message, tr(lang, "tk_none"), back_kb("menu_back", lang),
        )
        return

    icons = {
        "open": tr(lang, "tk_open"),
        "answered": tr(lang, "tk_answered"),
        "closed": tr(lang, "tk_closed"),
    }

    lines = [tr(lang, "tk_title")]

    for row in rows:
        status = icons.get(row["status"], row["status"])
        preview = esc((row["message"] or "")[:50])
        line = (
            f"#{row['id']} | {status}\n"
            f"{preview}\n"
            f"🕐 {esc(row['created_at'])}"
        )
        if row["status"] == "answered" and row["answered_at"]:
            line += f"\n↩️ رُدت: {esc(row['answered_at'])}"
        lines.append(line)

    b = InlineKeyboardBuilder()
    b.button(text=tr(lang, "tk_new"), callback_data="support_start")
    b.button(text=tr(lang, "back"), callback_data="menu_back")
    b.adjust(1)

    await safe_edit(cb.message, "\n\n".join(lines), b.as_markup())


@dp.callback_query(F.data == "history_pdf")
async def history_pdf(cb: types.CallbackQuery, state: FSMContext):
    """[USR-2] كشف حساب PDF بآخر 30 عملية."""

    if not await user_allowed(cb.from_user.id):
        await cb.answer("غير مسموح.", show_alert=True)
        return

    await cb.answer("جاري بناء الكشف...")
    await state.clear()
    lang = await user_lang(cb.from_user.id)

    user = await get_user(cb.from_user.id)

    if not user:
        await cb.answer("خطأ غير متوقع.", show_alert=True)
        return

    db = await get_db()

    try:
        cur = await db.execute(
            """
            SELECT type, amount, created_at
            FROM transactions
            WHERE user_id = ?
            ORDER BY id DESC
            LIMIT 30
            """,
            (user["id"],),
        )
        rows = await cur.fetchall()
    finally:
        await db.close()

    pdf_rows = []

    for row in rows:
        disp = round2(float(row["amount"]))
        if row["type"] in ("withdraw", "transfer_out"):
            disp = -disp
        pdf_rows.append((
            str(row["created_at"])[:16],
            f"{TX_ICONS.get(row['type'], '-')} {disp:+.2f}",
        ))

    if not pdf_rows:
        pdf_rows = [("-", "0.00")]

    doc = build_receipt_pdf("Account Statement", pdf_rows)  # [NEW 32]

    if doc is None:
        await cb.message.answer(tr(lang, "pdf_unavailable"))
        return

    caption = tr(
        lang, "pdf_caption",
        n=len(rows), bal=money(user["balance"]),
    )

    try:
        await cb.message.answer_document(doc, caption=caption)
    except Exception as exc:
        logger.warning("تعذر إرسال كشف الحساب: %s", exc)


# ---------- [USR-4] كود هدية من رصيد المستخدم ----------

@dp.callback_query(F.data == "gift_own")
async def gift_own_start(cb: types.CallbackQuery, state: FSMContext):
    """[USR-4] بدء إنشاء كود هدية من رصيد المستخدم."""

    if not await user_allowed(cb.from_user.id):
        await cb.answer("غير مسموح.", show_alert=True)
        return

    lang = await user_lang(cb.from_user.id)
    user = await get_user(cb.from_user.id)

    if not user:
        await cb.answer("خطأ غير متوقع.", show_alert=True)
        return

    await cb.answer()
    await state.clear()
    await state.set_state(UserGiftFSM.amount)

    await cb.message.answer(tr(
        lang, "gift_own_prompt", bal=money(user["balance"]),
    ))


@dp.message(UserGiftFSM.amount)
async def gift_own_amount(message: types.Message, state: FSMContext):
    """[USR-4] التحقق من المبلغ وطلب التأكيد."""

    if not await user_allowed(message.from_user.id, message):
        return

    raw = (message.text or "").strip()

    if not raw or raw.startswith("/"):
        await state.clear()
        return

    amount = parse_amount(raw)  # [FIX 7]

    if amount is None:
        await message.answer(
            "❌ مبلغ غير صالح.\n\nللإلغاء أرسل /cancel"
        )
        return

    user = await get_user(message.from_user.id)

    if not user or round2(float(user["balance"] or 0)) < amount:
        await state.clear()
        await message.answer(
            tr(await user_lang(message.from_user.id),
               "gift_own_insufficient")
        )
        return

    await state.update_data(own_amount=amount)
    lang = await user_lang(message.from_user.id)

    b = InlineKeyboardBuilder()
    b.button(text="✅ نعم، أصدر", callback_data="gift_own_ok")
    b.button(text="❌ إلغاء", callback_data="gift_own_no")
    b.adjust(2)

    await message.answer(
        tr(lang, "gift_own_confirm", amount=money(amount)),
        reply_markup=b.as_markup(),
    )


@dp.callback_query(F.data == "gift_own_ok")
async def gift_own_ok(cb: types.CallbackQuery, state: FSMContext):
    """[USR-4] الإصدار: خصم فوري + إنشاء الكود."""

    if not await user_allowed(cb.from_user.id):
        await cb.answer("غير مسموح.", show_alert=True)
        return

    data = await state.get_data()
    amount = data.get("own_amount")

    if not amount:
        await cb.answer("انتهت الجلسة — أعد المحاولة.", show_alert=True)
        return

    lang = await user_lang(cb.from_user.id)

    code = await generate_unique_gift_code(amount)

    db = await get_db()

    try:
        await db.execute("BEGIN IMMEDIATE")

        cur = await db.execute(
            "SELECT * FROM users WHERE telegram_id = ?",
            (cb.from_user.id,),
        )
        user = await cur.fetchone()

        if not user or round2(float(user["balance"] or 0)) < amount:
            await db.rollback()
            await cb.answer(
                tr(lang, "gift_own_insufficient"), show_alert=True,
            )
            await state.clear()
            return

        new_balance = round2(float(user["balance"] or 0) - amount)

        await db.execute(
            "UPDATE users SET balance = ? WHERE telegram_id = ?",
            (new_balance, cb.from_user.id),
        )
        await db.execute(
            """
            INSERT INTO transactions
            (user_id, type, amount, note, created_at)
            VALUES (?, 'gift_out', ?, ?, ?)
            """,
            (user["id"], amount, f"gift_code={code}", now_iso()),
        )
        await db.execute(
            "UPDATE gift_codes SET created_by = ? WHERE code = ?",
            (cb.from_user.id, code),
        )
        await db.commit()
    finally:
        await db.close()

    await state.clear()
    await cb.answer("تم إنشاء الكود 🎁", show_alert=True)

    await cb.message.answer(tr(
        lang, "gift_own_done", code=code, amount=money(amount),
    ))


@dp.callback_query(F.data == "gift_own_no")
async def gift_own_no(cb: types.CallbackQuery, state: FSMContext):
    """[USR-4] إلغاء."""
    await cb.answer("أُلغي.")
    await state.clear()


async def expire_user_gifts() -> int:
    """
    [USR-4] أكواد الهدايا الشخصية غير المستخدمة بعد 7 أيام:
    إلغاء + استرداد المبلغ لصانعها تلقائياً.
    """
    cutoff = (
        datetime.now(timezone.utc) - timedelta(days=7)
    ).isoformat(timespec="seconds")

    db = await get_db()

    try:
        await db.execute("BEGIN IMMEDIATE")

        cur = await db.execute(
            """
            SELECT code, amount, created_by
            FROM gift_codes
            WHERE created_by > 0
              AND used_by IS NULL
              AND created_at < ?
            """,
            (cutoff,),
        )
        rows = await cur.fetchall()

        if not rows:
            await db.rollback()
            return 0

        count = 0

        for row in rows:
            cur = await db.execute(
                """
                UPDATE gift_codes
                SET used_by = -1, used_at = ?
                WHERE code = ?
                  AND used_by IS NULL
                """,
                (now_iso(), row["code"]),
            )

            if cur.rowcount != 1:
                continue

            cur = await db.execute(
                "SELECT * FROM users WHERE telegram_id = ?",
                (row["created_by"],),
            )
            owner = await cur.fetchone()

            if owner:
                new_balance = round2(
                    float(owner["balance"] or 0) + float(row["amount"])
                )
                await db.execute(
                    "UPDATE users SET balance = ? WHERE telegram_id = ?",
                    (new_balance, row["created_by"]),
                )
                await db.execute(
                    """
                    INSERT INTO transactions
                    (user_id, type, amount, note, created_at)
                    VALUES (?, 'refund', ?, ?, ?)
                    """,
                    (
                        owner["id"], round2(float(row["amount"])),
                        f"expired_gift_code={row['code']}", now_iso(),
                    ),
                )

            count += 1

        await db.commit()
        return count
    except Exception:
        await db.rollback()
        raise
    finally:
        await db.close()


# ---------- [USR-1] التحويل بين المستخدمين ----------

async def _transfer_used_today(user_id: int) -> float:
    """[USR-1] مجموع تحويلات المستخدم الصادرة اليوم."""
    like = f"{datetime.now(timezone.utc):%Y-%m-%d}%"

    db = await get_db()

    try:
        cur = await db.execute(
            """
            SELECT COALESCE(SUM(amount), 0) AS s
            FROM transactions
            WHERE user_id = ?
              AND type = 'transfer_out'
              AND created_at LIKE ?
            """,
            (user_id, like),
        )
        return float((await cur.fetchone())["s"])
    finally:
        await db.close()


async def do_transfer(sender_tid: int, receiver_tid: int, amount: float):
    """
    [USR-1] نواة التحويل داخل معاملة واحدة.
    يعيد (ok, reason, new_sender_balance).
    """
    db = await get_db()

    try:
        await db.execute("BEGIN IMMEDIATE")

        cur = await db.execute(
            "SELECT * FROM users WHERE telegram_id = ?",
            (sender_tid,),
        )
        sender = await cur.fetchone()

        if not sender:
            await db.rollback()
            return False, "sender_missing", 0.0

        sender_balance = round2(float(sender["balance"] or 0))  # [FIX 7]

        if sender_balance < amount:
            await db.rollback()
            return False, "insufficient", sender_balance

        cur = await db.execute(
            "SELECT * FROM users WHERE telegram_id = ?",
            (receiver_tid,),
        )
        receiver = await cur.fetchone()

        if not receiver or receiver["is_banned"]:
            await db.rollback()
            return False, "receiver_invalid", sender_balance

        receiver_balance = round2(float(receiver["balance"] or 0))

        new_sender = round2(sender_balance - amount)  # [FIX 7]
        new_receiver = round2(receiver_balance + amount)  # [FIX 7]

        await db.execute(
            "UPDATE users SET balance = ? WHERE telegram_id = ?",
            (new_sender, sender_tid),
        )
        await db.execute(
            "UPDATE users SET balance = ? WHERE telegram_id = ?",
            (new_receiver, receiver_tid),
        )
        await db.execute(
            """
            INSERT INTO transactions
            (user_id, type, amount, note, created_at)
            VALUES (?, 'transfer_out', ?, ?, ?)
            """,
            (sender["id"], amount, f"to={receiver_tid}", now_iso()),
        )
        await db.execute(
            """
            INSERT INTO transactions
            (user_id, type, amount, note, created_at)
            VALUES (?, 'transfer_in', ?, ?, ?)
            """,
            (receiver["id"], amount, f"from={sender_tid}", now_iso()),
        )
        await db.commit()
        return True, "ok", new_sender
    except Exception:
        await db.rollback()
        raise
    finally:
        await db.close()


@dp.callback_query(F.data == "svc_transfer")
async def svc_transfer(cb: types.CallbackQuery, state: FSMContext):
    """[USR-1] بدء التحويل."""

    if not await user_allowed(cb.from_user.id):
        await cb.answer("غير مسموح.", show_alert=True)
        return

    lang = await user_lang(cb.from_user.id)
    await cb.answer()
    await state.clear()
    await state.set_state(TransferFSM.tid)

    await cb.message.answer(
        tr(lang, "tr_prompt_tid"),
        reply_markup=back_kb("menu_back", lang),
    )


@dp.message(TransferFSM.tid)
async def transfer_tid(message: types.Message, state: FSMContext):
    """[USR-1] استلام معرف المستلم."""

    if not await user_allowed(message.from_user.id, message):
        return

    raw = (message.text or "").strip()

    if not raw or raw.startswith("/"):
        await state.clear()
        return

    lang = await user_lang(message.from_user.id)

    if not raw.isdigit():
        await message.answer(
            "❌ أرسل Telegram ID رقمياً.\n\nللإلغاء أرسل /cancel"
        )
        return

    receiver_tid = int(raw)

    if receiver_tid == message.from_user.id:
        await state.clear()
        await message.answer(tr(lang, "tr_err_self"))
        return

    receiver = await get_user(receiver_tid)

    if not receiver:
        await message.answer(tr(lang, "tr_err_notfound") + "\n\n/cancel")
        return

    if receiver["is_banned"]:
        await state.clear()
        await message.answer(tr(lang, "tr_err_banned"))
        return

    sender = await get_user(message.from_user.id)
    name = receiver["full_name"] or str(receiver_tid)

    await state.update_data(tr_tid=receiver_tid, tr_name=name)
    await state.set_state(TransferFSM.amount)

    await message.answer(tr(
        lang, "tr_prompt_amount",
        name=esc(name),
        bal=money(sender["balance"] if sender else 0),
    ))


@dp.message(TransferFSM.amount)
async def transfer_amount(message: types.Message, state: FSMContext):
    """[USR-1] استلام المبلغ + السقف اليومي + طلب التأكيد."""

    if not await user_allowed(message.from_user.id, message):
        return

    amount = parse_amount(message.text)  # [FIX 7]

    if amount is None:
        await message.answer(
            "❌ مبلغ غير صالح.\n\nللإلغاء أرسل /cancel"
        )
        return

    lang = await user_lang(message.from_user.id)
    sender = await get_user(message.from_user.id)

    if not sender or round2(float(sender["balance"] or 0)) < amount:
        await message.answer(tr(lang, "tr_err_insufficient"))
        return

    cap = await get_float_setting("transfer_daily_cap", 0.0)  # [USR-1]

    if cap > 0:
        used = await _transfer_used_today(sender["id"])

        if round2(used + amount) > round2(cap):
            left = max(0.0, round2(cap - used))
            await message.answer(tr(
                lang, "tr_cap", cap=money(cap), left=money(left),
            ))
            return

    data = await state.get_data()
    receiver_tid = data.get("tr_tid")
    name = data.get("tr_name") or str(receiver_tid)

    if not receiver_tid:
        await state.clear()
        return

    await state.update_data(tr_amount=amount)
    await message.answer(
        tr(lang, "tr_confirm",
           tid=receiver_tid, name=esc(name), amount=money(amount)),
        reply_markup=_transfer_confirm_kb(),
    )


def _transfer_confirm_kb():
    b = InlineKeyboardBuilder()
    b.button(text="✅ تأكيد", callback_data="transfer_ok")
    b.button(text="❌ إلغاء", callback_data="transfer_no")
    b.adjust(2)
    return b.as_markup()


@dp.callback_query(F.data == "transfer_ok")
async def transfer_ok(cb: types.CallbackQuery, state: FSMContext):
    """[USR-1] التنفيذ داخل معاملة واحدة."""

    if not await user_allowed(cb.from_user.id):
        await cb.answer("غير مسموح.", show_alert=True)
        return

    data = await state.get_data()
    receiver_tid = data.get("tr_tid")
    amount = data.get("tr_amount")

    if not receiver_tid or not amount:
        await cb.answer("انتهت الجلسة — أعد المحاولة.", show_alert=True)
        return

    lang = await user_lang(cb.from_user.id)

    ok, reason, _balance = await do_transfer(
        cb.from_user.id, receiver_tid, amount,
    )

    if not ok:
        await cb.answer(
            tr(lang, "tr_err_insufficient")
            if reason == "insufficient"
            else tr(lang, "tr_err_banned"),
            show_alert=True,
        )
        await state.clear()
        return

    await state.clear()
    await cb.answer("تم التحويل ✅", show_alert=True)
    await cb.message.answer(tr(
        lang, "tr_done", amount=money(amount), tid=receiver_tid,
    ))

    try:
        await bot.send_message(
            receiver_tid,
            tr(await user_lang(receiver_tid), "tr_received",
               amount=money(amount), tid=cb.from_user.id),
        )
    except Exception as exc:
        logger.warning("تعذر إشعار مستلم التحويل: %s", exc)


@dp.callback_query(F.data == "transfer_no")
async def transfer_no(cb: types.CallbackQuery, state: FSMContext):
    """[USR-1] إلغاء التحويل."""
    await cb.answer("أُلغي التحويل.")
    await state.clear()



# ============================================================
# [USR2-1/2/5/6 + ADM2-2/5] ROUND 3 — PHASE 1
# ============================================================

_HIST_FILTERS = {
    "all": "",
    "deposit": " AND type = 'deposit'",
    "withdraw": " AND type = 'withdraw'",
    "transfer": " AND type IN ('transfer_in', 'transfer_out')",
    "gift": " AND type IN ('gift', 'gift_out')",
}  # [USR2-6]


def _hist_filter_sql(filt: str) -> str:
    """[USR2-6] جملة WHERE للفلتر المختار (آمنة — قائمة مغلقة)."""
    return _HIST_FILTERS.get(filt, "")


_RQ_STATUS_KEYS = {
    "pending": "rq_pending",
    "approved": "rq_approved",
    "rejected": "rq_rejected",
    "expired": "rq_expired",
    "awaiting_admin": "rq_awaiting",
}


async def render_my_requests(telegram_id: int, page: int, lang: str,
                             filt: str = "all"):
    """[USR2-1 + R6-PLUS2] طلباتي مع فلتر زمني."""
    page_size = 5

    cutoff = ""

    if filt == "week":
        cutoff = (
            datetime.now(timezone.utc) - timedelta(days=7)
        ).isoformat(timespec="seconds")
    elif filt == "month":
        cutoff = (
            datetime.now(timezone.utc) - timedelta(days=30)
        ).isoformat(timespec="seconds")

    db = await get_db()

    try:
        if cutoff:
            cur = await db.execute(
                "SELECT COUNT(*) AS c FROM finance_requests"
                " WHERE telegram_id = ? AND created_at >= ?",
                (telegram_id, cutoff),
            )
        else:
            cur = await db.execute(
                "SELECT COUNT(*) AS c FROM finance_requests"
                " WHERE telegram_id = ?",
                (telegram_id,),
            )
        total = (await cur.fetchone())["c"]

        if cutoff:
            cur = await db.execute(
                """
                SELECT id, type, amount, status, created_at, processed_at
                FROM finance_requests
                WHERE telegram_id = ? AND created_at >= ?
                ORDER BY id DESC
                LIMIT ? OFFSET ?
                """,
                (telegram_id, cutoff, page_size, page * page_size),
            )
        else:
            cur = await db.execute(
                """
                SELECT id, type, amount, status, created_at, processed_at
                FROM finance_requests
                WHERE telegram_id = ?
                ORDER BY id DESC
                LIMIT ? OFFSET ?
                """,
                (telegram_id, page_size, page * page_size),
            )
        rows = await cur.fetchall()
    finally:
        await db.close()

    if not rows:
        return (
            f"{tr(lang, 'rq_title')}\n\n{tr(lang, 'rq_none')}",
            back_kb("menu_back", lang),
        )

    pages = max(1, math.ceil(total / page_size))
    page = min(max(page, 0), pages - 1)

    icons = {"deposit": "💰", "withdraw": "🏦"}
    lines = [f"{tr(lang, 'rq_title')} — صفحة {page + 1}/{pages}"]  # [UI-5]

    for row in rows:
        status = tr(lang, _RQ_STATUS_KEYS.get(row["status"], "rq_pending"))
        icon = icons.get(row["type"], "📋")
        line = (
            f"{icon} {money(row['amount'])} | {status}\n"
            f"🆔 #{row['id']} | 🕐 {esc(row['created_at'])[:16]}"
        )
        if row["processed_at"]:
            line += f"\n⏱ {esc(row['processed_at'])[:16]}"
        lines.append(line)

    b = InlineKeyboardBuilder()

    # [R6-PLUS2] صف الفلاتر الزمنية
    for f, key in (("all", "rq_all"), ("week", "rq_week"),
                   ("month", "rq_month")):
        mark = "✓ " if filt == f else ""
        b.button(
            text=mark + r6t(lang, key),
            callback_data=f"my_requests:0:{f}",
        )

    nav = 1
    b.button(text=f"📄 {page + 1}/{pages}", callback_data="noop")  # [UI-5]
    if page > 0:
        b.button(text="⬅️", callback_data=f"my_requests:{page - 1}:{filt}")
        nav += 1
    if page < pages - 1:
        b.button(text="➡️", callback_data=f"my_requests:{page + 1}:{filt}")
        nav += 1
    b.button(text=tr(lang, "back"), callback_data="menu_back")

    sizes = [3]
    sizes += [3] * math.ceil(len(rows) / 3)
    sizes.append(nav)
    sizes.append(1)
    b.adjust(*sizes)

    return "\n\n".join(lines), b.as_markup()


@dp.callback_query(F.data.startswith("my_requests:"))
async def my_requests(cb: types.CallbackQuery, state: FSMContext):
    """[USR2-1] طلباتي المالية."""

    if not await user_allowed(cb.from_user.id):
        await cb.answer("غير مسموح.", show_alert=True)
        return

    await state.clear()

    parts = cb.data.split(":")
    try:
        page = max(0, int(parts[1]))
    except (ValueError, IndexError):
        page = 0

    filt = parts[2] if len(parts) > 2 and parts[2] in (
        "all", "week", "month",
    ) else "all"  # [R6-PLUS2]

    lang = await user_lang(cb.from_user.id)
    text, kb = await render_my_requests(
        cb.from_user.id, page, lang, filt,
    )
    await cb.answer()
    await safe_edit(cb.message, text, kb)


@dp.callback_query(F.data == "my_refs")
async def my_refs(cb: types.CallbackQuery, state: FSMContext):
    """[USR2-2] قائمة الإحالات + زر مشاركة الرابط."""

    if not await user_allowed(cb.from_user.id):
        await cb.answer("غير مسموح.", show_alert=True)
        return

    await cb.answer()
    await state.clear()
    lang = await user_lang(cb.from_user.id)

    db = await get_db()

    try:
        cur = await db.execute(
            """
            SELECT full_name, username, created_at
            FROM users
            WHERE referrer_id = ?
            ORDER BY id DESC LIMIT 10
            """,
            (cb.from_user.id,),
        )
        rows = await cur.fetchall()

        cur = await db.execute(
            "SELECT COUNT(*) AS c FROM users WHERE referrer_id = ?",
            (cb.from_user.id,),
        )
        total = (await cur.fetchone())["c"]

        cur = await db.execute(
            """
            SELECT COALESCE(SUM(amount), 0) AS s
            FROM transactions
            WHERE user_id = (SELECT id FROM users WHERE telegram_id = ?)
              AND type = 'referral'
            """,
            (cb.from_user.id,),
        )
        earned = float((await cur.fetchone())["s"])
    finally:
        await db.close()

    # [R6-PLUS4] زرا العدد والرابط يظهران دائماً
    common = InlineKeyboardBuilder()
    common.button(
        text=f"{r6t(lang, 'refs_count_btn')}: {total}",
        callback_data="noop",
    )
    common.button(
        text=r6t(lang, "ref_my_link"),
        callback_data="my_ref_link",
    )

    if not rows:
        common.button(text=tr(lang, "back"), callback_data="menu_back")
        common.adjust(1)
        await safe_edit(
            cb.message, tr(lang, "ref_none"), common.as_markup(),
        )
        return

    body = "".join(
        f"• {esc(r['full_name'] or r['username'] or '—')}"
        f" — {esc(r['created_at'])[:10]}\n"
        for r in rows
    )
    text = tr(
        lang, "ref_title", n=total, earned=money(earned),
    ) + body

    b = common

    if BOT_USERNAME:  # [USR2-2] مشاركة عبر t.me/share
        link = urllib.parse.quote(
            f"https://t.me/{BOT_USERNAME}?start=ref_{cb.from_user.id}",
            safe=":/?=&",
        )
        share_url = (
            "https://t.me/share/url?url=" + link
            + "&text=" + urllib.parse.quote("🎁 جرّب هذا البوت!")
        )
        b.button(text=tr(lang, "ref_share"), url=share_url)

    b.button(
        text=r6t(lang, "refs_top_btn"),
        callback_data="refs_top",
    )  # [R6-PLUS2]
    b.button(text=tr(lang, "back"), callback_data="menu_back")
    b.adjust(1)

    await safe_edit(cb.message, text, b.as_markup())


@dp.callback_query(F.data == "my_ref_link")
async def my_ref_link(cb: types.CallbackQuery, state: FSMContext):
    """[R6-PLUS4] رابط الإحالة الخاص بالمستخدم (محتسب بالنظام)."""

    if not await user_allowed(cb.from_user.id):
        await cb.answer("غير مسموح.", show_alert=True)
        return

    await cb.answer()
    await state.clear()
    lang = await user_lang(cb.from_user.id)

    if not BOT_USERNAME:
        await cb.answer("الرابط غير متاح حالياً.", show_alert=True)
        return

    link = f"https://t.me/{BOT_USERNAME}?start=ref_{cb.from_user.id}"

    b = InlineKeyboardBuilder()

    link_q = urllib.parse.quote(link, safe=":/?=&")
    b.button(
        text=tr(lang, "ref_share"),
        url=(
            "https://t.me/share/url?url=" + link_q
            + "&text=" + urllib.parse.quote("🎁 جرّب هذا البوت!")
        ),
    )
    b.button(text=tr(lang, "back"), callback_data="my_refs")
    b.adjust(1)

    await safe_edit(
        cb.message, r6t(lang, "ref_link_title").format(link=link),
        b.as_markup(),
    )


@dp.callback_query(F.data.startswith("qw:"))
async def quick_withdraw(cb: types.CallbackQuery, state: FSMContext):
    """[USR2-5] زر آخر مبلغ سحب — يعاد تمريره للتدفق كأنه مُدخل يدوياً."""

    if not await user_allowed(cb.from_user.id):
        await cb.answer("غير مسموح.", show_alert=True)
        return

    raw = cb.data.split(":", 1)[1]

    if not raw.replace(".", "", 1).isdigit():
        await cb.answer("قيمة غير صالحة.", show_alert=True)
        return

    await cb.answer()
    shim = SimpleNamespace(
        from_user=cb.from_user,
        text=raw,
        answer=cb.message.answer,
    )
    await withdraw_amount(shim, state)


_WH_ICONS = {
    "credited": "✅",
    "duplicate": "♻️",
    "conflict": "⚠️",
    "user_not_found": "👤",
    "invalid": "❌",
    "ignored": "➖",
}


@dp.callback_query(F.data == "admin_whlog")
async def admin_whlog(cb: types.CallbackQuery, state: FSMContext):
    """[ADM2-5] آخر 20 حدث ويب هوك للتشخيص السريع."""

    if not await is_admin_or_supervisor(cb.from_user.id):
        await cb.answer("غير مصرّح.", show_alert=True)
        return

    await cb.answer()
    await state.clear()

    db = await get_db()

    try:
        cur = await db.execute(
            """
            SELECT event_id, source, result, user_tid, amount, created_at
            FROM webhook_events
            ORDER BY rowid DESC LIMIT 20
            """
        )
        rows = await cur.fetchall()
    finally:
        await db.close()

    if not rows:
        await safe_edit(
            cb.message, "📭 لا توجد أحداث بعد.",
            back_kb("admin_tools_menu"),
        )
        return

    lines = ["🧾 <b>سجل أحداث الويب هوك</b> — آخر "
             f"{len(rows)}\n"]

    for row in rows:
        icon = _WH_ICONS.get(row["result"] or "", "•")
        eid = esc(str(row["event_id"])[:18])
        amt = f"{money(row['amount'])}" if row["amount"] else "—"
        lines.append(
            f"{icon} <code>{eid}</code>\n"
            f"👤 {row['user_tid'] or '—'} | 💵 {amt} | "
            f"🕐 {esc(row['created_at'])[:16]}"
        )

    await safe_edit(
        cb.message, "\n\n".join(lines), back_kb("admin_tools_menu"),
    )


async def _fetch_user_notes(target_tid: int, limit: int = 3) -> list:
    """[ADM2-2] آخر ملاحظات الإدارة عن مستخدم."""
    db = await get_db()

    try:
        cur = await db.execute(
            """
            SELECT note, created_at FROM user_notes
            WHERE target_tid = ?
            ORDER BY id DESC LIMIT ?
            """,
            (target_tid, limit),
        )
        return await cur.fetchall()
    finally:
        await db.close()


@dp.callback_query(F.data.startswith("ucard_note:"))
async def ucard_note(cb: types.CallbackQuery, state: FSMContext):
    """[ADM2-2] بدء إضافة ملاحظة إدارية على مستخدم."""

    if not await is_admin_or_supervisor(cb.from_user.id, "users"):
        await cb.answer("غير مصرّح.", show_alert=True)
        return

    try:
        tid = int(cb.data.split(":", 1)[1])
    except (ValueError, IndexError):
        await cb.answer("معرف غير صالح.", show_alert=True)
        return

    await cb.answer()
    await state.clear()
    await state.update_data(note_target=tid)
    await state.set_state(AdminNoteFSM.text)

    await cb.message.answer(
        f"🗒 أرسل الملاحظة عن المستخدم <code>{tid}</code>:\n\n"
        "للإلغاء أرسل /cancel"
    , reply_markup=back_kb(f"admin_user_card:{tid}"))


@dp.message(AdminNoteFSM.text)
async def admin_note_save(message: types.Message, state: FSMContext):
    """[ADM2-2] حفظ الملاحظة (تظهر في كارت المستخدم)."""

    if not await is_admin_or_supervisor(message.from_user.id, "users"):
        await state.clear()
        return

    raw = (message.text or "").strip()

    if not raw or raw.startswith("/"):
        await state.clear()
        return

    data = await state.get_data()
    tid = data.get("note_target")

    if not tid:
        await state.clear()
        return

    db = await get_db()

    try:
        await db.execute(
            """
            INSERT INTO user_notes
            (target_tid, author_id, note, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (tid, message.from_user.id, raw[:500], now_iso()),
        )
        await db.commit()
    finally:
        await db.close()

    await state.clear()
    await audit(  # [NEW 22]
        message.from_user.id, "user_note", tid, raw[:60],
    )

    await message.answer(
        f"✅ حُفظت الملاحظة عن <code>{tid}</code>.",
        reply_markup=back_kb("admin_users"),
    )



# ============================================================
# [ADM2-1/3/4/7 + USR2-7] ROUND 3 — PHASE 2
# ============================================================

_SEG_LABELS = {
    "all": "👥 الكل",
    "active": "🔥 نشطوا اليوم",
    "bal": "💰 حسب الرصيد",
    "ar": "🇸🇦 العربي فقط",
    "en": "🇬🇧 English only",
    "ru": "🇷🇺 Русский только",
    "inactive": "💤 غائبون 14+ يوماً",
}


async def broadcast_targets(segment: str, min_balance=None) -> list:
    """[ADM2-1] حلّ شريحة البث إلى قائمة معرفات."""
    db = await get_db()

    try:
        if segment == "active":
            like = f"{datetime.now(timezone.utc):%Y-%m-%d}%"
            cur = await db.execute(
                """
                SELECT DISTINCT u.telegram_id AS telegram_id
                FROM users u
                JOIN transactions t ON t.user_id = u.id
                WHERE u.is_banned = 0
                  AND t.created_at LIKE ?
                ORDER BY u.id
                """,
                (like,),
            )
        elif segment == "bal" and min_balance is not None:
            cur = await db.execute(
                "SELECT telegram_id FROM users"
                " WHERE is_banned = 0 AND balance >= ?"
                " ORDER BY id",
                (float(min_balance),),
            )
        elif segment in ("ar", "en", "ru"):
            cur = await db.execute(
                "SELECT telegram_id FROM users"
                " WHERE is_banned = 0 AND lang = ?"
                " ORDER BY id",
                (segment,),
            )
        elif segment == "inactive":  # [R6-PLUS3] غائبون عن الشحن
            cutoff = (
                datetime.now(timezone.utc) - timedelta(days=14)
            ).isoformat(timespec="seconds")
            cur = await db.execute(
                """
                SELECT u.telegram_id AS telegram_id FROM users u
                WHERE u.is_banned = 0
                  AND COALESCE(u.ban_until, '') = ''
                  AND u.created_at <= ?
                  AND NOT EXISTS (
                    SELECT 1 FROM transactions t
                    WHERE t.user_id = u.id AND t.type = 'deposit'
                      AND t.created_at > ?
                  )
                ORDER BY u.id
                """,
                (cutoff, cutoff),
            )
        else:
            cur = await db.execute(
                "SELECT telegram_id FROM users"
                " WHERE is_banned = 0 ORDER BY id"
            )

        return [row["telegram_id"] for row in await cur.fetchall()]
    finally:
        await db.close()


@dp.callback_query(F.data.startswith("bseg:"))
async def admin_bseg(cb: types.CallbackQuery, state: FSMContext):
    """[ADM2-1] اختيار شريحة البث."""

    if cb.from_user.id != ADMIN_USER_ID:
        await cb.answer("للأدمن الرئيسي فقط.", show_alert=True)
        return

    seg = cb.data.split(":", 1)[1]

    if seg not in _SEG_LABELS:
        await cb.answer("شريحة غير معروفة.", show_alert=True)
        return

    await cb.answer()

    if seg == "bal":  # [ADM2-1] يطلب الحد الأدنى
        await state.set_state(AdminBroadcastFSM.bal)
        await cb.message.answer(
            "💰 أرسل الحد الأدنى للرصيد (رقم):\n\nللإلغاء أرسل /cancel"
        , reply_markup=back_kb("admin_broadcast"))
        return

    await state.update_data(broadcast_segment=seg)

    skb = InlineKeyboardBuilder.from_markup(broadcast_confirm_kb())
    skb.button(  # [ADM3-10]
        text="🗓 جدولة الإرسال", callback_data=f"bsched:{seg}",
    )
    skb.adjust(1)

    await safe_edit(
        cb.message,
        f"📣 جاهز للبث إلى: <b>{_SEG_LABELS[seg]}</b>\n\nتأكيد؟"
        "\nأو جدولته لوقت لاحق:",
        skb.as_markup(),
    )


@dp.message(AdminBroadcastFSM.bal)
async def admin_bseg_bal(message: types.Message, state: FSMContext):
    """[ADM2-1] حد الرصيد لشريحة البث."""

    if message.from_user.id != ADMIN_USER_ID:
        await state.clear()
        return

    amount = parse_amount(message.text)  # [FIX 7]

    if amount is None:
        await message.answer("❌ رقم غير صالح.\n\nللإلغاء أرسل /cancel")
        return

    await state.update_data(
        broadcast_segment="bal",
        broadcast_min_balance=amount,
    )
    await message.answer(
        f"📣 جاهز للبث إلى: <b>💰 رصيد ≥ {money(amount)}</b>\n\nتأكيد؟",
        reply_markup=broadcast_confirm_kb(),
    )


def _ticket_rate_kb(ticket_id: int):
    """[USR2-7] أزرار تقييم الدعم 1-5 نجوم."""
    b = InlineKeyboardBuilder()

    for i in range(1, 6):
        b.button(
            text="⭐" * i,
            callback_data=f"trate:{ticket_id}:{i}",
        )

    b.adjust(5)
    return b.as_markup()


@dp.callback_query(F.data.startswith("trate:"))
async def ticket_rate(cb: types.CallbackQuery, state: FSMContext):
    """[USR2-7] المستخدم يقيّم خدمة الدعم (مرة واحدة)."""

    parts = cb.data.split(":")

    try:
        ticket_id = int(parts[1])
        stars = int(parts[2])
    except (ValueError, IndexError):
        await cb.answer("تقييم غير صالح.", show_alert=True)
        return

    if not 1 <= stars <= 5:
        await cb.answer("تقييم غير صالح.", show_alert=True)
        return

    db = await get_db()

    try:
        cur = await db.execute(
            """
            UPDATE support_tickets
            SET rating = ?
            WHERE id = ?
              AND user_tid = ?
              AND rating IS NULL
            """,
            (stars, ticket_id, cb.from_user.id),
        )
        changed = cur.rowcount
        await db.commit()
    finally:
        await db.close()

    if not changed:
        await cb.answer(tr(await user_lang(cb.from_user.id), "rate_done"),
                        show_alert=True)
        return

    await cb.answer(
        tr(await user_lang(cb.from_user.id), "rate_thanks"),
        show_alert=True,
    )


async def monthly_pl_if_due(now: datetime | None = None) -> bool:
    """
    [ADM2-4] تقرير P&L شهري للشهر المُنقضي — يُرسل مرة واحدة شهرياً.
    """
    now = now or datetime.now(timezone.utc)
    ym = f"{now:%Y-%m}"

    if (await get_setting("last_pl_month") or "") == ym:
        return False

    if now.hour < 9:
        return False

    first_this = now.replace(day=1, hour=0, minute=0, second=0,
                             microsecond=0)
    prev_end = first_this
    prev_start = (prev_end - timedelta(days=1)).replace(day=1)
    before_start = (prev_start - timedelta(days=1)).replace(day=1)

    start_s = f"{prev_start:%Y-%m-%d}"
    end_s = f"{prev_end:%Y-%m-%d}"

    db = await get_db()

    try:
        async def agg(sql, params):
            cur = await db.execute(sql, params)
            row = await cur.fetchone()
            return row

        row = await agg(
            """
            SELECT COUNT(*) c, COALESCE(SUM(amount), 0) s
            FROM transactions
            WHERE type = 'deposit' AND created_at >= ? AND created_at < ?
            """,
            (start_s, end_s),
        )
        dep_n, dep_sum = row["c"], float(row["s"])

        row = await agg(
            """
            SELECT COUNT(*) c, COALESCE(SUM(amount), 0) s
            FROM transactions
            WHERE type = 'withdraw' AND created_at >= ? AND created_at < ?
            """,
            (start_s, end_s),
        )
        wd_n, wd_sum = row["c"], float(row["s"])

        row = await agg(
            """
            SELECT COALESCE(SUM(amount), 0) s FROM transactions
            WHERE type = 'refund' AND created_at >= ? AND created_at < ?
            """,
            (start_s, end_s),
        )
        refund_sum = float(row["s"])

        row = await agg(
            """
            SELECT COALESCE(SUM(amount), 0) s FROM transactions
            WHERE type = 'gift' AND created_at >= ? AND created_at < ?
            """,
            (start_s, end_s),
        )
        gift_sum = float(row["s"])

        row = await agg(
            """
            SELECT COALESCE(SUM(amount), 0) s FROM payouts
            WHERE status = 'paid' AND processed_at >= ?
              AND processed_at < ?
            """,
            (start_s, end_s),
        )
        paid_sum = float(row["s"])

        # العمولة المحصلة من ملاحظات عمليات الإيداع
        cur = await db.execute(
            """
            SELECT note FROM transactions
            WHERE type = 'deposit' AND created_at >= ? AND created_at < ?
            """,
            (start_s, end_s),
        )
        commission = 0.0

        for nrow in await cur.fetchall():
            m = re.search(r"commission=([\d.]+)", nrow["note"] or "")

            if m:
                commission += float(m.group(1))

        # مقارنة بالشهر الذي قبله
        row = await agg(
            """
            SELECT COALESCE(SUM(amount), 0) s FROM transactions
            WHERE type = 'deposit' AND created_at >= ? AND created_at < ?
            """,
            (f"{before_start:%Y-%m-%d}", start_s),
        )
        prev_dep = float(row["s"])

        row = await agg(
            """
            SELECT COALESCE(SUM(amount), 0) s FROM transactions
            WHERE type = 'withdraw' AND created_at >= ? AND created_at < ?
            """,
            (f"{before_start:%Y-%m-%d}", start_s),
        )
        prev_wd = float(row["s"])
    finally:
        await db.close()

    house_net = round2(dep_sum - wd_sum - refund_sum - gift_sum)

    def _delta(cur_v: float, old_v: float) -> str:
        if old_v <= 0:
            return "—"
        pct = (cur_v - old_v) / old_v * 100.0
        arrow = "📈" if pct >= 0 else "📉"
        return f"{arrow} {pct:+.0f}%"

    text = (
        f"📊 <b>تقرير {prev_start:%Y-%m} الشهري</b>\n\n"
        f"💰 الإيداعات: {dep_n} عملية = {money(dep_sum)}"
        f"  {_delta(dep_sum, prev_dep)}\n"
        f"🏦 السحوبات: {wd_n} عملية = {money(wd_sum)}"
        f"  {_delta(wd_sum, prev_wd)}\n"
        f"٪ العمولة المحصلة: {money(round2(commission))}\n"
        f"🚀 مدفوعات مُسلمة: {money(paid_sum)}\n"
        f"↩️ استردادات: {money(refund_sum)}\n"
        f"🎁 هدايا مجانية: {money(gift_sum)}\n\n"
        f"🧮 <b>صافي الحركة: {money(house_net)}</b>"
    )

    try:
        await bot.send_message(ADMIN_USER_ID, text)
        await mirror(text)  # [ADM3-2]
    except Exception as exc:
        logger.warning("تعذر إرسال التقرير الشهري: %s", exc)
        return False

    await set_setting("last_pl_month", ym)
    return True


@dp.callback_query(F.data == "admin_sup_quota")
async def admin_sup_quota(cb: types.CallbackQuery, state: FSMContext):
    """[ADM2-3] ضبط الحصة المالية اليومية لمشرف."""

    if cb.from_user.id != ADMIN_USER_ID:
        await cb.answer("للأدمن الرئيسي فقط.", show_alert=True)
        return

    await cb.answer()
    await state.clear()
    await state.set_state(AdminSupQuotaFSM.value)

    await cb.message.answer(
        "💼 <b>الحصة اليومية لمشرف</b>\n\n"
        "أرسل: <code>tid amount</code>\n"
        "مثال: <code>555 100</code>\n\n"
        "ما يعتمده المشرف من سحوبات يتجاوز حصته اليومية\n"
        "يرفع تلقائياً لموافقتك النهائية.\n\n"
        "<code>555 0</code> = حصة غير محدودة\n"
        "للإلغاء أرسل /cancel"
    , reply_markup=back_kb("admin_supervisors"))


@dp.message(AdminSupQuotaFSM.value)
async def admin_sup_quota_save(message: types.Message, state: FSMContext):
    """[ADM2-3] حفظ الحصة."""

    if message.from_user.id != ADMIN_USER_ID:
        await state.clear()
        return

    parts = (message.text or "").strip().split()

    if (len(parts) != 2 or not parts[0].isdigit()
            or (not parts[1].replace(".", "", 1).isdigit())):
        await message.answer(
            "❌ الصيغة: <code>tid amount</code>\n\nللإلغاء أرسل /cancel"
        )
        return

    tid = int(parts[0])
    quota = float(parts[1])

    if quota < 0:
        await message.answer("❌ الحصة لا تكون سالبة.")
        return

    db = await get_db()

    try:
        cur = await db.execute(
            "SELECT telegram_id FROM supervisors WHERE telegram_id = ?",
            (tid,),
        )
        row = await cur.fetchone()

        if not row:
            await message.answer("❌ المشرف غير موجود.")
            await state.clear()
            return

        await db.execute(
            "UPDATE supervisors SET daily_quota = ? WHERE telegram_id = ?",
            (quota, tid),
        )
        await db.commit()
    finally:
        await db.close()

    await state.clear()
    await audit(  # [NEW 22]
        message.from_user.id, "sup_quota", tid, f"quota={quota:g}",
    )

    quota_txt = "غير محدودة" if quota == 0 else f"{money(quota)} يومياً"
    await message.answer(
        f"✅ حصة <code>{tid}</code>: <b>{quota_txt}</b>.",
        reply_markup=back_kb("admin_supervisors"),
    )


@dp.callback_query(F.data == "admin_supstats")
async def admin_supstats(cb: types.CallbackQuery, state: FSMContext):
    """[ADM2-7] أداء المشرفين خلال 7 أيام."""

    if not await is_admin_or_supervisor(cb.from_user.id):
        await cb.answer("غير مصرّح.", show_alert=True)
        return

    await cb.answer()
    await state.clear()

    cutoff = (
        datetime.now(timezone.utc) - timedelta(days=7)
    ).isoformat(timespec="seconds")

    db = await get_db()

    try:
        cur = await db.execute(
            """
            SELECT processed_by, status, COUNT(*) c,
                   AVG(
                       (julianday(processed_at)
                        - julianday(created_at)) * 1440.0
                   ) mins
            FROM finance_requests
            WHERE processed_by > 0
              AND processed_at IS NOT NULL
              AND created_at >= ?
            GROUP BY processed_by, status
            """,
            (cutoff,),
        )
        rows = await cur.fetchall()
    finally:
        await db.close()

    if not rows:
        await safe_edit(
            cb.message,
            "📭 لا نشاط معالجة خلال 7 أيام.",
            back_kb("admin_supervisors"),
        )
        return

    stats = {}

    for row in rows:
        sid = row["processed_by"]
        entry = stats.setdefault(
            sid, {"approved": 0, "rejected": 0, "awaiting_admin": 0,
                  "mins": []},
        )
        entry[row["status"]] = entry.get(row["status"], 0) + row["c"]

        if row["status"] in ("approved", "rejected") and row["mins"]:
            entry["mins"].append(float(row["mins"]))

    lines = ["🏋️ <b>أداء المشرفين — آخر 7 أيام</b>\n"]

    for sid, s in sorted(
        stats.items(),
        key=lambda kv: -(kv[1]["approved"] + kv[1]["rejected"]),
    ):
        avg = (
            f"{sum(s['mins']) / len(s['mins']):.0f} د"
            if s["mins"] else "—"
        )
        lines.append(
            f"👤 <code>{sid}</code>\n"
            f"✅ {s['approved']} | ❌ {s['rejected']}"
            f" | 👁 {s['awaiting_admin']} | ⏱ {avg}"
        )

    await safe_edit(
        cb.message, "\n\n".join(lines), back_kb("admin_supervisors"),
    )



# ============================================================
# [USR2-3/4 + ADM2-6] ROUND 3 — PHASE 3
# ============================================================

@dp.callback_query(F.data == "admin_bonus")
async def admin_bonus(cb: types.CallbackQuery, state: FSMContext):
    """[USR2-3] ضبط حملة مكافأة الإيداع."""

    if cb.from_user.id != ADMIN_USER_ID:
        await cb.answer("للأدمن الرئيسي فقط.", show_alert=True)
        return

    await cb.answer()
    await state.clear()
    await state.set_state(AdminBonusFSM.value)

    pct = await get_float_setting("bonus_percent", 0.0)
    bmax = await get_float_setting("bonus_max", 0.0)

    current = (
        f"+{pct:g}% (بحد أقصى {money(bmax)})"
        if pct > 0 else "معطّلة"
    )

    await cb.message.answer(
        "🎁 <b>حملة مكافأة الإيداع</b>\n\n"
        f"الحالة الحالية: <b>{current}</b>\n\n"
        "أرسل: <code>نسبة حد</code>\n"
        "مثال: <code>10 500</code> = +10% بحد أقصى 500 لكل شحنة\n\n"
        "<code>0</code> لإنهاء الحملة.\n"
        "للإلغاء أرسل /cancel"
    , reply_markup=back_kb("admin_settings_menu"))


@dp.message(AdminBonusFSM.value)
async def admin_bonus_save(message: types.Message, state: FSMContext):
    """[USR2-3] حفظ/إنهاء الحملة."""

    if message.from_user.id != ADMIN_USER_ID:
        await state.clear()
        return

    raw = (message.text or "").strip()

    if not raw or raw.startswith("/"):
        await state.clear()
        return

    if raw == "0":
        await set_setting("bonus_percent", "0")
        await set_setting("bonus_max", "0")
        await state.clear()
        await audit(message.from_user.id, "bonus_off")  # [NEW 22]

        await message.answer(
            "✅ أُنهيت حملة المكافأة.",
            reply_markup=back_kb("admin_settings_menu"),
        )
        return

    parts = raw.split()

    if len(parts) != 2:
        await message.answer(
            "❌ الصيغة: <code>نسبة حد</code>\n\nللإلغاء أرسل /cancel"
        )
        return

    if (not parts[0].replace(".", "", 1).isdigit()
            or not parts[1].replace(".", "", 1).isdigit()):
        await message.answer("❌ أرقام فقط.\n\nللإلغاء أرسل /cancel")
        return

    pct = min(100.0, max(0.0, float(parts[0])))
    bmax = max(0.0, float(parts[1]))

    await set_setting("bonus_percent", str(pct))
    await set_setting("bonus_max", str(bmax))
    await state.clear()
    await audit(  # [NEW 22]
        message.from_user.id, "bonus_set",
        f"pct={pct:g}", f"max={bmax:g}",
    )

    await message.answer(
        f"✅ الحملة نشطة: <b>+{pct:g}%</b>"
        f" (حد أقصى {money(bmax)} لكل شحنة).",
        reply_markup=back_kb("admin_settings_menu"),
    )


@dp.callback_query(F.data == "admin_promo")
async def admin_promo(cb: types.CallbackQuery, state: FSMContext):
    """[USR2-4] إنشاء كود إعفاء من العمولة."""

    if not await is_admin_or_supervisor(cb.from_user.id, "gifts"):
        await cb.answer("غير مصرّح.", show_alert=True)
        return

    await cb.answer()
    await state.clear()
    await state.set_state(AdminPromoFSM.value)

    await cb.message.answer(
        "🎟 <b>كود إعفاء من العمولة</b>\n\n"
        "أرسل: <code>CODE عدد</code>\n"
        "مثال: <code>SUMMER 25</code> = 25 شحنة بلا عمولة\n\n"
        "(الأحرف اللاتينية والأرقام، حتى 20 حرفاً)\n"
        "للإلغاء أرسل /cancel"
    , reply_markup=back_kb("admin_tools_menu"))


@dp.message(AdminPromoFSM.value)
async def admin_promo_save(message: types.Message, state: FSMContext):
    """[USR2-4] حفظ الكود."""

    if not await is_admin_or_supervisor(message.from_user.id, "gifts"):
        await state.clear()
        return

    parts = (message.text or "").strip().split()

    if (len(parts) != 2 or not parts[0]
            or not parts[0].isalnum()
            or len(parts[0]) > 20
            or not parts[1].isdigit()):
        await message.answer(
            "❌ الصيغة: <code>CODE عدد</code>\n"
            "مثال: <code>SUMMER 25</code>\n\nللإلغاء أرسل /cancel"
        )
        return

    code = parts[0].upper()
    uses = min(1000, int(parts[1]))

    db = await get_db()

    try:
        await db.execute(
            """
            INSERT OR REPLACE INTO promo_codes
            (code, uses_left, created_by, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (code, uses, message.from_user.id, now_iso()),
        )
        await db.commit()
    finally:
        await db.close()

    await state.clear()
    await audit(  # [NEW 22]
        message.from_user.id, "promo_create", code, f"uses={uses}",
    )

    await message.answer(
        f"🎟 كود الإعفاء جاهز:\n\n<code>{code}</code>\n"
        f"Reusable: {uses} مرة\n"
        "يستخدمه المستخدم من شاشة الشحن، وشحنته القادمة بلا عمولة.",
        reply_markup=admin_gifts_kb(),
    )


@dp.callback_query(F.data == "dpromo")
async def dpromo(cb: types.CallbackQuery, state: FSMContext):
    """[USR2-4] بدء إدخال كود الإعفاء."""

    if not await user_allowed(cb.from_user.id):
        await cb.answer("غير مسموح.", show_alert=True)
        return

    lang = await user_lang(cb.from_user.id)
    await cb.answer()
    await state.set_state(PromoCodeFSM.code)

    await cb.message.answer(tr(lang, "promo_prompt"))


@dp.message(PromoCodeFSM.code)
async def promo_code_submit(message: types.Message, state: FSMContext):
    """[USR2-4] التحقق من الكود والعودة لتدفق الشحن."""

    if not await user_allowed(message.from_user.id, message):
        return

    raw = (message.text or "").strip().upper()

    if not raw or raw.startswith("/"):
        await state.clear()
        return

    lang = await user_lang(message.from_user.id)

    db = await get_db()

    try:
        cur = await db.execute(
            "SELECT uses_left FROM promo_codes"
            " WHERE code = ? AND uses_left > 0",
            (raw,),
        )
        row = await cur.fetchone()
    finally:
        await db.close()

    if not row:
        await message.answer(tr(lang, "promo_bad"))
        return

    await state.update_data(promo=raw)
    await state.set_state(DepositFSM.amount)
    await message.answer(tr(lang, "promo_ok"))


async def auto_protect_if_needed() -> bool:
    """
    [ADM2-6] حماية تلقائية اختيارية:
    إيقاف السحوبات عند تراكم >20 طلباً أو فشل 3 مدفوعات متتالية.
    """
    if (await get_setting("auto_protect") or "0") != "1":
        return False

    if (await get_setting("withdraws_paused") or "0") == "1":
        return False  # موقوفة أصلاً — لا تكرار

    db = await get_db()

    try:
        cur = await db.execute(
            "SELECT COUNT(*) AS c FROM finance_requests"
            " WHERE status = 'pending'"
        )
        pending = (await cur.fetchone())["c"]

        cur = await db.execute(
            "SELECT status FROM payouts ORDER BY id DESC LIMIT 3"
        )
        last3 = [r["status"] for r in await cur.fetchall()]
    finally:
        await db.close()

    fail_streak = len(last3) == 3 and all(
        s == "failed" for s in last3
    )

    if pending <= 20 and not fail_streak:
        return False

    if pending > 20:
        cause = f"تراكم {pending} طلباً معلق"
    else:
        cause = "فشل 3 مدفوعات متتالية"

    await set_setting("withdraws_paused", "1")
    await set_setting(
        "pause_reason_wd", f"🤖 إيقاف تلقائي: {cause}",
    )

    try:
        await bot.send_message(
            ADMIN_USER_ID,
            "🤖 <b>حماية تلقائية</b>\n\n"
            f"أوقفتُ السحوبات تلقائياً: {cause}.\n"
            "راجع الطابور الموحد ثم شغّل السحوبات من ⏸️ إيقاف الخدمات.",
        )
        await mirror(
            "🤖 <b>حماية تلقائية</b>\n\nأُوقفت السحوبات تلقائياً.",
        )  # [ADM3-2]
    except Exception as exc:
        logger.warning("تعذر تنبيه الأدمن بالحماية التلقائية: %s", exc)

    return True


@dp.callback_query(F.data == "admin_autoprotect")
async def admin_autoprotect(cb: types.CallbackQuery, state: FSMContext):
    """[ADM2-6] تبديل الحماية التلقائية."""

    if cb.from_user.id != ADMIN_USER_ID:
        await cb.answer("للأدمن الرئيسي فقط.", show_alert=True)
        return

    current = (await get_setting("auto_protect") or "0") == "1"
    await set_setting("auto_protect", "0" if current else "1")
    await audit(  # [NEW 22]
        cb.from_user.id, "auto_protect_toggle",
        "off" if current else "on",
    )
    await cb.answer("تم ✅")

    text, kb = await render_pause_text()
    await safe_edit(cb.message, text, kb)



# ============================================================
# [ADM3-2/3/4/7/8/12] ROUND 4 — PHASE 1
# ============================================================

async def mirror(text: str):
    """[ADM3-2] نسخ إشعارات الإدارة إلى غرفة المراقبة (إن ضُبطت)."""
    chat_id = (await get_setting("mirror_chat_id") or "").strip()

    if not chat_id.lstrip("-").isdigit():
        return

    chat_id = int(chat_id)

    if chat_id == ADMIN_USER_ID:
        return  # الأدمن يستلم أصلاً — لا تكرار

    try:
        await bot.send_message(chat_id, text)
    except Exception as exc:
        logger.warning("تعذر النسخ لغرفة المراقبة: %s", exc)


@dp.callback_query(F.data == "admin_test_ping")
async def admin_test_ping(cb: types.CallbackQuery, state: FSMContext):
    """[ADM3-3] رسالة اختبار: تؤكد وصول الإشعارات للأدمن والغرفة."""

    if cb.from_user.id != ADMIN_USER_ID:
        await cb.answer("للأدمن الرئيسي فقط.", show_alert=True)
        return

    await cb.answer()
    await state.clear()

    stamp = now_iso()
    results = ["✅ خاص الأدمن: وصلت ✅"]

    try:
        await bot.send_message(
            ADMIN_USER_ID,
            f"📳 رسالة اختبار — {stamp}",
        )
    except Exception:
        results = ["❌ خاص الأدمن: فشل الإرسال!"]

    chat_id = (await get_setting("mirror_chat_id") or "").strip()

    if chat_id.lstrip("-").isdigit() and int(chat_id) != ADMIN_USER_ID:
        try:
            await bot.send_message(int(chat_id), f"📳 اختبار الغرفة — {stamp}")
            results.append("✅ غرفة المراقبة: وصلت ✅")
        except Exception:
            results.append("❌ غرفة المراقبة: البوت لا يصل إليها!")

    await safe_edit(
        cb.message,
        "📳 <b>نتيجة اختبار الإشعارات</b>\n\n" + "\n".join(results),
        back_kb("admin_tools_menu"),
    )


@dp.callback_query(F.data == "admin_mirror")
async def admin_mirror(cb: types.CallbackQuery, state: FSMContext):
    """[ADM3-2] ضبط غرفة المراقبة."""

    if cb.from_user.id != ADMIN_USER_ID:
        await cb.answer("للأدمن الرئيسي فقط.", show_alert=True)
        return

    await cb.answer()
    await state.clear()
    await state.set_state(AdminMirrorFSM.value)

    current = (await get_setting("mirror_chat_id") or "").strip()

    await cb.message.answer(
        "📬 <b>غرفة المراقبة</b>\n\n"
        "تُنسخ إليها إشعارات الإدارة (الطلبات/التذاكر/التنبيهات).\n\n"
        f"المعرف الحالي: <code>{esc(current) if current else '—'}</code>\n\n"
        "أرسل معرف المجموعة/القناة (يبدأ بـ -100 غالباً).\n"
        "أرسل <code>0</code> للتعطيل.\n"
        "للإلغاء أرسل /cancel"
    , reply_markup=back_kb("admin_settings_menu"))


@dp.message(AdminMirrorFSM.value)
async def admin_mirror_save(message: types.Message, state: FSMContext):
    """[ADM3-2] حفظ/تعطيل الغرفة مع اختبار وصول فوري."""

    if message.from_user.id != ADMIN_USER_ID:
        await state.clear()
        return

    raw = (message.text or "").strip()

    if not raw or raw.startswith("/"):
        await state.clear()
        return

    if raw == "0":
        await set_setting("mirror_chat_id", "")
        await state.clear()
        await audit(message.from_user.id, "mirror_off")  # [NEW 22]

        await message.answer(
            "✅ أُعطّلت غرفة المراقبة.",
            reply_markup=back_kb("admin_settings_menu"),
        )
        return

    if not raw.lstrip("-").isdigit():
        await message.answer("❌ معرف غير صالح.\n\nللإلغاء أرسل /cancel")
        return

    chat_id = int(raw)
    await set_setting("mirror_chat_id", str(chat_id))
    await state.clear()
    await audit(  # [NEW 22]
        message.from_user.id, "mirror_set", chat_id,
    )

    try:
        await bot.send_message(
            chat_id,
            "📬 هذه الغرفة سجلّت الآن كغرفة مراقبة لهذا البوت ✅",
        )
        note = "واختبرنا الوصول: ✅ وصلت."
    except Exception:
        note = ("⚠️ لكن البوت لم يستطع الوصول إليها — "
                "أضف البوت للقناة/المجموعة أولاً!")

    await message.answer(
        f"✅ حُفظت الغرفة: <code>{chat_id}</code>\n{note}",
        reply_markup=back_kb("admin_settings_menu"),
    )


@dp.callback_query(F.data == "admin_hidebal")
async def admin_hidebal(cb: types.CallbackQuery, state: FSMContext):
    """[ADM3-8] تبديل إخفاء الأرصدة عن المشرفين."""

    if cb.from_user.id != ADMIN_USER_ID:
        await cb.answer("للأدمن الرئيسي فقط.", show_alert=True)
        return

    current = (await get_setting("staff_hide_balance") or "0") == "1"
    await set_setting("staff_hide_balance", "0" if current else "1")
    await audit(  # [NEW 22]
        cb.from_user.id, "hide_balance_toggle",
        "off" if current else "on",
    )
    await cb.answer(
        "🙈 الأرصدة الآن مخفية عن المشرفين"
        if not current
        else "👁 الأرصدة ظاهرة للجميع",
        show_alert=True,
    )
    # [R6-REV] تحديث الشاشة ليعكس الزر الحالة الجديدة فوراً
    status = await admin_status_line()
    await safe_edit(
        cb.message,
        f"⚙️ <b>الإعدادات والأدوات</b>\n{status}\n\nاختر ما تريد ضبطه:",
        await admin_settings_kb(),
    )


@dp.callback_query(F.data == "admin_sim")
async def admin_sim(cb: types.CallbackQuery, state: FSMContext):
    """[ADM3-7] محاكي الشحن."""

    if cb.from_user.id != ADMIN_USER_ID:
        await cb.answer("للأدمن الرئيسي فقط.", show_alert=True)
        return

    await cb.answer()
    await state.clear()
    await state.set_state(AdminSimFSM.amount)

    await cb.message.answer(
        "🧮 <b>محاكي الشحن</b>\n\n"
        "أرسل مبلغاً — أحسب لك صافي المستخدم\n"
        "بالإعدادات الحالية (عمولة + مكافأة):\n\n"
        "للإلغاء أرسل /cancel"
    , reply_markup=back_kb("admin_settings_menu"))


@dp.message(AdminSimFSM.amount)
async def admin_sim_calc(message: types.Message, state: FSMContext):
    """[ADM3-7] حساب المحاكاة بالإعدادات الحية."""

    if message.from_user.id != ADMIN_USER_ID:
        await state.clear()
        return

    amount = parse_amount(message.text)  # [FIX 7]

    if amount is None:
        await message.answer("❌ مبلغ غير صالح.\n\nللإلغاء أرسل /cancel")
        return

    await state.clear()

    pct = await get_float_setting("commission_percent", 0.0)
    commission = round2(amount * pct / 100.0)
    net = round2(amount - commission)

    bonus = 0.0
    bonus_pct = await get_float_setting("bonus_percent", 0.0)  # [USR2-3]

    if bonus_pct > 0:
        bonus = round2(net * bonus_pct / 100.0)
        bonus_max = await get_float_setting("bonus_max", 0.0)

        if bonus_max > 0:
            bonus = min(bonus, round2(bonus_max))
        net = round2(net + bonus)

    await message.answer(
        "🧮 <b>نتيجة المحاكاة</b>\n\n"
        f"💵 المبلغ الخام: {money(amount)}\n"
        f"٪ العمولة ({pct:g}%): -{money(commission)}\n"
        + (f"🎁 المكافأة: +{money(bonus)}\n" if bonus > 0 else "")
        + f"\n✅ <b>يستلمه المستخدم: {money(net)}</b>",
        reply_markup=back_kb("admin_settings_menu"),
    )


async def weekly_report_if_due() -> bool:
    """[ADM3-12] ملخص أسبوعي تلقائي كل أحد بعد 09:00 UTC."""
    if not await feat_on("weekly_report"):  # [R6-PLUS3]
        return False

    now = datetime.now(timezone.utc)
    today = f"{now:%Y-%m-%d}"

    if (await get_setting("last_weekly_report") or "") == today:
        return False

    if now.weekday() != 6 or now.hour < 9:  # الأحد
        return False

    start = (now - timedelta(days=7)).strftime("%Y-%m-%d")

    db = await get_db()

    try:
        async def one(sql, params):
            cur = await db.execute(sql, params)
            return await cur.fetchone()

        row = await one(
            "SELECT COUNT(*) c, COALESCE(SUM(amount), 0) s"
            " FROM transactions WHERE type='deposit'"
            " AND created_at >= ?",
            (start,),
        )
        dep_n, dep_s = row["c"], float(row["s"])

        row = await one(
            "SELECT COUNT(*) c, COALESCE(SUM(amount), 0) s"
            " FROM transactions WHERE type='withdraw'"
            " AND created_at >= ?",
            (start,),
        )
        wd_n, wd_s = row["c"], float(row["s"])

        row = await one(
            "SELECT COUNT(*) c FROM users WHERE created_at >= ?",
            (start,),
        )
        new_users = row["c"]

        row = await one(
            "SELECT COUNT(*) c FROM support_tickets"
            " WHERE created_at >= ?",
            (start,),
        )
        tickets = row["c"]

        row = await one(
            "SELECT COALESCE(AVG(rating), 0) a FROM support_tickets"
            " WHERE rating IS NOT NULL",
            (),
        )
        rating = float(row["a"])
    finally:
        await db.close()

    text = (
        "📈 <b>التقرير الأسبوعي</b>\n\n"
        f"💰 شحن: {dep_n} عملية = {money(dep_s)}\n"
        f"🏦 سحب: {wd_n} عملية = {money(wd_s)}\n"
        f"👥 مستخدمون جدد: {new_users}\n"
        f"💬 تذاكر: {tickets}\n"
        f"⭐ متوسط الرضا: {rating:.1f}"
    )

    try:
        await bot.send_message(ADMIN_USER_ID, text)
        await mirror(text)  # [ADM3-2]
    except Exception as exc:
        logger.warning("تعذر إرسال التقرير الأسبوعي: %s", exc)
        return False

    await set_setting("last_weekly_report", today)
    return True



# ============================================================
# [ADM3-1/9/11] ROUND 4 — PHASE 2
# ============================================================


_pin_unlocked_until: float = 0.0  # [ADM3-1] قفل مؤقت بعد إدخال الرمز


def _pin_hash(pin: str) -> str:
    return hashlib.sha256(pin.encode()).hexdigest()


async def pin_gate(cb) -> bool:
    """
    [ADM3-1] بوابة رمز التأكيد:
    True = تابع العملية، False = أُوقفها (الرمز مطلوب).
    """

    stored = (await get_setting("admin_pin") or "").strip()

    if not stored:
        return True  # بلا رمز = الحماية معطلة

    if time.monotonic() < _pin_unlocked_until:
        return True  # فُتح القفل مؤقتاً

    await cb.answer(
        "🔒 العملية محمية — أرسل رمز التأكيد أولاً",
        show_alert=True,
    )
    return False


@dp.callback_query(F.data == "admin_pinset")
async def admin_pinset(cb: types.CallbackQuery, state: FSMContext):
    """[ADM3-1] ضبط/إزالة رمز التأكيد."""

    if cb.from_user.id != ADMIN_USER_ID:
        await cb.answer("للأدمن الرئيسي فقط.", show_alert=True)
        return

    await cb.answer()
    await state.clear()
    await state.set_state(AdminPinFSM.set_value)

    current = bool((await get_setting("admin_pin") or "").strip())

    await cb.message.answer(
        "🔑 <b>رمز التأكيد</b>\n\n"
        "يُطلب قبل: المدفوعات/تعديل الرصيد/التصدير/البث\n"
        "وبعد إدخاله الصحيح يبقى القفل مفتوحاً 15 دقيقة.\n\n"
        f"الحالة: {'مفعّل ✅' if current else 'معطّل'}\n\n"
        "أرسل رمزاً (4-8 أرقام) للتفعيل،\n"
        "أو <code>0</code> للتعطيل.\n"
        "للإلغاء أرسل /cancel"
    , reply_markup=back_kb("admin_settings_menu"))


@dp.message(AdminPinFSM.set_value)
async def admin_pinset_save(message: types.Message, state: FSMContext):
    """[ADM3-1] حفظ/إزالة الرمز (يُخزن مُهشّراً)."""

    global _pin_unlocked_until

    if message.from_user.id != ADMIN_USER_ID:
        await state.clear()
        return

    raw = (message.text or "").strip()

    if not raw or raw.startswith("/"):
        await state.clear()
        return

    if raw == "0":
        await set_setting("admin_pin", "")
        _pin_unlocked_until = 0.0
        await state.clear()
        await audit(message.from_user.id, "pin_off")  # [NEW 22]

        await message.answer(
            "✅ أُعطّل رمز التأكيد.",
            reply_markup=back_kb("admin_settings_menu"),
        )
        return

    if not (raw.isdigit() and 4 <= len(raw) <= 8):
        await message.answer(
            "❌ الرمز: 4-8 أرقام فقط.\n\nللإلغاء أرسل /cancel"
        )
        return

    await set_setting("admin_pin", _pin_hash(raw))
    await state.clear()
    await audit(message.from_user.id, "pin_set")  # [NEW 22]

    await message.answer(
        "✅ فُعّل رمز التأكيد — العمليات الحساسة سيتطلبها.\n"
        "احفظه جيداً: لإزالته أرسل <code>0</code> من نفس الشاشة.",
        reply_markup=back_kb("admin_settings_menu"),
    )


@dp.message(AdminPinFSM.code)
async def admin_pin_enter(message: types.Message, state: FSMContext):
    """
    [ADM3-1] إدخال الرمز لفتح القفل 15 دقيقة.
    متاح لأي موظف: معرفة الرمز هي التصريح —
    ومن لا يملك صلاحيات العملية فلن ينفذها بعد الفتح أصلاً.
    """

    global _pin_unlocked_until

    raw = (message.text or "").strip()

    if not raw or raw.startswith("/"):
        await state.clear()
        return

    stored = (await get_setting("admin_pin") or "").strip()

    if not stored:
        await state.clear()
        return

    if _pin_hash(raw) == stored:
        _pin_unlocked_until = time.monotonic() + 900
        await state.clear()
        await message.answer(
            "🔓 فُتح القفل لمدة 15 دقيقة —\n"
            "أعد الضغط على الزر الذي أردته.",
        )
        await audit(message.from_user.id, "pin_unlock")  # [NEW 22]
    else:
        await message.answer(
            "❌ رمز خاطئ — أعد المحاولة أو /cancel للإلغاء."
        )


# ---------- [ADM3-9] الردود الجاهزة ----------

async def _send_ticket_reply(
    admin_id: int, ticket_id: int, user_tid: int, raw: str,
) -> bool:
    """[ADM3-9] نواة الرد: إرسال للمستخدم + إغلاق التذكرة + تدقيق."""
    lang = await user_lang(user_tid)

    try:
        await bot.send_message(
            user_tid,
            tr(lang, "support_reply", msg=esc(raw)),
        )
    except Exception as exc:
        logger.warning("تعذر إرسال رد التذكرة: %s", exc)
        return False

    db = await get_db()

    try:
        await db.execute(
            """
            UPDATE support_tickets
            SET status = 'answered',
                answered_at = ?,
                answered_by = ?
            WHERE id = ?
              AND status = 'open'
            """,
            (now_iso(), admin_id, ticket_id),
        )
        await db.commit()
    finally:
        await db.close()

    await audit(  # [NEW 22]
        admin_id, "ticket_reply", f"ticket={ticket_id}",
        f"user={user_tid}",
    )
    return True


async def render_canned_kb():
    """[ADM3-9] لوحة إدارة القوالب."""
    db = await get_db()

    try:
        cur = await db.execute(
            "SELECT id, title, body FROM canned_replies ORDER BY id"
        )
        rows = await cur.fetchall()
    finally:
        await db.close()

    b = InlineKeyboardBuilder()

    for row in rows:
        b.button(
            text=f"🗑 #{row['id']} {row['title'][:16]}",
            callback_data=f"candel:{row['id']}",
        )

    b.button(text="➕ إضافة قالب", callback_data="admin_canned_add")
    b.button(text="🔙 رجوع", callback_data="admin_tickets:0")
    b.adjust(1)

    return rows, b.as_markup()


@dp.callback_query(F.data == "admin_canned")
async def admin_canned(cb: types.CallbackQuery, state: FSMContext):
    """[ADM3-9] إدارة الردود الجاهزة."""

    if not await is_admin_or_supervisor(cb.from_user.id):
        await cb.answer("غير مصرّح.", show_alert=True)
        return

    await cb.answer()
    await state.clear()

    rows, kb = await render_canned_kb()

    lines = ["💬 <b>الردود الجاهزة</b>\n"]

    if rows:
        lines += [f"#{r['id']} — {esc(r['title'])}" for r in rows]
    else:
        lines.append("لا قوالب بعد.")

    await safe_edit(cb.message, "\n".join(lines), kb)


@dp.callback_query(F.data == "admin_canned_add")
async def admin_canned_add(cb: types.CallbackQuery, state: FSMContext):
    """[ADM3-9] بدء إضافة قالب."""

    if not await is_admin_or_supervisor(cb.from_user.id):
        await cb.answer("غير مصرّح.", show_alert=True)
        return

    await cb.answer()
    await state.clear()
    await state.set_state(AdminCannedFSM.value)

    await cb.message.answer(
        "➕ أرسل القالب بصيغة:\n\n<code>عنوان قصير | نص الرد</code>\n\n"
        "للإلغاء أرسل /cancel"
    , reply_markup=back_kb("admin_canned"))


@dp.message(AdminCannedFSM.value)
async def admin_canned_save(message: types.Message, state: FSMContext):
    """[ADM3-9] حفظ القالب."""

    if not await is_admin_or_supervisor(message.from_user.id, "users"):
        await state.clear()
        return

    raw = (message.text or "").strip()

    if not raw or raw.startswith("/"):
        await state.clear()
        return

    parts = raw.split("|", 1)

    if len(parts) != 2 or not parts[0].strip() or not parts[1].strip():
        await message.answer(
            "❌ الصيغة: <code>عنوان | نص</code>\n\nللإلغاء أرسل /cancel"
        )
        return

    db = await get_db()

    try:
        await db.execute(
            """
            INSERT INTO canned_replies (title, body, created_at)
            VALUES (?, ?, ?)
            """,
            (parts[0].strip()[:40], parts[1].strip()[:500], now_iso()),
        )
        await db.commit()
    finally:
        await db.close()

    await state.clear()
    await audit(  # [NEW 22]
        message.from_user.id, "canned_add", parts[0].strip()[:40],
    )

    await message.answer(
        "✅ حُفظ القالب — سيظهر بأزرار عند الرد على التذاكر.",
        reply_markup=back_kb("admin_tickets:0"),
    )


@dp.callback_query(F.data.startswith("candel:"))
async def admin_canned_del(cb: types.CallbackQuery, state: FSMContext):
    """[ADM3-9] حذف قالب."""

    if not await is_admin_or_supervisor(cb.from_user.id):
        await cb.answer("غير مصرّح.", show_alert=True)
        return

    try:
        cid = int(cb.data.split(":", 1)[1])
    except (ValueError, IndexError):
        await cb.answer("معرف غير صالح.", show_alert=True)
        return

    db = await get_db()

    try:
        await db.execute("DELETE FROM canned_replies WHERE id = ?", (cid,))
        await db.commit()
    finally:
        await db.close()

    await cb.answer("حُذف 🗑")
    await audit(cb.from_user.id, "canned_del", cid)  # [NEW 22]

    rows, kb = await render_canned_kb()
    lines = ["💬 <b>الردود الجاهزة</b>\n"]

    if rows:
        lines += [f"#{r['id']} — {esc(r['title'])}" for r in rows]
    else:
        lines.append("لا قوالب بعد.")

    await safe_edit(cb.message, "\n".join(lines), kb)


@dp.callback_query(F.data.startswith("cuse:"))
async def canned_use(cb: types.CallbackQuery, state: FSMContext):
    """[ADM3-9] استخدام قالب جاهز للرد على تذكرة."""

    if not await is_admin_or_supervisor(cb.from_user.id):
        await cb.answer("غير مصرّح.", show_alert=True)
        return

    parts = cb.data.split(":")

    try:
        ticket_id, cid = int(parts[1]), int(parts[2])
    except (ValueError, IndexError):
        await cb.answer("مرجع غير صالح.", show_alert=True)
        return

    db = await get_db()

    try:
        cur = await db.execute(
            "SELECT user_tid, status FROM support_tickets WHERE id = ?",
            (ticket_id,),
        )
        trow = await cur.fetchone()

        cur = await db.execute(
            "SELECT title, body FROM canned_replies WHERE id = ?", (cid,),
        )
        crow = await cur.fetchone()
    finally:
        await db.close()

    if not trow or trow["status"] != "open":
        await cb.answer("التذكرة مغلقة أو غير موجودة.", show_alert=True)
        return

    if not crow:
        await cb.answer("القالب غير موجود.", show_alert=True)
        return

    await cb.answer()

    ok = await _send_ticket_reply(
        cb.from_user.id, ticket_id, trow["user_tid"], crow["body"],
    )

    if ok:
        await cb.message.answer(
            f"✅ أُرسل الرد الجاهز «{esc(crow['title'])}»"
            f" على التذكرة #{ticket_id}.",
            reply_markup=back_kb("admin_inbox"),
        )
    else:
        await cb.message.answer(
            "❌ تعذر الوصول للمستخدم (ربما لم يبدأ البوت)."
        )


# ---------- [ADM3-11] تنظيف البيانات القديمة ----------

@dp.callback_query(F.data == "admin_clean")
async def admin_clean(cb: types.CallbackQuery, state: FSMContext):
    """[ADM3-11] بدء تنظيف البيانات الأقدم من X يوم."""

    if cb.from_user.id != ADMIN_USER_ID:
        await cb.answer("للأدمن الرئيسي فقط.", show_alert=True)
        return

    await cb.answer()
    await state.clear()
    await state.set_state(AdminCleanFSM.days)

    await cb.message.answer(
        "🧹 <b>تنظيف البيانات القديمة</b>\n\n"
        "أرسل عدد الأيام — سيُحذف ما هو أقدم منها من:\n"
        "• أحداث الويب هوك\n"
        "• سجل التدقيق\n"
        "• التذاكر المغلقة/المُجيبة\n\n"
        "(10-3650)\nللإلغاء أرسل /cancel"
    , reply_markup=back_kb("admin_tools_menu"))


@dp.message(AdminCleanFSM.days)
async def admin_clean_preview(message: types.Message, state: FSMContext):
    """[ADM3-11] معاينة ما سيُحذف قبل التنفيذ."""

    if message.from_user.id != ADMIN_USER_ID:
        await state.clear()
        return

    raw = (message.text or "").strip()

    if not raw or raw.startswith("/"):
        await state.clear()
        return

    if not raw.isdigit() or not 10 <= int(raw) <= 3650:
        await message.answer(
            "❌ أرسل عدداً بين 10 و 3650.\n\nللإلغاء أرسل /cancel"
        )
        return

    days = int(raw)
    cutoff = (
        datetime.now(timezone.utc) - timedelta(days=days)
    ).isoformat(timespec="seconds")

    db = await get_db()

    try:
        async def cnt(sql, params):
            cur = await db.execute(sql, params)
            return (await cur.fetchone())["c"]

        n_events = await cnt(
            "SELECT COUNT(*) c FROM webhook_events"
            " WHERE created_at < ?", (cutoff,),
        )
        n_audit = await cnt(
            "SELECT COUNT(*) c FROM admin_audit"
            " WHERE created_at < ?", (cutoff,),
        )
        n_tickets = await cnt(
            "SELECT COUNT(*) c FROM support_tickets"
            " WHERE status IN ('closed','answered')"
            " AND created_at < ?", (cutoff,),
        )
    finally:
        await db.close()

    total = n_events + n_audit + n_tickets

    await state.update_data(clean_days=days)
    await message.answer(
        f"🧹 <b>معاينة التنفيذ</b> (أقدم من {days} يوماً)\n\n"
        f"• أحداث الويب هوك: {n_events}\n"
        f"• سجل التدقيق: {n_audit}\n"
        f"• تذاكر مغلقة: {n_tickets}\n\n"
        f"الإجمالي: <b>{total}</b> صف",
        reply_markup=_clean_confirm_kb(total),
    )


def _clean_confirm_kb(total: int):
    b = InlineKeyboardBuilder()

    if total > 0:
        b.button(text="🗑 نعم، نفّذ التنظيف", callback_data="clean_go")

    b.button(text="❌ إلغاء", callback_data="clean_no")
    b.adjust(1)
    return b.as_markup()


@dp.callback_query(F.data == "clean_go")
async def admin_clean_go(cb: types.CallbackQuery, state: FSMContext):
    """[ADM3-11] تنفيذ الحذف."""

    if cb.from_user.id != ADMIN_USER_ID:
        await cb.answer("للأدمن الرئيسي فقط.", show_alert=True)
        return

    data = await state.get_data()
    days = data.get("clean_days")

    if not days:
        await cb.answer("انتهت الجلسة — أعد من البداية.", show_alert=True)
        return

    cutoff = (
        datetime.now(timezone.utc) - timedelta(days=int(days))
    ).isoformat(timespec="seconds")

    db = await get_db()

    try:
        cur = await db.execute(
            "DELETE FROM webhook_events WHERE created_at < ?", (cutoff,),
        )
        d1 = cur.rowcount
        cur = await db.execute(
            "DELETE FROM admin_audit WHERE created_at < ?", (cutoff,),
        )
        d2 = cur.rowcount
        cur = await db.execute(
            "DELETE FROM support_tickets"
            " WHERE status IN ('closed','answered')"
            " AND created_at < ?", (cutoff,),
        )
        d3 = cur.rowcount
        await db.commit()
    finally:
        await db.close()

    await state.clear()
    await audit(  # [NEW 22]
        cb.from_user.id, "data_cleanup", f"days={days}",
        f"events={d1};audit={d2};tickets={d3}",
    )

    await safe_edit(
        cb.message,
        f"✅ حُذف {d1 + d2 + d3} صف\n"
        f"(أحداث: {d1} | تدقيق: {d2} | تذاكر: {d3})",
        back_kb("admin_tools_menu"),
    )


@dp.callback_query(F.data == "clean_no")
async def admin_clean_no(cb: types.CallbackQuery, state: FSMContext):
    await cb.answer("أُلغي التنظيف.")
    await state.clear()



# ============================================================
# [ADM3-5/6/10] ROUND 4 — PHASE 3
# ============================================================

async def do_broadcast_copy(status_message, chat_id, message_id, targets):
    """[ADM3-10] نواة إرسال البث — مشتركة بين الفوري والمجدول."""
    sent = 0
    failed = 0
    total = len(targets)

    for index, target_id in enumerate(targets, start=1):

        try:
            await bot.copy_message(
                chat_id=target_id,
                from_chat_id=chat_id,
                message_id=message_id,
            )
            sent += 1
        except Exception:
            failed += 1

        if index % 25 == 0:
            try:
                await status_message.edit_text(
                    f"📣 جاري البث... {index}/{total}"
                )
            except Exception:
                pass

        # احترام حدود معدل الإرسال في تلجرام (~20 رسالة/ثانية)
        await asyncio.sleep(0.05)

    return sent, failed


async def scheduled_broadcast_if_due() -> bool:
    """[ADM3-10] تنفيذ البث المجدول عند حلول وقته."""
    raw = (await get_setting("scheduled_broadcast") or "").strip()

    if not raw:
        return False

    try:
        job = json.loads(raw)
        run_h, run_m = map(int, str(job["time"]).split(":"))
    except Exception:
        await set_setting("scheduled_broadcast", "")
        return False

    now = datetime.now(timezone.utc)
    today = f"{now:%Y-%m-%d}"

    if (await get_setting("last_sched_broadcast") or "") == today:
        return False

    cur_min = now.hour * 60 + now.minute

    if cur_min < run_h * 60 + run_m:
        return False  # لم يحل الوقت بعد

    targets = await broadcast_targets(
        job.get("segment") or "all",
        job.get("min_balance"),
    )

    if not targets:
        await set_setting("scheduled_broadcast", "")
        return False

    status = await bot.send_message(
        ADMIN_USER_ID,
        f"📣 تنفيذ البث المجدول ({job['time']} UTC) إلى {len(targets)}...",
    )

    sent, failed = await do_broadcast_copy(
        status, job["chat_id"], job["message_id"], targets,
    )

    try:
        await status.edit_text(
            "✅ <b>انتهى البث المجدول</b>\n\n"
            f"📬 وصلت: {sent} | 🚫 فشل: {failed}"
        )
    except Exception:
        pass

    await set_setting("last_sched_broadcast", today)
    await set_setting("scheduled_broadcast", "")
    await audit(  # [NEW 22]
        ADMIN_USER_ID, "broadcast_scheduled",
        f"targets={len(targets)}", f"sent={sent};failed={failed}",
    )
    return True


@dp.callback_query(F.data.startswith("bsched:"))
async def admin_bsched(cb: types.CallbackQuery, state: FSMContext):
    """[ADM3-10] بدء جدولة البث للشريحة المختارة."""

    if cb.from_user.id != ADMIN_USER_ID:
        await cb.answer("للأدمن الرئيسي فقط.", show_alert=True)
        return

    seg = cb.data.split(":", 1)[1]

    if seg not in _SEG_LABELS:
        await cb.answer("شريحة غير معروفة.", show_alert=True)
        return

    data = await state.get_data()
    chat_id = data.get("broadcast_chat_id")
    message_id = data.get("broadcast_message_id")

    if not chat_id or not message_id:
        await cb.answer("لا توجد رسالة محفوظة.", show_alert=True)
        return

    await cb.answer()
    await state.update_data(sched_seg=seg)

    if seg == "bal":
        await state.set_state(AdminBcastSchedFSM.amount)
        await cb.message.answer(
            "💰 أرسل الحد الأدنى للرصيد لهذا البث المجدول:"
        , reply_markup=back_kb("admin_broadcast"))
        return

    await state.set_state(AdminBcastSchedFSM.time)
    await cb.message.answer(
        f"🗓 جدولة البث إلى <b>{_SEG_LABELS[seg]}</b>\n\n"
        "أرسل وقت الإرسال <code>HH:MM</code> (UTC):\n"
        "مثال: <code>20:00</code>\n\nللإلغاء أرسل /cancel"
    )


@dp.message(AdminBcastSchedFSM.amount)
async def admin_bsched_amount(message: types.Message, state: FSMContext):
    """[ADM3-10] حد الرصيد ثم سؤال الوقت."""

    if message.from_user.id != ADMIN_USER_ID:
        await state.clear()
        return

    amount = parse_amount(message.text)  # [FIX 7]

    if amount is None:
        await message.answer("❌ رقم غير صالح.")
        return

    await state.update_data(sched_min=amount)
    await state.set_state(AdminBcastSchedFSM.time)
    await message.answer(
        f"💰 الحد: ≥ {money(amount)}\n\n"
        "الآن أرسل وقت الإرسال <code>HH:MM</code> (UTC):"
    , reply_markup=back_kb("admin_broadcast"))


@dp.message(AdminBcastSchedFSM.time)
async def admin_bsched_time(message: types.Message, state: FSMContext):
    """[ADM3-10] حفظ الجدولة."""

    if message.from_user.id != ADMIN_USER_ID:
        await state.clear()
        return

    raw = (message.text or "").strip()

    if not raw or raw.startswith("/"):
        await state.clear()
        return

    match = re.fullmatch(r"(\d{1,2}):(\d{2})", raw)

    if not match:
        await message.answer(
            "❌ الصيغة <code>HH:MM</code>\nمثال: <code>20:00</code>"
        )
        return

    hh, mm = int(match.group(1)), int(match.group(2))

    if not (hh < 24 and mm < 60):
        await message.answer("❌ وقت غير منطقي.")
        return

    data = await state.get_data()
    chat_id = data.get("broadcast_chat_id")
    message_id = data.get("broadcast_message_id")
    seg = data.get("sched_seg") or "all"
    min_balance = data.get("sched_min")

    job = {
        "chat_id": chat_id,
        "message_id": message_id,
        "segment": seg,
        "time": f"{hh:02d}:{mm:02d}",
    }

    if min_balance is not None:
        job["min_balance"] = float(min_balance)

    await set_setting(
        "scheduled_broadcast", json.dumps(job, ensure_ascii=False),
    )
    await state.clear()
    await audit(  # [NEW 22]
        message.from_user.id, "broadcast_schedule",
        f"segment={seg}", f"time={job['time']}",
    )

    await message.answer(
        "✅ حُفظت الجدولة: البث سيُرسل تلقائياً اليوم\n"
        f"الساعة <b>{job['time']} UTC</b> إلى <b>{_SEG_LABELS[seg]}</b>\n\n"
        "للإلغاء قبل التنفيذ: أرسل كلمة <code>إلغاء البث</code> من شاشة البث.",
        reply_markup=back_kb("admin_tools_menu"),
    )


@dp.callback_query(F.data == "admin_budget")
async def admin_budget(cb: types.CallbackQuery, state: FSMContext):
    """[ADM3-5] ضبط ميزانية السحوبات اليومية."""

    if cb.from_user.id != ADMIN_USER_ID:
        await cb.answer("للأدمن الرئيسي فقط.", show_alert=True)
        return

    await cb.answer()
    await state.clear()
    await state.set_state(AdminBudgetFSM.value)

    current = await get_float_setting("payout_budget_daily", 0.0)
    current_txt = money(current) if current > 0 else "معطّلة (0)"

    await cb.message.answer(
        "💸 <b>ميزانية السحوبات اليومية</b>\n\n"
        "أي اعتماد سحب يجعل إجمالي اليوم يتجاوزها يُرفض\n"
        "(يرجع الزر للمعالجة بعد رفع الميزانية أو غداً).\n\n"
        f"الحالية: <b>{current_txt}</b>\n\n"
        "أرسل المبلغ الجديد، أو <code>0</code> للتعطيل.\n"
        "للإلغاء أرسل /cancel"
    , reply_markup=back_kb("admin_settings_menu"))


@dp.message(AdminBudgetFSM.value)
async def admin_budget_save(message: types.Message, state: FSMContext):
    """[ADM3-5] حفظ الميزانية."""

    if message.from_user.id != ADMIN_USER_ID:
        await state.clear()
        return

    raw = (message.text or "").strip()

    if raw in ("0", "٠"):  # تعطيل صريح (parse_amount يرفض الصفر)
        amount = 0.0
    else:
        amount = parse_amount(raw)  # [FIX 7]

        if amount is None:
            await message.answer("❌ مبلغ غير صالح.\n\nللإلغاء أرسل /cancel")
            return

    await set_setting("payout_budget_daily", str(amount))
    await state.clear()
    await audit(  # [NEW 22]
        message.from_user.id, "payout_budget", f"amount={amount:g}",
    )

    if amount > 0:
        await message.answer(
            f"✅ ميزانية السحوبات اليومية: <b>{money(amount)}</b>.",
            reply_markup=back_kb("admin_settings_menu"),
        )
    else:
        await message.answer(
            "✅ أُعطّلت الميزانية (بلا حد).",
            reply_markup=back_kb("admin_settings_menu"),
        )


@dp.callback_query(F.data.startswith("adjlist:"))
async def admin_adjlist(cb: types.CallbackQuery, state: FSMContext):
    """[ADM3-6] آخر تعديلات الرصيد لمستخدم مع أزرار التراجع."""

    if not await is_admin_or_supervisor(cb.from_user.id, "finance"):
        await cb.answer("غير مصرّح.", show_alert=True)
        return

    if not await pin_gate(cb):  # [ADM3-1] عملية مالية
        return

    try:
        tid = int(cb.data.split(":", 1)[1])
    except (ValueError, IndexError):
        await cb.answer("معرف غير صالح.", show_alert=True)
        return

    await cb.answer()
    await state.clear()

    db = await get_db()

    try:
        cur = await db.execute(
            """
            SELECT id, admin_id, amount, note, undone, created_at
            FROM balance_adjustments
            WHERE target_tid = ?
            ORDER BY id DESC LIMIT 5
            """,
            (tid,),
        )
        rows = await cur.fetchall()
    finally:
        await db.close()

    if not rows:
        await safe_edit(
            cb.message,
            f"♻️ لا تعديلات يدوية مسجلة على <code>{tid}</code>.",
            back_kb("admin_users"),
        )
        return

    lines = [f"♻️ <b>آخر تعديلات</b> <code>{tid}</code>\n"]
    b = InlineKeyboardBuilder()

    for row in rows:
        sign = "+" if float(row["amount"]) >= 0 else ""
        mark = "↩️ مُتراجع" if row["undone"] else f"{sign}{money(row['amount'])}"
        lines.append(
            f"#{row['id']} | {mark} | بواسطة <code>{row['admin_id']}</code>\n"
            f"🕐 {esc(row['created_at'])[:16]}"
        )

        if not row["undone"]:
            b.button(text=f"↩️ تراجع #{row['id']}",
                     callback_data=f"adjundo:{row['id']}")

    b.button(text="🔙 رجوع", callback_data="admin_users")
    b.adjust(2, 1)

    await safe_edit(cb.message, "\n\n".join(lines), b.as_markup())


@dp.callback_query(F.data.startswith("adjundo:"))
async def admin_adjundo(cb: types.CallbackQuery, state: FSMContext):
    """[ADM3-6] تنفيذ التراجع: قيد معاكس + علامة مرة واحدة."""

    if not await is_admin_or_supervisor(cb.from_user.id, "finance"):
        await cb.answer("غير مصرّح.", show_alert=True)
        return

    if not await pin_gate(cb):  # [ADM3-1]
        return

    try:
        adj_id = int(cb.data.split(":", 1)[1])
    except (ValueError, IndexError):
        await cb.answer("معرف غير صالح.", show_alert=True)
        return

    db = await get_db()

    try:
        cur = await db.execute(
            "SELECT * FROM balance_adjustments WHERE id = ?", (adj_id,),
        )
        adj = await cur.fetchone()
    finally:
        await db.close()

    if not adj:
        await cb.answer("التعديل غير موجود.", show_alert=True)
        return

    if adj["undone"]:
        await cb.answer("سبق التراجع عن هذا التعديل.", show_alert=True)
        return

    result = await apply_balance_adjust(
        adj["target_tid"], round2(-float(adj["amount"])),
        cb.from_user.id,
    )

    if result is None:
        await cb.answer(
            "تعذر التراجع (مستخدم غير موجود أو الرصيد سيصبح سالباً).",
            show_alert=True,
        )
        return

    db = await get_db()

    try:
        await db.execute(
            "UPDATE balance_adjustments SET undone = 1 WHERE id = ?",
            (adj_id,),
        )
        await db.commit()
    finally:
        await db.close()

    await cb.answer("تم التراجع ↩️", show_alert=True)
    await audit(  # [NEW 22]
        cb.from_user.id, "adjust_undo", adj_id,
        f"target={adj['target_tid']};amount={adj['amount']:g}",
    )

    await safe_edit(
        cb.message,
        f"✅ تراجعت عن التعديل #{adj_id}\n"
        f"الرصيد الجديد: {money(result[1])}",
        back_kb("admin_users"),
    )


# ============================================================
# [ADM4-1/4/5/6] ROUND 5 — PHASE 1
# ============================================================

class AdminTagFSM(StatesGroup):  # [ADM4-1] وسوم المستخدمين
    add = State()
    search = State()


class AdminAnnFSM(StatesGroup):  # [ADM4-4] نشر إعلان
    text = State()
    days = State()
    photo = State()  # [R6-PLUS2] صورة الإعلان


class AdminAnomalyFSM(StatesGroup):  # [ADM4-5] عتبات الشواذ
    values = State()


def _tag_manager_kb(tid: int, tags) -> types.InlineKeyboardMarkup:
    """[ADM4-1] لوحة إدارة وسوم مستخدم."""
    b = InlineKeyboardBuilder()

    for row in tags:
        b.button(
            text=f"✖️ {row['tag']}",
            callback_data=f"tagdel:{tid}:{row['id']}",
        )

    b.button(text="➕ إضافة وسم", callback_data=f"tagadd:{tid}")
    b.button(text="🔙 كارت المستخدم", callback_data=f"admin_user_card:{tid}")
    b.adjust(*([1] * (len(tags) + 2)))
    return b.as_markup()


async def _render_tag_manager(tid: int):
    """[ADM4-1] نص + لوحة إدارة الوسوم."""
    db = await get_db()

    try:
        cur = await db.execute(
            "SELECT id, tag FROM user_tags WHERE telegram_id = ?"
            " ORDER BY id",
            (tid,),
        )
        tags = await cur.fetchall()
    finally:
        await db.close()

    text = f"🏷 <b>وسوم المستخدم</b> <code>{tid}</code>\n"

    if tags:
        text += "\n".join(f"• {esc(t['tag'])}" for t in tags)
    else:
        text += "لا وسوم بعد."

    text += (
        "\n\nاضغط ✖️ لحذف وسم، أو أضف وسماً جديداً"
        "\n(الحد الأقصى 3 وسوم لكل مستخدم، طول الوسم 20 حرفاً)."
    )
    return text, _tag_manager_kb(tid, tags)


@dp.callback_query(F.data.startswith("ucard_tag:"))
async def admin_ucard_tag(cb: types.CallbackQuery, state: FSMContext):
    """[ADM4-1] فتح مدير الوسوم من كارت المستخدم."""

    if not await is_admin_or_supervisor(cb.from_user.id, "users"):
        await cb.answer("غير مصرّح.", show_alert=True)
        return

    try:
        tid = int(cb.data.split(":", 1)[1])
    except (ValueError, IndexError):
        await cb.answer("معرف غير صالح.", show_alert=True)
        return

    await cb.answer()
    await state.clear()

    text, kb = await _render_tag_manager(tid)
    await safe_edit(cb.message, text, kb)


@dp.callback_query(F.data.startswith("tagadd:"))
async def admin_tag_add(cb: types.CallbackQuery, state: FSMContext):
    """[ADM4-1] بدء إضافة وسم."""

    if not await is_admin_or_supervisor(cb.from_user.id, "users"):
        await cb.answer("غير مصرّح.", show_alert=True)
        return

    try:
        tid = int(cb.data.split(":", 1)[1])
    except (ValueError, IndexError):
        await cb.answer("معرف غير صالح.", show_alert=True)
        return

    await cb.answer()
    await state.clear()
    await state.update_data(tag_tid=tid)
    await state.set_state(AdminTagFSM.add)
    await cb.message.answer(
        f"🏷 أرسل الوسم للمستخدم <code>{tid}</code>:"
        "\n(مثال: VIP أو مموّل أو متعثر — حتى 20 حرفاً)"
        "\nللإلغاء أرسل /cancel"
    , reply_markup=back_kb(f"admin_user_card:{tid}"))


@dp.message(AdminTagFSM.add)
async def admin_tag_add_save(message: types.Message, state: FSMContext):
    """[ADM4-1] حفظ الوسم الجديد."""

    if not await is_admin_or_supervisor(message.from_user.id, "users"):
        await state.clear()
        return

    tag = (message.text or "").strip()[:20]

    if not tag or tag.startswith("/"):
        await state.clear()
        return

    data = await state.get_data()
    tid = data.get("tag_tid")

    if not tid:
        await message.answer("انتهت الجلسة — أعد من الكارت.")
        await state.clear()
        return

    db = await get_db()

    try:
        cur = await db.execute(
            "SELECT COUNT(*) AS c FROM user_tags WHERE telegram_id = ?",
            (tid,),
        )
        count = (await cur.fetchone())["c"]

        if count >= 3:
            await message.answer("⚠️ الحد الأقصى 3 وسوم — احذف واحداً أولاً.")
            await state.clear()
            return

        await db.execute(
            "INSERT OR IGNORE INTO user_tags"
            " (telegram_id, tag, created_at) VALUES (?, ?, ?)",
            (tid, tag, now_iso()),
        )
        await db.commit()
    finally:
        await db.close()

    await state.clear()
    await audit(  # [NEW 22]
        message.from_user.id, "user_tag", tid, f"tag={tag}",
    )

    kb = InlineKeyboardBuilder()
    kb.button(text="🏷 إدارة الوسوم", callback_data=f"ucard_tag:{tid}")
    kb.adjust(1)
    await message.answer(
        f"✅ أُضيف الوسم: <b>{esc(tag)}</b>",
        reply_markup=kb.as_markup(),
    )


@dp.callback_query(F.data.startswith("tagdel:"))
async def admin_tag_del(cb: types.CallbackQuery, state: FSMContext):
    """[ADM4-1] حذف وسم وإعادة عرض المدير."""

    if not await is_admin_or_supervisor(cb.from_user.id, "users"):
        await cb.answer("غير مصرّح.", show_alert=True)
        return

    parts = cb.data.split(":")

    try:
        tid, tag_id = int(parts[1]), int(parts[2])
    except (ValueError, IndexError):
        await cb.answer("معرف غير صالح.", show_alert=True)
        return

    db = await get_db()

    try:
        await db.execute(
            "DELETE FROM user_tags WHERE id = ? AND telegram_id = ?",
            (tag_id, tid),
        )
        await db.commit()
    finally:
        await db.close()

    await cb.answer("حُذف الوسم.")
    await audit(  # [NEW 22]
        cb.from_user.id, "user_tag_del", tid, f"tag_id={tag_id}",
    )

    text, kb = await _render_tag_manager(tid)
    await safe_edit(cb.message, text, kb)


@dp.callback_query(F.data == "admin_tagsearch")
async def admin_tagsearch(cb: types.CallbackQuery, state: FSMContext):
    """[ADM4-1] فلترة المستخدمين بالوسم."""

    if not await is_admin_or_supervisor(cb.from_user.id, "users"):
        await cb.answer("غير مصرّح.", show_alert=True)
        return

    await cb.answer()
    await state.clear()
    await state.set_state(AdminTagFSM.search)
    await cb.message.answer(
        "🏷 أرسل الوسم لعرض كل مستخدميه:\nللإلغاء أرسل /cancel"
    , reply_markup=back_kb("admin_users"))


@dp.message(AdminTagFSM.search)
async def admin_tag_search_go(message: types.Message, state: FSMContext):
    """[ADM4-1] نتائج الفلترة بالوسم."""

    if not await is_admin_or_supervisor(message.from_user.id, "users"):
        await state.clear()
        return

    tag = (message.text or "").strip()[:20]

    if not tag or tag.startswith("/"):
        await state.clear()
        return

    await state.clear()

    db = await get_db()

    try:
        cur = await db.execute(
            """
            SELECT u.telegram_id AS tid, u.full_name AS full_name,
                   u.balance AS balance, u.is_banned AS is_banned
            FROM user_tags t
            JOIN users u ON u.telegram_id = t.telegram_id
            WHERE t.tag = ?
            ORDER BY u.id LIMIT 20
            """,
            (tag,),
        )
        rows = await cur.fetchall()
    finally:
        await db.close()

    if not rows:
        await message.answer(
            f"📭 لا مستخدمين بالوسم «{esc(tag)}».",
            reply_markup=back_kb("admin_users"),
        )
        return

    lines = [f"🏷 <b>وسم «{esc(tag)}»</b> — {len(rows)} مستخدم\n"]
    b = InlineKeyboardBuilder()

    for row in rows:
        flag = " 🚫" if row["is_banned"] else ""
        lines.append(
            f"<code>{row['tid']}</code> | "
            f"{esc((row['full_name'] or '—')[:18])}{flag}"
        )
        b.button(text=f"👤 {row['tid']}",
                 callback_data=f"admin_user_card:{row['tid']}")

    b.button(text="🔙 رجوع", callback_data="admin_users")
    b.adjust(*([2] * max(1, (len(rows) + 1) // 2)), 1)
    await message.answer("\n".join(lines), reply_markup=b.as_markup())


async def _render_anns_admin():
    """[ADM4-4] شاشة إدارة الإعلانات."""
    now_str = now_iso()

    db = await get_db()

    try:
        cur = await db.execute(
            "SELECT id, text, expires_at FROM announcements"
            " WHERE expires_at > ? ORDER BY id DESC LIMIT 10",
            (now_str,),
        )
        rows = await cur.fetchall()
    finally:
        await db.close()

    if rows:
        lines = [f"📢 <b>الإعلانات النشطة</b> ({len(rows)})\n"]
        for row in rows:
            short = esc(row["text"][:80])
            lines.append(
                f"#{row['id']} حتى {esc(row['expires_at'])[:10]}\n{short}"
            )
    else:
        lines = ["📢 لا إعلانات نشطة حالياً."]

    b = InlineKeyboardBuilder()

    for row in rows:
        b.button(text=f"🗑 حذف #{row['id']}",
                 callback_data=f"anndel:{row['id']}")

    b.button(text="➕ نشر إعلان", callback_data="ann_new")
    b.button(text="🔙 رجوع", callback_data="admin_tools_menu")

    sizes = [2] * len(rows) if rows else []
    sizes += [1, 1]
    b.adjust(*sizes)
    return "\n\n".join(lines), b.as_markup()


@dp.callback_query(F.data == "admin_anns")
async def admin_anns(cb: types.CallbackQuery, state: FSMContext):
    """[ADM4-4] إدارة الإعلانات."""

    if cb.from_user.id != ADMIN_USER_ID:
        await cb.answer("للأدمن الرئيسي فقط.", show_alert=True)
        return

    await cb.answer()
    await state.clear()

    text, kb = await _render_anns_admin()
    await safe_edit(cb.message, text, kb)


@dp.callback_query(F.data == "ann_new")
async def admin_ann_new(cb: types.CallbackQuery, state: FSMContext):
    """[ADM4-4] بدء نشر إعلان."""

    if cb.from_user.id != ADMIN_USER_ID:
        await cb.answer("للأدمن الرئيسي فقط.", show_alert=True)
        return

    await cb.answer()
    await state.clear()
    await state.set_state(AdminAnnFSM.text)
    await cb.message.answer(
        "📢 أرسل نص الإعلان (حتى 800 حرف):\nللإلغاء أرسل /cancel"
    , reply_markup=back_kb("admin_anns"))


@dp.message(AdminAnnFSM.text)
async def admin_ann_text(message: types.Message, state: FSMContext):
    """[ADM4-4] استلام النص ثم سؤال المدة."""

    if message.from_user.id != ADMIN_USER_ID:
        await state.clear()
        return

    text = (message.text or "").strip()[:800]

    if not text or text.startswith("/"):
        await state.clear()
        return

    await state.update_data(ann_text=text)
    await state.set_state(AdminAnnFSM.days)
    await message.answer(
        "🗓 كم يوماً يبقى الإعلان ظاهراً؟"
        "\nأرسل رقماً من 1 إلى 365 (للإلغاء /cancel)"
    , reply_markup=back_kb("admin_anns"))


@dp.message(AdminAnnFSM.days)
async def admin_ann_days(message: types.Message, state: FSMContext):
    """[ADM4-4] حفظ الإعلان."""

    if message.from_user.id != ADMIN_USER_ID:
        await state.clear()
        return

    raw = (message.text or "").strip()

    if not raw or raw.startswith("/"):
        await state.clear()
        return

    try:
        days = int(raw)
    except ValueError:
        await message.answer("❌ أرسل رقماً من 1 إلى 365.")
        return

    if not (1 <= days <= 365):
        await message.answer("❌ المدة من 1 إلى 365 يوماً.")
        return

    data = await state.get_data()
    ann_text = data.get("ann_text") or ""

    if not ann_text:
        await message.answer("انتهت الجلسة — أعد النشر.")
        await state.clear()
        return

    # [R6-PLUS2] خطوة اختيارية: صورة الإعلان
    await state.update_data(ann_days=days)
    await state.set_state(AdminAnnFSM.photo)

    b = InlineKeyboardBuilder()
    b.button(text="⏭ نشر بدون صورة", callback_data="ann_nophoto")
    b.adjust(1)

    await message.answer(
        "🖼 هل تريد إرفاق صورة بالإعلان؟\n"
        "أرسل الصورة الآن أو اضغط «⏭ نشر بدون صورة»:",
        reply_markup=b.as_markup(),
    )


async def _create_announcement(admin_id: int, text: str, days: int,
                               photo_file_id: str = ""):
    """[R6-PLUS2] حفظ الإعلان (نص + صورة اختيارية)."""
    expires = (
        datetime.now(timezone.utc) + timedelta(days=days)
    ).isoformat(timespec="seconds")

    db = await get_db()

    try:
        cur = await db.execute(
            "INSERT INTO announcements"
            " (text, created_by, created_at, expires_at, photo_file_id)"
            " VALUES (?, ?, ?, ?, ?)",
            (text, admin_id, now_iso(), expires, photo_file_id),
        )
        ann_id = cur.lastrowid
        await db.commit()
    finally:
        await db.close()

    await audit(admin_id, "announcement", ann_id, f"days={days}")

    # [R6-PLUS3] بث فوري لمشتركي الجرس 🔔
    pushed = 0

    if await feat_on("ann_push"):
        db_p = await get_db()

        try:
            cur_p = await db_p.execute(
                "SELECT telegram_id FROM users"
                " WHERE ann_notify = 1 AND is_banned = 0"
                " AND COALESCE(ban_until, '') = '' LIMIT 300",
            )
            subs = await cur_p.fetchall()
        finally:
            await db_p.close()

        for srow in subs:
            try:
                await bot.send_message(srow["telegram_id"], text[:3500])
                pushed += 1
            except Exception:
                continue

    kb = InlineKeyboardBuilder()
    kb.button(text="📢 شاشة الإعلانات", callback_data="admin_anns")
    kb.adjust(1)
    await bot.send_message(
        admin_id,
        f"✅ نُشر الإعلان #{ann_id} لمدة {days} يوماً."
        + ("\n🖼 مع صورة." if photo_file_id else "")
        + (f"\n🔔 بُثّ لـ {pushed} مشترك." if pushed else "")
        + "\nيظهر للمستخدمين من زر «🍀 عروضنا الحالية».",
        reply_markup=kb.as_markup(),
    )


@dp.message(AdminAnnFSM.photo, F.photo)
async def admin_ann_photo(message: types.Message, state: FSMContext):
    """[R6-PLUS2] استلام صورة الإعلان."""

    if message.from_user.id != ADMIN_USER_ID:
        await state.clear()
        return

    data = await state.get_data()
    days = int(data.get("ann_days") or 1)
    ann_text = data.get("ann_text") or ""
    await state.clear()

    photo_id = message.photo[-1].file_id

    await _create_announcement(
        message.from_user.id, ann_text, days, photo_id,
    )


@dp.callback_query(F.data == "ann_nophoto")
async def ann_nophoto(cb: types.CallbackQuery, state: FSMContext):
    """[R6-PLUS2] نشر بدون صورة."""

    if cb.from_user.id != ADMIN_USER_ID:
        await cb.answer("للأدمن فقط.", show_alert=True)
        return

    data = await state.get_data()
    days = int(data.get("ann_days") or 1)
    ann_text = data.get("ann_text") or ""
    await state.clear()

    if not ann_text:
        await cb.answer("انتهت الجلسة.", show_alert=True)
        return

    await _create_announcement(cb.from_user.id, ann_text, days, "")
    await cb.answer("✅ نُشر بدون صورة", show_alert=True)


@dp.callback_query(F.data.startswith("anndel:"))
async def admin_ann_del(cb: types.CallbackQuery, state: FSMContext):
    """[ADM4-4] حذف إعلان."""

    if cb.from_user.id != ADMIN_USER_ID:
        await cb.answer("للأدمن الرئيسي فقط.", show_alert=True)
        return

    try:
        ann_id = int(cb.data.split(":", 1)[1])
    except (ValueError, IndexError):
        await cb.answer("معرف غير صالح.", show_alert=True)
        return

    db = await get_db()

    try:
        await db.execute(
            "DELETE FROM announcements WHERE id = ?", (ann_id,),
        )
        await db.execute(
            "DELETE FROM announcement_reads WHERE announcement_id = ?",
            (ann_id,),
        )
        await db.commit()
    finally:
        await db.close()

    await cb.answer("حُذف الإعلان.")
    await audit(  # [NEW 22]
        cb.from_user.id, "announcement_del", ann_id,
    )

    text, kb = await _render_anns_admin()
    await safe_edit(cb.message, text, kb)


@dp.callback_query(F.data == "ann_menu")
async def ann_menu(cb: types.CallbackQuery, state: FSMContext):
    """[ADM4-4] شاشة الإعلانات للمستخدم + تعليم كمقروءة."""

    if not await user_allowed(cb.from_user.id):
        await cb.answer("غير مسموح.", show_alert=True)
        return

    await cb.answer()
    await state.clear()

    now_str = now_iso()
    tid = cb.from_user.id

    db = await get_db()

    try:
        cur = await db.execute(
            "SELECT id, text, created_at FROM announcements"
            " WHERE expires_at > ? ORDER BY id DESC LIMIT 10",
            (now_str,),
        )
        rows = await cur.fetchall()

        cur = await db.execute(
            "SELECT announcement_id FROM announcement_reads"
            " WHERE telegram_id = ?",
            (tid,),
        )
        read_ids = {r["announcement_id"] for r in await cur.fetchall()}

        for row in rows:  # تعليم الكل كمقروءة بعد العرض
            await db.execute(
                "INSERT OR IGNORE INTO announcement_reads"
                " (announcement_id, telegram_id, read_at) VALUES (?, ?, ?)",
                (row["id"], tid, now_str),
            )
        await db.commit()
    finally:
        await db.close()

    if not rows:
        await safe_edit(
            cb.message, "📢 لا إعلانات حالياً.", back_kb("menu_back"),
        )
        return

    lines = ["📢 <b>الإعلانات</b>\n"]

    for row in rows:
        fresh = "" if row["id"] in read_ids else "🆕 "
        lines.append(f"{fresh}🗓 {esc(row['created_at'])[:10]}\n{row['text']}")

    await safe_edit(cb.message, "\n\n".join(lines), back_kb("menu_back"))


async def check_anomaly_deposit(telegram_id: int, amount: float, created_at):
    """[ADM4-5] تنبيه: إيداع ضخم أو إيداع فوري لحساب جديد."""
    try:
        dep_max = await get_float_setting("anom_dep_max", 0.0)
        new_dep = await get_float_setting("anom_new_dep", 0.0)
        alerts = []

        if dep_max > 0 and amount >= dep_max:
            alerts.append(f"💎 إيداع مفرد كبير: <b>{money(amount)}</b>")

        if new_dep > 0 and amount >= new_dep and created_at:
            try:
                created = datetime.fromisoformat(str(created_at))

                if created.tzinfo is None:
                    created = created.replace(tzinfo=timezone.utc)

                age_min = (
                    datetime.now(timezone.utc) - created
                ).total_seconds() / 60

                if age_min <= 10:
                    alerts.append("🆕 إيداع فوري بعد التسجيل مباشرة")
            except Exception:
                pass

        if not alerts:
            return

        text = (
            "🚨 <b>تنبيه شواذ — شحن</b>\n\n"
            f"👤 <code>{telegram_id}</code>\n"
            f"💰 المبلغ: {money(amount)}\n\n"
            + "\n".join(alerts)
        )
        await bot.send_message(ADMIN_USER_ID, text)
        await mirror(text)
        await audit(  # [NEW 22]
            0, "anomaly_deposit", telegram_id, f"amount={round2(amount):g}",
        )
    except Exception:
        logger.exception("فحص شواذ الإيداع فشل")


async def check_anomaly_withdraw(telegram_id: int):
    """[ADM4-5] تنبيه: تكرار طلبات السحب خلال ساعة."""
    try:
        cnt_max = int(float(await get_setting("anom_wd_count") or 3))

        if cnt_max <= 0:
            return

        hour_ago = (
            datetime.now(timezone.utc) - timedelta(hours=1)
        ).isoformat(timespec="seconds")

        db = await get_db()

        try:
            cur = await db.execute(
                "SELECT COUNT(*) AS c FROM finance_requests"
                " WHERE telegram_id = ? AND type = 'withdraw'"
                " AND created_at >= ?",
                (telegram_id, hour_ago),
            )
            count = (await cur.fetchone())["c"]
        finally:
            await db.close()

        if count != cnt_max:
            return  # تنبيه واحد عند بلوغ العتبة بالضبط

        text = (
            "🚨 <b>تنبيه شواذ — سحب</b>\n\n"
            f"👤 <code>{telegram_id}</code>\n"
            f"🔁 {count} طلبات سحب خلال ساعة واحدة"
        )
        await bot.send_message(ADMIN_USER_ID, text)
        await mirror(text)
        await audit(  # [NEW 22]
            0, "anomaly_withdraw", telegram_id, f"count={count}",
        )
    except Exception:
        logger.exception("فحص شواذ السحب فشل")


@dp.callback_query(F.data == "admin_anomaly")
async def admin_anomaly(cb: types.CallbackQuery, state: FSMContext):
    """[ADM4-5] شاشة عتبات كشف الشواذ."""

    if cb.from_user.id != ADMIN_USER_ID:
        await cb.answer("للأدمن الرئيسي فقط.", show_alert=True)
        return

    await cb.answer()
    await state.clear()

    dep_max = await get_float_setting("anom_dep_max", 0.0)
    wd_cnt = int(float(await get_setting("anom_wd_count") or 3))
    new_dep = await get_float_setting("anom_new_dep", 0.0)

    def flag(value):
        return "✅ مفعّل" if value > 0 else "⭕ معطّل"

    await safe_edit(
        cb.message,
        "🚨 <b>كشف الشواذ</b>\n\n"
        "تنبيهات فورية (لك ولغرفة المراقبة) عند:\n"
        "• إيداع مفرد ضخم\n"
        "• تكرار طلبات سحب متلاحقة\n"
        "• إيداع فوري بعد التسجيل مباشرة\n\n"
        f"💎 حد الإيداع المفرد: {money(dep_max)} — {flag(dep_max)}\n"
        f"🔁 طلبات السحب/ساعة: {wd_cnt} — {flag(wd_cnt)}\n"
        f"🆕 حد إيداع الجديد: {money(new_dep)} — {flag(new_dep)}",
        InlineKeyboardBuilder()
        .button(text="✏️ تعديل العتبات", callback_data="anom_edit")
        .button(text="🔙 رجوع", callback_data="admin_settings_menu")
        .adjust(1)
        .as_markup(),
    )


@dp.callback_query(F.data == "anom_edit")
async def admin_anom_edit(cb: types.CallbackQuery, state: FSMContext):
    """[ADM4-5] تعديل العتبات."""

    if cb.from_user.id != ADMIN_USER_ID:
        await cb.answer("للأدمن الرئيسي فقط.", show_alert=True)
        return

    await cb.answer()
    await state.clear()
    await state.set_state(AdminAnomalyFSM.values)
    await cb.message.answer(
        "🚨 أرسل ثلاثة أرقام مفصولة بمسافة:\n"
        "حد_الإيداع_المفرد عدد_طلبات_السحب_في_الساعة حد_إيداع_الجديد\n\n"
        "مثال: <code>1000 3 200</code>\n"
        "(صفر = تعطيل الفحص المعني — للإلغاء /cancel)"
    , reply_markup=back_kb("admin_anomaly"))


@dp.message(AdminAnomalyFSM.values)
async def admin_anom_save(message: types.Message, state: FSMContext):
    """[ADM4-5] حفظ العتبات."""

    if message.from_user.id != ADMIN_USER_ID:
        await state.clear()
        return

    parts = (message.text or "").split()

    if not parts or parts[0].startswith("/"):
        await state.clear()
        return

    if len(parts) != 3:
        await message.answer(
            "❌ الصيغة: <code>حد_الإيداع عدد_السحب حد_الجديد</code>"
        )
        return

    try:
        dep_max = parse_amount(parts[0]) or 0.0
        wd_cnt = int(float(parts[1]))
        new_dep = parse_amount(parts[2]) or 0.0
    except (ValueError, TypeError):
        await message.answer("❌ أرقام غير صالحة.")
        return

    if not (0 <= wd_cnt <= 50):
        await message.answer("❌ عدد طلبات السحب من 0 إلى 50.")
        return

    await set_setting("anom_dep_max", str(dep_max))
    await set_setting("anom_wd_count", str(wd_cnt))
    await set_setting("anom_new_dep", str(new_dep))
    await state.clear()
    await audit(  # [NEW 22]
        message.from_user.id, "anomaly_thresholds",
        "", f"dep={dep_max:g};wd={wd_cnt};new={new_dep:g}",
    )

    wd_line = (
        f"🔁 {wd_cnt} طلب سحب/ساعة"
        if wd_cnt > 0 else "🔁 طلبات السحب معطّلة"
    )
    await message.answer(
        "✅ حُفظت عتبات كشف الشواذ:\n"
        f"💎 إيداع مفرد ≥ {money(dep_max) if dep_max else 'معطّل'}\n"
        + wd_line,
        reply_markup=back_kb("admin_settings_menu"),
    )


@dp.callback_query(F.data == "admin_accreport")
async def admin_accreport(cb: types.CallbackQuery, state: FSMContext):
    """[ADM4-6] التقرير المحاسبي PDF للشهر الحالي."""

    if cb.from_user.id != ADMIN_USER_ID:
        await cb.answer("للأدمن الرئيسي فقط.", show_alert=True)
        return

    await cb.answer("جاري بناء التقرير...")

    now = datetime.now(timezone.utc)
    month_start = now.replace(
        day=1, hour=0, minute=0, second=0, microsecond=0,
    ).isoformat(timespec="seconds")
    today = now.isoformat(timespec="seconds")

    db = await get_db()

    try:
        cur = await db.execute(
            "SELECT COUNT(*) AS c, COALESCE(SUM(amount), 0) AS s"
            " FROM transactions WHERE type = 'deposit' AND created_at >= ?",
            (month_start,),
        )
        dep = await cur.fetchone()

        cur = await db.execute(
            "SELECT COUNT(*) AS c, COALESCE(SUM(amount), 0) AS s"
            " FROM finance_requests"
            " WHERE type = 'withdraw' AND status = 'approved'"
            " AND created_at >= ?",
            (month_start,),
        )
        wd = await cur.fetchone()

        cur = await db.execute(
            "SELECT COUNT(*) AS c, COALESCE(SUM(amount), 0) AS s"
            " FROM payouts WHERE status = 'paid' AND created_at >= ?",
            (month_start,),
        )
        paid = await cur.fetchone()

        cur = await db.execute(
            "SELECT COUNT(*) AS c FROM users WHERE created_at >= ?",
            (month_start,),
        )
        new_users = (await cur.fetchone())["c"]

        cur = await db.execute(
            """
            SELECT u.telegram_id AS tid, SUM(t.amount) AS total
            FROM transactions t
            JOIN users u ON u.id = t.user_id
            WHERE t.type = 'deposit' AND t.created_at >= ?
            GROUP BY t.user_id ORDER BY total DESC LIMIT 10
            """,
            (month_start,),
        )
        top_rows = await cur.fetchall()
    finally:
        await db.close()

    rows = [
        ("Period", f"{month_start[:10]} to {today[:10]}"),
        ("Deposits", f"{dep['c']} ops / {round2(dep['s']):g}"),
        ("Withdrawals approved",
         f"{wd['c']} ops / {round2(wd['s']):g}"),
        ("Payouts paid", f"{paid['c']} ops / {round2(paid['s']):g}"),
        ("New users", new_users),
    ]

    for index, row in enumerate(top_rows, start=1):
        rows.append((
            f"Top depositor #{index}",
            f"{row['tid']} = {round2(row['total']):g}",
        ))

    pdf = build_receipt_pdf(
        f"Accounting Report {today[:7]}", rows,
    )

    if pdf is None:
        await bot.send_message(
            ADMIN_USER_ID,
            "⚠️ مكتبة fpdf2 غير مثبتة — لا يمكن إنشاء التقرير.",
        )
        return

    caption = (
        f"🧾 <b>التقرير المحاسبي</b> — {today[:7]}\n"
        f"شحن: {dep['c']} عملية ({money(dep['s'])}) | "
        f"سحب معتمد: {money(wd['s'])} | "
        f"مدفوعات: {money(paid['s'])}"
    )
    await bot.send_document(ADMIN_USER_ID, pdf, caption=caption)

    mirror_chat = (await get_setting("mirror_chat_id") or "").strip()

    if mirror_chat.lstrip("-").isdigit() and int(mirror_chat) != ADMIN_USER_ID:
        try:
            from fpdf import FPDF  # noqa: F401 — ضمان توفر المكتبة أعلاه

            pdf2 = build_receipt_pdf(
                f"Accounting Report {today[:7]}", rows,
            )
            await bot.send_document(int(mirror_chat), pdf2, caption=caption)
        except Exception as exc:
            logger.warning("نسخة التقرير للمرآة فشلت: %s", exc)

    await audit(  # [NEW 22]
        cb.from_user.id, "accounting_report", today[:7],
        f"dep={round2(dep['s']):g};wd={round2(wd['s']):g}",
    )


# ============================================================
# [ADM4-2/3 + USR4-1/3] ROUND 5 — PHASE 2 (FINANCIAL)
# ============================================================

class AdminLoyalFSM(StatesGroup):  # [USR4-1] عتبات الولاء
    values = State()


class AdminCheckinFSM(StatesGroup):  # [USR4-3] إعداد الحضور
    values = State()


class AdminContestFSM(StatesGroup):  # [ADM4-2] مسابقة الإحالات
    days = State()
    prizes = State()


class AdminAutowdFSM(StatesGroup):  # [ADM4-3] الاعتماد التلقائي
    cap = State()
    tid = State()


async def get_loyalty(telegram_id: int) -> dict:
    """[USR4-1] مستوى الولاء حسب إجمالي الإيداعات + خصم العمولة."""
    s2 = await get_float_setting("loyal_s2", 0.0)
    s3 = await get_float_setting("loyal_s3", 0.0)
    d2 = await get_float_setting("loyal_d2", 0.0)
    d3 = await get_float_setting("loyal_d3", 0.0)

    db = await get_db()

    try:
        cur = await db.execute(
            "SELECT COALESCE(SUM(amount), 0) AS s FROM transactions"
            " WHERE user_id = (SELECT id FROM users WHERE telegram_id = ?)"
            " AND type = 'deposit'",
            (telegram_id,),
        )
        total = round2((await cur.fetchone())["s"])
    finally:
        await db.close()

    if s2 <= 0 or s3 <= 0:  # الميزة معطّلة
        return {"tier": 1, "name": "", "discount": 0.0,
                "total": total, "line": "", "next_left": 0.0}

    if total >= s3:
        tier, name, discount = 3, "ذهبي", d3
    elif total >= s2:
        tier, name, discount = 2, "فضي", d2
    else:
        tier, name, discount = 1, "برونزي", 0.0

    line = f"💎 المستوى: <b>{name}</b>"

    if discount > 0:
        line += f" (خصم عمولة {money(discount)}%)"

    next_left = 0.0

    if tier == 1 and s2 > total:
        next_left = round2(s2 - total)
        line += f"\nباقي {money(next_left)} للوصول لمستوى فضي"
    elif tier == 2 and s3 > total:
        next_left = round2(s3 - total)
        line += f"\nباقي {money(next_left)} للوصول لمستوى ذهبي"

    return {"tier": tier, "name": name, "discount": discount,
            "total": total, "line": line, "next_left": next_left}


@dp.callback_query(F.data == "admin_loyal")
async def admin_loyal(cb: types.CallbackQuery, state: FSMContext):
    """[USR4-1] شاشة مستويات الولاء."""

    if cb.from_user.id != ADMIN_USER_ID:
        await cb.answer("للأدمن الرئيسي فقط.", show_alert=True)
        return

    await cb.answer()
    await state.clear()

    s2 = await get_float_setting("loyal_s2", 0.0)
    s3 = await get_float_setting("loyal_s3", 0.0)
    d2 = await get_float_setting("loyal_d2", 0.0)
    d3 = await get_float_setting("loyal_d3", 0.0)

    if s2 > 0:
        status = (
            f"✅ مفعّلة\n\n"
            f"🥈 فضي: إيداعات ≥ {money(s2)} → خصم {money(d2)}%\n"
            f"🥇 ذهبي: إيداعات ≥ {money(s3)} → خصم {money(d3)}%"
        )
    else:
        status = "⭕ معطّلة"

    await safe_edit(
        cb.message,
        "💎 <b>مستويات الولاء</b>\n\n"
        "ترقية تلقائية حسب إجمالي إيداعات المستخدم،"
        " مع خصم من عمولة الشحن:\n\n" + status,
        InlineKeyboardBuilder()
        .button(text="✏️ تعديل المستويات", callback_data="loyal_edit")
        .button(text="🔙 رجوع", callback_data="admin_settings_menu")
        .adjust(1)
        .as_markup(),
    )


@dp.callback_query(F.data == "loyal_edit")
async def admin_loyal_edit(cb: types.CallbackQuery, state: FSMContext):
    """[USR4-1] تعديل عتبات الولاء."""

    if cb.from_user.id != ADMIN_USER_ID:
        await cb.answer("للأدمن الرئيسي فقط.", show_alert=True)
        return

    await cb.answer()
    await state.clear()
    await state.set_state(AdminLoyalFSM.values)
    await cb.message.answer(
        "💎 أرسل أربعة أرقام مفصولة بمسافة:\n"
        "عتبة_الفضي عتبة_الذهبي خصم_الفضي% خصم_الذهبي%\n\n"
        "مثال: <code>1000 5000 2 5</code>\n"
        "(أصفار = تعطيل الميزة — للإلغاء /cancel)"
    , reply_markup=back_kb("admin_loyal"))


@dp.message(AdminLoyalFSM.values)
async def admin_loyal_save(message: types.Message, state: FSMContext):
    """[USR4-1] حفظ عتبات الولاء."""

    if message.from_user.id != ADMIN_USER_ID:
        await state.clear()
        return

    parts = (message.text or "").split()

    if not parts or parts[0].startswith("/"):
        await state.clear()
        return

    if len(parts) != 4:
        await message.answer(
            "❌ الصيغة: <code>فضي ذهبي خصم_فضي خصم_ذهبي</code>"
        )
        return

    try:
        s2, s3 = (parse_amount(x) or 0.0 for x in parts[:2])
        d2, d3 = (min(50.0, parse_amount(x) or 0.0) for x in parts[2:])
    except (ValueError, TypeError):
        await message.answer("❌ أرقام غير صالحة.")
        return

    if s3 > 0 and s3 <= s2:
        await message.answer("❌ عتبة الذهبية يجب أن تتجاوز الفضية.")
        return

    await set_setting("loyal_s2", str(s2))
    await set_setting("loyal_s3", str(s3))
    await set_setting("loyal_d2", str(d2))
    await set_setting("loyal_d3", str(d3))
    await state.clear()
    await audit(  # [NEW 22]
        message.from_user.id, "loyalty_tiers",
        "", f"s2={s2:g};s3={s3:g};d2={d2:g};d3={d3:g}",
    )

    if s2 > 0:
        result = (
            f"🥈 فضي ≥ {money(s2)} → -{money(d2)}% عمولة\n"
            f"🥇 ذهبي ≥ {money(s3)} → -{money(d3)}% عمولة"
        )
    else:
        result = "معطّلة"

    await message.answer(
        f"✅ مستويات الولاء: {result}",
        reply_markup=back_kb("admin_settings_menu"),
    )


async def do_checkin(telegram_id: int):
    """
    [USR4-3] حضور اليوم: مكافأة تتصاعد مع السلسلة.
    يعيد (ok, streak, amount, message).
    """
    if (await get_setting("checkin_enabled") or "0") != "1":
        return False, 0, 0.0, "🔥 الحضور اليومي معطّل حالياً."

    base = await get_float_setting("checkin_base", 0.0)
    cap = int(float(await get_setting("checkin_cap") or 1))

    if base <= 0:
        return False, 0, 0.0, "🔥 الحضور اليومي غير مضبوط بعد."

    now = datetime.now(timezone.utc)
    today = f"{now:%Y-%m-%d}"
    yesterday = f"{now - timedelta(days=1):%Y-%m-%d}"

    db = await get_db()

    try:
        await db.execute("BEGIN IMMEDIATE")

        cur = await db.execute(
            "SELECT 1 FROM checkins WHERE telegram_id = ? AND day = ?",
            (telegram_id, today),
        )

        if await cur.fetchone():
            await db.rollback()
            return False, 0, 0.0, "✅ حضرت اليوم بالفعل — عداوة غداً!"

        cur = await db.execute(
            "SELECT streak FROM checkins"
            " WHERE telegram_id = ? AND day = ?",
            (telegram_id, yesterday),
        )
        prev = await cur.fetchone()
        streak = (prev["streak"] + 1) if prev else 1

        amount = round2(base * min(streak, max(1, cap)))

        cur = await db.execute(
            "INSERT INTO checkins"
            " (telegram_id, day, streak, amount, created_at)"
            " VALUES (?, ?, ?, ?, ?)",
            (telegram_id, today, streak, amount, now_iso()),
        )

        if cur.rowcount != 1:  # سبق مسابقة ذرّية
            await db.rollback()
            return False, 0, 0.0, "✅ حضرت اليوم بالفعل — عداوة غداً!"

        cur = await db.execute(
            "SELECT id, balance FROM users WHERE telegram_id = ?",
            (telegram_id,),
        )
        user = await cur.fetchone()

        if not user:
            await db.rollback()
            return False, 0, 0.0, "حسابك غير موجود."

        new_balance = round2(float(user["balance"] or 0) + amount)
        await db.execute(
            "UPDATE users SET balance = ? WHERE id = ?",
            (new_balance, user["id"]),
        )
        await db.execute(
            "INSERT INTO transactions"
            " (user_id, type, amount, note, created_at)"
            " VALUES (?, 'bonus', ?, ?, ?)",
            (user["id"], amount, f"checkin;streak={streak}", now_iso()),
        )
        await db.commit()
    finally:
        await db.close()

    fire = "🔥" * min(streak, 5)
    msg = (
        f"{fire} حضرت اليوم!\n\n"
        f"📈 السلسلة: <b>{streak}</b> يوم متتالٍ\n"
        f"💰 المكافأة: <b>+{money(amount)}</b>\n"
    )

    if streak < cap:
        msg += f"\nغداً تصير {money(round2(base * (streak + 1)))} — لا تفوتها!"
    else:
        msg += "\nوصلت أقصى مضاعف السلسلة 🔥"

    return True, streak, amount, msg


@dp.callback_query(F.data == "checkin")
async def checkin_cb(cb: types.CallbackQuery, state: FSMContext):
    """[USR4-3] زر الحضور اليومي."""

    if not await user_allowed(cb.from_user.id):
        await cb.answer("غير مسموح.", show_alert=True)
        return

    await state.clear()

    _, _, _, msg = await do_checkin(cb.from_user.id)
    await cb.answer(msg, show_alert=True)


@dp.callback_query(F.data == "admin_checkin")
async def admin_checkin(cb: types.CallbackQuery, state: FSMContext):
    """[USR4-3] شاشة إعداد الحضور اليومي."""

    if cb.from_user.id != ADMIN_USER_ID:
        await cb.answer("للأدمن الرئيسي فقط.", show_alert=True)
        return

    await cb.answer()
    await state.clear()

    enabled = (await get_setting("checkin_enabled") or "0") == "1"
    base = await get_float_setting("checkin_base", 0.0)
    cap = int(float(await get_setting("checkin_cap") or 1))

    status = "✅ مفعّل" if enabled and base > 0 else "⭕ معطّل"

    await safe_edit(
        cb.message,
        "🔥 <b>مكافأة الحضور اليومي</b>\n\n"
        "زر «🔥 حضور اليوم» في بروفايل المستخدم:\n"
        "مكافأة يومية تتصاعد مع أيام السلسلة حتى السقف.\n\n"
        f"الحالة: {status}\n"
        f"💵 المبلغ الأساسي (يوم 1): {money(base)}\n"
        f"⚡ سقف مضاعف السلسلة: ×{cap}\n"
        f"(اليوم n = {money(base)} × n حتى السقف)",
        InlineKeyboardBuilder()
        .button(text="✏️ تعديل", callback_data="checkin_edit")
        .button(text="🔙 رجوع", callback_data="admin_settings_menu")
        .adjust(1)
        .as_markup(),
    )


@dp.callback_query(F.data == "checkin_edit")
async def admin_checkin_edit(cb: types.CallbackQuery, state: FSMContext):
    """[USR4-3] تعديل إعداد الحضور."""

    if cb.from_user.id != ADMIN_USER_ID:
        await cb.answer("للأدمن الرئيسي فقط.", show_alert=True)
        return

    await cb.answer()
    await state.clear()
    await state.set_state(AdminCheckinFSM.values)
    await cb.message.answer(
        "🔥 أرسل ثلاثة قيم مفصولة بمسافة:\n"
        "تشغيل(0/1) المبلغ_الأساسي سقف_السلسلة\n\n"
        "مثال: <code>1 2 5</code>\n"
        "(اليوم 1 = 2، اليوم 2 = 4... حتى ×5 — للإلغاء /cancel)"
    , reply_markup=back_kb("admin_checkin"))


@dp.message(AdminCheckinFSM.values)
async def admin_checkin_save(message: types.Message, state: FSMContext):
    """[USR4-3] حفظ إعداد الحضور."""

    if message.from_user.id != ADMIN_USER_ID:
        await state.clear()
        return

    parts = (message.text or "").split()

    if not parts or parts[0].startswith("/"):
        await state.clear()
        return

    if len(parts) != 3:
        await message.answer(
            "❌ الصيغة: <code>تشغيل(0/1) المبلغ سقف_السلسلة</code>"
        )
        return

    try:
        enabled = int(parts[0])
        base = parse_amount(parts[1]) or 0.0
        cap = int(float(parts[2]))
    except (ValueError, TypeError):
        await message.answer("❌ قيم غير صالحة.")
        return

    if enabled not in (0, 1) or not (1 <= cap <= 30):
        await message.answer("❌ التشغيل 0/1 والسقف من 1 إلى 30.")
        return

    if enabled and base <= 0:
        await message.answer("❌ المبلغ الأساسي يجب أن يتجاوز الصفر.")
        return

    await set_setting("checkin_enabled", str(enabled))
    await set_setting("checkin_base", str(base))
    await set_setting("checkin_cap", str(cap))
    await state.clear()
    await audit(  # [NEW 22]
        message.from_user.id, "checkin_setup",
        "", f"on={enabled};base={base:g};cap={cap}",
    )

    await message.answer(
        "✅ الحضور اليومي: "
        + ("مفعّل 🔥" if enabled else "معطّل")
        + f"\nالأساسي {money(base)} × السلسلة حتى ×{cap}",
        reply_markup=back_kb("admin_settings_menu"),
    )


async def _contest_leaderboard(limit: int = 10):
    """[ADM4-2] صدارة الإحالات ضمن نافذة المسابقة الحالية."""
    start = await get_setting("contest_start") or ""
    end = await get_setting("contest_end") or ""

    if not start or not end:
        return []

    db = await get_db()

    try:
        cur = await db.execute(
            """
            SELECT referrer_id AS rid, COUNT(*) AS c
            FROM users
            WHERE referrer_id IS NOT NULL AND referrer_id != 0
              AND created_at >= ? AND created_at <= ?
            GROUP BY referrer_id
            ORDER BY c DESC, rid
            LIMIT ?
            """,
            (start, end, limit),
        )
        return await cur.fetchall()
    finally:
        await db.close()


async def contest_grant() -> str:
    """
    [ADM4-2] منح جوائز المسابقة (أكواد هدايا) لأفضل المتصدرين.
    يعيد نص ملخص النتائج.
    """
    prizes_raw = (await get_setting("contest_prizes") or "").strip()
    granted = (await get_setting("contest_granted") or "0")

    if granted == "1":
        return "سبق منح جوائز هذه المسابقة."

    if not prizes_raw:
        return "لا جوائز مضبوطة."

    try:
        prizes = [parse_amount(x) for x in prizes_raw.split(",")]
    except (ValueError, TypeError):
        prizes = []

    prizes = [p for p in prizes if p]

    if not prizes:
        return "جوائز غير صالحة."

    top = await _contest_leaderboard(limit=len(prizes))

    if not top:
        await set_setting("contest_granted", "1")
        return "انتهت المسابقة بلا متصدرين — لا جوائز."

    lines = ["🏆 <b>نتائج مسابقة الإحالات</b>\n"]

    for index, row in enumerate(top):
        prize = prizes[index]
        code = await generate_unique_gift_code(prize)

        lines.append(
            f"🥇 المركز {index + 1}: <code>{row['rid']}</code>"
            f" — {row['c']} إحالة — كود بقيمة <b>{money(prize)}</b>"
            f"\n<code>{code}</code>"
        )

        try:
            await bot.send_message(
                row["rid"],
                f"🏆 مبروك! المركز {index + 1} في مسابقة الإحالات"
                f" ({row['c']} إحالة)\n"
                f"🎁 كود هدية بقيمة {money(prize)}:\n<code>{code}</code>\n\n"
                "استخدمه من 🎁 الهدايا بالقائمة.",
            )
        except Exception as exc:
            logger.warning(
                "إبلاغ فائز المسابقة %s فشل: %s", row["rid"], exc,
            )

        await audit(  # [NEW 22]
            ADMIN_USER_ID, "contest_prize", row["rid"],
            f"rank={index + 1};refs={row['c']};prize={prize:g};code={code}",
        )

    await set_setting("contest_granted", "1")
    return "\n".join(lines)


async def contest_if_due() -> bool:
    """[ADM4-2] منح تلقائي عند انتهاء مهل المسابقة."""
    end = (await get_setting("contest_end") or "").strip()
    granted = (await get_setting("contest_granted") or "0")

    if not end or granted == "1":
        return False

    try:
        end_dt = datetime.fromisoformat(end)

        if end_dt.tzinfo is None:
            end_dt = end_dt.replace(tzinfo=timezone.utc)
    except ValueError:
        return False

    if datetime.now(timezone.utc) < end_dt:
        return False

    summary = await contest_grant()

    if "سبق منح" not in summary:
        text = f"⏰ <b>انتهت مسابقة الإحالات</b>\n\n{summary}"

        try:
            await bot.send_message(ADMIN_USER_ID, text)
        except Exception as exc:
            logger.warning("تقرير المسابقة فشل: %s", exc)

        await mirror(text)
        return True

    return False


def _contest_status_kb():
    b = InlineKeyboardBuilder()
    b.button(text="⏹ إنهاء ومنح الآن", callback_data="contest_endnow")
    b.button(text="🔙 رجوع", callback_data="admin_tools_menu")
    b.adjust(1)
    return b.as_markup()


@dp.callback_query(F.data == "admin_contest")
async def admin_contest(cb: types.CallbackQuery, state: FSMContext):
    """[ADM4-2] شاشة مسابقة الإحالات."""

    if cb.from_user.id != ADMIN_USER_ID:
        await cb.answer("للأدمن الرئيسي فقط.", show_alert=True)
        return

    await cb.answer()
    await state.clear()

    start = (await get_setting("contest_start") or "").strip()
    end = (await get_setting("contest_end") or "").strip()
    prizes = (await get_setting("contest_prizes") or "").strip()
    granted = (await get_setting("contest_granted") or "0") == "1"

    if not start or not end:
        await safe_edit(
            cb.message,
            "🏆 <b>مسابقة الإحالات</b>\n\n"
            "لا مسابقة جارية. ابدأ واحدة وحدد المدة والجوائز،"
            " وعند الانتهاء تُمنح أكواد الهدايا تلقائياً لأفضل المتصدرين.",
            InlineKeyboardBuilder()
            .button(text="➕ بدء مسابقة", callback_data="contest_new")
            .button(text="🔙 رجوع", callback_data="admin_tools_menu")
            .adjust(1)
            .as_markup(),
        )
        return

    top = await _contest_leaderboard()

    lines = [f"🏆 <b>مسابقة الإحالات</b> {'(منحت ✅)' if granted else '(جارية)'}\n"]
    lines.append(f"🗓 من {start[:10]} حتى {end[:10]}")
    lines.append("🎁 الجوائز: " + " | ".join(
        f"م{i + 1}: {money(p)}"
        for i, p in enumerate(
            [parse_amount(x) or 0.0 for x in prizes.split(",")]
        )
    ))

    if top:
        lines.append("\n<b>الصدارة الحالية:</b>")

        for index, row in enumerate(top):
            lines.append(f"{index + 1}. <code>{row['rid']}</code> — {row['c']}")

    await safe_edit(cb.message, "\n".join(lines), _contest_status_kb())


@dp.callback_query(F.data == "contest_new")
async def admin_contest_new(cb: types.CallbackQuery, state: FSMContext):
    """[ADM4-2] بدء مسابقة جديدة."""

    if cb.from_user.id != ADMIN_USER_ID:
        await cb.answer("للأدمن الرئيسي فقط.", show_alert=True)
        return

    await cb.answer()
    await state.clear()
    await state.set_state(AdminContestFSM.days)
    await cb.message.answer(
        "🏆 كم يوماً تدوم المسابقة؟ (1-90)\nللإلغاء أرسل /cancel"
    , reply_markup=back_kb("admin_contest"))


@dp.message(AdminContestFSM.days)
async def admin_contest_days(message: types.Message, state: FSMContext):
    """[ADM4-2] المدة ثم الجوائز."""

    if message.from_user.id != ADMIN_USER_ID:
        await state.clear()
        return

    raw = (message.text or "").strip()

    if not raw or raw.startswith("/"):
        await state.clear()
        return

    try:
        days = int(raw)
    except ValueError:
        await message.answer("❌ أرسل رقماً من 1 إلى 90.")
        return

    if not (1 <= days <= 90):
        await message.answer("❌ المدة من 1 إلى 90 يوماً.")
        return

    await state.update_data(contest_days=days)
    await state.set_state(AdminContestFSM.prizes)
    await message.answer(
        "🎁 أرسل جوائز المراكز مفصولة بفواصل (1-5 مراكز):\n"
        "مثال: <code>100,50,25</code>\n(للإلغاء /cancel)"
    , reply_markup=back_kb("admin_contest"))


@dp.message(AdminContestFSM.prizes)
async def admin_contest_prizes(message: types.Message, state: FSMContext):
    """[ADM4-2] حفظ المسابقة."""

    if message.from_user.id != ADMIN_USER_ID:
        await state.clear()
        return

    raw = (message.text or "").strip()

    if not raw or raw.startswith("/"):
        await state.clear()
        return

    parts = [x.strip() for x in raw.split(",")]

    if not (1 <= len(parts) <= 5):
        await message.answer("❌ من مركز واحد إلى خمسة.")
        return

    prizes = []

    for part in parts:
        value = parse_amount(part)

        if value is None:
            await message.answer(f"❌ مبلغ غير صالح: {esc(part)}")
            return

        prizes.append(value)

    data = await state.get_data()
    days = data.get("contest_days")

    if not days:
        await message.answer("انتهت الجلسة — أعد البداية.")
        await state.clear()
        return

    now = datetime.now(timezone.utc)
    start = now.isoformat(timespec="seconds")
    end = (now + timedelta(days=int(days))).isoformat(timespec="seconds")

    await set_setting("contest_start", start)
    await set_setting("contest_end", end)
    await set_setting("contest_prizes", ",".join(f"{p:g}" for p in prizes))
    await set_setting("contest_granted", "0")
    await state.clear()
    await audit(  # [NEW 22]
        message.from_user.id, "contest_start",
        "", f"days={days};prizes={prizes}",
    )

    kb = InlineKeyboardBuilder()
    kb.button(text="🏆 شاشة المسابقة", callback_data="admin_contest")
    kb.adjust(1)
    await message.answer(
        f"✅ بدأت مسابقة الإحالات لمدة {days} يوماً!\n"
        "الجوائز: "
        + " | ".join(f"م{i + 1}: {money(p)}" for i, p in enumerate(prizes)),
        reply_markup=kb.as_markup(),
    )


@dp.callback_query(F.data == "contest_endnow")
async def admin_contest_endnow(cb: types.CallbackQuery, state: FSMContext):
    """[ADM4-2] إنهاء مبكر + منح فوري."""

    if cb.from_user.id != ADMIN_USER_ID:
        await cb.answer("للأدمن الرئيسي فقط.", show_alert=True)
        return

    await cb.answer("جاري المنح...")

    end = (await get_setting("contest_end") or "").strip()

    if end:  # قرص النهاية للآن حتى لا يعيد المجدول المنح
        await set_setting(
            "contest_end",
            datetime.now(timezone.utc).isoformat(timespec="seconds"),
        )

    summary = await contest_grant()
    await cb.message.answer(summary, reply_markup=_contest_status_kb())


async def auto_process_withdraw(request_id: int):
    """[ADM4-3] اعتماد ودفعة تلقائية لطلبات سحب قائمة الثقة."""
    try:
        if (await get_setting("auto_wd_enabled") or "0") != "1":
            return

        cap = await get_float_setting("auto_wd_cap", 0.0)

        if cap <= 0:
            return

        db = await get_db()

        try:
            cur = await db.execute(
                "SELECT * FROM finance_requests WHERE id = ?",
                (request_id,),
            )
            request = await cur.fetchone()
        finally:
            await db.close()

        if (not request or request["type"] != "withdraw"
                or request["status"] != "pending"
                or float(request["amount"]) > cap):
            return

        cur2 = await get_db()

        try:
            cur = await cur2.execute(
                "SELECT 1 FROM auto_wd_whitelist WHERE telegram_id = ?",
                (request["telegram_id"],),
            )
            trusted = await cur.fetchone()
        finally:
            await cur2.close()

        if not trusted:
            return

        _, status, payout_id = await process_finance_request(
            request_id, ADMIN_USER_ID, True,
        )

        if status == "approved" and payout_id:
            paid = await mark_payout_paid(
                payout_id, external_id="auto", admin_id=ADMIN_USER_ID,
            )

            if paid:
                amount = float(request["amount"])

                try:
                    await bot.send_message(
                        request["telegram_id"],
                        "⚡ <b>تم اعتماد سحبك ودفعه تلقائياً</b>\n\n"
                        f"💵 المبلغ: <b>{money(amount)}</b>\n"
                        "شكراً لثقتك! 🙏",
                    )
                except Exception as exc:
                    logger.warning(
                        "إبلاغ المستخدم بالاعتماد التلقائي فشل: %s", exc,
                    )

                text = (
                    "⚡ <b>سحب مؤتمت</b>\n\n"
                    f"👤 <code>{request['telegram_id']}</code>\n"
                    f"💵 {money(amount)} — عُتمد ودُفع تلقائياً"
                    f" (طلب #{request_id})"
                )
                await bot.send_message(ADMIN_USER_ID, text)
                await mirror(text)
                await audit(  # [NEW 22]
                    ADMIN_USER_ID, "auto_withdraw", request["telegram_id"],
                    f"request={request_id};amount={round2(amount):g}",
                )

            return

        if status == "budget_exceeded":  # يترك لمعالجة الفريق
            await audit(  # [NEW 22]
                ADMIN_USER_ID, "auto_withdraw_blocked", request_id,
                "budget_exceeded",
            )
    except Exception:
        logger.exception("الاعتماد التلقائي للسحب فشل")


@dp.callback_query(F.data == "admin_autowd")
async def admin_autowd(cb: types.CallbackQuery, state: FSMContext):
    """[ADM4-3] شاشة الاعتماد التلقائي."""

    if cb.from_user.id != ADMIN_USER_ID:
        await cb.answer("للأدمن الرئيسي فقط.", show_alert=True)
        return

    await cb.answer()
    await state.clear()

    enabled = (await get_setting("auto_wd_enabled") or "0") == "1"
    cap = await get_float_setting("auto_wd_cap", 0.0)

    db = await get_db()

    try:
        cur = await db.execute(
            "SELECT telegram_id FROM auto_wd_whitelist"
            " ORDER BY created_at LIMIT 30",
        )
        trusted = await cur.fetchall()
    finally:
        await db.close()

    lines = [
        "⚡ <b>الاعتماد التلقائي للسحوبات</b>\n\n"
        "طلبات سحب أعضاء قائمة الثقة تحت السقف"
        " تُعتمد وتُدفع تلقائياً دون انتظار.\n"
        "(حارس ميزانية السحوبات يبقى ساري الأثر)\n\n"
        f"الحالة: {'✅ مفعّل' if enabled and cap > 0 else '⭕ معطّل'}\n"
        f"السقف: {money(cap) if cap > 0 else '—'}\n"
        f"👥 قائمة الثقة: {len(trusted)}",
    ]
    b = InlineKeyboardBuilder()

    for row in trusted:
        b.button(
            text=f"🗑 {row['telegram_id']}",
            callback_data=f"autowd_del:{row['telegram_id']}",
        )

    b.button(
        text="⏯ تفعيل/تعطيل",
        callback_data="autowd_toggle",
    )
    b.button(text="✏️ السقف", callback_data="autowd_cap")
    b.button(text="➕ إضافة للقائمة", callback_data="autowd_add")
    b.button(text="🔙 رجوع", callback_data="admin_settings_menu")

    # [FIX 5.18.6] صفر خفي: عدد القائمة مضاعف 3 كان يولّد صفاً بحجم 0
    sizes = [3] * (len(trusted) // 3)

    if len(trusted) % 3:
        sizes.append(len(trusted) % 3)

    sizes += [1, 1, 1, 1]
    b.adjust(*sizes)
    await safe_edit(cb.message, "\n".join(lines), b.as_markup())


@dp.callback_query(F.data == "autowd_toggle")
async def admin_autowd_toggle(cb: types.CallbackQuery, state: FSMContext):
    """[ADM4-3] تبديل التفعيل."""

    if cb.from_user.id != ADMIN_USER_ID:
        await cb.answer("للأدمن الرئيسي فقط.", show_alert=True)
        return

    current = (await get_setting("auto_wd_enabled") or "0") == "1"
    await set_setting("auto_wd_enabled", "0" if current else "1")
    await cb.answer(
        "فُعّل الاعتماد التلقائي." if not current else "عُطّل.",
        show_alert=True,
    )
    await audit(  # [NEW 22]
        cb.from_user.id, "auto_wd_toggle", "", f"enabled={not current}",
    )

    text = "⚡ الاعتماد التلقائي للسحوبات"
    await safe_edit(
        cb.message, text + "\n\nحُدّثت الحالة.",
        InlineKeyboardBuilder()
        .button(text="🔄 تحديث الشاشة", callback_data="admin_autowd")
        .adjust(1)
        .as_markup(),
    )


@dp.callback_query(F.data == "autowd_cap")
async def admin_autowd_cap(cb: types.CallbackQuery, state: FSMContext):
    """[ADM4-3] تعديل السقف."""

    if cb.from_user.id != ADMIN_USER_ID:
        await cb.answer("للأدمن الرئيسي فقط.", show_alert=True)
        return

    await cb.answer()
    await state.clear()
    await state.set_state(AdminAutowdFSM.cap)
    await cb.message.answer(
        "⚡ أرسل سقف المبلغ للاعتماد التلقائي:\nللإلغاء أرسل /cancel"
    , reply_markup=back_kb("admin_autowd"))


@dp.message(AdminAutowdFSM.cap)
async def admin_autowd_cap_save(message: types.Message, state: FSMContext):
    """[ADM4-3] حفظ السقف."""

    if message.from_user.id != ADMIN_USER_ID:
        await state.clear()
        return

    amount = parse_amount(message.text)  # [FIX 7]

    if amount is None:
        await message.answer("❌ مبلغ غير صالح.")
        return

    await set_setting("auto_wd_cap", str(amount))
    await state.clear()
    await audit(  # [NEW 22]
        message.from_user.id, "auto_wd_cap", "", f"cap={amount:g}",
    )

    kb = InlineKeyboardBuilder()
    kb.button(text="⚡ شاشة الاعتماد", callback_data="admin_autowd")
    kb.adjust(1)
    await message.answer(
        f"✅ السقف: {money(amount)}",
        reply_markup=kb.as_markup(),
    )


@dp.callback_query(F.data == "autowd_add")
async def admin_autowd_add(cb: types.CallbackQuery, state: FSMContext):
    """[ADM4-3] إضافة لقائمة الثقة."""

    if cb.from_user.id != ADMIN_USER_ID:
        await cb.answer("للأدمن الرئيسي فقط.", show_alert=True)
        return

    await cb.answer()
    await state.clear()
    await state.set_state(AdminAutowdFSM.tid)
    await cb.message.answer(
        "➕ أرسل Telegram ID لإضافته لقائمة الثقة:\nللإلغاء أرسل /cancel"
    , reply_markup=back_kb("admin_autowd"))


@dp.message(AdminAutowdFSM.tid)
async def admin_autowd_add_save(message: types.Message, state: FSMContext):
    """[ADM4-3] حفظ عضو الثقة."""

    if message.from_user.id != ADMIN_USER_ID:
        await state.clear()
        return

    raw = (message.text or "").strip()

    if not raw or raw.startswith("/"):
        await state.clear()
        return

    if not raw.isdigit():
        await message.answer("❌ أرسل Telegram ID رقمياً.")
        return

    tid = int(raw)

    db = await get_db()

    try:
        await db.execute(
            "INSERT OR IGNORE INTO auto_wd_whitelist"
            " (telegram_id, created_by, created_at) VALUES (?, ?, ?)",
            (tid, message.from_user.id, now_iso()),
        )
        await db.commit()
    finally:
        await db.close()

    await state.clear()
    await audit(  # [NEW 22]
        message.from_user.id, "auto_wd_trust", tid,
    )

    kb = InlineKeyboardBuilder()
    kb.button(text="⚡ شاشة الاعتماد", callback_data="admin_autowd")
    kb.adjust(1)
    await message.answer(f"✅ أُضيف <code>{tid}</code> لقائمة الثقة.",
                         reply_markup=kb.as_markup())


@dp.callback_query(F.data.startswith("autowd_del:"))
async def admin_autowd_del(cb: types.CallbackQuery, state: FSMContext):
    """[ADM4-3] إزالة من قائمة الثقة."""

    if cb.from_user.id != ADMIN_USER_ID:
        await cb.answer("للأدمن الرئيسي فقط.", show_alert=True)
        return

    try:
        tid = int(cb.data.split(":", 1)[1])
    except (ValueError, IndexError):
        await cb.answer("معرف غير صالح.", show_alert=True)
        return

    db = await get_db()

    try:
        await db.execute(
            "DELETE FROM auto_wd_whitelist WHERE telegram_id = ?", (tid,),
        )
        await db.commit()
    finally:
        await db.close()

    await cb.answer("أُزيل من القائمة.")
    await audit(  # [NEW 22]
        cb.from_user.id, "auto_wd_untrust", tid,
    )

    # إعادة رسم الشاشة عبر المعالج الأصلي
    await admin_autowd(cb, state)


# ============================================================
# [USR4-2/4/5/6] ROUND 5 — PHASE 3 (USERS)
# ============================================================

class WdAcctFSM(StatesGroup):  # [USR4-2] حفظ وجهة سحب
    label = State()
    acct = State()


class CalcDepFSM(StatesGroup):  # [USR4-5] حاسبة الشحن
    amount = State()
    reverse = State()  # [R6-PLUS2] أريد صافي


def mask_acct(destination: str) -> str:
    """[USR4-2] إخفاء وجهة الدفع وعرض آخر 4 أحرف فقط."""
    text = str(destination or "").strip()

    if len(text) <= 4:
        return "•••"

    return f"•••{text[-4:]}"


async def get_payout_accounts(telegram_id: int):
    """[USR4-2] وجهات السحب المحفوظة لمستخدم."""
    db = await get_db()

    try:
        cur = await db.execute(
            "SELECT id, label, destination, created_at FROM payout_accounts"
            " WHERE telegram_id = ? ORDER BY id",
            (telegram_id,),
        )
        return await cur.fetchall()
    finally:
        await db.close()


async def get_payout_account(acct_id: int, telegram_id: int):
    """[USR4-2] وجهة واحدة بفحص الملكية."""
    db = await get_db()

    try:
        cur = await db.execute(
            "SELECT id, label, destination FROM payout_accounts"
            " WHERE id = ? AND telegram_id = ?",
            (acct_id, telegram_id),
        )
        return await cur.fetchone()
    finally:
        await db.close()


@dp.callback_query(F.data.startswith("wdacct:"))
async def wdacct_pick(cb: types.CallbackQuery, state: FSMContext):
    """[USR4-2] تحديد وجهة السحب للطلب القادم."""

    if not await user_allowed(cb.from_user.id):
        await cb.answer("غير مسموح.", show_alert=True)
        return

    try:
        acct_id = int(cb.data.split(":", 1)[1])
    except (ValueError, IndexError):
        await cb.answer("معرف غير صالح.", show_alert=True)
        return

    acct = await get_payout_account(acct_id, cb.from_user.id)

    if not acct:
        await cb.answer("الوجهة غير موجودة.", show_alert=True)
        return

    await state.update_data(wd_acct=acct_id)
    await cb.answer(
        f"✅ حُددت «{acct['label']}» لهذا السحب.", show_alert=True,
    )


@dp.callback_query(F.data == "wdacct_add")
async def wdacct_add(cb: types.CallbackQuery, state: FSMContext):
    """[USR4-2] بدء حفظ وجهة جديدة."""

    if not await user_allowed(cb.from_user.id):
        await cb.answer("غير مسموح.", show_alert=True)
        return

    accounts = await get_payout_accounts(cb.from_user.id)

    if len(accounts) >= 3:
        await cb.answer("الحد الأقصى 3 وجهات — احذف واحدة أولاً.",
                        show_alert=True)
        return

    await cb.answer()
    await state.set_state(WdAcctFSM.label)
    await cb.message.answer(
        "📒 أرسل اسم الوجهة (مثال: بنك الراجحي أو USDT):"
        "\nحتى 20 حرفاً — للإلغاء أرسل /cancel"
    )


@dp.message(WdAcctFSM.label)
async def wdacct_label_save(message: types.Message, state: FSMContext):
    """[USR4-2] الاسم ثم رقم الحساب."""

    if not await user_allowed(message.from_user.id, message):
        await state.clear()
        return

    label = (message.text or "").strip()[:20]

    if not label or label.startswith("/"):
        await state.clear()
        return

    await state.update_data(wd_label=label)
    await state.set_state(WdAcctFSM.acct)
    await message.answer(
        "🔢 الآن أرسل رقم الحساب/العنوان:\nحتى 60 حرفاً — للإلغاء /cancel"
    )


@dp.message(WdAcctFSM.acct)
async def wdacct_acct_save(message: types.Message, state: FSMContext):
    """[USR4-2] حفظ الوجهة."""

    if not await user_allowed(message.from_user.id, message):
        await state.clear()
        return

    destination = (message.text or "").strip()[:60]

    if not destination or destination.startswith("/"):
        await state.clear()
        return

    data = await state.get_data()
    label = data.get("wd_label") or "وجهة"

    db = await get_db()

    try:
        cur = await db.execute(
            "SELECT COUNT(*) AS c FROM payout_accounts"
            " WHERE telegram_id = ?",
            (message.from_user.id,),
        )

        if (await cur.fetchone())["c"] >= 3:
            await db.rollback()
            await message.answer("⚠️ الحد الأقصى 3 وجهات.")
            await state.clear()
            return

        await db.execute(
            "INSERT OR IGNORE INTO payout_accounts"
            " (telegram_id, label, destination, created_at)"
            " VALUES (?, ?, ?, ?)",
            (message.from_user.id, label, destination, now_iso()),
        )
        await db.commit()
    finally:
        await db.close()

    await state.clear()
    await message.answer(
        f"✅ حُفظت الوجهة «{esc(label)}».\n"
        "ستجدها بشاشة السحب لاختيارها بسرعة.",
        reply_markup=back_kb("menu_back"),
    )


@dp.callback_query(F.data == "wdacct_del")
async def wdacct_del(cb: types.CallbackQuery, state: FSMContext):
    """[USR4-2] شاشة حذف الوجهات."""

    if not await user_allowed(cb.from_user.id):
        await cb.answer("غير مسموح.", show_alert=True)
        return

    accounts = await get_payout_accounts(cb.from_user.id)

    if not accounts:
        await cb.answer("لا وجهات محفوظة.", show_alert=True)
        return

    await cb.answer()
    b = InlineKeyboardBuilder()

    for acct in accounts:
        b.button(
            text=f"🗑 {acct['label']} {mask_acct(acct['destination'])}",
            callback_data=f"wdaccdel:{acct['id']}",
        )

    b.button(text="🔙 رجوع", callback_data="svc_withdraw")
    b.adjust(1)
    await cb.message.answer("🗑 اختر الوجهة للحذف:", reply_markup=b.as_markup())


@dp.callback_query(F.data.startswith("wdaccdel:"))
async def wdacct_del_go(cb: types.CallbackQuery, state: FSMContext):
    """[USR4-2] تنفيذ الحذف."""

    if not await user_allowed(cb.from_user.id):
        await cb.answer("غير مسموح.", show_alert=True)
        return

    try:
        acct_id = int(cb.data.split(":", 1)[1])
    except (ValueError, IndexError):
        await cb.answer("معرف غير صالح.", show_alert=True)
        return

    db = await get_db()

    try:
        await db.execute(
            "DELETE FROM payout_accounts WHERE id = ? AND telegram_id = ?",
            (acct_id, cb.from_user.id),
        )
        await db.commit()
    finally:
        await db.close()

    await cb.answer("حُذفت الوجهة.")


@dp.callback_query(F.data.startswith("ucard_accts:"))
async def admin_ucard_accts(cb: types.CallbackQuery, state: FSMContext):
    """[USR4-2] وجهات سحب المستخدم — للفريق المالي."""

    if not await is_admin_or_supervisor(cb.from_user.id, "finance"):
        await cb.answer("غير مصرّح.", show_alert=True)
        return

    try:
        tid = int(cb.data.split(":", 1)[1])
    except (ValueError, IndexError):
        await cb.answer("معرف غير صالح.", show_alert=True)
        return

    await cb.answer()
    await state.clear()

    accounts = await get_payout_accounts(tid)

    if accounts:
        lines = [f"📒 <b>وجهات سحب</b> <code>{tid}</code>\n"]

        for acct in accounts:
            lines.append(
                f"• {esc(acct['label'])}: "
                f"<code>{esc(acct['destination'])}</code>"
                f" ({esc(acct['created_at'])[:10]})"
            )
    else:
        lines = [f"📒 لا وجهات محفوظة لـ <code>{tid}</code>."]

    await safe_edit(
        cb.message, "\n".join(lines),
        back_kb(f"admin_user_card:{tid}"),
    )


async def _balance_series(user_id: int, current_balance: float):
    """[USR4-4] سلسلة (وقت، رصيد) معاد بناؤها لآخر 30 يوماً."""
    cutoff = (
        datetime.now(timezone.utc) - timedelta(days=30)
    ).isoformat(timespec="seconds")

    db = await get_db()

    try:
        cur = await db.execute(
            "SELECT amount, type, created_at FROM transactions"
            " WHERE user_id = ? AND created_at >= ?"
            " ORDER BY created_at DESC, id DESC",
            (user_id, cutoff),
        )
        rows = await cur.fetchall()
    finally:
        await db.close()

    credit = {"deposit", "gift", "referral", "register",
              "refund", "bonus", "transfer_in"}
    debit = {"withdraw", "transfer_out", "gift_out"}

    points = [(datetime.now(timezone.utc), round2(current_balance))]
    balance = round2(current_balance)

    for row in rows:
        try:
            amount = float(row["amount"])
        except (TypeError, ValueError):
            continue

        try:
            when = datetime.fromisoformat(row["created_at"])

            if when.tzinfo is None:
                when = when.replace(tzinfo=timezone.utc)
        except ValueError:
            continue

        tx_type = row["type"]

        if tx_type in credit or tx_type == "admin_adjust":
            balance = round2(balance - amount)
        elif tx_type in debit:
            balance = round2(balance + amount)

        points.append((when, balance))

    points.reverse()
    return points


@dp.callback_query(F.data == "my_chart")
async def my_chart(cb: types.CallbackQuery, state: FSMContext):
    """[USR4-4] منحنى الرصيد — آخر 30 يوماً (PNG)."""

    if not await user_allowed(cb.from_user.id):
        await cb.answer("غير مسموح.", show_alert=True)
        return

    await cb.answer("جاري بناء المنحنى...")
    await state.clear()

    user = await get_user(cb.from_user.id)

    if not user:
        await cb.answer("حسابك غير موجود.", show_alert=True)
        return

    points = await _balance_series(
        user["id"], float(user["balance"] or 0),
    )

    if len(points) < 2:
        await cb.message.answer(
            "📈 لا عمليات كافية لرسم المنحنى في آخر 30 يوماً."
        )
        return

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        await cb.message.answer(
            "⚠️ مكتبة الرسم غير متوفرة حالياً — حاول لاحقاً."
        )
        return

    xs = [p[0] for p in points]
    ys = [p[1] for p in points]

    import io

    buf = io.BytesIO()

    fig, ax = plt.subplots(figsize=(8, 3.5))
    ax.plot(xs, ys, marker="o", markersize=3, linewidth=1.6, color="#0a7")
    ax.fill_between(xs, ys, alpha=0.15, color="#0a7")
    ax.set_title("My Balance - last 30 days")
    ax.set_ylabel("Balance")
    ax.grid(True, alpha=0.3)
    fig.autofmt_xdate()
    fig.tight_layout()
    fig.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)

    from aiogram.types import BufferedInputFile as _BIF

    await cb.message.answer_document(
        _BIF(buf.getvalue(), filename=f"balance_{cb.from_user.id}.png"),
        caption=(
            f"📈 رصيدك الحالي: <b>{money(user['balance'])}</b>\n"
            f"آخر 30 يوماً — {len(points) - 1} عملية"
        ),
    )


@dp.callback_query(F.data == "calc_dep")
async def calc_dep(cb: types.CallbackQuery, state: FSMContext):
    """[USR4-5] حاسبة الشحن."""

    if not await user_allowed(cb.from_user.id):
        await cb.answer("غير مسموح.", show_alert=True)
        return

    await cb.answer()
    await state.clear()
    await state.set_state(CalcDepFSM.amount)
    await cb.message.answer(
        "🧮 <b>حاسبة الشحن</b>\n\n"
        "أرسل المبلغ الذي تفكر بشحنه —"
        " أحسب لك الصافي النهائي بعمولتك ومكافأة عرضك الحالية:"
        "\n\nللإلغاء أرسل /cancel",
        reply_markup=await _calc_kb(),
    )


async def _calc_kb(lang: str = "ar"):
    """[R6-PLUS2] أزرار الحاسبة: عكسية (حسب التفعيل) + رجوع."""
    b = InlineKeyboardBuilder()

    if await feat_on("rev_calc"):  # [R6-PLUS3]
        b.button(text=r6t(lang, "calc_rev_btn"), callback_data="calc_rev")

    b.button(text=r6t(lang, "back_main"), callback_data="back_to_recharge")
    b.adjust(1)
    return b.as_markup()


@dp.message(CalcDepFSM.amount)
async def calc_dep_calc(message: types.Message, state: FSMContext):
    """[USR4-5] حساب الصافي بنفس معادلة الاعتماد الحقيقية."""

    if not await user_allowed(message.from_user.id, message):
        await state.clear()
        return

    amount = parse_amount(message.text)  # [FIX 7]

    if amount is None:
        await message.answer("❌ مبلغ غير صالح.\n\nللإلغاء أرسل /cancel")
        return

    await state.clear()

    pct = await get_float_setting("commission_percent", 0.0)
    loyal = await get_loyalty(message.from_user.id)  # [USR4-1]
    pct = max(0.0, pct - loyal["discount"])
    commission = round2(amount * pct / 100.0)
    net = round2(amount - commission)

    bonus = 0.0
    bonus_pct = await get_float_setting("bonus_percent", 0.0)  # [USR2-3]

    if bonus_pct > 0:
        bonus = round2(net * bonus_pct / 100.0)
        bonus_max = await get_float_setting("bonus_max", 0.0)

        if bonus_max > 0:
            bonus = min(bonus, round2(bonus_max))

    total = round2(net + bonus)

    lines = [
        "🧮 <b>تقدير صافي شحنتك</b>\n",
        f"💰 المبلغ: <b>{money(amount)}</b>",
    ]

    if pct > 0:
        lines.append(f"➖ العمولة ({money(pct)}%): {money(commission)}")
    else:
        lines.append("✅ بلا عمولة")

    lines.append(f"💵 الصافي: <b>{money(net)}</b>")

    if bonus > 0:
        lines.append(f"🎁 مكافأة الإيداع ({bonus_pct:g}%): +{money(bonus)}")

    if total != net:
        lines.append(f"🏁 الإجمالي في محفظتك: <b>{money(total)}</b>")

    if loyal["discount"] > 0:
        lines.append(
            f"\n💎 شمل خصم مستوى {loyal['name']}: -{money(loyal['discount'])}%"
        )

    lines.append("\n⚠️ تقدير استرشادي — النهائي بعد اعتماد الشحن.")

    kb = InlineKeyboardBuilder()
    kb.button(text="💰 شحن هذا المبلغ", callback_data="svc_deposit")
    kb.button(text="🔙 رجوع", callback_data="menu_back")
    kb.adjust(1)
    await message.answer("\n".join(lines), reply_markup=kb.as_markup())


@dp.callback_query(F.data == "my_export")
async def my_export(cb: types.CallbackQuery, state: FSMContext):
    """[USR4-6] تصدير بيانات المستخدم — مرة كل 24 ساعة."""

    if not await user_allowed(cb.from_user.id):
        await cb.answer("غير مسموح.", show_alert=True)
        return

    await state.clear()

    day_ago = (
        datetime.now(timezone.utc) - timedelta(hours=24)
    ).isoformat(timespec="seconds")

    db = await get_db()

    try:
        cur = await db.execute(
            "SELECT created_at FROM my_exports WHERE telegram_id = ?",
            (cb.from_user.id,),
        )
        last = await cur.fetchone()
    finally:
        await db.close()

    if last and last["created_at"] > day_ago:
        await cb.answer(
            "صدّرت بياناتك خلال 24 ساعة الماضية — حاول غداً.",
            show_alert=True,
        )
        return

    await cb.answer("جاري تجهيز الملف...")

    user = await get_user(cb.from_user.id)

    if not user:
        await cb.answer("حسابك غير موجود.", show_alert=True)
        return

    db = await get_db()

    try:
        cur = await db.execute(
            "SELECT id, created_at, type, amount, note FROM transactions"
            " WHERE user_id = ? ORDER BY id",
            (user["id"],),
        )
        rows = await cur.fetchall()
    finally:
        await db.close()

    csv_file = build_csv_file(
        f"my_data_{cb.from_user.id}",
        ["id", "date", "type", "amount", "note"],
        [(r["id"], r["created_at"], r["type"], r["amount"], r["note"])
         for r in rows],
    )

    dep_sum = round2(sum(
        float(r["amount"]) for r in rows if r["type"] == "deposit"
    ))
    wd_sum = round2(sum(
        float(r["amount"]) for r in rows if r["type"] == "withdraw"
    ))
    loyal = await get_loyalty(cb.from_user.id)

    caption = (
        "📦 <b>بياناتك</b>\n\n"
        f"👤 <code>{cb.from_user.id}</code> — عضو منذ "
        f"{esc(user['created_at'])[:10]}\n"
        f"💰 رصيدك: <b>{money(user['balance'])}</b>\n"
        f"💰 إجمالي شحانتك: {money(dep_sum)}\n"
        f"🏦 إجمالي سحباتك: {money(wd_sum)}\n"
        f"📄 عدد العمليات: {len(rows)}\n"
    )

    if loyal["line"]:
        caption += f"\n{loyal['line']}"

    await cb.message.answer_document(csv_file, caption=caption)

    db = await get_db()

    try:
        await db.execute(
            "INSERT OR REPLACE INTO my_exports"
            " (telegram_id, created_at) VALUES (?, ?)",
            (cb.from_user.id, now_iso()),
        )
        await db.commit()
    finally:
        await db.close()


# ============================================================
# ============================================================
# [R6] واجهة 55bets الأصلية — الشاشات والمسارات
# ============================================================



# ============================================================
# [R6] 55BETS INTERFACE — واجهة 55bets الكاملة (الجولة 6)
# يحافظ على الأزرار والمسميات والنصوص والترتيب الأصلي حرفياً،
# مع تشغيل كل ميزات المحرك خلفها.
# ============================================================

class AdminWalletFSM(StatesGroup):  # [R6] رقم محفظة الإيداع
    value = State()


class ShareHappyFSM(StatesGroup):  # [R6] شاركنا سعادتك
    media = State()


BETS55_LOGIN_BASE = (  # رابط دخول اللاعبين — قابل للتجاوز بالبيئة
    os.getenv("BETS55_LOGIN_BASE") or "https://55bets.net"
)

# [R6] نصوص الواجهة بالعربية والإنكليزية (تبديل اللغة)
R6T = {
    "login": {"ar": "🎮 الدخول ل55bets", "en": "🎮 Login to 55bets",
              "ru": "🎮 Вход в 55bets"},
    "55bets": {"ar": "🎰 55bets حساب", "en": "🎰 55bets Account", "ru": "🎰 Аккаунт 55bets"},
    "recharge": {"ar": "💳 شحن رصيد البوت", "en": "💳 Top up bot balance", "ru": "💳 Пополнить баланс"},
    "withdraw": {"ar": "💰 سحب رصيد من البوت", "en": "💰 Withdraw from bot", "ru": "💰 Вывод из бота"},
    "rewards": {"ar": "🏆 جوائز", "en": "🏆 Rewards", "ru": "🏆 Награды"},
    "refs": {"ar": "👥 احالات", "en": "👥 Referrals", "ru": "👥 Рефералы"},
    "myinfo": {"ar": "🏪 معلومات ملفي", "en": "🏪 My profile", "ru": "🏪 Мой профиль"},
    "history": {"ar": "🧾 السجل", "en": "🧾 History", "ru": "🧾 История"},
    "gift": {"ar": "🎁 كود هدية", "en": "🎁 Gift code", "ru": "🎁 Подарочный код"},
    "contact": {"ar": "✉️ تواصل معنا", "en": "✉️ Contact us", "ru": "✉️ Связаться"},
    "share": {"ar": "🔥 شاركنا سعادتك", "en": "🔥 Share your joy", "ru": "🔥 Поделись радостью"},
    "tutorials": {"ar": "🎓 الشروحات", "en": "🎓 Tutorials", "ru": "🎓 Обучение"},
    "offers": {"ar": "🍀 عروضنا الحالية 🍀", "en": "🍀 Current offers 🍀", "ru": "🍀 Актуальные предложения"},
    "terms": {"ar": "📜 الشروط والأحكام", "en": "📜 Terms & Conditions", "ru": "📜 Условия"},
    "lang_btn": {"ar": "🌐 English", "en": "🌐 العربية"},
    "pending_reassure": {
        "ar": ("🕓 <b>طلبك #{rid} قيد المراجعة</b>\n\n"
               "فريقنا المالي يتابع طلبك الآن — شكراً لصبرك،"
               " وستصلك لحظة إنجازه. 💙"),
        "en": ("🕓 <b>Request #{rid} is under review</b>\n\n"
               "Our finance team is on it — thanks for your"
               " patience, you'll be notified once done. 💙"),
    },
    "wd_count_limit": {
        "ar": "🛑 بلغت الحد الأقصى لعدد طلبات السحب اليوم"
              " ({n} طلباً). حاول غداً.",
        "en": "🛑 You reached today's withdrawal request limit"
              " ({n}). Try again tomorrow.",
    },
    "quick_btn": {"ar": "⚙️ مبالغك السريعة",
                  "en": "⚙️ Your quick amounts"},
    "quick_prompt": {
        "ar": ("⚡ <b>مبالغك السريعة</b>\n\n"
               "أرسل حتى 4 مبالغ مفصولة بمسافة أو فاصلة"
               " (مثال: 20 50 100 250)\n"
               "وستظهر بأزرار شاشة الشحن.\n"
               "أو أرسل «مسح» للرجوع للمبالغ الافتراضية:"
               "\n\nللإلغاء أرسل /cancel"),
        "en": ("⚡ <b>Your quick amounts</b>\n\n"
               "Send up to 4 amounts separated by spaces"
               " (e.g. 20 50 100 250)\n"
               "They'll appear as deposit buttons.\n"
               "Send «clear» to restore defaults:"
               "\n\n/cancel to abort"),
    },
    "quick_done": {
        "ar": "✅ حُفظت مبالغك السريعة: {q}",
        "en": "✅ Quick amounts saved: {q}",
    },
    "quick_cleared": {
        "ar": "🗑 أُعيدت المبالغ الافتراضية.",
        "en": "🗑 Default amounts restored.",
    },
    "quick_invalid": {
        "ar": "❌ أرسل من 1 إلى 4 مبالغ صحيحة، أو «مسح».",
        "en": "❌ Send 1-4 valid amounts, or «clear».",
    },
    "help_dep": {
        "ar": "🆘 تحتاج مساعدة في الشحن؟ اكتب مشكلتك وسيتواصل"
             " معك الفريق فوراً:",
        "en": "🆘 Need help with a deposit? Describe the issue"
             " and the team will reach out:",
    },
    "help_wd": {
        "ar": "🆘 تحتاج مساعدة في السحب؟ اكتب مشكلتك وسيتواصل"
             " معك الفريق فوراً:",
        "en": "🆘 Need help with a withdrawal? Describe the"
             " issue and the team will reach out:",
    },
    "help_btn": {"ar": "🆘 مساعدة", "en": "🆘 Help"},
    "support_closed": {
        "ar": ("🕐 <b>فريق الدعم متاح من {h}</b>\n"
               "تم تسجيل تذكرتك وسيصلك الرد عند توفرهم. شكراً"
               " لصبرك!"),
        "en": ("🕐 <b>Support is available {h}</b>\n"
               "Your ticket is logged — we'll reply once"
               " available. Thanks for your patience!"),
    },
    "anniv_month": {
        "ar": "🎂 <b>شهر معنا!</b>\n\n"
              "مرّ شهر على انضمامك — هدية منا: "
              "<b>{p} نقطة ⭐</b> أُضيفت لرصيد نقاطك. شكراً"
              " لثقتك! 💙",
        "en": "🎂 <b>One month with us!</b>\n\n"
              "A gift from us: <b>{p} points ⭐</b> added to"
              " your balance. Thank you! 💙",
    },
    "anniv_year": {
        "ar": "🎉 <b>ذكرى سنوية!</b>\n\n"
              "مرّت سنة على انضمامك — هدية منا: "
              "<b>{p} نقطة ⭐</b>. نحب وجودك معنا! 💙",
        "en": "🎉 <b>Anniversary!</b>\n\n"
              "One year with us — a gift: <b>{p} points"
              " ⭐</b>. We love having you! 💙",
    },
    "points_line": {"ar": "⭐ نقاطك:", "en": "⭐ Your points:",
                    "ru": "⭐ Ваши баллы:"},
    "points_btn": {"ar": "⭐ استبدال النقاط", "en": "⭐ Redeem points",
                   "ru": "⭐ Обмен баллов"},
    "points_title": {"ar": "⭐ <b>نقاط الولاء</b>\n\nرصيدك: <b>{p}</b>"
                          " نقطة\n\nكل 1$ شحن = نقطة. استبدلها برصيد:",
                     "en": "⭐ <b>Loyalty points</b>\n\nBalance:"
                           " <b>{p}</b> points\n\nEvery $1 deposited ="
                           " 1 point. Redeem for balance:",
                     "ru": "⭐ <b>Баллы лояльности</b>\n\nБаланс:"
                           " <b>{p}</b>\n\nКаждые $1 пополнения = 1"
                           " балл. Обменяйте на баланс:"},
    "points_low": {"ar": "❌ نقاطك غير كافية لهذا الاستبدال.",
                   "en": "❌ Not enough points for this redemption.",
                   "ru": "❌ Недостаточно баллов."},
    "points_done": {"ar": "✅ تم الاستبدال! أُضيف {r} إلى رصيدك.",
                    "en": "✅ Redeemed! {r} added to your balance.",
                    "ru": "✅ Обменяно! {r} добавлено на баланс."},
    "hide_bal_btn": {"ar": "🙈 إخفاء رصيدي", "en": "🙈 Hide my balance",
                     "ru": "🙈 Скрыть баланс"},
    "show_bal_btn": {"ar": "👁 إظهار رصيدي", "en": "👁 Show my balance",
                     "ru": "👁 Показать баланс"},
    "bal_hidden": {"ar": "••••", "en": "••••", "ru": "••••"},
    "refs_top_btn": {"ar": "🏆 الصدارة", "en": "🏆 Leaderboard",
                     "ru": "🏆 Лидеры"},
    "refs_count_btn": {
        "ar": "👥 عدد إحالاتي", "en": "👥 My referral count",
        "ru": "👥 Мои рефералы",
    },
    "ref_my_link": {
        "ar": "🔗 رابط الإحالة الخاص بي",
        "en": "🔗 My referral link",
        "ru": "🔗 Моя реферальная ссылка",
    },
    "ref_link_title": {
        "ar": ("🔗 <b>رابط الإحالة الخاص بك</b>\n\n"
               "<code>{link}</code>\n\n"
               "📤 أرسله لأصدقائك — يُحتسب لك تلقائياً بمجرد دخولهم "
               "عبر الرابط، وتحصل على أرباح من عمولاتهم."),
        "en": ("🔗 <b>Your referral link</b>\n\n"
               "<code>{link}</code>\n\n"
               "📤 Send it to friends — it counts automatically "
               "once they join through it."),
        "ru": ("🔗 <b>Ваша реферальная ссылка</b>\n\n"
               "<code>{link}</code>\n\n"
               "📤 Отправьте друзьям — засчитывается автоматически."),
    },
    "refs_top_title": {"ar": "🏆 <b>صدارة الإحالات</b>\n",
                       "en": "🏆 <b>Referral leaderboard</b>\n",
                       "ru": "🏆 <b>Лидеры рефералов</b>\n"},
    "calc_rev_btn": {"ar": "🔄 عكسية: أريد صافي",
                     "en": "🔄 Reverse: I want a net amount",
                     "ru": "🔄 Обратно: хочу чистыми"},
    "calc_rev_prompt": {
        "ar": "🧮 أرسل المبلغ الصافي الذي تريد بيدي\n"
              "وأحسب لك كم يجب أن تشحنه:",
        "en": "🧮 Send the net amount you want to receive\n"
              "and I'll calculate what to deposit:",
        "ru": "🧮 Отправьте сумму, которую хотите получить,\n"
              "и я рассчитаю размер пополнения:",
    },
    "calc_rev_result": {
        "ar": "🧮 اشحن <code>{g}</code>\n\n"
              "🏷 العمولة: {c}\n✅ صافيك: <b>{n}</b>",
        "en": "🧮 Deposit <code>{g}</code>\n\n🏷 Fee: {c}\n"
              "✅ Your net: <b>{n}</b>",
        "ru": "🧮 Пополните на <code>{g}</code>\n\n🏷 Комиссия: {c}\n"
              "✅ Чистыми: <b>{n}</b>",
    },
    "rq_all": {"ar": "📋 الكل", "en": "📋 All", "ru": "📋 Все"},
    "rq_week": {"ar": "🗓 أسبوع", "en": "🗓 Week", "ru": "🗓 Неделя"},
    "rq_month": {"ar": "📆 شهر", "en": "📆 Month", "ru": "📆 Месяц"},
    "admpanel": {"ar": "👑 لوحة تحكم الأدمن", "en": "👑 Admin panel", "ru": "👑 Админ панель"},
    "ich_pick": {"ar": "اختر من قائمة 55bets:",
                 "en": "Choose from the 55bets menu:"},
    "sec_create": {"ar": "🔹 55bets انشاء حساب",
                   "en": "🔹 Create 55bets account"},
    "sec_dep": {"ar": "💵 شحن حساب", "en": "💵 Deposit to account"},
    "sec_wd": {"ar": "💳 سحب رصيد من الحساب",
               "en": "💳 Withdraw from account"},
    "back_main": {"ar": "↩️ رجوع للقائمة الرئيسية",
                  "en": "↩️ Back to main menu"},
    "back_ich": {"ar": "↩️ رجوع لقائمة 55bets",
                 "en": "↩️ Back to 55bets menu"},
    "recharge_pick": {
        "ar": "اختر طريقة الدفع لشحن رصيد البوت:",
        "en": "Choose a payment method to top up your bot balance:",
    },
    "withdraw_pick": {
        "ar": "اختر طريقة السحب المناسبة لك:",
        "en": "Choose a suitable withdrawal method:",
    },
    "m_sham": {"ar": "شام كاش (Sham Cash)", "en": "Sham Cash"},
    "m_sham_code": {
        "ar": "شام كاش — رمز حساب",
        "en": "Sham Cash — Account code",
        "ru": "Sham Cash — код счета",
    },
    "sham_code_title": {
        "ar": ("<b>شحن عبر شام كاش — رمز الحساب</b>\n\n"
               "يرجى التحويل إلى رمز الحساب التالي:\n"
               "<code>{code}</code>\n\n"
               "الرجاء إدخال <b>المبلغ</b> الذي قمت بتحويله:"),
        "en": ("<b>Top up via Sham Cash — Account code</b>\n\n"
               "Please transfer to the following account code:\n"
               "<code>{code}</code>\n\n"
               "Then enter the <b>amount</b> you transferred:"),
        "ru": ("<b>Пополнение через Sham Cash — код счета</b>\n\n"
               "Переведите на следующий код счета:\n"
               "<code>{code}</code>\n\n"
               "Затем введите <b>сумму</b> пополнения:"),
    },
    "bell_on": {"ar": "🔔 اشتراك بالإعلانات", "en": "🔔 Notify me offers",
                "ru": "🔔 Уведомлять об акциях"},
    "bell_off": {"ar": "🔕 إلغاء اشتراك الإعلانات",
                 "en": "🔕 Unsubscribe offers",
                 "ru": "🔕 Отписаться от акций"},
    "bell_sub": {"ar": "✅ ستستلم الإعلانات الجديدة تلقائياً.",
                 "en": "✅ You'll receive new offers automatically.",
                 "ru": "✅ Вы будете получать новые акции."},
    "bell_unsub": {"ar": "🔕 تم إلغاء اشتراك الإعلانات.",
                   "en": "🔕 Offers subscription removed.",
                   "ru": "🔕 Подписка отменена."},
    "digest_msg": {
        "ar": ("📭 <b>ملخصك الأسبوعي</b>\n\n"
               "💰 شحناتك: {dep}\n"
               "🏦 سحوباتك: {wd}\n"
               "⭐ نقاط كسبتها: {pts}\n"
               "👥 ترتيبك بالإحالات: {rank}\n\n"
               "شكراً لثقتك — استمر! 🎰"),
        "en": ("📭 <b>Your weekly digest</b>\n\n"
               "💰 Deposits: {dep}\n"
               "🏦 Withdrawals: {wd}\n"
               "⭐ Points earned: {pts}\n"
               "👥 Referral rank: {rank}\n\n"
               "Thanks for your trust — keep going! 🎰"),
        "ru": ("📭 <b>Ваша недельная сводка</b>\n\n"
               "💰 Пополнения: {dep}\n"
               "🏦 Выводы: {wd}\n"
               "⭐ Баллов получено: {pts}\n"
               "👥 Место в рейтинге: {rank}\n\n"
               "Спасибо за доверие! 🎰"),
    },
    "digest_btn_on": {"ar": "📭 ملخصي الأسبوعي: مفعّل",
                      "en": "📭 My weekly digest: on",
                      "ru": "📭 Моя сводка: вкл"},
    "digest_btn_off": {"ar": "📭 ملخصي الأسبوعي: معطل",
                       "en": "📭 My weekly digest: off",
                       "ru": "📭 Моя сводка: выкл"},
    "points_hist_btn": {"ar": "📜 سجل نقاطي", "en": "📜 Points history",
                        "ru": "📜 История баллов"},
    "points_hist_title": {
        "ar": "📜 <b>سجل النقاط</b>\n",
        "en": "📜 <b>Points history</b>\n",
        "ru": "📜 <b>История баллов</b>\n",
    },
    "m_syriatel": {"ar": "سيرياتيل كاش (Syriatel Cash)",
                   "en": "Syriatel Cash"},
    "calc": {"ar": "🧮 حاسبة الشحن", "en": "🧮 Deposit calculator"},
    "sham_title": {
        "ar": ("<b>شحن عبر شام كاش (Sham Cash)</b>\n\n"
               "يرجى التحويل إلى الرقم / المعرف التالي:\n"
               "<code>{wallet}</code>\n\n"
               "الرجاء إدخال <b>المبلغ</b> الذي قمت بتحويله:"),
        "en": ("<b>Top up via Sham Cash</b>\n\n"
               "Please transfer to the following number / ID:\n"
               "<code>{wallet}</code>\n\n"
               "Then enter the <b>amount</b> you transferred:"),
    },
    "syr_title": {
        "ar": ("<b>شحن عبر سيرياتيل كاش (Syriatel Cash)</b>\n\n"
               "يرجى التحويل إلى رقم سيرياتيل كاش التالي:\n"
               "<code>{wallet}</code>\n\n"
               "الرجاء إدخال <b>المبلغ</b> الذي قمت بتحويله:"),
        "en": ("<b>Top up via Syriatel Cash</b>\n\n"
               "Please transfer to the following Syriatel Cash number:\n"
               "<code>{wallet}</code>\n\n"
               "Then enter the <b>amount</b> you transferred:"),
    },
    "syr_code_title": {  # [MENU-ORG] عرض رمز الإيداع بسيرياتل كاش
        "ar": ("<b>شحن عبر سيرياتيل كاش — رمز الإيداع</b>\n\n"
               "يرجى التحويل إلى رمز الإيداع التالي:\n"
               "<code>{code}</code>\n\n"
               "الرجاء إدخال <b>المبلغ</b> الذي قمت بتحويله:"),
        "en": ("<b>Top up via Syriatel Cash — Deposit code</b>\n\n"
               "Please transfer to the following deposit code:\n"
               "<code>{code}</code>\n\n"
               "Then enter the <b>amount</b> you transferred:"),
    },
    "sham_off": {
        "ar": "🔴 الشحن عبر شام كاش معطل حالياً — راجع الإدارة.",
        "en": "🔴 Sham Cash top-ups are currently disabled — contact support.",
    },
    "syr_off": {
        "ar": "🔴 الشحن عبر سيرياتيل كاش معطل حالياً — راجع الإدارة.",
        "en": "🔴 Syriatel Cash top-ups are currently disabled — contact support.",
    },
    "wd_sham_title": {
        "ar": ("<b>سحب عبر شام كاش (Sham Cash)</b>\n\n"
               "يرجى إدخال <b>رقم حساب شام كاش أو المعرف</b>"
               " الخاص بك لاستلام المبلغ:"),
        "en": ("<b>Withdraw via Sham Cash</b>\n\n"
               "Please enter <b>your Sham Cash account number or ID</b>"
               " to receive the funds:"),
    },
    "wd_syr_title": {
        "ar": ("<b>سحب عبر سيرياتيل كاش (Syriatel Cash)</b>\n\n"
               "يرجى إدخال <b>رقم سيرياتيل كاش</b> الخاص بك لاستلام المبلغ:"),
        "en": ("<b>Withdraw via Syriatel Cash</b>\n\n"
               "Please enter <b>your Syriatel Cash number</b>"
               " to receive the funds:"),
    },
    "wd_acct_short": {
        "ar": "❌ الحساب قصير جداً — أرسل رقماً/معرفاً صحيحاً:",
        "en": "❌ Account is too short — send a valid number/ID:",
    },
    "wd_dest_bad": {  # [R6-PLUS7 U31]
        "ar": ("❌ الرقم غير صالح — أرسل <b>أرقاماً فقط</b> "
               "(مثال: 0951234567):"),
        "en": ("❌ Invalid number — send <b>digits only</b> "
               "(e.g. 0951234567):"),
    },
    "wd_dest_doubt": {  # [R6-PLUS7 U31]
        "ar": ("⚠️ الرقم <code>{d}</code> لا يبدو رقماً سورياً معتاداً.\n"
               "تأكد أنه صحيح قبل المتابعة:"),
        "en": ("⚠️ <code>{d}</code> does not look like a standard Syrian "
               "number.\nPlease confirm before continuing:"),
    },
    "step_of": {  # [V1]
        "ar": "\n\n📍 <b>الخطوة {n} من {t}</b>\n{bar}",
        "en": "\n\n📍 <b>Step {n} of {t}</b>\n{bar}",
    },
    "bal_line": {  # [V2]
        "ar": "\n💳 رصيدك الحالي: <b>{b}</b>",
        "en": "\n💳 Your balance: <b>{b}</b>",
    },
    "favamt_btn": {  # [R6-PLUS10 U37]
        "ar": "⭐ مبلغك المفضل", "en": "⭐ Your usual amount",
    },
    "txid_dup": {  # [R6-PLUS10 F8]
        "ar": ("⛔ رقم العملية <code>{t}</code> مسجّل سلفاً بهذه"
               " الطريقة — كل عملية لها رقم مختلف."),
        "en": ("⛔ Transaction ID <code>{t}</code> was already used"
               " with this method — each transfer has a unique ID."),
    },
    "lastreq_title": {  # [R6-PLUS10 U35]
        "ar": "📍 <b>آخر طلباتك</b>\n\n",
        "en": "📍 <b>Your latest request</b>\n\n",
    },
    "lastreq_none": {  # [U35]
        "ar": "📭 لا توجد لديك طلبات بعد.",
        "en": "📭 You have no requests yet.",
    },
    "req_type_dep": {"ar": "🛒 شحن", "en": "🛒 Deposit"},
    "req_type_wd": {"ar": "🏦 سحب", "en": "🏦 Withdraw"},
    "req_st_pending": {"ar": "⏳ قيد المراجعة", "en": "⏳ Under review"},
    "req_st_approved": {"ar": "✅ تم الاعتماد", "en": "✅ Approved"},
    "req_st_rejected": {"ar": "❌ مرفوض", "en": "❌ Rejected"},
    "req_st_expired": {"ar": "⌛ انتهت صلاحيته", "en": "⌛ Expired"},
    "wd_dest_reenter": {  # [R6-PLUS7 U31]
        "ar": "✏️ أعد إرسال <b>رقم الحساب</b>:",
        "en": "✏️ Please resend the <b>account number</b>:",
    },
    "wd_amount_prompt": {
        "ar": "💵 يرجى إدخال <b>المبلغ المراد سحبه</b>:",
        "en": "💵 Please enter <b>the amount to withdraw</b>:",
    },
    "dep_txid_ask": {
        "ar": "📝 ممتاز، الان يرجى إرسال <b>رقم العملية (TXID)</b> لـ {m}:",
        "en": "📝 Great, now please send the <b>transaction ID (TXID)</b>"
              " for {m}:",
    },
    "dep_txid_only": {
        "ar": "📝 أرسل <b>رقم العملية (TXID)</b> نصياً:",
        "en": "📝 Please send the <b>transaction ID (TXID)</b> as text:",
    },
    "txid_long": {  # [TXID-40] حد أعلى 40 حرفاً/رقماً
        "ar": "❌ رقم العملية يجب ألا يتجاوز <b>40 حرفاً أو رقماً</b>."
              "\nعدّ الأحرف وأعد إرسال الرقم الصحيح كما في تطبيق شام كاش:",
        "en": "❌ The transaction ID must not exceed <b>40 characters or"
              " digits</b>.\nPlease resend the correct code as shown in"
              " your Sham Cash app:",
        "ru": "❌ Номер операции должен быть не длиннее <b>40 символов"
              " или цифр</b>.\nОтправьте правильный номер, как в приложении"
              " Sham Cash:",
    },
    "dep_expired": {
        "ar": "انتهت الجلسة — ابدأ الشحن من جديد.",
        "en": "Session expired — please start the top-up again.",
    },
    "dep_success": {
        "ar": ("✅ <b>تم استلام طلب الشحن بنجاح!</b>\n\n"
               "💰 المبلغ: <code>{amt}</code>\n"
               "🆔 رقم العملية: <code>{txid}</code>\n"
               "🧾 رقم الطلب: <code>#{rid}</code>\n\n"
               "سيتم مراجعة الطلب وإضافة الرصيد قريباً."),
        "en": ("✅ <b>Your top-up request was received!</b>\n\n"
               "💰 Amount: <code>{amt}</code>\n"
               "🆔 Transaction ID: <code>{txid}</code>\n"
               "🧾 Request #: <code>{rid}</code>\n\n"
               "Your request will be reviewed and credited soon."),
    },
    "wd_success": {
        "ar": ("📨 <b>تم إرسال طلب السحب.</b>\n\n"
               "💵 المبلغ: <b>{amt}</b>\n"
               "🆔 رقم الطلب: <b>#{rid}</b>{wd_line}\n\n"
               "سيتم خصم المبلغ بعد موافقة الإدارة."),
        "en": ("📨 <b>Your withdrawal request has been submitted.</b>\n\n"
               "💵 Amount: <b>{amt}</b>\n"
               "🆔 Request #: <b>#{rid}</b>{wd_line}\n\n"
               "The amount will be deducted once approved by the admin."),
    },
    "wd_method_line": {"ar": "\n💳 الطريقة: <b>{m}</b>",
                       "en": "\n💳 Method: <b>{m}</b>"},
    "wd_dest_line": {"ar": "\n📒 وجهة الدفع: {l} — <code>{d}</code>",
                     "en": "\n📒 Payout destination: {l} — <code>{d}</code>"},
    "wd_manual_line": {"ar": "\n🏦 حساب الاستلام: <code>{d}</code>",
                       "en": "\n🏦 Receiving account: <code>{d}</code>"},
    "rewards_text": {
        "ar": "سيتم الإعلان عن الجوائز ضمن القناة الخاصة بالبوت بشكل دائم",
        "en": "Rewards will be announced in the bot's official channel"
              " on an ongoing basis",
    },
    "mi_title": {"ar": "🏪 <b>معلومات حسابك على 55bets:</b>",
                 "en": "🏪 <b>Your 55bets account info:</b>"},
    "mi_user": {"ar": "👤 <b>اسم المستخدم:</b>", "en": "👤 <b>Username:</b>"},
    "mi_pw": {"ar": "🔑 <b>كلمة المرور:</b>", "en": "🔑 <b>Password:</b>"},
    "mi_bal": {"ar": "💰 <b>رصيدك في البوت:</b>",
               "en": "💰 <b>Your bot balance:</b>"},
    "mi_refs": {"ar": "👥 <b>إحالاتك:</b>", "en": "👥 <b>Referrals:</b>"},
    "mi_notitle": {"ar": "🏪 <b>معلومات ملفي:</b>",
                   "en": "🏪 <b>My profile:</b>"},
    "mi_nocreate": {
        "ar": "لم تقم بإنشاء حساب 55bets عبر البوت بعد.",
        "en": "You haven't created an 55bets account via the bot yet.",
    },
    "b_stats": {"ar": "📊 إحصائياتك", "en": "📊 Your stats", "ru": "📊 Статистика"},
    "b_transfer": {"ar": "💸 تحويل رصيد لمستخدم",
                   "en": "💸 Transfer to a user"},
    "b_checkin": {"ar": "🔥 حضور اليوم", "en": "🔥 Daily check-in", "ru": "🔥 Ежедневный визит"},
    "b_tickets": {"ar": "💬 تذاكري", "en": "💬 My tickets", "ru": "💬 Мои тикеты"},
    "contact_text": {
        "ar": "فرق الدعم موجودة لخدمتكم على مدار الساعة:\n\nاختر المشكلة:",
        "en": "Our support team is available around the clock:\n\n"
              "Choose your issue:",
    },
    "c_bot": {"ar": "مشكلة ضمن البوت", "en": "Bot issue"},
    "c_site": {"ar": "مشكلة ضمن موقع 55bets", "en": "55bets website issue"},
    "c_dev": {"ar": "💻 تواصل مع المطور", "en": "💻 Contact the developer"},
    "back_contact": {"ar": "↩️ رجوع للجهات الفنية",
                     "en": "↩️ Back to contacts"},
    "site_issue_text": {
        "ar": ("في حال ورود مشكلة تقنية ضمن الموقع يرجى التواصل:\n"
               "مع الدّعم الرسمي للموقع عبر الرابط -\n"
               "https://direct.lc.chat/16220229\n"
               "أو عبر صفحة الموقع الرّسمية على منصّة Facebook.\n"
               "https://www.facebook.com/profile.php?id=61550987614559"),
        "en": ("For technical issues on the website please contact:\n"
               "The site's official support via the link -\n"
               "https://direct.lc.chat/16220229\n"
               "or via the site's official Facebook page.\n"
               "https://www.facebook.com/profile.php?id=61550987614559"),
    },
    "dev_text": {
        "ar": "💻 <b>الخدمات البرمجية</b>\n\n"
              "للخدمات البرمجية قم بالتواصل مع @Hamooshii",
        "en": "💻 <b>Software services</b>\n\n"
              "For software services contact @Hamooshii",
    },
    "dev_tg": {"ar": "👨‍💻 التواصل على تلجرام",
               "en": "👨‍💻 Contact on Telegram"},
    "share_text": {
        "ar": ("أرباحكم و إصاباتكم هي الأمل اللي بيدفعنا لنكمل و بخلينا"
               " ع طول فخورين بالخدمة اللي عم نقدمها\n\n"
               "و من خلال هاد الزر بتقدر تشارك صور إصابتك مع الفريق"
               " و تفرحهم معك 🥰\n\n"
               "كيف ؟ بس أرسل صورة إصابة أو مجموعة صور في رسالة واحدة"
               " و بصيرو عنا ⚡️"),
        "en": ("Your profits and big wins are the hope that keeps us going"
               " and makes us proud of the service we provide\n\n"
               "Through this button you can share screenshots of your wins"
               " with the team and make them happy with you 🥰\n\n"
               "How? Just send a photo of your win — or several photos"
               " in one message — and it's ours ⚡️"),
    },
    "share_ok": {
        "ar": "🥰 وصلت الصور للفريق — ربنا يزيدك من فضوله و يوفقك"
              " بالإصابة الجاية! ⚡️",
        "en": "🥰 The screenshots reached the team — may luck bring you"
              " even bigger wins! ⚡️",
    },
    "tut_title": {
        "ar": "🎓 <b>الشروحات</b> 🎓\n\n"
              "اختر أحد المواضيع من القائمة أدناه لعرض شرح مفصل.",
        "en": "🎓 <b>Tutorials</b> 🎓\n\n"
              "Pick a topic from the list below for a detailed guide.",
    },
    "tut1_btn": {"ar": "ما هو 55bets", "en": "What is 55bets"},
    "tut2_btn": {"ar": "إنشاء حساب 55bets", "en": "Create an 55bets account"},
    "tut3_btn": {"ar": "شحن رصيد في البوت", "en": "Top up your bot balance"},
    "tut4_btn": {"ar": "شحن حساب 55bets", "en": "Deposit to 55bets account"},
    "tut5_btn": {"ar": "سحب من حساب 55bets",
                 "en": "Withdraw from 55bets account"},
    "tut6_btn": {"ar": "سحب رصيد من البوت", "en": "Withdraw from the bot"},
    "tut_back": {"ar": "رجوع ↩️", "en": "Back ↩️"},
    "tut1_body": {
        "ar": ("موقع 55bets هو عبارة عن موقع للمراهنات الرياضية والعاب"
               " السلوتات و الكازينو\n\n"
               "يقوم المراهن باختيار لعبة او كازينو من الأيقونات الموجودة"
               " بعد فتح الموقع او من خيار البحث ضمن القائمة كل لعبة تحمل"
               " طريقة لعب خاصة و حدود رهانات متنوعة و أرباح قصوى مختلفة\n\n"
               "لمعرفة طريقة اللعب يمكنك استخدام الخيار التجريبي حيث تستطيع"
               " اللعب بأموال وهمية دون خسارة أموالك لكي تكون فكرة عن اللعبة"
               " و طريقة اللعب\n\n"
               "⚠️ هذا موقع ترفيهي و ليس مصدرا للدخل⚠️\n"
               " لا شيء مضمون سوى المتعة 🔥\n\n"
               "https://55bets.net"),
        "en": ("55bets is a sports betting, slots and casino website\n\n"
               "After opening the site, pick a game or casino from the icons"
               " or use the search option in the menu. Each game has its own"
               " play style, betting limits and maximum payouts\n\n"
               "To learn how to play, use the demo mode where you can play"
               " with virtual money without losing yours, to get a feel for"
               " the game\n\n"
               "⚠️ This is an entertainment website, not a source of income⚠️\n"
               " Nothing is guaranteed except the fun 🔥\n\n"
               "https://55bets.net"),
    },
    "tut2_body": {
        "ar": ("كيفية انشاء حساب 55bets:\n\n"
               "بعد الدخول الى البوت و الأنضمام للقناة قم بالتالي:\n"
               "1- اضغط على 55bets.\n"
               "2- اضغط على إنشاء حساب.\n"
               "3- قم بادخال اسم للحساب الجديد.\n"
               "4- ضع كلمة سر بطول 8 ارقام او اكثر.\n\n"
               "مبروك الحساب✅"),
        "en": ("How to create an 55bets account:\n\n"
               "After entering the bot and joining the channel, do the"
               " following:\n"
               "1- Tap 55bets.\n"
               "2- Tap Create account.\n"
               "3- Enter a name for the new account.\n"
               "4- Set a password of 8 digits or more.\n\n"
               "Congrats on your account ✅"),
    },
    "tut3_body": {
        "ar": ("💡 <b>طريقة شحن البوت:</b>\n\nاختر خيار 'شحن رصيد البوت'"
               " ثم اختر طريقة الدفع (شام كاش أو سيرياتيل كاش)، قم بتحويل"
               " المبلغ وأرسل المعرف ورقم العملية للتأكيد."),
        "en": ("💡 <b>How to top up the bot:</b>\n\nChoose 'Top up bot"
               " balance', pick a payment method (Sham Cash or Syriatel"
               " Cash), transfer the amount, then send the ID and the"
               " transaction number to confirm."),
    },
    "tut4_body": {
        "ar": ("💡 <b>طريقة شحن حساب 55bets:</b>\n\nتأكد من وجود رصيد"
               " في البوت ثم اختر '55bets حساب' -> 'شحن حساب' وأدخل المبلغ"
               " المراد تحويله إلى حسابك في الموقع."),
        "en": ("💡 <b>How to deposit to your 55bets account:</b>\n\nMake"
               " sure you have bot balance, then choose '55bets Account'"
               " -> 'Deposit to account' and enter the amount you want to"
               " move to your site account."),
    },
    "tut5_body": {
        "ar": ("💡 <b>طريقة السحب من 55bets:</b>\n\nقم باختيار"
               " '55bets حساب' -> 'سحب رصيد' وسيتم نقل الرصيد من الموقع"
               " إلى محفظتك بالبوت."),
        "en": ("💡 <b>How to withdraw from 55bets:</b>\n\nChoose"
               " '55bets Account' -> 'Withdraw from account' and the"
               " balance will be moved from the site to your bot wallet."),
    },
    "tut6_body": {
        "ar": ("💡 <b>طريقة السحب من البوت:</b>\n\nاختر 'سحب رصيد من"
               " البوت'، أدخل رقم الحساب أو المحفظة الخاصة بك والمبلغ"
               " وستصلك الحوالة."),
        "en": ("💡 <b>How to withdraw from the bot:</b>\n\nChoose"
               " 'Withdraw from bot', enter your account/wallet number and"
               " the amount, and the transfer will be sent to you."),
    },
    "offers_header": {"ar": "🍀 <b>العروض الحالية:</b>",
                      "en": "🍀 <b>Current offers:</b>"},
    "offers_none": {
        "ar": "تابع قناة البوت الرسمية للاطلاع على أحدث العروض والخصومات"
              " والجوائز الأسبوعية!",
        "en": "Follow the bot's official channel for the latest offers,"
              " discounts and weekly prizes!",
    },
    "terms_header": {"ar": "📜 <b>الشروط والأحكام:</b>",
                     "en": "📜 <b>Terms & Conditions:</b>"},
    "terms_default": {
        "ar": ("1. يجب أن يكون عمر المستخدم فوق ١٨ عاماً ويتحمل المسؤولية"
               " تجاه نفسه أمام القانون والمجتمع المحلي.\n"
               "2. يتحمل المستخدم مسؤولية الحفاظ على معلومات حسابه.\n"
               "3. أية عملية شحن أو سحب خاطئة بالبيانات المدخلة هي"
               " مسؤولية المستخدم.\n"
               "4. قم بحفظ لقطة شاشة لمعلومات حسابك أو قم بتسجيلها على ورقة"
               " واحفظها بعيداً عن متناول اليد، حسابك مسؤوليتك.\n"
               "5. مصمم لأجلك : البوت يقدم خدمات إنشاء الحسابات والسحب"
               " والتعبئة الفورية لموقع 55bets\n"
               "6. التزم بالقوانين : إنشاء أكثر من حساب على البوت يعرض"
               " حساباتك للحظر وتجميد الرصيد الموجود في الحسابات بحسب"
               " الشروط وأحكام الموقع للحد من الأنشطة الأحتيالية بناءً على"
               " سياسة اللعب النظيف\n"
               "7. مسؤوليتك تجاهنا : لا يحق لك كـ لاعب شحن وسحب رصيد بقصد"
               " التبديل بين طرق الدفع ويحق لإدارة البوت سحب أي رصيد"
               " والتحفظ عليه عند وجود عملية تبديل غير قانونية أو أي"
               " مخالفة لقوانين الموقع\n"
               "8. منكبر سوى قم بنشر البوت على وسائل التواصل الإجتماعي"
               " باستخدام رابط إحالتك واحصل على أرباح من مجمل عمليات"
               " التعبئة والسحب وفق الشروط\n"
               "9. قد تتغير الشروط في أي وقت ، ولأي إستفسار تواصل مع الدعم"
               " من واجهة البوت \" تواصل معنا \" ونحن موجودين لخدمتكم على"
               " مدار الساعة\n\n"
               "قناتنا موجودة لتبقى على اضطلاع بكل جديد ...\n\n"
               "نحن معكم لتقديم تجربة أفضل ❤️"),
        "en": ("1. Users must be over 18 years old and take responsibility"
               " for themselves before the law and their local"
               " community.\n"
               "2. The user is responsible for keeping their account"
               " information safe.\n"
               "3. Any deposit or withdrawal made with wrong entered data"
               " is the user's responsibility.\n"
               "4. Save a screenshot of your account info or write it down"
               " on paper and keep it out of reach — your account is your"
               " responsibility.\n"
               "5. Made for you: the bot provides account creation,"
               " withdrawal and instant top-up services for 55bets\n"
               "6. Follow the rules: creating more than one account on the"
               " bot exposes your accounts to banning and freezing of"
               " their balances per the site's terms, to limit fraudulent"
               " activity under the fair-play policy\n"
               "7. Your responsibility to us: as a player you may not"
               " deposit and withdraw with the intent of switching payment"
               " methods; the bot administration may withdraw and hold any"
               " balance if an illegal swap or any violation of the site's"
               " rules occurs\n"
               "8. Don't stop here: share the bot on social media using"
               " your referral link and earn from all top-up and"
               " withdrawal operations per the terms\n"
               "9. Terms may change at any time. For any question contact"
               " support from the bot's \"Contact us\" section — we are"
               " here for you around the clock\n\n"
               "Our channel is here to stay so you can keep up with all"
               " the new stuff...\n\n"
               "We are with you to deliver a better experience ❤️"),
    },
    "hist_title": {"ar": "🧾 <b>سجل عملياتك الأخيرة:</b>",
                   "en": "🧾 <b>Your recent transactions:</b>"},
    "hist_page": {"ar": "— صفحة {p}", "en": "— page {p}"},
    "done_no_photo": {"ar": "✅ إتمام الطلب بدون صورة",
                      "en": "✅ Finish without a screenshot"},
    "photo_ok": {"ar": "📎 وصلت صورة الإيصال وأُرفقت بطلبك — شكراً!",
                 "en": "📎 The receipt screenshot was attached to your"
                       " request — thanks!"},
    "photo_hint": {"ar": "📸 أرسل صورة الإيصال الآن، أو اضغط «✅ إتمام»",
                   "en": "📸 Send the receipt screenshot now, or tap"
                         " '✅ Finish'"},
    "wd_cooldown": {"ar": "⏱ أرسلت سحباً مؤخراً — يمكنك طلب سحب جديد"
                          " بعد {m}.",
                    "en": "⏱ You submitted a withdrawal recently — you"
                          " can request a new one in {m}."},
    "wd_fee_line": {"ar": "\n🏷 عمولة السحب: <code>{f}</code>"
                          " (من إجمالي {g})",
                    "en": "\n🏷 Withdrawal fee: <code>{f}</code>"
                          " (of {g})"},
    "mi_site_bal": {"ar": "🎮 رصيدك بالموقع:", "en": "🎮 Site balance:",
                    "ru": "🎮 Баланс на сайте:"},
    "myinfo_recent": {"ar": "\n\n🧾 <b>آخر عملياتك:</b>",
                      "en": "\n\n🧾 <b>Your recent activity:</b>"},
    "offer_exp_days": {"ar": "⏳ ينتهي بعد {d} يوم",
                       "en": "⏳ expires in {d} days"},
    "offer_exp_today": {"ar": "⏳ آخر يوم اليوم!",
                        "en": "⏳ last day today!"},
    "hist_type": {"ar": "📌 <b>{t}</b> ({m})",
                  "en": "📌 <b>{t}</b> ({m})"},
    "hist_amount": {"ar": "💵 المبلغ:", "en": "💵 Amount:"},
    "hist_details": {"ar": "📝 التفاصيل:", "en": "📝 Details:"},
    "hist_date": {"ar": "🗓 التاريخ:", "en": "🗓 Date:"},
}


def r6t(lang: str, key: str) -> str:
    """[R6] نص واجهة بحسب اللغة (ru يرجع لإنجليزي ثم عربي)."""
    entry = R6T.get(key) or {}
    return (
        entry.get(lang) or entry.get("en") or entry.get("ar") or key
    )


def greeting_text(lang: str, name: str) -> str:
    """[R6] ترحيب باسم المستخدم."""
    display = (name or "").strip()

    if not display:
        display = "my friend" if lang == "en" else "صديقي"

    display = esc(display)

    if lang == "en":
        return f"Hello {display} 👋, how can I help you today :"

    if lang == "ru":
        return f"Привет, {display} 👋, чем могу помочь сегодня :"

    return f"مرحباً {display} 👋، كيف يمكنني مساعدتك اليوم :"


async def greeting_text_smart(lang: str, name: str) -> str:
    """[R6-PLUS9 V3] ترحيب بتحية حسب وقت دمشق (ميزة قابلة للإيقاف)."""
    base = greeting_text(lang, name)

    if not await feat_on("smart_welcome") or lang == "ru":
        return base

    h = (datetime.now(timezone.utc) + timedelta(hours=3)).hour

    if lang == "en":
        greet = "Good morning" if 5 <= h < 17 else "Good evening"
        return base.replace("Hello", greet, 1)

    greet = "صباح الخير" if 5 <= h < 17 else "مساء الخير"

    return base.replace("مرحباً", greet, 1)


async def fmt_dt(value) -> str:
    """[R6-PLUS9 V6] عرض تاريخ/وقت بتوقيت دمشق عند تفعيل الميزة،
    وإلا UTC كما هو (النص غير القابل للتحليل يُعاد كما كان)."""
    s = str(value or "")

    try:
        dt = datetime.fromisoformat(s)
    except ValueError:
        return s

    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)

    if await feat_on("damascus_time"):
        dt = dt + timedelta(hours=3)

        return dt.strftime("%Y-%m-%d %H:%M") + " دمشق"

    return dt.strftime("%Y-%m-%d %H:%M") + " UTC"


async def ui_step_bar(lang: str, n: int, t: int) -> str:
    """[R6-PLUS9 V1] مؤشر خطوات التدفقات (بميزة قابلة للإيقاف)."""
    if not await feat_on("step_bars"):
        return ""

    filled = "▓" * max(0, min(t, n - 1))
    empty = "░" * max(0, t - (n - 1))

    return r6t(lang, "step_of").format(n=n, t=t, bar=filled + empty)


async def ui_bal_line(lang: str, tid: int) -> str:
    """[R6-PLUS9 V2] سطر الرصيد الحالي (بميزة قابلة للإيقاف)."""
    if not await feat_on("bal_bar"):
        return ""

    u = await get_user(tid)

    return r6t(lang, "bal_line").format(
        b=money(float(u["balance"] or 0)) if u else "0",
    )


def cancel_kb(lang: str, back_cb: str = "menu_back"):
    """[R6-PLUS9 V7] إلغاء صريح + رجوع لكل شاشات الإدخال."""
    b = InlineKeyboardBuilder()
    b.button(text="❌ إلغاء", callback_data="flow_cancel")
    b.button(text=tr(lang, "back"), callback_data=back_cb)
    b.adjust(2)

    return b.as_markup()


# [R6-PLUS9 V11] آخر شاشة إدارية لكل أدمن (زر «رجوع للسابقة»)
_last_admin_screen: dict = {}


def _with_data(cb, data: str):
    """[V11] إعادة استخدام نفس الكائن بمعطيات مختلفة."""
    try:
        cb.data = data
    except Exception:
        pass

    return cb


def _55bets_login_url(username: str, password: str) -> str:
    """[R6] رابط الدخول التلقائي ل55bets ببيانات المستخدم."""
    if username and password:
        from urllib.parse import quote

        return (
            f"{BETS55_LOGIN_BASE}"
            f"?accounts={quote(username)}&login={quote(password)}"
        )

    return f"{BETS55_LOGIN_BASE}?accounts=%2A&login=%2A"


async def _user_login_url(telegram_id: int) -> str:
    user = await get_user(telegram_id)

    if not user or not user["site_username"]:
        return f"{BETS55_LOGIN_BASE}?accounts=%2A&login=%2A"

    plain = ""
    if user["site_password"]:
        plain = decrypt_password(user["site_password"]) or ""

    return _55bets_login_url(user["site_username"], plain)


async def _unread_announcements(telegram_id: int) -> int:
    """[R6-PLUS2] عدد الإعلانات الفعالة التي لم يقرأها المستخدم."""
    db = await get_db()

    try:
        cur = await db.execute(
            "SELECT COUNT(*) AS c FROM announcements a"
            " WHERE a.expires_at > ? AND NOT EXISTS ("
            " SELECT 1 FROM announcement_reads r"
            " WHERE r.announcement_id = a.id AND r.telegram_id = ?)",
            (now_iso(), telegram_id),
        )
        return (await cur.fetchone())["c"]
    finally:
        await db.close()


async def get_55bets_main_menu(url: str, is_admin: bool = False, lang: str = "ar",
                          offers_badge: bool = False):
    """[R6] القائمة الرئيسية — نفس الأزرار والترتيب + زر تبديل اللغة."""
    b = InlineKeyboardBuilder()
    b.button(text=r6t(lang, "login"), url=url)
    b.button(text=r6t(lang, "55bets"), callback_data="menu_55bets")
    b.button(text=r6t(lang, "recharge"), callback_data="menu_recharge_bot")
    b.button(text=r6t(lang, "withdraw"), callback_data="menu_withdraw_bot")
    b.button(text=r6t(lang, "rewards"), callback_data="menu_rewards")
    b.button(text=r6t(lang, "refs"), callback_data="my_refs")
    b.button(text=r6t(lang, "myinfo"), callback_data="menu_my_info")
    b.button(text=r6t(lang, "history"), callback_data="my_history:0")
    b.button(text=r6t(lang, "gift"), callback_data="menu_gift")
    b.button(text=r6t(lang, "contact"), callback_data="menu_contact_us")
    b.button(text=r6t(lang, "share"), callback_data="menu_share_happiness")
    b.button(text=r6t(lang, "tutorials"), callback_data="menu_tutorials")
    b.button(
        text=r6t(lang, "offers") + (" 🔴" if offers_badge else ""),
        callback_data="menu_current_offers",
    )
    b.button(text=r6t(lang, "terms"), callback_data="menu_terms")
    b.button(text=r6t(lang, "lang_btn"), callback_data="toggle_lang")

    if is_admin:
        b.button(text=r6t(lang, "admpanel"), callback_data="admin_home")
        if not await panel_hidden_on():  # [PHIDE 5.18.2]
            b.button(text="🎰 لوحة الوكيل",
                     callback_data="panel_home")  # [MENU-ORG] بجانب لوحة الأدمن

    # [MENU-ORG] الصف الأخير: لوحة الأدمن + لوحة الوكيل جنباً إلى جنب
    b.adjust(*(1, 1, 2, 2, 1, 2, 2, 2, 2, 2) if is_admin
             else (1, 1, 2, 2, 1, 2, 2, 2, 2, 1))
    return b.as_markup()


async def main_menu_content(telegram_id: int):
    """[R6-PLUS9 V8] بناء محتوى القائمة الرئيسية (نص + أزرار)."""
    lang = await user_lang(telegram_id)
    user = await get_user(telegram_id)
    name = ""

    if user:
        name = user["full_name"] or user["username"] or ""

    url = await _user_login_url(telegram_id)
    # [R6-PLUS4F] زر اللوحة يظهر للمشرف المصرّح له أيضاً
    is_admin = await is_admin_or_supervisor(telegram_id)
    badge = (
        await _unread_announcements(telegram_id) > 0
        if await feat_on("offers_badge") else False
    )  # [R6-PLUS2 + R6-PLUS3]
    kb = await get_55bets_main_menu(url, is_admin, lang, offers_badge=badge)
    text = await greeting_text_smart(lang, name)  # [V3]

    return text, kb


async def send_55bets_main(message_or_cb_msg, telegram_id: int, edit=True):
    """[R6] عرض/تحديث القائمة الرئيسية بترحيب باسم المستخدم."""
    text, kb = await main_menu_content(telegram_id)

    if edit:
        await safe_edit(message_or_cb_msg, text, kb)
    else:
        await message_or_cb_msg.answer(text, reply_markup=kb)


def get_55bets_section_keyboard(user_id: int, login_url: str,
                                 lang: str = "ar"):
    """[R6] قسم 55bets — نفس الأزرار والترتيب."""
    b = InlineKeyboardBuilder()
    b.button(text=r6t(lang, "login"), url=login_url)
    b.button(text=r6t(lang, "sec_create"), callback_data="55bets_create")
    b.button(text=r6t(lang, "sec_dep"), callback_data="55bets_deposit")
    b.button(text=r6t(lang, "sec_wd"), callback_data="55bets_withdraw")
    b.button(text=r6t(lang, "back_main"), callback_data="back_to_main")
    b.adjust(1, 1, 2, 1)
    return b.as_markup()


@dp.callback_query(F.data.in_({"menu_55bets", "back_to_55bets"}))
async def menu_55bets(cb: types.CallbackQuery, state: FSMContext):
    """[R6] قائمة 55bets."""

    if not await user_allowed(cb.from_user.id):
        await cb.answer("غير مسموح.", show_alert=True)
        return

    await cb.answer()
    await state.clear()
    lang = await user_lang(cb.from_user.id)
    url = await _user_login_url(cb.from_user.id)
    await safe_edit(
        cb.message,
        r6t(lang, "ich_pick"),
        get_55bets_section_keyboard(cb.from_user.id, url, lang),
    )


@dp.callback_query(F.data == "55bets_create")
async def bets55_create(cb: types.CallbackQuery, state: FSMContext):
    """[R6] إنشاء حساب 55bets — نفس فحص التكرار الأصلي."""
    user = await get_user(cb.from_user.id)

    if user and user["site_username"]:
        acc_user = esc(user["site_username"])
        lang = await user_lang(cb.from_user.id)
        url = await _user_login_url(cb.from_user.id)
        kb = InlineKeyboardBuilder()
        kb.button(text=r6t(lang, "login"), url=url)
        kb.button(
            text=r6t(lang, "back_ich"), callback_data="back_to_55bets",
        )
        kb.adjust(1)
        await safe_edit(
            cb.message,
            f"⚠️ <b>لديك حساب مسجل بالفعل!</b>\n\n"
            f"لا يمكنك إنشاء أكثر من حساب واحد عبر البوت.\n"
            f"👤 <b>اسم المستخدم الخاص بك:</b> <code>{acc_user}</code>",
            kb.as_markup(),
        )
        return

    await svc_create_account(cb, state)


@dp.callback_query(F.data == "55bets_deposit")
async def bets55_deposit_info(cb: types.CallbackQuery, state: FSMContext):
    """[R6] شحن حساب 55bets (توجيه أصلي)."""

    if not await user_allowed(cb.from_user.id):
        await cb.answer("غير مسموح.", show_alert=True)
        return

    lang = await user_lang(cb.from_user.id)
    tip = (
        "Make sure to top up your bot balance first, then move it to your"
        " account."
    ) if lang == "en" else (
        "يرجى التأكد من شحن رصيدك في البوت أولاً ثم تحويله للحساب."
    )
    await cb.answer()
    await state.clear()
    await safe_edit(
        cb.message,
        f"{r6t(lang, 'sec_dep')} — {tip}",
        back_kb("back_to_55bets", lang),
    )


@dp.callback_query(F.data == "55bets_withdraw")
async def bets55_withdraw_info(cb: types.CallbackQuery, state: FSMContext):
    """[R6] سحب من حساب 55bets (توجيه أصلي)."""

    if not await user_allowed(cb.from_user.id):
        await cb.answer("غير مسموح.", show_alert=True)
        return

    lang = await user_lang(cb.from_user.id)
    tip = (
        "Select the amount and move the balance from the site to the bot."
    ) if lang == "en" else (
        "حدد المبلغ المطلوب وسحب الرصيد إلى البوت."
    )
    await cb.answer()
    await state.clear()
    await safe_edit(
        cb.message,
        f"{r6t(lang, 'sec_wd')} — {tip}",
        back_kb("back_to_55bets", lang),
    )


# ------------------------------------------------------------
# [R6] الشحن — طرائق الدفع الأصلي (شام كاش / سيرياتيل كاش)
# ------------------------------------------------------------

def get_recharge_methods_kb(lang: str = "ar"):
    b = InlineKeyboardBuilder()
    b.button(text=r6t(lang, "m_sham"), callback_data="pay_sham_cash")
    b.button(text=r6t(lang, "m_syriatel"), callback_data="pay_syriatel_cash")
    b.button(text=r6t(lang, "calc"), callback_data="calc_dep")  # [USR4-5]
    b.button(text=r6t(lang, "back_main"), callback_data="back_to_main")
    b.adjust(1)
    return b.as_markup()


def _reorder_kb_by_cb(kb, fav_cb: str):
    """[AUDIT F4] تصدير صف المفضلة (بمطابقة callback_data) لأول القائمة."""
    rows = [list(r) for r in kb.inline_keyboard]
    fav_rows = [r for r in rows if r[0].callback_data == fav_cb]
    rest = [r for r in rows if r[0].callback_data != fav_cb]

    if not fav_rows:
        return kb

    nb = InlineKeyboardBuilder()

    for r in fav_rows + rest:
        nb.row(*r)

    return nb.as_markup()


_DEP_FAV_CB = {
    "شام كاش": "pay_sham_cash",
    "شام كاش (رمز حساب)": "pay_sham_cash",
    "سيرياتيل كاش": "pay_syriatel_cash",
}

_WD_FAV_CB = {
    "شام كاش": "withdraw_sham_cash",
    "سيرياتيل كاش": "withdraw_syriatel_cash",
}


async def recharge_kb_for(tid: int, lang: str):
    """[R6-PLUS3 + AUDIT F4] طرق الشحن والمفضلة أولاً (بcallback_data)."""
    kb = get_recharge_methods_kb(lang)

    if not await feat_on("fav_method"):
        return kb

    user = await get_user(tid)
    fav = (user["last_dep_method"] or "") if user else ""

    return _reorder_kb_by_cb(kb, _DEP_FAV_CB.get(fav, ""))


async def withdraw_kb_for(tid: int, lang: str):
    """[AUDIT F4] طرق السحب والمفضلة أولاً (كانت تُحفظ ولا تُستخدم)."""
    kb = get_withdraw_methods_kb(lang)

    if not await feat_on("fav_method"):
        return kb

    user = await get_user(tid)
    fav = (user["last_wd_method"] or "") if user else ""

    return _reorder_kb_by_cb(kb, _WD_FAV_CB.get(fav, ""))


def get_withdraw_methods_kb(lang: str = "ar"):
    b = InlineKeyboardBuilder()
    b.button(text=r6t(lang, "m_sham"), callback_data="withdraw_sham_cash")
    b.button(text=r6t(lang, "m_syriatel"),
             callback_data="withdraw_syriatel_cash")
    b.button(text=r6t(lang, "back_main"), callback_data="back_to_main")
    b.adjust(1)
    return b.as_markup()


def recharge_amount_kb(lang: str = "ar"):
    """[R6-NEW] مبالغ سريعة + رجوع — شاشة إدخال مبلغ الشحن."""
    b = InlineKeyboardBuilder()

    for amount in (10, 25, 50, 100):
        b.button(text=f"＋{amount}", callback_data=f"dep_quick:{amount}")

    b.button(text=r6t(lang, "back_main"), callback_data="back_to_recharge")
    b.adjust(4, 1)
    return b.as_markup()


async def recharge_amount_kb_for(tid: int, lang: str):
    """[R6-PLUS5] المبالغ السريعة الخاصة + زر مساعدة داخل التدفق."""
    user = await get_user(tid)
    custom = []

    if user and (user["quick_amounts"] or "").strip():
        for part in user["quick_amounts"].split(","):
            try:
                v = float(part.strip())

                if v > 0:
                    custom.append(v)
            except ValueError:
                continue

    fav_on = await feat_on("fav_amount")  # [R6-PLUS10 U37]
    fav = 0.0

    if fav_on:
        try:
            fav = float((await get_setting(f"fav_amount_{tid}") or "0"))
        except ValueError:
            fav = 0.0

    out = InlineKeyboardBuilder()

    if fav > 0:  # المبلغ المفضل يتصدر القائمة
        out.button(text=f"⭐{fav:g}", callback_data=f"dep_quick:{fav:g}")

    for amount in (custom or [10, 25, 50, 100])[:4]:
        mark = "⚡" if custom else "＋"
        out.button(
            text=f"{mark}{amount:g}",
            callback_data=f"dep_quick:{amount:g}",
        )

    out.button(
        text=r6t(lang, "quick_btn"),
        callback_data="quickset",
    )  # [R6-PLUS5]

    if fav_on:
        out.button(
            text=r6t(lang, "favamt_btn"),
            callback_data="favamt_set",
        )  # [U37]

    out.button(
        text=r6t(lang, "help_btn"),
        callback_data="flowhelp:dep",
    )  # [R6-PLUS5]
    out.button(text=r6t(lang, "back_main"), callback_data="back_to_recharge")

    if fav > 0:
        out.adjust(1, 4, 2, 1, 1)
    elif fav_on:
        out.adjust(4, 2, 1, 1)
    else:
        out.adjust(4, 1, 1, 1)

    return out.as_markup()

@dp.callback_query(F.data.startswith("flowhelp:"))
async def flowhelp(cb: types.CallbackQuery, state: FSMContext):
    """[R6-PLUS5] مساعدة فورية داخل تدفق الشحن/السحب."""

    if not await user_allowed(cb.from_user.id):
        await cb.answer("غير مسموح.", show_alert=True)
        return

    ctx = cb.data.split(":", 1)[1]

    if ctx not in ("dep", "wd"):
        await cb.answer("خيار غير معروف.", show_alert=True)
        return

    await cb.answer()
    await state.clear()
    await state.set_state(SupportFSM.message)
    await state.update_data(flow_ctx=ctx)  # [AUDIT F6]

    lang = await user_lang(cb.from_user.id)
    ctx_text = r6t(
        lang, "help_dep" if ctx == "dep" else "help_wd",
    )

    await cb.message.answer(ctx_text)


@dp.callback_query(F.data == "quickset")
async def quickset_start(cb: types.CallbackQuery, state: FSMContext):
    """[R6-PLUS5] ضبط المبالغ السريعة الخاصة."""

    if not await user_allowed(cb.from_user.id):
        await cb.answer("غير مسموح.", show_alert=True)
        return

    await cb.answer()
    await state.clear()
    await state.set_state(QuickAmtFSM.value)

    await cb.message.answer(r6t(await user_lang(cb.from_user.id),
                                "quick_prompt"))


@dp.message(QuickAmtFSM.value)
async def quickset_save(message: types.Message, state: FSMContext):
    """[R6-PLUS5] حفظ المبالغ السريعة."""

    if not await user_allowed(message.from_user.id, message):
        await state.clear()
        return

    raw = (message.text or "").strip()

    if not raw or raw.startswith("/"):
        await state.clear()
        return

    lang = await user_lang(message.from_user.id)

    if raw in ("مسح", "clear"):
        await update_user(message.from_user.id, quick_amounts="")
        await state.clear()
        await message.answer(r6t(lang, "quick_cleared"))
        return

    vals = []

    for part in raw.replace("،", " ").replace(",", " ").split():
        try:
            v = float(part)

            if 0 < v <= MAX_AMOUNT:
                vals.append(v)
        except ValueError:
            continue

    vals = sorted(set(vals))[:4]

    if not vals:
        await message.answer(r6t(lang, "quick_invalid"))
        return

    await update_user(
        message.from_user.id,
        quick_amounts=",".join(f"{v:g}" for v in vals),
    )
    await state.clear()

    await message.answer(
        r6t(lang, "quick_done").format(
            q="، ".join(f"{v:g}" for v in vals),
        )
    )


@dp.callback_query(F.data.in_({"menu_recharge_bot", "back_to_recharge"}))
async def menu_recharge_bot(cb: types.CallbackQuery, state: FSMContext):
    """[R6] شاشة طرق الدفع."""

    if not await user_allowed(cb.from_user.id):
        await cb.answer("غير مسموح.", show_alert=True)
        return

    await cb.answer()
    await state.clear()
    lang = await user_lang(cb.from_user.id)
    await safe_edit(
        cb.message,
        r6t(lang, "recharge_pick"),
        await recharge_kb_for(cb.from_user.id, lang),  # [R6-PLUS3]
    )


@dp.callback_query(F.data.in_({"menu_withdraw_bot", "back_to_withdraw"}))
async def menu_withdraw_bot(cb: types.CallbackQuery, state: FSMContext):
    """[R6] شاشة طرق السحب."""

    if not await user_allowed(cb.from_user.id):
        await cb.answer("غير مسموح.", show_alert=True)
        return

    await cb.answer()
    await state.clear()
    lang = await user_lang(cb.from_user.id)
    await safe_edit(
        cb.message,
        r6t(lang, "withdraw_pick")
        + await ui_step_bar(lang, 1, 4),  # [V1]
        await withdraw_kb_for(cb.from_user.id, lang),  # [AUDIT F4]
    )


async def _wallet_number(method_key: str) -> str:
    setting_key = f"{method_key}_wallet_number"
    value = (await get_setting(setting_key) or "").strip()
    return value or "09XXXXXXXX"


@dp.callback_query(F.data == "pay_sham_cash")
async def pay_sham_cash(cb: types.CallbackQuery, state: FSMContext):
    """[R6] شحن شام كاش — نفس النص الأصلي + رقم المحفظة من اللوحة."""

    if not await user_allowed(cb.from_user.id):
        await cb.answer("غير مسموح.", show_alert=True)
        return

    lang = await user_lang(cb.from_user.id)

    if (await get_setting("accept_sham") or "1") != "1":
        await cb.answer(r6t(lang, "sham_off"), show_alert=True)
        return

    await cb.answer()
    await state.clear()
    await state.update_data(deposit_method="شام كاش")
    await state.set_state(DepositFSM.amount)

    if await feat_on("fav_method"):  # [R6-PLUS3]
        await update_user(cb.from_user.id, last_dep_method="شام كاش")

    # [R6-PLUS4] نمط العرض يحدده الأدمن: رقم محفظة أو رمز حساب
    if (await get_setting("sham_code_mode") or "wallet") == "code":
        code = (await get_setting("sham_account_code") or "").strip() \
            or "—"
        await safe_edit(
            cb.message,
            r6t(lang, "sham_code_title").format(code=esc(code))
            + await ui_step_bar(lang, 2, 4)  # [V1]
            + await ui_bal_line(lang, cb.from_user.id),  # [V2]
            await recharge_amount_kb_for(cb.from_user.id, lang),
        )
        return

    wallet = await _wallet_number("sham")
    await safe_edit(
        cb.message,
        r6t(lang, "sham_title").format(wallet=esc(wallet))
        + await ui_step_bar(lang, 2, 4)  # [V1]
        + await ui_bal_line(lang, cb.from_user.id),  # [V2]
        await recharge_amount_kb_for(cb.from_user.id, lang),
    )


@dp.callback_query(F.data == "pay_syriatel_cash")
async def pay_syriatel_cash(cb: types.CallbackQuery, state: FSMContext):
    """[R6] شحن سيرياتيل كاش — نفس النص الأصلي."""

    if not await user_allowed(cb.from_user.id):
        await cb.answer("غير مسموح.", show_alert=True)
        return

    lang = await user_lang(cb.from_user.id)

    if (await get_setting("accept_syriatel") or "1") != "1":
        await cb.answer(r6t(lang, "syr_off"), show_alert=True)
        return

    await cb.answer()
    await state.clear()
    await state.update_data(deposit_method="سيرياتيل كاش")

    if await feat_on("fav_method"):  # [R6-PLUS3]
        await update_user(cb.from_user.id, last_dep_method="سيرياتيل كاش")
    await state.set_state(DepositFSM.amount)

    # [MENU-ORG] نمط العرض يحدده الأدمن: رقم محفظة أو رمز إيداع
    if (await get_setting("syriatel_code_mode") or "wallet") == "code":
        code = (await get_setting("syriatel_account_code") or "").strip() \
            or "—"
        await safe_edit(
            cb.message,
            r6t(lang, "syr_code_title").format(code=esc(code))
            + await ui_step_bar(lang, 2, 4)  # [V1]
            + await ui_bal_line(lang, cb.from_user.id),  # [V2]
            await recharge_amount_kb_for(cb.from_user.id, lang),
        )
        return

    wallet = await _wallet_number("syriatel")
    await safe_edit(
        cb.message,
        r6t(lang, "syr_title").format(wallet=esc(wallet))
        + await ui_step_bar(lang, 2, 4)  # [V1]
        + await ui_bal_line(lang, cb.from_user.id),  # [V2]
        await recharge_amount_kb_for(cb.from_user.id, lang),
    )


@dp.message(DepositFSM.txid)
async def deposit_txid(message: types.Message, state: FSMContext):
    """[R6] رقم العملية ثم إنشاء الطلب بنفس ردود الواجهة الأصلية."""

    if not await user_allowed(message.from_user.id, message):
        return

    # [R6-PLUS7 E4] منع العمليات المالية خلال نافذة الصيانة
    if await _maint_fin_msg(message, state):
        return

    lang = await user_lang(message.from_user.id)
    txid = (message.text or "").strip()

    if not txid:
        await message.answer(r6t(lang, "dep_txid_only"))
        return

    if txid.startswith("/"):
        await state.clear()
        return

    # [TXID-40] حد أعلى 40 حرفاً أو رقماً — بلا قصّ صامت
    if len(txid) > 40:
        await message.answer(r6t(lang, "txid_long"))
        return

    data = await state.get_data()
    amount = data.get("dep_amount")
    method = data.get("deposit_method") or "شام كاش"
    promo = data.get("promo") or ""  # [USR2-4]

    if not amount:
        await state.clear()
        await message.answer(
            r6t(lang, "dep_expired"),
            reply_markup=back_kb("back_to_recharge", lang),
        )
        return

    # [R6-PLUS10 F8] منع تكرار رقم العملية لنفس الطريقة
    if await feat_on("txid_dedup"):
        db_x = await get_db()

        try:
            cur_x = await db_x.execute(
                "SELECT note FROM finance_requests"
                " WHERE type = 'deposit'"
                " AND status IN ('pending', 'approved')"
                " AND instr(note || ';', 'txid=' || ? || ';') > 0"
                " LIMIT 5",
                (txid,),
            )
            dup_rows = await cur_x.fetchall()
        finally:
            await db_x.close()

        for d in dup_rows:
            d_method = ""

            for part in (d["note"] or "").split(";"):
                if part.startswith("method="):
                    d_method = part[7:]

            if d_method == method:
                await message.answer(
                    r6t(lang, "txid_dup").format(t=esc(txid)),
                )
                await state.clear()
                return

    request_id = await create_finance_request(
        message.from_user.id, "deposit", amount,
        promo_code=promo, note=f"method={method};txid={txid}",
    )

    # [R6-NEW] نافذة اختيارية لإرفاق صورة إيصال التحويل
    await state.update_data(dep_rid=request_id)
    await state.set_state(DepositFSM.photo)

    b_done = InlineKeyboardBuilder()
    b_done.button(
        text=r6t(lang, "done_no_photo"), callback_data="dep_done",
    )
    b_done.adjust(1)

    dep_receipt = (
        tr(lang, "receipt_line")  # [V5]
        if await feat_on("clear_receipt") else ""
    )

    await message.answer(
        r6t(lang, "dep_success").format(
            amt=money(amount), txid=esc(txid), rid=request_id,
        ) + dep_receipt,
        reply_markup=b_done.as_markup(),
    )

    # [AUTODEP-NOTE 5.18.21] توضيح مسار التحقق الآلي بالإشعار نفسه —
    # كان الأدمن يعتمد يدوياً «فوراً» فتُجهض نافذة الآلي قبل أن تبدو
    auto_note = ""

    if (method == "شام كاش"
            and await feat_on("sham_auto_dep")
            and await _sham_load()):
        auto_note = (
            "\n\n🤖 <b>التحقق الآلي جارٍ الآن</b> (نافذة ~25 دقيقة)"
            " — إن تطابق رقم العملية والمبلغ سيعتمد الطلب تلقائياً"
            " خلال ثوانٍ.\n💡 اتركه إن أردت المسار الآلي؛"
            " اعتمادك اليدوي يوقفه."
        )

    # [NEW 15] إشعار الفريق المالي كاملاً
    await notify_finance_staff(
        "💰 <b>طلب شحن جديد</b>\n\n"
        f"👤 المستخدم: <code>{message.from_user.id}</code>\n"
        f"💳 الطريقة: <b>{esc(method)}</b>\n"
        f"💵 المبلغ: <b>{money(amount)}</b>\n"
        f"🆔 رقم العملية: <code>{esc(txid)}</code>\n"
        f"🧾 الطلب: #{request_id}" + auto_note,
        request_id,
        exclude_id=message.from_user.id,
    )


@dp.callback_query(F.data == "dep_done")
async def dep_done(cb: types.CallbackQuery, state: FSMContext):
    """[R6-NEW] إنهاء طلب الشحن بدون صورة إيصال."""
    await cb.answer()
    await state.clear()
    await send_55bets_main(cb.message, cb.from_user.id, edit=True)


@dp.message(DepositFSM.photo, F.photo)
async def dep_photo(message: types.Message, state: FSMContext):
    """[R6-NEW] استلام صورة الإيصال وإرفاقها بالطلب للفريق المالي."""

    if not await user_allowed(message.from_user.id, message):
        return

    lang = await user_lang(message.from_user.id)
    data = await state.get_data()
    rid = data.get("dep_rid")
    await state.clear()

    caption = (
        f"📎 إيصال طلب الشحن #{rid}"
        f" من <code>{message.from_user.id}</code>"
    )

    for staff_id in await get_finance_staff_ids():
        try:
            await message.copy_to(staff_id, caption=caption)
        except Exception as exc:
            logger.warning("تعذر تمرير إيصال إلى %s: %s", staff_id, exc)

    mirror_chat = (await get_setting("mirror_chat_id") or "").strip()

    if mirror_chat.lstrip("-").isdigit():
        try:
            await message.copy_to(int(mirror_chat), caption=caption)
        except Exception:
            pass

    await message.answer(
        r6t(lang, "photo_ok"),
        reply_markup=back_kb("back_to_main", lang),
    )


@dp.message(DepositFSM.photo)
async def dep_photo_other(message: types.Message, state: FSMContext):
    """[R6-NEW] تلميح إن وصل شيء غير صورة."""

    if (message.text or "").startswith("/"):
        await state.clear()
        return

    lang = await user_lang(message.from_user.id)
    await message.answer(r6t(lang, "photo_hint"))


@dp.callback_query(F.data == "withdraw_sham_cash")
async def withdraw_sham_cash(cb: types.CallbackQuery, state: FSMContext):
    """[R6] سحب شام كاش — نفس النص الأصلي."""

    if not await user_allowed(cb.from_user.id):
        await cb.answer("غير مسموح.", show_alert=True)
        return

    if await feat_on("fav_method"):  # [R6-PLUS3]
        await update_user(cb.from_user.id, last_wd_method="شام كاش")

    lang = await user_lang(cb.from_user.id)
    await cb.answer()
    await state.clear()
    await state.update_data(withdraw_method="شام كاش")
    await state.set_state(WithdrawFSM.account)

    await safe_edit(
        cb.message,
        r6t(lang, "wd_sham_title")
        + await ui_step_bar(lang, 2, 4)  # [V1]
        + await ui_bal_line(lang, cb.from_user.id),  # [V2]
        cancel_kb(lang, "back_to_withdraw"),  # [V7]
    )


@dp.callback_query(F.data == "withdraw_syriatel_cash")
async def withdraw_syriatel_cash(cb: types.CallbackQuery, state: FSMContext):
    """[R6] سحب سيرياتيل كاش — نفس النص الأصلي."""

    if not await user_allowed(cb.from_user.id):
        await cb.answer("غير مسموح.", show_alert=True)
        return

    if await feat_on("fav_method"):  # [R6-PLUS3]
        await update_user(cb.from_user.id, last_wd_method="سيرياتيل كاش")

    lang = await user_lang(cb.from_user.id)
    await cb.answer()
    await state.clear()
    await state.update_data(withdraw_method="سيرياتيل كاش")
    await state.set_state(WithdrawFSM.account)

    await safe_edit(
        cb.message,
        r6t(lang, "wd_syr_title")
        + await ui_step_bar(lang, 2, 4)  # [V1]
        + await ui_bal_line(lang, cb.from_user.id),  # [V2]
        cancel_kb(lang, "back_to_withdraw"),  # [V7]
    )


WD_DEST_MAX = 40  # [WD-40] وجهات المحافظ: حتى 40 خانة


def _norm_wd_dest(raw: str):
    """[R6-PLUS7 U31 + WD-40] تحقق وجهة السحب → (المطبّع، ok/doubt/bad).

    ok: رقم موبايل سوري (09xxxxxxxx / 9xxxxxxxx / +963…).
    doubt: أرقام فقط لكن لا تطابق الصيغة السورية — يُعرض للتأكيد.
    alpha: معرف/رمز شام كاش (حروف ورموز) — مقبول حتى 40 خانة.
    bad: طول غير منطقي (فوق 40 أو أقل من 5) — يُرفض.
    """
    s = (raw or "").strip()

    # [WD-40] عنوان حرفي/مختلط (معرف شام كاش مثلاً): مقبول حتى 40
    if any(ch.isalpha() for ch in s):
        if 5 <= len(s) <= WD_DEST_MAX:
            return s, "alpha"

        return s, "bad"

    d = re.sub(r"[ \-().]", "", s).lstrip("+")

    if not d.isdigit() or not (6 <= len(d) <= 15):
        # أرقام فقط بطول غير قياسي: مقبول حتى 40 للتأكيد بدل الرفض
        if d.isdigit() and len(d) <= WD_DEST_MAX:
            return d, "doubt"

        return s, "bad"

    if re.fullmatch(r"(?:00963|963)?0?9\d{8}", d):
        if d.startswith("00963"):
            return "+963" + d[5:], "ok"

        if d.startswith("963") and len(d) == 12:
            return "+963" + d[3:], "ok"

        if d.startswith("0"):
            return "+963" + d[1:], "ok"

        return "+963" + d, "ok"

    return d, "doubt"


@dp.message(WithdrawFSM.account)
async def withdraw_account_save(message: types.Message, state: FSMContext):
    """[R6] حفظ حساب الاستلام ثم سؤال المبلغ (نفس رد الواجهة الأصلي)."""

    if not await user_allowed(message.from_user.id, message):
        return

    dest = (message.text or "").strip()[:60]

    if not dest or dest.startswith("/"):
        await state.clear()
        return

    lang = await user_lang(message.from_user.id)

    if len(dest) < 5:
        await message.answer(r6t(lang, "wd_acct_short"))
        return

    # [R6-PLUS7 U31 + WD-40] تحقق صيغة الوجهة قبل قبول الطلب
    if await feat_on("wd_dest_check"):
        norm, verdict = _norm_wd_dest(dest)

        if verdict == "bad":
            await message.answer(r6t(lang, "wd_dest_bad"))
            return

        if verdict == "alpha":  # [WD-40] معرف حرفي — يمر مباشرة
            dest = norm

        elif verdict == "doubt":
            await state.update_data(wd_dest_pending=norm)
            await state.set_state(WithdrawFSM.dest_confirm)

            kb = InlineKeyboardBuilder()
            kb.button(text="✅ تأكيد", callback_data="wd_dest_keep")
            kb.button(text="✏️ تعديل", callback_data="wd_dest_edit")
            kb.adjust(2)
            await message.answer(
                r6t(lang, "wd_dest_doubt").format(d=norm),
                reply_markup=kb.as_markup(),
            )
            return

        dest = norm

    await state.update_data(wd_dest=dest)
    await state.set_state(WithdrawFSM.amount)
    await message.answer(
        r6t(lang, "wd_amount_prompt")
        + await ui_step_bar(lang, 3, 4)  # [V1]
        + await ui_bal_line(lang, message.from_user.id),  # [V2]
        reply_markup=cancel_kb(lang, "back_to_withdraw"),  # [V7]
    )


@dp.callback_query(F.data == "wd_dest_keep")
async def wd_dest_keep(cb: types.CallbackQuery, state: FSMContext):
    """[R6-PLUS7 U31] تأكيد وجهة مشكوك بها والمتابعة للمبلغ."""

    if not await user_allowed(cb.from_user.id):
        await cb.answer("غير مسموح.", show_alert=True)
        return

    data = await state.get_data()
    dest = (data.get("wd_dest_pending") or "").strip()

    if not dest:
        await cb.answer("انتهت الجلسة — أعد إدخال الرقم.", show_alert=True)
        await state.clear()
        return

    lang = await user_lang(cb.from_user.id)
    await cb.answer()
    await state.clear()
    await state.update_data(wd_dest=dest)
    await state.set_state(WithdrawFSM.amount)
    await cb.message.answer(
        r6t(lang, "wd_amount_prompt")
        + await ui_step_bar(lang, 3, 4)  # [V1]
        + await ui_bal_line(lang, cb.from_user.id),  # [V2]
        reply_markup=cancel_kb(lang, "back_to_withdraw"),  # [V7]
    )


@dp.callback_query(F.data == "wd_dest_edit")
async def wd_dest_edit(cb: types.CallbackQuery, state: FSMContext):
    """[R6-PLUS7 U31] إعادة إدخال رقم الوجهة."""

    if not await user_allowed(cb.from_user.id):
        await cb.answer("غير مسموح.", show_alert=True)
        return

    lang = await user_lang(cb.from_user.id)
    await cb.answer()
    await state.clear()
    await state.update_data(wd_dest_pending="")
    await state.set_state(WithdrawFSM.account)
    await cb.message.answer(r6t(lang, "wd_dest_reenter"))


# ------------------------------------------------------------
# [R6] الأقسام الثابتة بنصوصها الأصلية حرفياً
# ------------------------------------------------------------

@dp.callback_query(F.data == "menu_rewards")
async def menu_rewards(cb: types.CallbackQuery, state: FSMContext):
    """[R6] الجوائز — النص الأصلي."""

    if not await user_allowed(cb.from_user.id):
        await cb.answer("غير مسموح.", show_alert=True)
        return

    lang = await user_lang(cb.from_user.id)
    await cb.answer()
    await state.clear()
    await safe_edit(
        cb.message,
        r6t(lang, "rewards_text"),
        back_kb("back_to_main", lang),
    )


@dp.callback_query(F.data == "menu_rates")
async def menu_rates(cb: types.CallbackQuery, state: FSMContext):
    """[R6-PLUS7 U32] شاشة الأسعار والحدود للمستخدم."""

    if not await user_allowed(cb.from_user.id):
        await cb.answer("غير مسموح.", show_alert=True)
        return

    if not await feat_on("rates_screen"):
        await cb.answer()
        return

    lang = await user_lang(cb.from_user.id)
    await cb.answer()
    await state.clear()

    dep = await amount_limits("deposit")
    wd = await amount_limits("withdraw")
    ppu = await get_float_setting("points_per_unit", 1.0)
    fee = await get_float_setting("withdraw_fee_percent", 0.0)
    wcnt = await get_float_setting("daily_wd_count", 0.0)

    text = tr(
        lang, "rates_limits",
        ppu=f"{ppu:g}",
        fee=f"{fee:g}",
        dmin=money(dep["min"]), dmax=money(dep["max"]),
        wmin=money(wd["min"]), wmax=money(wd["max"]),
        wcnt=f"{int(wcnt)}" if wcnt > 0 else "∞",
    )

    await safe_edit(
        cb.message,
        text,
        back_kb("menu_back", lang),
    )


async def _render_my_info(msg, telegram_id: int, edit: bool = True):
    """[R6-CH] بناء صفحة معلومات ملفي — مشتركة بين الزر وأمر /my_info."""
    lang = await user_lang(telegram_id)
    user = await get_user(telegram_id)

    db = await get_db()

    try:
        cur = await db.execute(
            "SELECT COUNT(*) AS c FROM users WHERE referrer_id = ?",
            (telegram_id,),
        )
        refs_count = (await cur.fetchone())["c"]
    finally:
        await db.close()

    loyal = await get_loyalty(telegram_id)  # [USR4-1]

    if user and user["site_username"]:
        acc_user = esc(user["site_username"])
        # [R6-REV] كلمة المرور تُعرض مباشرة (طلب المستخدم — بلا إخفاء)
        plain_pw = decrypt_password(user["site_password"] or "") \
            if user["site_password"] else ""
        bal_str = (
            r6t(lang, "bal_hidden")
            if user["hide_balance"] else money(user["balance"])
        )
        live_line = ""  # [R6-PLUS12 site_balance_live]

        if await feat_on("site_balance_live") and panel_ready() and user["site_username"]:
            client = ipanel.get_panel()
            player, perr = await panel_call(
                client.find_player, user["site_username"],
            )

            if not perr and player:
                live_bal, lerr = await panel_call(
                    client.player_balance, player.get("playerId"),
                )

                if not lerr and live_bal is not None:
                    live_line = (
                        f"\n{r6t(lang, 'mi_site_bal')} "
                        f"<b>{live_bal:.2f}</b>"
                    )

        info_text = (
            r6t(lang, "mi_title") + "\n\n"
            + f"{r6t(lang, 'mi_user')} <code>{acc_user}</code>\n"
            + f"{r6t(lang, 'mi_pw')} <code>{esc(plain_pw)}</code>\n"
            + f"{r6t(lang, 'mi_bal')} <b>{bal_str}</b>"
            + live_line + "\n"
            + f"{r6t(lang, 'mi_refs')} {refs_count}"
        )
    else:
        bal_str = (
            r6t(lang, "bal_hidden")
            if (user and user["hide_balance"])
            else money(user["balance"] if user else 0)
        )
        info_text = (
            r6t(lang, "mi_notitle") + "\n\n"
            + r6t(lang, "mi_nocreate") + "\n"
            + f"{r6t(lang, 'mi_bal')} <b>{bal_str}</b>\n"
            + f"{r6t(lang, 'mi_refs')} {refs_count}"
        )

    # [R6-PLUS2] سطر النقاط
    if user and (user["points"] or 0) > 0:
        info_text += (
            f"\n{r6t(lang, 'points_line')} "
            f"<b>{user['points']}</b>"
        )

    if loyal["line"]:
        info_text += f"\n{loyal['line']}"

    # [R6-NEW] آخر 3 عمليات مباشرة في صفحة ملفي
    if user:
        db_r = await get_db()

        try:
            cur_r = await db_r.execute(
                "SELECT type, amount, created_at FROM transactions"
                " WHERE user_id = ? ORDER BY id DESC LIMIT 3",
                (user["id"],),
            )
            recent = await cur_r.fetchall()
        finally:
            await db_r.close()

        rlines = []

        for r in recent:
            icon = TX_ICONS.get(r["type"], "•")
            disp = float(r["amount"] or 0)

            if r["type"] in ("withdraw", "transfer_out"):
                disp = -disp

            rlines.append(
                f"{icon} {money(disp)} — {esc(r['created_at'])[:16]}"
            )

        if rlines:
            info_text += (
                r6t(lang, "myinfo_recent") + "\n" + "\n".join(rlines)
            )

    b = InlineKeyboardBuilder()
    b.button(text=r6t(lang, "b_stats"), callback_data="menu_stats")
    b.button(text=r6t(lang, "b_transfer"), callback_data="svc_transfer")
    b.button(text=r6t(lang, "b_checkin"), callback_data="checkin")
    b.button(text=r6t(lang, "b_tickets"), callback_data="my_tickets")

    if await feat_on("bal_alert"):  # [R6-PLUS10 U36]
        b.button(
            text=tr(lang, "balalert_btn"),
            callback_data="balalert_set",
        )

    # [R6-PLUS2] النقاط وإخفاء الرصيد
    if user and (user["points"] or 0) > 0:
        b.button(text=r6t(lang, "points_btn"), callback_data="points_hub")

    if user:
        hide_btn = (
            r6t(lang, "show_bal_btn") if user["hide_balance"]
            else r6t(lang, "hide_bal_btn")
        )
        b.button(text=hide_btn, callback_data="myhide")
        b.button(  # [R6-PLUS3] الملخص الأسبوعي الشخصي
            text=r6t(
                lang,
                "digest_btn_on" if user["digest_enabled"]
                else "digest_btn_off",
            ),
            callback_data="mydigest",
        )

    # [R6-CH] زر تبديل اللغة أُزيل من هنا — يبقى في القائمة الرئيسية فقط
    b.button(text=r6t(lang, "back_main"), callback_data="back_to_main")
    b.adjust(1)

    if edit:
        await safe_edit(msg, info_text, b.as_markup())
    else:
        await msg.answer(info_text, reply_markup=b.as_markup())


@dp.callback_query(F.data == "menu_my_info")
async def menu_my_info(cb: types.CallbackQuery, state: FSMContext):
    """[R6] معلومات ملفي — بيانات 55bets + ميزاتنا المساندة."""

    if not await user_allowed(cb.from_user.id):
        await cb.answer("غير مسموح.", show_alert=True)
        return

    await cb.answer()
    await state.clear()
    await _render_my_info(cb.message, cb.from_user.id, edit=True)


@dp.callback_query(F.data == "mydigest")
async def mydigest_toggle(cb: types.CallbackQuery, state: FSMContext):
    """[R6-PLUS3] تشغيل/إيقاف الملخص الأسبوعي الشخصي."""

    if not await user_allowed(cb.from_user.id):
        await cb.answer("غير مسموح.", show_alert=True)
        return

    user = await get_user(cb.from_user.id)

    if user:
        await update_user(
            cb.from_user.id,
            digest_enabled=0 if user["digest_enabled"] else 1,
        )
        await cb.answer(
            "✅ ستصلك كل أحد."
            if not user["digest_enabled"] else "🔕 أُوقف الملخص.",
            show_alert=True,
        )

    await _render_my_info(cb.message, cb.from_user.id, edit=True)


async def digest_if_due():
    """[R6-PLUS3] الملخص الأسبوعي الشخصي — كل أحد بعد 09:00 UTC."""
    if not await feat_on("digest"):
        return

    now = datetime.now(timezone.utc)

    if now.weekday() != 6 or now.hour < 9:
        return

    today = f"{now:%Y-%m-%d}"

    if (await get_setting("last_digest_date") or "") == today:
        return

    start = (now - timedelta(days=7)).isoformat(timespec="seconds")
    await _digest_send_all(start)


async def _digest_send_all(start: str) -> int:
    """[R6-PLUS3] إرسال الملخص لكل المشتركين (منطق قابل للاختبار)."""
    db = await get_db()

    try:
        cur = await db.execute(
            "SELECT telegram_id, lang, id FROM users"
            " WHERE digest_enabled = 1 AND is_banned = 0"
            " AND COALESCE(ban_until, '') = '' LIMIT 100",
        )
        users = await cur.fetchall()
        sent = 0

        for u in users:
            cur2 = await db.execute(
                "SELECT COALESCE(SUM(CASE WHEN type = 'deposit' THEN"
                " amount ELSE 0 END), 0) AS dep,"
                " COALESCE(SUM(CASE WHEN type = 'withdraw' THEN"
                " amount ELSE 0 END), 0) AS wd,"
                " COALESCE(SUM(CASE WHEN type = 'points_earn' THEN"
                " amount ELSE 0 END), 0) AS pts"
                " FROM transactions WHERE user_id = ?"
                " AND created_at >= ?",
                (u["id"], start),
            )
            s = await cur2.fetchone()

            cur3 = await db.execute(
                "SELECT COUNT(*) + 1 AS rk FROM users w"
                " WHERE w.referrer_id IS NOT NULL"
                " GROUP BY w.referrer_id"
                " HAVING COUNT(*) > ("
                " SELECT COUNT(*) FROM users x"
                " WHERE x.referrer_id = ("
                " SELECT referrer_id FROM users WHERE id = ?)"
                " AND x.referrer_id IS NOT NULL)",
                (u["id"],),
            )
            rk_row = await cur3.fetchone()
            rank = f"#{rk_row['rk']}" if rk_row else "—"

            try:
                await bot.send_message(
                    u["telegram_id"],
                    r6t(u["lang"] or "ar", "digest_msg").format(
                        dep=money(s["dep"]),
                        wd=money(s["wd"]),
                        pts=int(s["pts"]),
                        rank=rank,
                    ),
                )
                sent += 1
            except Exception:
                continue
    finally:
        await db.close()

    logger.info("الملخص الأسبوعي الشخصي: أُرسل إلى %s مستخدماً.", sent)
    return sent


@dp.callback_query(F.data == "myhide")
async def myhide_toggle(cb: types.CallbackQuery, state: FSMContext):
    """[R6-PLUS2] إخفاء/إظهار الرصيد في صفحة ملفي."""

    if not await user_allowed(cb.from_user.id):
        await cb.answer("غير مسموح.", show_alert=True)
        return

    await cb.answer()
    await state.clear()

    user = await get_user(cb.from_user.id)

    if user:
        await update_user(
            cb.from_user.id,
            hide_balance=0 if user["hide_balance"] else 1,
        )

    await _render_my_info(cb.message, cb.from_user.id, edit=True)


@dp.callback_query(F.data == "points_hub")
async def points_hub(cb: types.CallbackQuery, state: FSMContext):
    """[R6-PLUS2] مركز استبدال نقاط الولاء."""

    if not await user_allowed(cb.from_user.id):
        await cb.answer("غير مسموح.", show_alert=True)
        return

    await cb.answer()
    await state.clear()

    user = await get_user(cb.from_user.id)
    pts = int(user["points"] or 0) if user else 0

    lang = await user_lang(cb.from_user.id)
    b = InlineKeyboardBuilder()

    for cost, reward in ((500, 5), (1000, 10), (2500, 25)):
        mark = "✅" if pts >= cost else "🔒"
        b.button(
            text=f"{mark} {cost} ⭐ → {money(reward)}",
            callback_data=f"predeem:{cost}:{reward}",
        )

    b.button(
        text=r6t(lang, "points_hist_btn"),
        callback_data="points_hist",
    )  # [R6-PLUS3]
    b.button(text=r6t(lang, "back_main"), callback_data="back_to_main")
    b.adjust(1)

    await safe_edit(
        cb.message,
        r6t(lang, "points_title").format(p=pts),
        b.as_markup(),
    )


@dp.callback_query(F.data == "points_hist")
async def points_hist(cb: types.CallbackQuery, state: FSMContext):
    """[R6-PLUS3] سجل كسب واستبدال النقاط."""

    if not await user_allowed(cb.from_user.id):
        await cb.answer("غير مسموح.", show_alert=True)
        return

    await cb.answer()
    await state.clear()

    lang = await user_lang(cb.from_user.id)

    db = await get_db()

    try:
        cur = await db.execute(
            "SELECT t.type, t.amount, t.created_at FROM transactions t"
            " JOIN users u ON u.id = t.user_id"
            " WHERE u.telegram_id = ?"
            " AND t.type IN ('points_earn', 'points_redeem')"
            " ORDER BY t.id DESC LIMIT 15",
            (cb.from_user.id,),
        )
        rows = await cur.fetchall()
    finally:
        await db.close()

    lines = [r6t(lang, "points_hist_title")]

    for r in rows:
        sign = "+" if r["type"] == "points_earn" else "−"
        badge = "🎯" if r["type"] == "points_earn" else "🛒"
        lines.append(
            f"{badge} {sign}{int(r['amount'])} ⭐ | "
            f"{esc(r['created_at'])[:16]}"
        )

    if not rows:
        lines.append("—")

    await safe_edit(
        cb.message, "\n".join(lines), back_kb("back_to_main", lang),
    )


@dp.callback_query(F.data.startswith("predeem:"))
async def points_redeem(cb: types.CallbackQuery, state: FSMContext):
    """[R6-PLUS2] استبدال ذري للنقاط برصيد."""

    if not await user_allowed(cb.from_user.id):
        await cb.answer("غير مسموح.", show_alert=True)
        return

    try:
        cost = int(cb.data.split(":")[1])
        reward = float(cb.data.split(":")[2])
    except (ValueError, IndexError):
        await cb.answer("خيار غير صالح.", show_alert=True)
        return

    lang = await user_lang(cb.from_user.id)
    db = await get_db()

    try:
        cur = await db.execute(
            "SELECT id, points FROM users WHERE telegram_id = ?",
            (cb.from_user.id,),
        )
        urow = await cur.fetchone()

        if not urow or (urow["points"] or 0) < cost:
            await cb.answer(r6t(lang, "points_low"), show_alert=True)
            return

        await db.execute(
            "UPDATE users SET points = points - ?,"
            " balance = balance + ? WHERE id = ?",
            (cost, reward, urow["id"]),
        )
        await db.execute(
            "INSERT INTO transactions"
            " (user_id, type, amount, note, created_at)"
            " VALUES (?, 'points_redeem', ?, ?, ?)",
            (urow["id"], reward, f"points={cost}", now_iso()),
        )
        await db.commit()
    finally:
        await db.close()

    await cb.answer(
        r6t(lang, "points_done").format(r=money(reward)),
        show_alert=True,
    )
    await points_hub(cb, state)


@dp.callback_query(F.data == "refs_top")
async def refs_top(cb: types.CallbackQuery, state: FSMContext):
    """[R6-PLUS2] صدارة الإحالات للمستخدمين."""

    if not await user_allowed(cb.from_user.id):
        await cb.answer("غير مسموح.", show_alert=True)
        return

    await cb.answer()
    await state.clear()
    lang = await user_lang(cb.from_user.id)

    db = await get_db()

    try:
        cur = await db.execute(
            "SELECT r.telegram_id AS tid, r.full_name AS fn,"
            " COUNT(*) AS c FROM users u"
            " JOIN users r ON r.telegram_id = u.referrer_id"
            " WHERE u.referrer_id IS NOT NULL"
            " GROUP BY u.referrer_id ORDER BY c DESC LIMIT 10",
        )
        rows = await cur.fetchall()
    finally:
        await db.close()

    lines = [r6t(lang, "refs_top_title")]
    my_rank = "—"

    for i, row in enumerate(rows, 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 \
            else f"{i}."
        name = row["fn"] or str(row["tid"])

        if row["tid"] == cb.from_user.id:
            my_rank = f"#{i}"
            lines.append(f"{medal} <b>{esc(name[:20])} — {row['c']}</b>")
        else:
            lines.append(f"{medal} {esc(name[:20])} — {row['c']}")

    lines.append(f"\n📍 ترتيبك: <b>{my_rank}</b>")

    b = InlineKeyboardBuilder()
    b.button(text=tr(lang, "back"), callback_data="my_refs")
    b.adjust(1)

    await safe_edit(cb.message, "\n".join(lines), b.as_markup())


@dp.callback_query(F.data == "calc_rev")
async def calc_rev(cb: types.CallbackQuery, state: FSMContext):
    """[R6-PLUS2] الحاسبة العكسية: أريد صافي كذا."""

    if not await user_allowed(cb.from_user.id):
        await cb.answer("غير مسموح.", show_alert=True)
        return

    if not await feat_on("rev_calc"):  # [R6-PLUS3]
        await cb.answer("الميزة معطلة حالياً.", show_alert=True)
        return

    await cb.answer()
    await state.clear()
    await state.set_state(CalcDepFSM.reverse)

    lang = await user_lang(cb.from_user.id)

    await cb.message.answer(
        r6t(lang, "calc_rev_prompt") + "\n\nللإلغاء أرسل /cancel",
        reply_markup=back_kb("back_to_recharge", lang),
    )


@dp.message(CalcDepFSM.reverse)
async def calc_rev_calc(message: types.Message, state: FSMContext):
    """[R6-PLUS2] حساب المبلغ المطلوب شحنه لصافٍ مطلوب."""

    if not await user_allowed(message.from_user.id, message):
        await state.clear()
        return

    lang = await user_lang(message.from_user.id)
    net = parse_amount(message.text)

    if net is None or net <= 0:
        await message.answer(
            "❌ أرسل مبلغاً صحيحاً أكبر من 0.\n\nللإلغاء أرسل /cancel"
        )
        return

    comm = await get_float_setting("commission_percent", 0.0)

    if comm >= 100:
        gross = net
        fee = 0.0
    else:
        gross = round2(net / (1 - comm / 100.0))
        fee = round2(gross - net)

    await state.clear()

    await message.answer(
        r6t(lang, "calc_rev_result").format(
            g=money(gross), c=money(fee), n=money(net),
        ),
        reply_markup=back_kb("back_to_recharge", lang),
    )


@dp.callback_query(F.data == "menu_contact_us")
async def menu_contact_us(cb: types.CallbackQuery, state: FSMContext):
    """[R6] تواصل معنا — نفس الأزرار + تذاكري."""

    if not await user_allowed(cb.from_user.id):
        await cb.answer("غير مسموح.", show_alert=True)
        return

    await cb.answer()
    await state.clear()

    lang = await user_lang(cb.from_user.id)
    b = InlineKeyboardBuilder()
    b.button(text=r6t(lang, "c_bot"), callback_data="support_bot_issue")
    b.button(text=r6t(lang, "c_site"), callback_data="support_site_issue")
    b.button(text=r6t(lang, "c_dev"), callback_data="contact_developer")
    b.button(text=r6t(lang, "back_main"), callback_data="back_to_main")
    b.adjust(1)
    await safe_edit(
        cb.message,
        r6t(lang, "contact_text"),
        b.as_markup(),
    )


@dp.callback_query(F.data == "support_bot_issue")
async def support_bot_issue(cb: types.CallbackQuery, state: FSMContext):
    """[R6] مشكلة ضمن البوت → تذكرة دعم حقيقية (NEW 38)."""
    await support_start(cb, state)


@dp.callback_query(F.data == "back_to_contact")
async def back_to_contact(cb: types.CallbackQuery, state: FSMContext):
    """[R6] رجوع لشاشة الجهات الفنية."""
    await menu_contact_us(cb, state)


@dp.callback_query(F.data == "support_site_issue")
async def support_site_issue(cb: types.CallbackQuery, state: FSMContext):
    """[R6] مشكلة الموقع — النص الأصلي."""

    if not await user_allowed(cb.from_user.id):
        await cb.answer("غير مسموح.", show_alert=True)
        return

    lang = await user_lang(cb.from_user.id)
    await cb.answer()
    await state.clear()
    await safe_edit(
        cb.message,
        r6t(lang, "site_issue_text"),
        back_kb("back_to_contact", lang),
    )


@dp.callback_query(F.data == "contact_developer")
async def contact_developer(cb: types.CallbackQuery, state: FSMContext):
    """[R6] المطور — النص الأصلي."""

    if not await user_allowed(cb.from_user.id):
        await cb.answer("غير مسموح.", show_alert=True)
        return

    await cb.answer()
    await state.clear()

    lang = await user_lang(cb.from_user.id)
    b = InlineKeyboardBuilder()
    b.button(text=r6t(lang, "dev_tg"), url="https://t.me/Hamooshii")
    b.button(
        text=r6t(lang, "back_contact"), callback_data="back_to_contact",
    )
    b.adjust(1)
    await safe_edit(
        cb.message,
        r6t(lang, "dev_text"),
        b.as_markup(),
    )


@dp.callback_query(F.data == "menu_share_happiness")
async def menu_share_happiness(cb: types.CallbackQuery, state: FSMContext):
    """[R6] شاركنا سعادتك — النص الأصلي + استلام الصور."""

    if not await user_allowed(cb.from_user.id):
        await cb.answer("غير مسموح.", show_alert=True)
        return

    lang = await user_lang(cb.from_user.id)
    await cb.answer()
    await state.clear()
    await state.set_state(ShareHappyFSM.media)
    await safe_edit(
        cb.message,
        r6t(lang, "share_text"),
        back_kb("back_to_main", lang),
    )


@dp.message(ShareHappyFSM.media)
async def share_happy_media(message: types.Message, state: FSMContext):
    """[R6] تمرير صور الإصابات للأدمن وغرفة المراقبة."""

    if not await user_allowed(message.from_user.id, message):
        return

    try:
        await message.copy_to(ADMIN_USER_ID)
    except Exception as exc:
        logger.warning("تعذر تمرير إصابة للأدمن: %s", exc)

    mirror_chat = (await get_setting("mirror_chat_id") or "").strip()

    if (mirror_chat.lstrip("-").isdigit()
            and int(mirror_chat) != ADMIN_USER_ID):
        try:
            await message.copy_to(int(mirror_chat))
        except Exception:
            pass

    lang = await user_lang(message.from_user.id)
    await state.clear()
    await message.answer(
        r6t(lang, "share_ok"),
        reply_markup=back_kb("back_to_main", lang),
    )


@dp.callback_query(F.data == "menu_tutorials")
async def menu_tutorials(cb: types.CallbackQuery, state: FSMContext):
    """[R6] الشروحات — نفس الأزرار الستة."""

    if not await user_allowed(cb.from_user.id):
        await cb.answer("غير مسموح.", show_alert=True)
        return

    await cb.answer()
    await state.clear()

    lang = await user_lang(cb.from_user.id)
    admin_text = await get_text("tutorials") or ""

    text = r6t(lang, "tut_title")

    if admin_text.strip():
        text += f"\n\n{admin_text.strip()}"

    b = InlineKeyboardBuilder()
    b.button(text=r6t(lang, "tut1_btn"), callback_data="tut_what_is_55bets")
    b.button(text=r6t(lang, "tut2_btn"), callback_data="tut_create_account")
    b.button(text=r6t(lang, "tut3_btn"), callback_data="tut_recharge_bot")
    b.button(text=r6t(lang, "tut4_btn"), callback_data="tut_charge_55bets")
    b.button(text=r6t(lang, "tut5_btn"), callback_data="tut_withdraw_55bets")
    b.button(text=r6t(lang, "tut6_btn"), callback_data="tut_withdraw_bot")
    b.button(text=r6t(lang, "tut_back"), callback_data="back_to_main")
    b.adjust(1)
    await safe_edit(cb.message, text, b.as_markup())


def _tut_kb(lang: str = "ar"):
    b = InlineKeyboardBuilder()
    b.button(text=r6t(lang, "tut_back"), callback_data="back_to_tutorials")
    b.adjust(1)
    return b.as_markup()


@dp.callback_query(F.data == "back_to_tutorials")
async def back_to_tutorials(cb: types.CallbackQuery, state: FSMContext):
    await menu_tutorials(cb, state)


@dp.callback_query(F.data == "tut_what_is_55bets")
async def tut_what_is_55bets(cb: types.CallbackQuery, state: FSMContext):
    """[R6] نص الشرح الأصلي."""

    if not await user_allowed(cb.from_user.id):
        await cb.answer("غير مسموح.", show_alert=True)
        return

    lang = await user_lang(cb.from_user.id)
    await cb.answer()
    await state.clear()
    await safe_edit(
        cb.message, r6t(lang, "tut1_body"), _tut_kb(lang),
    )


@dp.callback_query(F.data == "tut_create_account")
async def tut_create_account(cb: types.CallbackQuery, state: FSMContext):
    """[R6] نص الشرح الأصلي."""

    if not await user_allowed(cb.from_user.id):
        await cb.answer("غير مسموح.", show_alert=True)
        return

    lang = await user_lang(cb.from_user.id)
    await cb.answer()
    await state.clear()
    await safe_edit(
        cb.message, r6t(lang, "tut2_body"), _tut_kb(lang),
    )


@dp.callback_query(F.data == "tut_recharge_bot")
async def tut_recharge_bot(cb: types.CallbackQuery, state: FSMContext):
    """[R6] نص الشرح الأصلي."""

    if not await user_allowed(cb.from_user.id):
        await cb.answer("غير مسموح.", show_alert=True)
        return

    await cb.answer()
    await state.clear()
    lang = await user_lang(cb.from_user.id)
    await safe_edit(
        cb.message, r6t(lang, "tut3_body"), _tut_kb(lang),
    )


@dp.callback_query(F.data == "tut_charge_55bets")
async def tut_charge_55bets(cb: types.CallbackQuery, state: FSMContext):
    """[R6] نص الشرح الأصلي."""

    if not await user_allowed(cb.from_user.id):
        await cb.answer("غير مسموح.", show_alert=True)
        return

    await cb.answer()
    await state.clear()
    lang = await user_lang(cb.from_user.id)
    await safe_edit(
        cb.message, r6t(lang, "tut4_body"), _tut_kb(lang),
    )


@dp.callback_query(F.data == "tut_withdraw_55bets")
async def tut_withdraw_55bets(cb: types.CallbackQuery, state: FSMContext):
    """[R6] نص الشرح الأصلي."""

    if not await user_allowed(cb.from_user.id):
        await cb.answer("غير مسموح.", show_alert=True)
        return

    await cb.answer()
    await state.clear()
    lang = await user_lang(cb.from_user.id)
    await safe_edit(
        cb.message, r6t(lang, "tut5_body"), _tut_kb(lang),
    )


@dp.callback_query(F.data == "tut_withdraw_bot")
async def tut_withdraw_bot(cb: types.CallbackQuery, state: FSMContext):
    """[R6] نص الشرح الأصلي."""

    if not await user_allowed(cb.from_user.id):
        await cb.answer("غير مسموح.", show_alert=True)
        return

    await cb.answer()
    await state.clear()
    lang = await user_lang(cb.from_user.id)
    await safe_edit(
        cb.message, r6t(lang, "tut6_body"), _tut_kb(lang),
    )


@dp.callback_query(F.data == "menu_current_offers")
async def menu_current_offers(cb: types.CallbackQuery, state: FSMContext):
    """[R6] العروض — الإعلانات الحقيقية (ADM4-4) أو النص الأصلي."""

    if not await user_allowed(cb.from_user.id):
        await cb.answer("غير مسموح.", show_alert=True)
        return

    await cb.answer()
    await state.clear()

    now_str = now_iso()
    tid = cb.from_user.id

    db = await get_db()

    try:
        cur = await db.execute(
            "SELECT id, text, created_at, expires_at, photo_file_id"
            " FROM announcements"
            " WHERE expires_at > ? ORDER BY id DESC LIMIT 5",
            (now_str,),
        )
        rows = await cur.fetchall()

        for row in rows:
            await db.execute(
                "INSERT OR IGNORE INTO announcement_reads"
                " (announcement_id, telegram_id, read_at)"
                " VALUES (?, ?, ?)",
                (row["id"], tid, now_str),
            )
        await db.commit()
    finally:
        await db.close()

    admin_text = (await get_text("offers") or "").strip()

    lang = await user_lang(cb.from_user.id)
    header = r6t(lang, "offers_header")

    if rows:
        lines = [header + "\n"]
        photo_count = 0  # [R6-PLUS2]

        for row in rows:
            exp_badge = ""

            try:
                exp_dt = datetime.fromisoformat(row["expires_at"])
                days_left = (exp_dt - datetime.now(timezone.utc)).days

                if days_left <= 0:
                    exp_badge = " " + r6t(lang, "offer_exp_today")
                else:
                    exp_badge = " " + r6t(lang, "offer_exp_days").format(
                        d=days_left,
                    )
            except (ValueError, TypeError):
                exp_badge = ""

            block = (
                f"🗓 {esc(row['created_at'])[:10]}{exp_badge}\n"
                f"{row['text']}"
            )

            # [R6-PLUS2] إعلان بصورة — تُرسل قبل النص الموحد
            if row["photo_file_id"]:
                photo_count += 1

                try:
                    await cb.message.answer_photo(
                        row["photo_file_id"],
                        caption=block[:1024],
                    )
                except Exception:
                    lines.append("🖼\n" + block)
            else:
                lines.append(block)

        text = "\n\n".join(lines)

        if photo_count:
            text += f"\n\n🖼 ({photo_count})"
    elif admin_text:
        text = f"{header}\n\n{admin_text}"
    else:
        text = f"{header}\n\n{r6t(lang, 'offers_none')}"

    b = InlineKeyboardBuilder()

    user_b = await get_user(cb.from_user.id)
    subscribed = bool(user_b and user_b["ann_notify"]) if user_b else False
    b.button(
        text=r6t(lang, "bell_off" if subscribed else "bell_on"),
        callback_data="annbell",
    )  # [R6-PLUS3]
    b.button(text=tr(lang, "back"), callback_data="back_to_main")
    b.adjust(1)

    await safe_edit(cb.message, text, b.as_markup())


@dp.callback_query(F.data == "annbell")
async def annbell(cb: types.CallbackQuery, state: FSMContext):
    """[R6-PLUS3] اشتراك/إلغاء استلام الإعلانات الجديدة فوراً."""

    if not await user_allowed(cb.from_user.id):
        await cb.answer("غير مسموح.", show_alert=True)
        return

    user = await get_user(cb.from_user.id)
    subscribed = bool(user and user["ann_notify"])

    await update_user(cb.from_user.id, ann_notify=0 if subscribed else 1)

    lang = await user_lang(cb.from_user.id)
    await cb.answer(
        r6t(lang, "bell_unsub" if subscribed else "bell_sub"),
        show_alert=True,
    )

    b = InlineKeyboardBuilder()
    b.button(
        text=r6t(lang, "bell_on" if subscribed else "bell_off"),
        callback_data="annbell",
    )
    b.button(text=tr(lang, "back"), callback_data="back_to_main")
    b.adjust(1)

    await safe_edit(cb.message, cb.message.text or "", b.as_markup())


@dp.callback_query(F.data == "menu_terms")
async def menu_terms(cb: types.CallbackQuery, state: FSMContext):
    """[R6] الشروط — نص الأدمن (NEW 17) أو النص الأصلي."""

    if not await user_allowed(cb.from_user.id):
        await cb.answer("غير مسموح.", show_alert=True)
        return

    await cb.answer()
    await state.clear()

    lang = await user_lang(cb.from_user.id)
    admin_text = (await get_text("terms") or "").strip()

    if admin_text:
        text = f"{r6t(lang, 'terms_header')}\n\n{admin_text}"
    else:
        text = (
            f"{r6t(lang, 'terms_header')}\n\n"
            + r6t(lang, "terms_default")
        )

    await safe_edit(cb.message, text, back_kb("back_to_main", lang))


@dp.callback_query(F.data == "back_to_main")
async def back_to_main(cb: types.CallbackQuery, state: FSMContext):
    """[R6] رجوع أصلي للقائمة الرئيسية."""

    if not await user_allowed(cb.from_user.id):
        await cb.answer("البوت متوقف أو الحساب محظور.", show_alert=True)
        return

    await cb.answer()
    await state.clear()
    await send_55bets_main(cb.message, cb.from_user.id, edit=True)


# ------------------------------------------------------------
# [R6] لوحة الأدمن — نفس قائمة الواجهة الأصلية موصولة بمحركنا
# ------------------------------------------------------------

def get_admin_home_kb():
    """[R6] لوحة الأدمن — نفس أزرار الواجهة الأصلية وترتيبها."""
    b = InlineKeyboardBuilder()
    b.button(text="👥 إدارة المستخدمين", callback_data="admin_manage_users")
    b.button(text="🤖 إدارة البوت", callback_data="admin_manage_bot")
    b.button(text="⚙️ إدارة شام كاش", callback_data="admin_manage_sham")
    b.button(text="📱 إدارة سيرياتل كاش",
             callback_data="admin_manage_syriatel")  # [MENU-ORG] بجانب شام
    b.button(text="💳 إدارة الشحن والعروض",
             callback_data="admin_manage_recharge")
    b.button(text="🏦 أرصدة المحافظ", callback_data="admin_wallets_balance")
    b.button(text="📈 الإحصائيات", callback_data="admin_statistics")  # [DEDUP 5.18.5] توحيد
    b.button(text="📅 تقرير مخصص", callback_data="admin_custom_report")
    b.button(text="🎛 تفعيل الميزات",
             callback_data="features_hub")  # [PANELHUB 5.18.14]
    b.button(text="⚙️ الإعدادات والأدوات",
             callback_data="admin_settings_menu")  # [SETTOOLS 5.18.13]
    b.button(text="↩️ رجوع للقائمة الرئيسية", callback_data="back_to_main")
    b.adjust(2, 2, 2, 2, 2, 1)  # [PANELHUB 5.18.14] الميزات والإعدادات باللوحة
    return b.as_markup()


@dp.callback_query(F.data == "admin_home")
async def admin_home(cb: types.CallbackQuery, state: FSMContext):
    """[R6] لوحة الأدمن الرئيسية بواجهة المشروع الأصلي."""

    if not await is_admin_or_supervisor(cb.from_user.id):
        await cb.answer("⚠️ هذه اللوحة مخصصة للأدمن فقط!", show_alert=True)
        return

    await cb.answer()
    await state.clear()
    await safe_edit(
        cb.message,
        "👑 <b>مرحباً بك في لوحة تحكم الأدمن:</b>",
        get_admin_home_kb(),
    )




async def admin_manage_bot_kb():
    """[PANELHUB 5.18.14] إدارة البوت بعد دمج محتويات «اللوحة الكاملة».

    العمليات التشغيلية ثم أقسام الإدارة (الطابور بعدادات حية عند
    تفعيل live_counters).
    """
    active = await is_bot_active()
    m_icon = "🔴" if not active else "🟢"

    b = InlineKeyboardBuilder()
    b.button(text=f"{m_icon} إيقاف للصيانة / تشغيل",
             callback_data="toggle_maintenance")
    b.button(text="🟢 نظام الـ API: تلقائي (V2 ثم V1)",
             callback_data="toggle_api_system")
    b.button(text="💰 دفع مكافآت الإحالة الدورية",
             callback_data="pay_referral_rewards")
    b.button(text="📣 نشر القنوات والمجموعات",
             callback_data="admin_chpost")  # [R6-CH]
    b.button(text="⏰ تذكير الطلبات العالقة",
             callback_data="admin_stale")  # [R6-PLUS2]
    b.button(text="⭐ آخر التقييمات",
             callback_data="admin_rates")  # [R6-PLUS3]

    # [PANELHUB 5.18.14] أقسام «اللوحة الكاملة» المنقولة
    if await feat_on("live_counters"):
        db = await get_db()
        try:
            cur = await db.execute(
                "SELECT COUNT(*) AS c FROM finance_requests"
                " WHERE status = 'pending'",
            )
            fin = (await cur.fetchone())["c"]
            cur = await db.execute(
                "SELECT COUNT(*) AS c FROM support_tickets"
                " WHERE status = 'open'",
            )
            tkt = (await cur.fetchone())["c"]
        finally:
            await db.close()
        b.button(text=f"🧾 الطابور الموحد ({fin + tkt})",
                 callback_data="admin_inbox")
        b.button(text=f"💳 المالية ({fin})", callback_data="admin_finance")
    else:
        b.button(text="🧾 الطابور الموحد", callback_data="admin_inbox")
        b.button(text="💳 المالية", callback_data="admin_finance")
    b.button(text="🎁 الهدايا", callback_data="admin_gifts")
    b.button(text="🛡 المشرفون", callback_data="admin_supervisors")
    b.button(text="📈 إحصائيات", callback_data="admin_statistics")
    b.button(text="📊 KPI حي", callback_data="admin_kpi")  # [NEW 42]
    b.button(text="📥 التقارير", callback_data="admin_reports")  # [NEW 14]
    b.button(text="↩️ رجوع", callback_data="admin_home")
    b.adjust(2, 2, 2, 1, 2, 2, 1, 1)  # [USERDUP 5.18.15] بلا المستخدمين (مكرر)
    return b.as_markup()


@dp.callback_query(F.data == "admin_manage_bot")
async def admin_manage_bot(cb: types.CallbackQuery, state: FSMContext):
    """[R6] إدارة البوت — نفس الأزرار الأصلية موصولة بالإعدادات الحية."""

    if not await is_admin_or_supervisor(cb.from_user.id, "all"):
        await cb.answer("⚠️ للأدمن فقط!", show_alert=True)
        return

    await cb.answer()
    await state.clear()

    markup = await admin_manage_bot_kb()  # [PANELHUB 5.18.14]
    await safe_edit(
        cb.message,
        "🤖 <b>إدارة البوت:</b>\n\nاختر الخيار المطلوب لتعديل الإعدادات:",
        markup,
    )


async def admin_manage_bot_render(cb: types.CallbackQuery):
    markup = await admin_manage_bot_kb()  # [PANELHUB 5.18.14]
    await safe_edit(
        cb.message,
        "🤖 <b>إدارة البوت:</b>\n\nاختر الخيار المطلوب لتعديل الإعدادات:",
        markup,
    )


@dp.callback_query(F.data == "toggle_maint_scope")
async def toggle_maint_scope(cb: types.CallbackQuery, state: FSMContext):
    """[R6-PLUS7 E4] نطاق الصيانة: إيقاف كامل أو المالية فقط."""

    if cb.from_user.id != ADMIN_USER_ID:
        await cb.answer("للأدمن الرئيسي فقط.", show_alert=True)
        return

    cur = (await get_setting("maintenance_scope") or "all").strip()
    new = "finance" if cur == "all" else "all"
    await set_setting("maintenance_scope", new)

    label = "العمليات المالية فقط 🟡" if new == "finance" \
        else "إيقاف كامل 🔴"
    await cb.answer(f"نطاق الصيانة: {label}", show_alert=True)
    await audit(cb.from_user.id, "maint_scope", "", f"scope={new}")


@dp.callback_query(F.data == "toggle_maintenance")
async def toggle_maintenance_r6(cb: types.CallbackQuery, state: FSMContext):
    """[R6] صيانة — موصولة بإيقاف البوت الحقيقي."""

    if not await is_admin_or_supervisor(cb.from_user.id, "all"):
        await cb.answer("⚠️ للأدمن فقط!", show_alert=True)
        return

    current = await is_bot_active()
    await set_setting("bot_active", "0" if current else "1")

    status = "متوقف للصيانة 🔴" if current else "يعمل بنجاح 🟢"
    await cb.answer(f"حالة البوت الان: {status}", show_alert=True)
    await audit(  # [NEW 22]
        cb.from_user.id, "maintenance_toggle", "",
        f"active={not current}",
    )
    await admin_manage_bot_render(cb)


@dp.callback_query(F.data == "toggle_syriatel_auto")
async def toggle_syriatel_auto(cb: types.CallbackQuery, state: FSMContext):
    """[R6] تشغيل/إيقاف الشحن الآلي لسيرياتيل."""

    if not await is_admin_or_supervisor(cb.from_user.id, "all"):
        await cb.answer("⚠️ للأدمن فقط!", show_alert=True)
        return

    current = (await get_setting("accept_syriatel") or "1") == "1"
    await set_setting("accept_syriatel", "0" if current else "1")
    status = "مفعل 🟢" if not current else "معطل 🔴"
    await cb.answer(f"شحن سيرياتيل أوتو: {status}", show_alert=True)
    await audit(  # [NEW 22]
        cb.from_user.id, "method_toggle", "syriatel",
        f"enabled={not current}",
    )
    await admin_manage_bot_render(cb)


@dp.callback_query(F.data == "toggle_sham_auto")
async def toggle_sham_auto(cb: types.CallbackQuery, state: FSMContext):
    """[R6] تشغيل/إيقاف الشحن الآلي لشام كاش."""

    if not await is_admin_or_supervisor(cb.from_user.id, "all"):
        await cb.answer("⚠️ للأدمن فقط!", show_alert=True)
        return

    current = (await get_setting("accept_sham") or "1") == "1"
    await set_setting("accept_sham", "0" if current else "1")
    status = "مفعل 🟢" if not current else "معطل 🔴"
    await cb.answer(f"شحن شام كاش أوتو: {status}", show_alert=True)
    await audit(  # [NEW 22]
        cb.from_user.id, "method_toggle", "sham",
        f"enabled={not current}",
    )
    await admin_manage_bot_render(cb)


@dp.callback_query(F.data == "toggle_api_system")
async def toggle_api_system(cb: types.CallbackQuery, state: FSMContext):
    """[R6] حالة نظام الاستقبال الآلي (Webhook)."""

    if not await is_admin_or_supervisor(cb.from_user.id, "all"):
        await cb.answer("⚠️ للأدمن فقط!", show_alert=True)
        return

    day_ago = (
        datetime.now(timezone.utc) - timedelta(days=1)
    ).isoformat(timespec="seconds")

    db = await get_db()

    try:
        cur = await db.execute(
            "SELECT COUNT(*) AS c FROM webhook_events WHERE created_at >= ?",
            (day_ago,),
        )
        events = (await cur.fetchone())["c"]
        cur = await db.execute(
            "SELECT COUNT(*) AS c FROM webhook_events"
            " WHERE result = 'credited'",
        )
        credited = (await cur.fetchone())["c"]
    finally:
        await db.close()

    await cb.answer(
        f"نظام الـ API مفعل تلقائياً (V2 ثم V1)\n"
        f"آخر 24س: {events} حدث | إجمالي الشحن الآلي: {credited}",
        show_alert=True,
    )


@dp.callback_query(F.data == "pay_referral_rewards")
async def pay_referral_rewards(cb: types.CallbackQuery, state: FSMContext):
    """[R6] مكافآت الإحالة — تُدفع تلقائياً ونعرض إحصاءها."""

    if not await is_admin_or_supervisor(cb.from_user.id, "finance"):
        await cb.answer("⚠️ للأدمن فقط!", show_alert=True)
        return

    db = await get_db()

    try:
        cur = await db.execute(
            "SELECT COUNT(DISTINCT referrer_id) AS c FROM users"
            " WHERE referrer_id IS NOT NULL AND referrer_id != 0",
        )
        referrers = (await cur.fetchone())["c"]
        cur = await db.execute(
            "SELECT COALESCE(SUM(amount), 0) AS s FROM transactions"
            " WHERE type = 'referral'",
        )
        paid_total = round2((await cur.fetchone())["s"])
    finally:
        await db.close()

    await safe_edit(
        cb.message,
        "💰 <b>دفع مكافآت الإحالة الدورية:</b>\n\n"
        "المكافآت تُدفع تلقائياً وفورياً عند كل شحن مؤهل.\n\n"
        f"👥 عدد المُحيلين: <code>{referrers}</code>\n"
        f"💵 إجمالي ما دُفع: <code>{money(paid_total)}</code>",
        InlineKeyboardBuilder()
        .button(text="⚙️ إعدادات النظام", callback_data="referral_settings")
        .button(text="↩️ رجوع", callback_data="admin_manage_bot")
        .adjust(1)
        .as_markup(),
    )


@dp.callback_query(F.data == "referral_settings")
async def referral_settings_r6(cb: types.CallbackQuery, state: FSMContext):
    """[R6] إعدادات الإحالة → لوحتنا الحقيقية (NEW 29)."""
    await admin_refbonus(cb, state)


@dp.callback_query(F.data == "syriatel_manual_codes")
async def syriatel_manual_codes(cb: types.CallbackQuery, state: FSMContext):
    """[MENU-ORG] أصبح = تغيير رقم الإيداع (توحيد بلا تكرار)."""
    await change_syriatel_deposit_acc(cb, state)


@dp.callback_query(F.data == "change_sham_deposit_acc")
async def change_sham_deposit_acc(cb: types.CallbackQuery, state: FSMContext):
    """[R6] رقم حساب شام كاش المعروض للمستخدمين."""

    if not await is_admin_or_supervisor(cb.from_user.id, "all"):
        await cb.answer("⚠️ للأدمن فقط!", show_alert=True)
        return

    await cb.answer()
    await state.clear()
    await state.update_data(wallet_key="sham")
    await state.set_state(AdminWalletFSM.value)

    current = await _wallet_number("sham")
    await cb.message.answer(
        "🔄 <b>تغيير حساب الإيداع لـ شام كاش:</b>\n\n"
        "أرسل الرقم / المعرف الجديد الذي سيظهر للمستخدمين:\n"
        f"الحالي: <code>{esc(current)}</code>\n"
        "للإلغاء أرسل /cancel",
     reply_markup=back_kb("admin_manage_bot"))


@dp.callback_query(F.data == "toggle_sham_mode")
async def toggle_sham_mode(cb: types.CallbackQuery, state: FSMContext):
    """[R6-PLUS4] الأدمن يختار ما يظهر للمستخدم: محفظة أو رمز حساب."""

    if not await is_admin_or_supervisor(cb.from_user.id, "all"):
        await cb.answer("⚠️ للأدمن فقط!", show_alert=True)
        return

    mode = (await get_setting("sham_code_mode") or "wallet") == "code"
    new_mode = "wallet" if mode else "code"
    await set_setting("sham_code_mode", new_mode)
    await audit(cb.from_user.id, "sham_mode", "", new_mode)
    await cb.answer(
        "🔣 سيرى المستخدم رمز الحساب" if new_mode == "code"
        else "💳 سيرى المستخدم رقم المحفظة",
        show_alert=True,
    )
    await admin_manage_sham(cb, state)  # إعادة رسم الشاشة


@dp.callback_query(F.data == "change_sham_code_acc")
async def change_sham_code_acc(cb: types.CallbackQuery, state: FSMContext):
    """[R6-PLUS3] رمز حساب شام كاش المعروض للمستخدمين."""

    if not await is_admin_or_supervisor(cb.from_user.id, "all"):
        await cb.answer("⚠️ للأدمن فقط!", show_alert=True)
        return

    await cb.answer()
    await state.clear()
    await state.update_data(wallet_key="sham_code")
    await state.set_state(AdminWalletFSM.value)

    current = (await get_setting("sham_account_code") or "").strip()

    await cb.message.answer(
        "🔣 <b>رمز حساب شام كاش (طريقة الشحن الجديدة):</b>\n\n"
        "أرسل الرمز الذي سيظهر للمستخدمين بشاشة «شام كاش — رمز حساب»:\n"
        f"الحالي: <code>{esc(current or '—')}</code>\n"
        "للإلغاء أرسل /cancel",
        reply_markup=back_kb("admin_manage_sham"),
    )


# ------------------------------------------------------------
# [R6-CH] إدارة القناة/المجموعة + النشر المجدول الدوري
# ------------------------------------------------------------

@dp.callback_query(F.data == "admin_rates")
async def admin_rates(cb: types.CallbackQuery, state: FSMContext):
    """[R6-PLUS3] آخر تقييمات السحب ⭐ للفريق المالي."""

    if not await is_admin_or_supervisor(cb.from_user.id, "reports"):
        await cb.answer("غير مصرّح.", show_alert=True)
        return

    await cb.answer()
    await state.clear()

    db = await get_db()

    try:
        cur = await db.execute(
            "SELECT r.stars, r.created_at, r.telegram_id,"
            " p.amount FROM payout_ratings r"
            " LEFT JOIN payouts p ON p.id = r.payout_id"
            " ORDER BY r.created_at DESC LIMIT 20",
        )
        rows = await cur.fetchall()

        cur = await db.execute(
            "SELECT COALESCE(AVG(stars), 0) AS a FROM payout_ratings"
            " WHERE created_at >= ?",
            (
                (
                    datetime.now(timezone.utc) - timedelta(days=7)
                ).isoformat(timespec="seconds"),
            ),
        )
        avg7 = (await cur.fetchone())["a"]
    finally:
        await db.close()

    lines = [
        "⭐ <b>آخر تقييمات السحب</b>",
        f"متوسط 7 أيام: <b>{avg7:.2f}/5</b> ({len(rows)} حديثة)\n",
    ]

    icons = {5: "⭐⭐⭐⭐⭐", 4: "⭐⭐⭐⭐", 3: "⭐⭐⭐",
             2: "⭐⭐", 1: "⭐"}

    for r in rows:
        amt = f" | {money(r['amount'])}" if r["amount"] else ""
        lines.append(
            f"{icons.get(r['stars'], '⭐')} | "
            f"<code>{r['telegram_id']}</code>{amt}\n"
            f"   🕐 {esc(r['created_at'])[:16]}"
        )

    if not rows:
        lines.append("لا توجد تقييمات بعد.")

    b = InlineKeyboardBuilder()
    b.button(text="🚀 المدفوعات", callback_data="admin_payouts")
    b.button(text="🔙 رجوع", callback_data="admin_manage_bot")
    b.adjust(1)

    await safe_edit(cb.message, "\n".join(lines), b.as_markup())


@dp.callback_query(F.data == "admin_destmatch")
async def admin_destmatch(cb: types.CallbackQuery, state: FSMContext):
    """[R6-PLUS2] وجهات السحب المستخدمة من أكثر من حساب."""

    if not await is_admin_or_supervisor(cb.from_user.id, "users"):
        await cb.answer("غير مصرّح.", show_alert=True)
        return

    await cb.answer()
    await state.clear()

    db = await get_db()

    try:
        cur = await db.execute(
            "SELECT destination, GROUP_CONCAT(DISTINCT user_tid) AS tids,"
            " COUNT(DISTINCT user_tid) AS n"
            " FROM payouts WHERE destination != ''"
            " GROUP BY destination HAVING n > 1"
            " ORDER BY MAX(id) DESC LIMIT 15",
        )
        rows = await cur.fetchall()
    finally:
        await db.close()

    if not rows:
        text = "✅ لا توجد وجهات مشتركة بين حسابات — كل شيء نظيف."
    else:
        lines = ["🕵️ <b>وجهات مستخدمة من أكثر من حساب</b>\n"]

        for row in rows:
            lines.append(
                f"🏦 <code>{esc(row['destination'])}</code> — "
                f"{row['n']} حسابات: {esc(row['tids'])}"
            )

        text = "\n\n".join(lines)

        text += (
            "\n\n💡 للحظر: أرسل معرف المستخدم في «حظر / فك الحظر»."
        )

    b = InlineKeyboardBuilder()
    b.button(
        text=("🔴 حجب الوجهة تلقائياً: ✅" if
              (await get_setting("dest_block") or "0") == "1"
              else "🟢 حجب الوجهة تلقائياً: ❌"),
        callback_data="toggle_destblock",
    )
    b.button(text="🔙 رجوع", callback_data="admin_users")
    b.adjust(1)

    await safe_edit(cb.message, text, b.as_markup())


@dp.callback_query(F.data == "toggle_destblock")
async def toggle_destblock(cb: types.CallbackQuery, state: FSMContext):

    if not await is_admin_or_supervisor(cb.from_user.id, "users"):
        await cb.answer("غير مصرّح.", show_alert=True)
        return

    current = (await get_setting("dest_block") or "0") == "1"
    await set_setting("dest_block", "0" if current else "1")
    await audit(cb.from_user.id, "dest_block",
                "on" if not current else "off")
    await admin_destmatch(cb, state)


@dp.callback_query(F.data == "sup_report")
async def sup_report(cb: types.CallbackQuery, state: FSMContext):
    """[R6-PLUS2] نشاط المشرفين هذا الشهر من سجل التدقيق."""

    if cb.from_user.id != ADMIN_USER_ID:
        await cb.answer("للأدمن الرئيسي فقط.", show_alert=True)
        return

    await cb.answer()
    await state.clear()

    month = now_iso()[:7]

    db = await get_db()

    try:
        cur = await db.execute(
            "SELECT admin_id, COUNT(*) AS c FROM admin_audit"
            " WHERE action = 'fin_approve' AND created_at LIKE ?"
            " GROUP BY admin_id ORDER BY c DESC",
            (month + "%",),
        )
        rows = await cur.fetchall()
    finally:
        await db.close()

    if not rows:
        text = "📭 لا نشاط اعتماد مسجل هذا الشهر."
    else:
        lines = [f"📊 <b>اعتمادات المشرفين — {month}</b>\n"]

        for row in rows:
            lines.append(
                f"🛡 <code>{row['admin_id']}</code>: {row['c']} اعتماد"
            )

        text = "\n".join(lines)

    await safe_edit(cb.message, text, back_kb("admin_supervisors"))


@dp.callback_query(F.data.startswith("tban:"))
async def tban_set(cb: types.CallbackQuery, state: FSMContext):
    """[R6-PLUS3] حظر مؤقت بمُدة — فك تلقائي بانتهاء المدة."""

    if not await is_admin_or_supervisor(cb.from_user.id, "users"):
        await cb.answer("غير مصرّح.", show_alert=True)
        return

    try:
        tid = int(cb.data.split(":")[1])
    except (ValueError, IndexError):
        await cb.answer("معرف غير صالح.", show_alert=True)
        return

    await cb.answer()
    await state.clear()
    await state.set_state(AdminTempBanFSM.days)
    await state.update_data(tban_tid=tid)

    user = await get_user(tid)
    current = ""

    if user and user["ban_until"]:
        try:
            if datetime.fromisoformat(user["ban_until"]) > \
                    datetime.now(timezone.utc):
                current = user["ban_until"][:16]
        except (ValueError, TypeError):
            pass

    await cb.message.answer(
        "⏳ <b>حظر مؤقت</b>\n\n"
        f"المستخدم: <code>{tid}</code>\n"
        + (f"محظور حالياً حتى: {esc(current)} UTC\n" if current else "")
        + "أرسل عدد الأيام (1-365)، أو 0 لإلغاء الحظر المؤقت:"
        "\n\nللإلغاء أرسل /cancel",
        reply_markup=back_kb("admin_users"),
    )


@dp.message(AdminTempBanFSM.days)
async def tban_days(message: types.Message, state: FSMContext):
    """[R6-PLUS3] حفظ مدة الحظر المؤقت."""

    if not await is_admin_or_supervisor(message.from_user.id, "users"):
        await state.clear()
        return

    raw = (message.text or "").strip()

    try:
        days = int(raw)
    except ValueError:
        await message.answer("❌ أرسل رقماً من 0 إلى 365.")
        return

    if not (0 <= days <= 365):
        await message.answer("❌ المدة من 0 إلى 365 يوماً.")
        return

    data = await state.get_data()
    tid = data.get("tban_tid")

    await state.clear()

    if not tid:
        await message.answer("انتهت الجلسة.")
        return

    if days == 0:
        await update_user(tid, ban_until=None)
        await message.answer(f"✅ أُلغي الحظر المؤقت عن <code>{tid}</code>.")
    else:
        until = (
            datetime.now(timezone.utc) + timedelta(days=days)
        ).isoformat(timespec="seconds")
        await update_user(tid, ban_until=until)
        await message.answer(
            f"⏳ حُظر <code>{tid}</code> مؤقتاً حتى\n"
            f"<code>{until[:16]}</code> UTC"
            f" ({days} يوماً) — يُفك تلقائياً."
        )

    await audit(message.from_user.id, "temp_ban", tid, f"days={days}")


@dp.callback_query(F.data.startswith("ucap:"))
async def ucap_set(cb: types.CallbackQuery, state: FSMContext):
    """[R6-PLUS2] سقف سحب يومي خاص بمستخدم."""

    if not await is_admin_or_supervisor(cb.from_user.id, "users"):
        await cb.answer("غير مصرّح.", show_alert=True)
        return

    try:
        tid = int(cb.data.split(":")[1])
    except (ValueError, IndexError):
        await cb.answer("معرف غير صالح.", show_alert=True)
        return

    await cb.answer()
    await state.clear()
    await state.set_state(AdminUserCapFSM.value)
    await state.update_data(cap_tid=tid)

    db = await get_db()

    try:
        cur = await db.execute(
            "SELECT wd_daily_cap FROM users WHERE telegram_id = ?",
            (tid,),
        )
        row = await cur.fetchone()
    finally:
        await db.close()

    current = float(row["wd_daily_cap"] or 0) if row else 0.0

    await cb.message.answer(
        f"🎚 <b>سقف السحب اليومي الخاص</b>\n"
        f"المستخدم: <code>{tid}</code>\n\n"
        f"الحالي: <b>{current:g}</b> (0 = استخدام السقف العام)\n"
        "أرسل القيمة الجديدة:\n\nللإلغاء أرسل /cancel",
        reply_markup=back_kb(f"admin_user_card:{tid}"),
    )


@dp.message(AdminUserCapFSM.value)
async def ucap_save(message: types.Message, state: FSMContext):

    if not await is_admin_or_supervisor(message.from_user.id, "users"):
        await state.clear()
        return

    try:
        val = float((message.text or "").strip().replace(",", "."))

        if not (0 <= val <= 1_000_000) or not math.isfinite(val):
            raise ValueError
    except Exception:
        await message.answer(
            "❌ أرسل رقماً صحيحاً (0 = السقف العام).\n\n"
            "للإلغاء أرسل /cancel"
        )
        return

    data = await state.get_data()
    tid = data.get("cap_tid")
    await state.clear()

    if not tid:
        return

    await update_user(tid, wd_daily_cap=val)
    await audit(message.from_user.id, "user_cap", tid, f"{val:g}")

    await message.answer(
        f"✅ سقف السحب الخاص بـ <code>{tid}</code> أصبح <b>{val:g}</b>.",
        reply_markup=back_kb(f"admin_user_card:{tid}"),
    )


@dp.callback_query(F.data == "admin_stale")
async def admin_stale(cb: types.CallbackQuery, state: FSMContext):
    """[R6-PLUS2] ضبط تذكير الطلبات العالقة."""

    if not await is_admin_or_supervisor(cb.from_user.id, "all"):
        await cb.answer("⚠️ للأدمن فقط!", show_alert=True)
        return

    await cb.answer()
    await state.clear()
    await state.set_state(AdminStaleFSM.value)

    current = await get_float_setting("pending_alert_hours", 6.0)

    await cb.message.answer(
        "⏰ <b>تذكير الطلبات العالقة</b>\n\n"
        f"الحالي: يذكّر بعد <b>{current:g} ساعة</b> من كل طلب معلق"
        " (كل 12 ساعة حتى المعالجة)\n"
        "أرسل عدد الساعات (0 = تعطيل، حتى 168):\n\n"
        "للإلغاء أرسل /cancel",
        reply_markup=back_kb("admin_manage_bot"),
    )


@dp.message(AdminStaleFSM.value)
async def admin_stale_save(message: types.Message, state: FSMContext):

    if not await is_admin_or_supervisor(message.from_user.id, "all"):
        await state.clear()
        return

    try:
        val = float((message.text or "").strip())

        if not (0 <= val <= 168) or not math.isfinite(val):
            raise ValueError
    except Exception:
        await message.answer(
            "❌ أرسل عدد ساعات صحيح (0 إلى 168).\n\nللإلغاء أرسل /cancel"
        )
        return

    await set_setting("pending_alert_hours", str(round(val, 1)))
    await state.clear()
    await audit(message.from_user.id, "stale_alert", f"{val:g}h")

    await message.answer(
        f"✅ التذكير أصبح بعد <b>{val:g} ساعة</b>.",
        reply_markup=back_kb("admin_manage_bot"),
    )


@dp.callback_query(F.data == "toggle_winback")
async def toggle_winback(cb: types.CallbackQuery, state: FSMContext):
    """[R6-PLUS2] تشغيل/إيقاف رسالة الرجوع للغائبين."""

    if not await is_admin_or_supervisor(cb.from_user.id, "all"):
        await cb.answer("⚠️ للأدمن فقط!", show_alert=True)
        return

    current = await feat_on("winback")  # [R6-PLUS3]
    await set_setting("feat_winback", "0" if current else "1")
    await audit(cb.from_user.id, "winback",
                "on" if not current else "off")
    await cb.answer(
        "✅ رسالة الرجوع مفعّلة" if not current
        else "⛔ رسالة الرجوع معطلة",
        show_alert=True,
    )
    await admin_manage_bot_render(cb)


@dp.callback_query(F.data == "admin_chpost")
async def admin_chpost(cb: types.CallbackQuery, state: FSMContext):
    """[R6-CH] شاشة إدارة النشر على القنوات والمجموعات."""

    if not await is_admin_or_supervisor(cb.from_user.id, "all"):
        await cb.answer("⚠️ للأدمن فقط!", show_alert=True)
        return

    await cb.answer()
    await state.clear()

    db = await get_db()

    try:
        cur = await db.execute("SELECT * FROM channel_posts ORDER BY id")
        rows = await cur.fetchall()
    finally:
        await db.close()

    channel = (await get_setting("channel_chat_id") or "").strip()

    b = InlineKeyboardBuilder()
    b.button(text="📣 تعيين/تغيير القناة أو المجموعة",
             callback_data="chp_set_chat")
    b.button(text="🧪 اختبار النشر الآن", callback_data="chp_test")
    b.button(text="➕ جدولة: آخر إعلان فعّال",
             callback_data="chp_new:announcement")
    b.button(text="➕ جدولة: نص مخصص", callback_data="chp_new:custom")
    b.button(text="➕ جدولة: تقرير يومي",
             callback_data="chp_new:daily_report")

    for row in rows:
        mark = "✅" if row["enabled"] else "⛔"
        label = _chp_kind_label(row["kind"])

        if row["interval_hours"]:
            when = f"كل {row['interval_hours']:g}س"
        elif row["at_time"]:
            when = f"يومياً {row['at_time']}"
        else:
            when = ""

        b.button(
            text=f"{mark} {label} {when}".rstrip(),
            callback_data=f"chp_toggle:{row['id']}",
        )
        b.button(text="🗑", callback_data=f"chp_del:{row['id']}")
        b.button(text="▶️ انشر الآن", callback_data=f"chp_now:{row['id']}")

    b.button(text="↩️ رجوع", callback_data="admin_manage_bot")

    sizes = [1] * 5

    for _ in rows:
        sizes += [2, 1]

    sizes.append(1)
    b.adjust(*sizes)

    await safe_edit(
        cb.message,
        "📣 <b>النشر على القنوات والمجموعات</b>\n\n"
        f"القناة الحالية: "
        f"<code>{esc(channel or '— لم تُحدد بعد')}</code>\n\n"
        "📝 <b>المعرّف الصحيح</b>: عام → @الاسم أو رابط t.me\n"
        "خاص → الرقم <code>-100…</code> (أعد توجيه منشوراً إلى "
        "<code>@getidsbot</code> لمعرفته)\n"
        "⚠️ أضف البوت مشرفاً بصلاحية النشر أولاً،\n"
        "ثم عيّن القناة وجدول المنشورات:",
        b.as_markup(),
    )


@dp.callback_query(F.data == "chp_set_chat")
async def chp_set_chat(cb: types.CallbackQuery, state: FSMContext):
    """[R6-CH] تعيين قناة/مجموعة النشر."""

    if not await is_admin_or_supervisor(cb.from_user.id, "all"):
        await cb.answer("⚠️ للأدمن فقط!", show_alert=True)
        return

    await cb.answer()
    await state.clear()
    await state.set_state(AdminChPostFSM.chat)

    await cb.message.answer(
        "📣 أرسل معرف القناة أو المجموعة:\n"
        "مثال: <code>@my_channel</code> أو <code>-1001234567890</code>\n"
        "أو الرابط العام: <code>t.me/my_channel</code>\n\n"
        "⚠️ روابط الدعوة الخاصة (<code>t.me/+…</code>) لا تكفي"
        " كمعرّف — الخاصة تحتاج الرقم.\n"
        "⚠️ أضف البوت مشرفاً فيها بصلاحية النشر أولاً.\n"
        "للإلغاء أرسل /cancel",
        reply_markup=back_kb("admin_chpost"),
    )


@dp.message(AdminChPostFSM.chat)
async def chp_chat_save(message: types.Message, state: FSMContext):
    """[R6-CH] حفظ القناة — تطبيع + تحقق حي + تشخيص دقيق.

    [CHPOST-5.16.3] لا يُحفظ فوق القناة السليمة إلا قيمة تعمل:
    الفشل يبقي القيمة القديمة كما هي مع شرح السبب وطريقة الإصلاح.
    """

    if not await is_admin_or_supervisor(message.from_user.id, "all"):
        await state.clear()
        return

    raw = (message.text or "").strip()

    if raw.startswith("/"):
        await state.clear()
        return

    kind, val = _chp_normalize(raw)

    if kind == "empty":
        await message.answer(
            "❌ الرسالة فارغة — أرسل @الاسم أو الرقم أو رابط t.me.",
        )
        return  # نبقى بالحالة للإعادة

    if kind == "invite":
        # روابط الدعوة الخاصة لا تكفي للعنونة إطلاقاً — بشرح واضح
        await message.answer(
            "❌ <b>رابط الدعوة الخاص لا يكفي كمعرّف</b> — تلجرام لا"
            " يسمح للبوتات بالعنونة به.\n\n"
            "الحلول:\n"
            "1️⃣ إن كانت القناة/المجموعة <b>عامة</b>: أرسل @اسمها أو"
            " رابط t.me.\n"
            "2️⃣ إن كانت <b>خاصة</b>: أعد توجيه أي منشور منها إلى"
            " <code>@getidsbot</code> أو <code>@userinfobot</code>"
            " وسيعطيك الرقم، ثم أرسله هنا بشكل "
            "<code>-1001234567890</code>.\n\n"
            "أرسل المعرّف الصحيح الآن (للإلغاء /cancel).",
        )
        return  # نبقى بالحالة — جاهز للقيمة الصحيحة

    target = val
    old = (await get_setting("channel_chat_id") or "").strip()

    try:
        chat = await bot.get_chat(target)
        chat_title = getattr(chat, "title", "") or str(target)

        # فحص العضوية والصلاحية (قد يفشل الفحص دون أن يفشل الوصول)
        status, can_post = "", None

        try:
            me = await bot.me()
            member = await bot.get_chat_member(target, me.id)
            status = getattr(member, "status", "") or ""
            can_post = bool(getattr(member, "can_post_messages", False))
        except Exception:
            pass

        await set_setting("channel_chat_id", str(val))
        await state.clear()

        # [CHPOST-5.16.3] مزامنة الجدولات القديمة مع القناة الجديدة
        # (لقطة chat_id بالصفوف كانت تُبقيها على القناة القديمة للأبد)
        db2 = await get_db()

        try:
            await db2.execute(
                "UPDATE channel_posts SET chat_id = ? WHERE chat_id != ?",
                (str(val), str(val)),
            )
            await db2.commit()
        finally:
            await db2.close()

        if status == "administrator" and can_post is False:
            await message.answer(
                "⚠️ <b>حُفظت القناة لكن ناقصة صلاحية!</b>\n"
                f"<b>{esc(chat_title)}</b>\n"
                "البوت مشرف <b>بدون صلاحية نشر المنشورات</b> — عدّل"
                " صلاحياته من إدارة القناة (فعّل «نشر الرسائل») ثم"
                " جرّب «🧪 اختبار النشر الآن».",
                reply_markup=back_kb("admin_chpost"),
            )
        elif status == "member":
            await message.answer(
                "⚠️ <b>حُفظت المجموعة لكن البوت ليس مشرفاً</b>\n"
                f"<b>{esc(chat_title)}</b>\n"
                "النشر العادي قد يعمل، لكن أضفه مشرفاً لضمان كل"
                " الميزات ثم جرّب «🧪 اختبار النشر الآن».",
                reply_markup=back_kb("admin_chpost"),
            )
        else:
            await message.answer(
                "✅ تم تعيين القناة والبوت يصل إليها:\n"
                f"<b>{esc(chat_title)}</b>\n"
                f"المعرّف المحفوظ: <code>{esc(str(val))}</code>\n"
                "جرّب «🧪 اختبار النشر الآن» للتأكد النهائي.",
                reply_markup=back_kb("admin_chpost"),
            )

        await audit(
            message.from_user.id, "chp_set_chat",
            f"kind={kind}", f"target={val}",
        )
        return
    except Exception as exc:
        exc_txt = str(exc)[:200]

    # فشل الوصول → لا نطمس القناة السابقة — تشخيص دقيق بدل التنبيه العام
    low = exc_txt.lower()
    hint = ""

    if "not found" in low:
        hint = (
            "المحادثة غير موجودة لدى البوت. للقنوات/المجموعات"
            " <b>الخاصة</b>: أرسل الرقم الرسمي مثل "
            "<code>-1001234567890</code> (أعد توجيه أي منشور منها إلى"
            " <code>@getidsbot</code> لمعرفة الرقم). وللعامة: "
            "<code>@الاسم</code> أو رابط t.me."
        )
    elif "not a member" in low or "participant" in low \
            or "forbidden" in low:
        hint = (
            "أضف البوت <b>مشرفاً</b> في القناة/المجموعة أولاً"
            " (بصلاحية نشر الرسائل) ثم أعد إرسال المعرّف هنا."
        )
    else:
        hint = f"تفاصيل تقنية: {esc(exc_txt[:120])}"

    keep = f"\n\nℹ️ بقي المعرّف السابق كما هو: <code>{esc(old)}</code>" \
        if old else ""
    await message.answer(
        "❌ <b>تعذر الوصول — لم يُحفظ تغيير القناة</b>\n"
        f"المدخل: <code>{esc(raw[:60])}</code>\n\n"
        f"{hint}{keep}\n\n"
        "صحّح المعرّف وأعد إرساله (للإلغاء /cancel).",
    )
    # نبقى بالحالة للإعادة — القيمة القديمة محفوظة


@dp.callback_query(F.data == "chp_test")
async def chp_test(cb: types.CallbackQuery, state: FSMContext):
    """[R6-CH] رسالة اختبار للقناة."""

    if not await is_admin_or_supervisor(cb.from_user.id, "all"):
        await cb.answer("⚠️ للأدمن فقط!", show_alert=True)
        return

    channel = (await get_setting("channel_chat_id") or "").strip()

    if not channel:
        await cb.answer("عيّن القناة أولاً.", show_alert=True)
        return

    target = await _chp_target(channel)

    if target is None:
        await cb.answer(
            "القناة المحفوظة بصيغة غير صالحة — أعد تعيينها.",
            show_alert=True,
        )
        return

    try:
        await bot.send_message(
            target,
            "🧪 رسالة اختبار — النشر من البوت يعمل ✅",
        )
    except Exception as exc:
        low = str(exc).lower()

        if "not found" in low:
            hint = " — القناة خاصة؟ استخدم رقم -100… أو @اسم"
        elif "forbidden" in low or "not a member" in low:
            hint = " — أضف البوت مشرفاً بصلاحية النشر"
        else:
            hint = ""

        await cb.answer(
            f"❌ فشل: {str(exc)[:80]}{hint}", show_alert=True,
        )
        return

    await cb.answer("✅ وصلت الرسالة للقناة", show_alert=True)


@dp.callback_query(F.data.startswith("chp_new:"))
async def chp_new(cb: types.CallbackQuery, state: FSMContext):
    """[R6-CH] بدء جدولة جديدة."""

    if not await is_admin_or_supervisor(cb.from_user.id, "all"):
        await cb.answer("⚠️ للأدمن فقط!", show_alert=True)
        return

    kind = cb.data.split(":", 1)[1]

    await cb.answer()
    await state.clear()
    await state.update_data(chp_kind=kind)

    if kind == "custom":
        await state.set_state(AdminChPostFSM.text)

        await cb.message.answer(
            "📝 أرسل النص المخصص الذي سيُنشر:\n\nللإلغاء أرسل /cancel",
            reply_markup=back_kb("admin_chpost"),
        )
    elif kind == "daily_report":
        await state.set_state(AdminChPostFSM.value)

        await cb.message.answer(
            "🕒 أرسل وقت النشر اليومي بنمط ساعة:دقيقة\n"
            "مثال: <code>21:00</code>\n\nللإلغاء أرسل /cancel",
            reply_markup=back_kb("admin_chpost"),
        )
    else:
        await state.set_state(AdminChPostFSM.value)

        await cb.message.answer(
            "🔁 أرسل الفترة بالساعات بين كل نشر\n"
            "مثال: <code>6</code>\n\nللإلغاء أرسل /cancel",
            reply_markup=back_kb("admin_chpost"),
        )


@dp.message(AdminChPostFSM.text)
async def chp_text_save(message: types.Message, state: FSMContext):
    """[R6-CH] حفظ النص المخصص ثم سؤال الفترة."""

    if not await is_admin_or_supervisor(message.from_user.id, "all"):
        await state.clear()
        return

    text = (message.text or "").strip()

    if text.startswith("/") or not text:
        await state.clear()
        return

    await state.update_data(chp_text=text[:3000])
    await state.set_state(AdminChPostFSM.value)

    await message.answer(
        "🔁 أرسل الفترة بالساعات بين كل نشر (مثال: <code>12</code>)\n"
        "أرسل <code>0</code> للنشر مرة واحدة الآن فقط\n\n"
        "للإلغاء أرسل /cancel",
    )


@dp.message(AdminChPostFSM.value)
async def chp_value_save(message: types.Message, state: FSMContext):
    """[R6-CH] حفظ الفترة/الوقت وإنشاء الجدولة."""

    if not await is_admin_or_supervisor(message.from_user.id, "all"):
        await state.clear()
        return

    data = await state.get_data()
    kind = data.get("chp_kind")
    raw = (message.text or "").strip()

    if raw.startswith("/"):
        await state.clear()
        return

    channel = (await get_setting("channel_chat_id") or "").strip()

    if not channel:
        await state.clear()

        await message.answer(
            "⚠️ عيّن القناة أولاً.",
            reply_markup=back_kb("admin_chpost"),
        )
        return

    if kind == "daily_report":
        if not re.fullmatch(r"([01]?\d|2[0-3]):([0-5]\d)", raw):
            await message.answer(
                "❌ النمط الصحيح: ساعة:دقيقة مثل <code>21:00</code>"
            )
            return

        db = await get_db()

        try:
            await db.execute(
                "INSERT INTO channel_posts"
                " (chat_id, kind, at_time, created_at)"
                " VALUES (?, ?, ?, ?)",
                (channel, kind, raw, now_iso()),
            )
            await db.commit()
        finally:
            await db.close()

        await state.clear()

        await message.answer(
            f"✅ سيُنشر التقرير اليومي كل يوم الساعة <b>{raw}</b>",
            reply_markup=back_kb("admin_chpost"),
        )
        return

    try:
        hours = float(raw.replace(",", "."))

        if not (0 <= hours <= 720) or not math.isfinite(hours):
            raise ValueError
    except Exception:
        await message.answer(
            "❌ أرسل عدد ساعات صحيح (0 إلى 720).\n\nللإلغاء أرسل /cancel"
        )
        return

    if kind == "custom":
        text = data.get("chp_text") or ""

        if hours == 0:
            target = await _chp_target(channel)

            try:
                await bot.send_message(target, text)
            except Exception as exc:
                logger.warning("فشل النشر الفوري: %s", exc)

            await state.clear()

            await message.answer(
                "✅ تم النشر مرة واحدة.",
                reply_markup=back_kb("admin_chpost"),
            )
            return

        db = await get_db()

        try:
            await db.execute(
                "INSERT INTO channel_posts"
                " (chat_id, kind, custom_text, interval_hours, created_at)"
                " VALUES (?, ?, ?, ?, ?)",
                (channel, kind, text, hours, now_iso()),
            )
            await db.commit()
        finally:
            await db.close()

        await state.clear()

        await message.answer(
            f"✅ جدولة نص مخصص كل <b>{hours:g} ساعة</b>.",
            reply_markup=back_kb("admin_chpost"),
        )
        return

    # announcement
    if hours == 0:
        hours = 6.0

    db = await get_db()

    try:
        await db.execute(
            "INSERT INTO channel_posts"
            " (chat_id, kind, interval_hours, created_at)"
            " VALUES (?, ?, ?, ?)",
            (channel, kind, hours, now_iso()),
        )
        await db.commit()
    finally:
        await db.close()

    await state.clear()

    await message.answer(
        f"✅ سيُنشر آخر إعلان فعّال كل <b>{hours:g} ساعة</b>.",
        reply_markup=back_kb("admin_chpost"),
    )


@dp.callback_query(F.data.startswith("chp_toggle:"))
async def chp_toggle(cb: types.CallbackQuery, state: FSMContext):
    """[R6-CH] تفعيل/تعطيل جدولة."""

    if not await is_admin_or_supervisor(cb.from_user.id, "all"):
        await cb.answer("⚠️ للأدمن فقط!", show_alert=True)
        return

    try:
        row_id = int(cb.data.split(":")[1])
    except (ValueError, IndexError):
        await cb.answer("معرف غير صالح.", show_alert=True)
        return

    db = await get_db()

    try:
        cur = await db.execute(
            "SELECT enabled FROM channel_posts WHERE id = ?", (row_id,),
        )
        row = await cur.fetchone()

        if row:
            await db.execute(
                "UPDATE channel_posts SET enabled = ? WHERE id = ?",
                (0 if row["enabled"] else 1, row_id),
            )
            await db.commit()
    finally:
        await db.close()

    await admin_chpost(cb, state)


@dp.callback_query(F.data.startswith("chp_del:"))
async def chp_del(cb: types.CallbackQuery, state: FSMContext):
    """[R6-CH] حذف جدولة."""

    if not await is_admin_or_supervisor(cb.from_user.id, "all"):
        await cb.answer("⚠️ للأدمن فقط!", show_alert=True)
        return

    try:
        row_id = int(cb.data.split(":")[1])
    except (ValueError, IndexError):
        await cb.answer("معرف غير صالح.", show_alert=True)
        return

    db = await get_db()

    try:
        await db.execute(
            "DELETE FROM channel_posts WHERE id = ?", (row_id,),
        )
        await db.commit()
    finally:
        await db.close()

    await cb.answer("تم الحذف")
    await admin_chpost(cb, state)


@dp.callback_query(F.data.startswith("chp_now:"))
async def chp_now(cb: types.CallbackQuery, state: FSMContext):
    """[R6-CH] نشر فوري لجدولة قائمة."""

    if not await is_admin_or_supervisor(cb.from_user.id, "all"):
        await cb.answer("⚠️ للأدمن فقط!", show_alert=True)
        return

    try:
        row_id = int(cb.data.split(":")[1])
    except (ValueError, IndexError):
        await cb.answer("معرف غير صالح.", show_alert=True)
        return

    db = await get_db()

    try:
        cur = await db.execute(
            "SELECT * FROM channel_posts WHERE id = ?", (row_id,),
        )
        row = await cur.fetchone()
    finally:
        await db.close()

    if not row:
        await cb.answer("الجدولة غير موجودة.", show_alert=True)
        return

    text = await _chp_text(row["kind"], row["custom_text"])

    if not text:
        await cb.answer(
            "لا يوجد محتوى للنشر (مثلاً لا إعلان فعّال).", show_alert=True,
        )
        return

    target = await _chp_target(row["chat_id"])

    photo = (
        await _chp_ann_photo()
        if row["kind"] == "announcement" else ""
    )  # [R6-PLUS2]

    try:
        await _send_chp(target, text, photo)
    except Exception as exc:
        await cb.answer(f"❌ فشل: {str(exc)[:80]}", show_alert=True)
        return

    db2 = await get_db()

    try:
        await db2.execute(
            "UPDATE channel_posts SET last_sent = ? WHERE id = ?",
            (now_iso(), row_id),
        )
        await db2.commit()
    finally:
        await db2.close()

    await cb.answer("✅ نُشر الآن")


@dp.message(AdminWalletFSM.value)
async def admin_wallet_save(message: types.Message, state: FSMContext):
    """[R6] حفظ رقم المحفظة."""

    if not await is_admin_or_supervisor(message.from_user.id, "all"):
        await state.clear()
        return

    raw = (message.text or "").strip()

    if not raw or raw.startswith("/"):
        await state.clear()
        return

    data = await state.get_data()
    key = data.get("wallet_key") or "sham"

    # [CODE-40] رموز الحساب تسمح حتى 40 خانة — أرقام المحافظ 30
    max_len = 40 if key in ("sham_code", "syriatel_code") else 30

    if not (3 <= len(raw) <= max_len):
        await message.answer(f"❌ القيمة بين 3 و{max_len} خانة.")
        return

    if key == "sham_code":  # [R6-PLUS3] رمز حساب شام كاش
        await set_setting("sham_account_code", raw)
        await state.clear()
        await audit(message.from_user.id, "sham_account_code", "", raw)

        kb = InlineKeyboardBuilder()
        kb.button(text="⚙️ إدارة شام كاش", callback_data="admin_manage_sham")
        kb.adjust(1)
        await message.answer(
            f"✅ حُفظ رمز الحساب: <code>{esc(raw)}</code>",
            reply_markup=kb.as_markup(),
        )
        return

    if key == "syriatel_code":  # [MENU-ORG] رمز إيداع سيرياتل كاش
        await set_setting("syriatel_account_code", raw)
        await state.clear()
        await audit(message.from_user.id, "syriatel_account_code", "", raw)

        kb = InlineKeyboardBuilder()
        kb.button(text="📱 إدارة سيرياتل كاش",
                  callback_data="admin_manage_syriatel")
        kb.adjust(1)
        await message.answer(
            f"✅ حُفظ رمز الإيداع: <code>{esc(raw)}</code>",
            reply_markup=kb.as_markup(),
        )
        return

    await set_setting(f"{key}_wallet_number", raw)
    await state.clear()
    await audit(  # [NEW 22]
        message.from_user.id, "wallet_number", key, raw,
    )

    kb = InlineKeyboardBuilder()  # [MENU-ORG] زر سياقي حسب المحفظة

    if key == "syriatel":
        kb.button(text="📱 إدارة سيرياتل كاش",
                  callback_data="admin_manage_syriatel")
    else:
        kb.button(text="⚙️ إدارة شام كاش", callback_data="admin_manage_sham")

    kb.adjust(1)
    await message.answer(
        f"✅ حُفظ رقم المحفظة: <code>{esc(raw)}</code>",
        reply_markup=kb.as_markup(),
    )


@dp.callback_query(F.data == "admin_manage_users")
async def admin_manage_users_r6(cb: types.CallbackQuery, state: FSMContext):
    """[R6] إدارة المستخدمين → لوحتنا الكاملة."""
    await admin_users(cb, state)


@dp.callback_query(F.data == "admin_manage_sham")
async def admin_manage_sham(cb: types.CallbackQuery, state: FSMContext):
    """[R6] إدارة شام كاش — المحفظة + حالة القبول + حركة اليوم."""

    if not await is_admin_or_supervisor(cb.from_user.id, "finance"):
        await cb.answer("⚠️ للأدمن فقط!", show_alert=True)
        return

    await cb.answer()
    await state.clear()

    today = f"{datetime.now(timezone.utc):%Y-%m-%d}"

    db = await get_db()

    try:
        cur = await db.execute(
            "SELECT COUNT(*) AS c, COALESCE(SUM(amount), 0) AS s"
            " FROM finance_requests WHERE type = 'deposit'"
            " AND status = 'approved' AND created_at LIKE ?"
            " AND note LIKE '%method=شام كاش%'",
            (f"{today}%",),
        )
        row = await cur.fetchone()
        dep_today_n, dep_today_s = row["c"], round2(row["s"])

        cur = await db.execute(
            "SELECT COUNT(*) AS c FROM finance_requests"
            " WHERE type = 'deposit' AND status = 'pending'"
            " AND note LIKE '%method=شام كاش%'",
        )
        pending = (await cur.fetchone())["c"]
    finally:
        await db.close()

    wallet = await _wallet_number("sham")
    enabled = (await get_setting("accept_sham") or "1") == "1"

    b = InlineKeyboardBuilder()
    b.button(  # [MENU-ORG] انتقل من الأدوات إلى هنا
        text="💵 ربط شام كاش (QR)",
        callback_data="sham_home",
    )
    b.button(  # [AUTO-DEP]
        text="🤖 الشحن الآلي",
        callback_data="sham_auto_screen",
    )
    b.button(  # [AUTO-WD]
        text="🤖 السحب الآلي",
        callback_data="sham_wd_screen",
    )
    b.button(  # [WGT 5.18.1]
        text="🛡 مقارنة رصيد المحفظة مع البوت",
        callback_data="wgt_screen",
    )
    b.button(
        text="🔄 تغيير حساب الإيداع",
        callback_data="change_sham_deposit_acc",
    )
    b.button(  # [R6-PLUS3]
        text="🔣 رمز حساب شام كاش",
        callback_data="change_sham_code_acc",
    )

    _mode = (await get_setting("sham_code_mode") or "wallet") == "code"
    b.button(  # [R6-PLUS4] الأدمن يحدد ما يظهر للمستخدم
        text=("🔣 يظهر للمستخدم: رمز الحساب" if _mode
              else "💳 يظهر للمستخدم: رقم المحفظة"),
        callback_data="toggle_sham_mode",
    )
    b.button(
        text=("🟢 قبول شحن شام كاش" if enabled
              else "🔴 قبول شحن شام كاش"),
        callback_data="toggle_sham_auto",
    )
    b.button(text="↩️ رجوع", callback_data="admin_home")
    b.adjust(1)

    await safe_edit(
        cb.message,
        "⚙️ <b>إدارة شام كاش</b>\n\n"
        f"💳 حساب الإيداع الحالي: <code>{esc(wallet)}</code>\n"
        f"الحالة: {'🟢 يقبل الشحن' if enabled else '🔴 معطل'}\n\n"
        f"📅 اليوم: {dep_today_n} إيداعاً بمجموع <b>{money(dep_today_s)}</b>\n"
        f"🟡 طلبات شام كاش المعلقة: {pending}",
        b.as_markup(),
    )


@dp.callback_query(F.data == "admin_manage_syriatel")
async def admin_manage_syriatel(cb: types.CallbackQuery, state: FSMContext):
    """[MENU-ORG] إدارة سيرياتل كاش — رقم ورمز الإيداع + القبول + حركة اليوم."""

    if not await is_admin_or_supervisor(cb.from_user.id, "finance"):
        await cb.answer("⚠️ للأدمن فقط!", show_alert=True)
        return

    await cb.answer()
    await state.clear()

    today = f"{datetime.now(timezone.utc):%Y-%m-%d}"

    db = await get_db()

    try:
        cur = await db.execute(
            "SELECT COUNT(*) AS c, COALESCE(SUM(amount), 0) AS s"
            " FROM finance_requests WHERE type = 'deposit'"
            " AND status = 'approved' AND created_at LIKE ?"
            " AND note LIKE '%method=سيرياتيل كاش%'",
            (f"{today}%",),
        )
        row = await cur.fetchone()
        dep_today_n, dep_today_s = row["c"], round2(row["s"])

        cur = await db.execute(
            "SELECT COUNT(*) AS c FROM finance_requests"
            " WHERE type = 'deposit' AND status = 'pending'"
            " AND note LIKE '%method=سيرياتيل كاش%'",
        )
        pending = (await cur.fetchone())["c"]
    finally:
        await db.close()

    wallet = await _wallet_number("syriatel")
    code = (await get_setting("syriatel_account_code") or "").strip()
    enabled = (await get_setting("accept_syriatel") or "1") == "1"
    _mode = (await get_setting("syriatel_code_mode") or "wallet") == "code"

    b = InlineKeyboardBuilder()
    b.button(
        text="💳 تغيير رقم الإيداع",
        callback_data="change_syriatel_deposit_acc",
    )
    b.button(
        text="🔣 رمز الإيداع",
        callback_data="change_syriatel_code_acc",
    )
    b.button(
        text=("🔣 يظهر للمستخدم: رمز الإيداع" if _mode
              else "💳 يظهر للمستخدم: رقم المحفظة"),
        callback_data="toggle_syriatel_mode",
    )
    b.button(
        text=("🟢 قبول شحن سيرياتيل كاش" if enabled
              else "🔴 قبول شحن سيرياتيل كاش"),
        callback_data="toggle_syriatel_auto",
    )
    b.button(text="↩️ رجوع", callback_data="admin_home")
    b.adjust(1)

    await safe_edit(
        cb.message,
        "📱 <b>إدارة سيرياتل كاش</b>\n\n"
        f"💳 رقم الإيداع الحالي: <code>{esc(wallet)}</code>\n"
        f"🔣 رمز الإيداع: <code>{esc(code or '—')}</code>\n"
        f"الحالة: {'🟢 يقبل الشحن' if enabled else '🔴 معطل'}\n\n"
        f"📅 اليوم: {dep_today_n} إيداعاً بمجموع <b>{money(dep_today_s)}</b>\n"
        f"🟡 طلبات سيرياتيل كاش المعلقة: {pending}",
        b.as_markup(),
    )


@dp.callback_query(F.data == "change_syriatel_deposit_acc")
async def change_syriatel_deposit_acc(cb: types.CallbackQuery,
                                      state: FSMContext):
    """[MENU-ORG] رقم إيداع سيرياتل كاش المعروض للمستخدمين."""

    if not await is_admin_or_supervisor(cb.from_user.id, "all"):
        await cb.answer("⚠️ للأدمن فقط!", show_alert=True)
        return

    await cb.answer()
    await state.clear()
    await state.update_data(wallet_key="syriatel")
    await state.set_state(AdminWalletFSM.value)

    current = await _wallet_number("syriatel")
    await cb.message.answer(
        "💳 <b>تغيير رقم الإيداع لسيرياتل كاش:</b>\n\n"
        "أرسل رقم محفظة سيرياتيل كاش الذي سيظهر للمستخدمين:\n"
        f"الحالي: <code>{esc(current)}</code>\n"
        "للإلغاء أرسل /cancel",
        reply_markup=back_kb("admin_manage_syriatel"),
    )


@dp.callback_query(F.data == "change_syriatel_code_acc")
async def change_syriatel_code_acc(cb: types.CallbackQuery,
                                   state: FSMContext):
    """[MENU-ORG] رمز إيداع سيرياتل كاش المعروض للمستخدمين."""

    if not await is_admin_or_supervisor(cb.from_user.id, "all"):
        await cb.answer("⚠️ للأدمن فقط!", show_alert=True)
        return

    await cb.answer()
    await state.clear()
    await state.update_data(wallet_key="syriatel_code")
    await state.set_state(AdminWalletFSM.value)

    current = (await get_setting("syriatel_account_code") or "").strip()

    await cb.message.answer(
        "🔣 <b>رمز إيداع سيرياتل كاش:</b>\n\n"
        "أرسل الرمز الذي سيظهر للمستخدمين عند اختيار العرض بالرمز:\n"
        f"الحالي: <code>{esc(current or '—')}</code>\n"
        "للإلغاء أرسل /cancel",
        reply_markup=back_kb("admin_manage_syriatel"),
    )


@dp.callback_query(F.data == "toggle_syriatel_mode")
async def toggle_syriatel_mode(cb: types.CallbackQuery, state: FSMContext):
    """[MENU-ORG] ما يظهر للمستخدم: رقم المحفظة أو رمز الإيداع."""

    if not await is_admin_or_supervisor(cb.from_user.id, "all"):
        await cb.answer("⚠️ للأدمن فقط!", show_alert=True)
        return

    mode = (await get_setting("syriatel_code_mode") or "wallet") == "code"
    new_mode = "wallet" if mode else "code"
    await set_setting("syriatel_code_mode", new_mode)
    await audit(cb.from_user.id, "syriatel_mode", "", new_mode)
    await cb.answer(
        "🔣 سيرى المستخدم رمز الإيداع" if new_mode == "code"
        else "💳 سيرى المستخدم رقم المحفظة",
        show_alert=True,
    )
    await admin_manage_syriatel(cb, state)  # إعادة رسم الشاشة


@dp.callback_query(F.data == "admin_manage_recharge")
async def admin_manage_recharge(cb: types.CallbackQuery, state: FSMContext):
    """[R6] الشحن والعروض → حملة المكافأة والإعلانات."""

    if not await is_admin_or_supervisor(cb.from_user.id, "finance"):
        await cb.answer("⚠️ للأدمن فقط!", show_alert=True)
        return

    await cb.answer()
    await state.clear()

    bonus_pct = await get_float_setting("bonus_percent", 0.0)
    bonus_max = await get_float_setting("bonus_max", 0.0)
    comm = await get_float_setting("commission_percent", 0.0)
    wd_fee = await get_float_setting("withdraw_fee_percent", 0.0)
    cd_min = await get_float_setting("withdraw_cooldown_min", 0.0)

    b = InlineKeyboardBuilder()
    b.button(text="🎁 إعدادات مكافأة الإيداع", callback_data="admin_bonus")
    b.button(text="📢 الإعلانات", callback_data="admin_anns")
    b.button(text="٪ عمولة الشحن", callback_data="admin_commission")
    b.button(text="💸 عمولة السحب", callback_data="admin_wdfee")  # [R6-NEW]
    b.button(text="⏱ تهدئة السحب",
             callback_data="admin_cooldown")  # [R6-NEW]
    b.button(text="↩️ رجوع", callback_data="admin_home")
    b.adjust(1)
    await safe_edit(
        cb.message,
        "💳 <b>إدارة الشحن والعروض</b>\n\n"
        f"٪ عمولة الشحن الحالية: <b>{money(comm)}%</b>\n"
        f"💸 عمولة السحب الحالية: <b>{wd_fee:g}%</b>\n"
        f"⏱ تهدئة السحب: "
        + (f"<b>{cd_min:g} دقيقة</b>" if cd_min > 0 else "معطّلة")
        + "\n"
        "🎁 حملة المكافأة: "
        + (f"{bonus_pct:g}% حتى {money(bonus_max)}"
           if bonus_pct > 0 else "معطّلة"),
        b.as_markup(),
    )


@dp.callback_query(F.data == "admin_wdfee")
async def admin_wdfee(cb: types.CallbackQuery, state: FSMContext):
    """[R6-NEW] ضبط عمولة السحب."""

    if not await is_admin_or_supervisor(cb.from_user.id, "finance"):
        await cb.answer("غير مصرّح.", show_alert=True)
        return

    await cb.answer()
    await state.clear()
    await state.set_state(AdminWdFeeFSM.value)

    current = await get_float_setting("withdraw_fee_percent", 0.0)

    await cb.message.answer(
        "💸 <b>عمولة السحب</b>\n\n"
        f"النسبة الحالية: <b>{current:g}%</b>\n\n"
        "تُخصم من مبلغ السحب ويصل المستخدم الصافي.\n"
        "أرسل النسبة الجديدة (0 إلى 50):\n"
        "للإلغاء أرسل /cancel"
    , reply_markup=back_kb("admin_manage_recharge"))


@dp.message(AdminWdFeeFSM.value)
async def admin_wdfee_save(message: types.Message, state: FSMContext):
    """[R6-NEW] حفظ عمولة السحب."""

    if not await is_admin_or_supervisor(message.from_user.id, "finance"):
        await state.clear()
        return

    try:
        pct = float((message.text or "").strip().replace(",", "."))
        if not (0 <= pct <= 50) or not math.isfinite(pct):
            raise ValueError
    except Exception:
        await message.answer(
            "❌ أرسل نسبة صحيحة بين 0 و 50.\n\nللإلغاء أرسل /cancel"
        )
        return

    await set_setting("withdraw_fee_percent", str(round(pct, 2)))
    await state.clear()
    await audit(message.from_user.id, "wd_fee_set", f"{pct:g}%")

    await message.answer(
        f"✅ عمولة السحب أصبحت <b>{pct:g}%</b>.",
        reply_markup=back_kb("admin_manage_recharge"),
    )


@dp.callback_query(F.data == "admin_cooldown")
async def admin_cooldown(cb: types.CallbackQuery, state: FSMContext):
    """[R6-NEW] فترة التهدئة بين السحوبات."""

    if not await is_admin_or_supervisor(cb.from_user.id, "finance"):
        await cb.answer("غير مصرّح.", show_alert=True)
        return

    await cb.answer()
    await state.clear()
    await state.set_state(AdminCooldownFSM.value)

    current = await get_float_setting("withdraw_cooldown_min", 0.0)

    await cb.message.answer(
        "⏱ <b>فترة التهدئة بين السحوبات</b>\n\n"
        f"الحالية: <b>{current:g} دقيقة</b>\n\n"
        "تمنع طلب سحب جديد قبل انتهاء المدة من السحب السابق.\n"
        "أرسل عدد الدقائق (0 = تعطيل، حتى 10080):\n"
        "للإلغاء أرسل /cancel"
    , reply_markup=back_kb("admin_manage_recharge"))


@dp.message(AdminCooldownFSM.value)
async def admin_cooldown_save(message: types.Message, state: FSMContext):
    """[R6-NEW] حفظ فترة التهدئة."""

    if not await is_admin_or_supervisor(message.from_user.id, "finance"):
        await state.clear()
        return

    try:
        minutes = float((message.text or "").strip())
        if not (0 <= minutes <= 10080) or not math.isfinite(minutes):
            raise ValueError
    except Exception:
        await message.answer(
            "❌ أرسل عدد دقائق صحيح (0 إلى 10080).\n\n"
            "للإلغاء أرسل /cancel"
        )
        return

    await set_setting("withdraw_cooldown_min", str(round(minutes, 1)))
    await state.clear()
    await audit(message.from_user.id, "wd_cooldown_set", f"{minutes:g}m")

    await message.answer(
        f"✅ فترة التهدئة أصبحت <b>{minutes:g} دقيقة</b>.",
        reply_markup=back_kb("admin_manage_recharge"),
    )


@dp.callback_query(F.data == "admin_cashier_stats")
async def admin_cashier_stats(cb: types.CallbackQuery, state: FSMContext):
    """[R6] إحصائيات الكاشيرة → KPI الحي (NEW 42)."""
    await admin_kpi(cb, state)


@dp.callback_query(F.data == "admin_stats")
async def admin_stats_r6(cb: types.CallbackQuery, state: FSMContext):
    """[DEDUP 5.18.5] الإحصائيات العامة القديمة = شاشة الإحصائيات الموحدة.

    يبقى المسجلاً aliasاً لأزرار الرسائل القديمة بالمحادثات.
    """

    if not await is_admin_or_supervisor(cb.from_user.id, "reports"):
        await cb.answer("⚠️ للأدمن فقط!", show_alert=True)
        return

    await admin_statistics(cb, state)
    return

    await cb.answer()
    await state.clear()

    db = await get_db()

    try:
        cur = await db.execute("SELECT COUNT(*) AS c FROM users")
        users_count = (await cur.fetchone())["c"]
        cur = await db.execute("SELECT COUNT(*) AS c FROM transactions")
        tx_count = (await cur.fetchone())["c"]
        cur = await db.execute(
            "SELECT COUNT(*) AS c FROM finance_requests"
            " WHERE status = 'pending'",
        )
        pending = (await cur.fetchone())["c"]
    finally:
        await db.close()

    b = InlineKeyboardBuilder()
    b.button(text="📈 إحصائيات موسعة", callback_data="admin_statistics")
    b.button(text="↩️ رجوع لوحة الأدمن", callback_data="admin_home")
    b.adjust(1)
    await safe_edit(
        cb.message,
        "📊 <b>الإحصائيات العامة:</b>\n\n"
        f"👤 عدد الحسابات المسجلة: <code>{users_count}</code>\n"
        f"🧾 إجمالي العمليات: <code>{tx_count}</code>\n"
        f"🟡 الطلبات المعلقة: <code>{pending}</code>",
        b.as_markup(),
    )


@dp.callback_query(F.data == "admin_custom_report")
async def admin_custom_report(cb: types.CallbackQuery, state: FSMContext):
    """[R6] تقرير مخصص → تقارير CSV (NEW 14)."""
    await admin_reports(cb, state)


@dp.callback_query(F.data == "admin_wallets_balance")
async def admin_wallets_balance(cb: types.CallbackQuery, state: FSMContext):
    """[R6] أرصدة المحافظ — حركة كل طريقة حقيقية من قاعدة البيانات."""

    if not await is_admin_or_supervisor(cb.from_user.id, "finance"):
        await cb.answer("⚠️ للأدمن فقط!", show_alert=True)
        return

    await cb.answer()
    await state.clear()

    async def method_sums(method, status):
        db = await get_db()
        try:
            cur = await db.execute(
                "SELECT COUNT(*) AS c, COALESCE(SUM(amount), 0) AS s"
                " FROM finance_requests WHERE note LIKE ?"
                " AND status = ?",
                (f"%method={method}%", status),
            )
            row = await cur.fetchone()
            return row["c"], round2(row["s"])
        finally:
            await db.close()

    sham_dep_n, sham_dep_s = await method_sums("شام كاش", "approved")
    syr_dep_n, syr_dep_s = await method_sums("سيرياتيل كاش", "approved")
    sham_wd_n, sham_wd_s = await method_sums("شام كاش", "pending")
    syr_wd_n, syr_wd_s = await method_sums("سيرياتيل كاش", "pending")

    db = await get_db()

    try:
        cur = await db.execute(
            "SELECT COALESCE(SUM(balance), 0) AS s FROM users",
        )
        total_balance = round2((await cur.fetchone())["s"])
        cur = await db.execute(
            "SELECT COALESCE(SUM(amount), 0) AS s FROM transactions"
            " WHERE type = 'deposit'",
        )
        dep_all = round2((await cur.fetchone())["s"])
    finally:
        await db.close()

    sham_wallet = await _wallet_number("sham")
    syr_wallet = await _wallet_number("syriatel")

    await safe_edit(
        cb.message,
        "🏦 <b>أرصدة المحافظ</b>\n\n"
        f"💳 شام كاش: <code>{esc(sham_wallet)}</code>\n"
        f"   شحن مكتمل: {sham_dep_n} ({money(sham_dep_s)})"
        " | معلق: "
        f"{sham_wd_n} ({money(sham_wd_s)})\n\n"
        f"📱 سيرياتيل كاش: <code>{esc(syr_wallet)}</code>\n"
        f"   شحن مكتمل: {syr_dep_n} ({money(syr_dep_s)})"
        " | معلق: "
        f"{syr_wd_n} ({money(syr_wd_s)})\n\n"
        f"💼 إجمالي أرصدة المستخدمين بالبوت: <b>{money(total_balance)}</b>\n"
        f"📥 إجمالي كل الشحنات المسجلة: {money(dep_all)}",
        InlineKeyboardBuilder()
        .button(text="↩️ رجوع لوحة الأدمن", callback_data="admin_home")
        .adjust(1)
        .as_markup(),
    )


# FALLBACK
# ============================================================

@dp.message()
async def fallback_message(message: types.Message, state: FSMContext):

    await state.clear()  # [FIX 2]

    if not await user_allowed(message.from_user.id, message):
        return

    lang = await user_lang(message.from_user.id)

    await message.answer(
        tr(lang, "fallback"),
        reply_markup=await menu_with_links(lang, message.from_user.id),
    )


# ============================================================
# ERROR HANDLER — [R6-PLUS8] تصنيف الأخطاء
# البريئة (زر منتهي/حظر/شبكة) سطر قصير، والجدّية إلى error_log
# ============================================================

ERROR_LOG_PATH = "error_log.txt"  # [R6-PLUS8] تفاصيل الأخطاء الجدية

_BENIGN_TELEGRAM = (
    "query is too old",           # ضغطة على رسالة قديمة
    "query id is invalid",        # نفس السبب
    "message is not modified",    # تعديل بلا تغيير
    "message to forward not found",
    "message to delete not found",
    "message to edit not found",
    "message can't be deleted",
    "chat not found",
    "user is deactivated",
)


def _error_uid(update) -> str:
    """[R6-PLUS8] معرف المستخدم من التحديث — للسجل فقط."""
    try:
        for attr in ("message", "callback_query",
                     "pre_checkout_query", "my_chat_member"):
            obj = getattr(update, attr, None)

            if obj is not None and getattr(obj, "from_user", None):
                return obj.from_user.id
    except Exception:
        pass

    return "؟"


async def _classify_error(exc) -> str:
    """[R6-PLUS8] تصنيف الاستثناء: benign | network | serious."""
    from aiogram.exceptions import (
        TelegramBadRequest,
        TelegramForbiddenError,
        TelegramNetworkError,
        TelegramRetryAfter,
    )

    msg = str(exc).lower()

    if isinstance(exc, TelegramBadRequest) and any(
        p in msg for p in _BENIGN_TELEGRAM
    ):
        return "benign"

    if isinstance(exc, (TelegramForbiddenError, TelegramRetryAfter)):
        return "benign"  # حظر لدى المستخدم أو ضغط تليجرام مؤقت

    try:
        from aiohttp import ClientError
    except ImportError:
        ClientError = ()

    if isinstance(
        exc, (TelegramNetworkError, asyncio.TimeoutError,
              ConnectionError, ClientError),
    ):
        return "network"

    return "serious"


@dp.errors()
async def global_error_handler(event):
    """[R6-PLUS8] كونسول نظيف: البريئة سطر، والتفصيل في error_log.txt."""

    exc = event.exception

    try:
        gated = await feat_on("quiet_errors")
    except Exception:
        gated = True  # حتى لو فشلت القاعدة نفسها

    if not gated:
        logger.error("حدث خطأ غير متوقع: %r", exc, exc_info=exc)
        return True

    kind = await _classify_error(exc)
    uid = _error_uid(event.update)

    if kind == "benign":
        logger.info(
            "[تجاهل] %s: %s", type(exc).__name__, str(exc)[:90],
        )
        return True

    if kind == "network":
        logger.warning(
            "[شبكة] انقطاع لحظي (%s) للمستخدم %s — سيُعاد تلقائياً",
            type(exc).__name__, uid,
        )
        return True

    # أخطاء تليجرام الأخرى أو برمجية: سطر قصير بالكونسول + التتبع بالملف
    logger.error(
        "[خطأ] %s: %s | المستخدم %s — التفاصيل في %s",
        type(exc).__name__, str(exc)[:90], uid, ERROR_LOG_PATH,
    )

    try:
        import traceback

        with open(ERROR_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(f"\n{'=' * 50}\n")
            f.write(
                f"{now_iso()} | user={uid} | "
                f"{type(exc).__name__}: {exc}\n",
            )
            f.write(
                "".join(traceback.format_exception(exc)).rstrip() + "\n",
            )
    except OSError:
        pass

    return True


# ============================================================
# MAIN
# ============================================================

# ============================================================
# KEEP-ALIVE [R6-PLUS11] — منع النوم على الاستضافة السحابية
# (Render Free): خادم صحة صغير على $PORT + نبض ذاتي كل 10 دقائق
# ============================================================

KEEPALIVE_INTERVAL = 60  # [AUDIT3] نبضة كل 60 ثانية (طلب المالك)
_keepalive_hits = {"health": 0, "ping": 0}


def _env_port() -> int:
    """[R6-PLUS11] منفذ الصحة: $PORT (Render) أو 10000."""
    try:
        return int(os.getenv("PORT", "10000") or "10000")
    except ValueError:
        return 10000


def keepalive_self_url() -> str:
    """[R6-PLUS11] عنوان الخدمة ذاته (Render يوفره تلقائياً)."""
    url = (os.getenv("RENDER_EXTERNAL_URL") or "").strip()

    if url:
        return url.rstrip("/")

    return (os.getenv("KEEP_ALIVE_URL") or "").strip().rstrip("/")


def keepalive_extra_urls() -> list:
    """[R6-PLUS11] عناوين إضافية للنبض (فواصل ,)."""
    raw = (os.getenv("KEEP_ALIVE_URLS") or "").strip()

    if not raw:
        return []

    return [
        u.strip().rstrip("/") for u in raw.split(",") if u.strip()
    ]


async def _health_handler(reader, writer):
    """[R6-PLUS11] أي GET يُجاب بـ200 + حالة JSON (يكفي لفحص المنفذ)."""
    try:
        await reader.read(4096)
        body = json.dumps({
            "status": "ok",
            "bot": BOT_VERSION,
            "time": now_iso(),
        }).encode()

        head = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: application/json\r\n"
            f"Content-Length: {len(body)}\r\n"
            "Connection: close\r\n\r\n"
        ).encode()

        writer.write(head + body)
        await writer.drain()
        _keepalive_hits["health"] += 1
    except Exception:
        pass
    finally:
        try:
            writer.close()
        except Exception:
            pass


async def start_health_server(port: int = None):
    """[R6-PLUS11] إقلاع خادم الصحة (0.0.0.0:port) — None عند الفشل."""
    if port is None:
        port = _env_port()

    try:
        server = await asyncio.start_server(
            _health_handler, "0.0.0.0", port,
        )
        logger.info("[keep-alive] خادم الصحة يعمل على المنفذ %s", port)
        return server
    except OSError as exc:
        logger.warning(
            "[keep-alive] تعذر فتح منفذ الصحة %s: %s", port, exc,
        )
        return None


async def keepalive_ping_once(urls: list) -> int:
    """[R6-PLUS11] نبضة واحدة: GET /healthz لكل عنوان — يرجع الناجح."""
    ok = 0

    try:
        import aiohttp  # متوفرة مع aiogram
    except ImportError:
        return 0

    async with aiohttp.ClientSession() as sess:
        for u in urls:
            try:
                async with sess.get(
                    u + "/healthz",
                    timeout=aiohttp.ClientTimeout(total=30),
                ) as resp:
                    if resp.status == 200:
                        ok += 1
            except Exception as exc:
                logger.warning(
                    "[keep-alive] فشل نبض %s: %s", u, exc,
                )

    if ok:
        _keepalive_hits["ping"] += 1

    return ok


async def _keepalive_loop():
    """[R6-PLUS11] نبض دوري — يخرج فوراً إن لم توجد عناوين."""
    self_url = keepalive_self_url()
    urls = ([self_url] if self_url else []) + keepalive_extra_urls()

    if not urls:
        return

    logger.info(
        "[keep-alive] نشط — نبضة كل %s ثانية إلى: %s",
        KEEPALIVE_INTERVAL, urls,
    )

    while True:
        await asyncio.sleep(KEEPALIVE_INTERVAL)
        await keepalive_ping_once(urls)


async def main(notify_crash: bool = False):
    global BOT_USERNAME

    logger.info("=" * 40)
    logger.info("Bot is starting...")
    logger.info("Database: %s", DB_PATH)
    logger.info("Admin ID: %s", ADMIN_USER_ID)
    logger.info("=" * 40)

    periodic_task = asyncio.create_task(_periodic_tasks())

    # [R6-PLUS11] keep-alive: يبدأ تلقائياً على Render فقط،
    # وعلى الجهاز المحلي لا شيء يتغير (لا PORT ولا عناوين)
    ka_server = None
    ka_task = None

    if os.getenv("KEEP_ALIVE", "1") != "0" and (
        keepalive_self_url()
        or keepalive_extra_urls()
        or os.getenv("PORT")
    ):
        ka_server = await start_health_server()
        ka_task = asyncio.create_task(_keepalive_loop())

    asyncio.create_task(_sham_sweep_loop())  # [EVDEP] المسح اليومي
    asyncio.create_task(_sham_wd_loop())  # [AUTO-WD] تنفيذ السحوبات
    try:
        # [R6-PLUS6] نسخة أمان قبل ترقية إصدار القاعدة (مرة/إقلاع)
        try:
            await pre_upgrade_backup_if_due()
        except Exception:
            logger.exception("فحص نسخة ما قبل الترقية فشل.")

        try:
            me = await bot.me()
            BOT_USERNAME = me.username or ""  # [NEW 29]
            logger.info("Bot username: @%s", BOT_USERNAME)
        except Exception as exc:
            logger.warning("تعذر جلب معلومات البوت: %s", exc)

        # [R6-CH] قائمة الأوامر الرسمية (تضمن عمل قائمة زر القائمة دائماً)
        try:
            base_cmds = [
                BotCommand(command="start",
                           description="القائمة الرئيسية"),
                BotCommand(command="my_info",
                           description="معلومات ملفي"),
                BotCommand(command="cancel",
                           description="إلغاء العملية الحالية"),
            ]
            await bot.set_my_commands(
                base_cmds, scope=BotCommandScopeDefault(),
            )

            if ADMIN_USER_ID:
                await bot.set_my_commands(
                    base_cmds + [
                        BotCommand(command="now",
                                   description="نبض البوت الآن"),
                        BotCommand(command="ops",
                                   description="تشخيص البوت الشامل"),
                    ],
                    scope=BotCommandScopeChat(chat_id=ADMIN_USER_ID),
                )
        except Exception as exc:
            logger.warning("تعذر ضبط قائمة الأوامر: %s", exc)

        try:
            await bot.delete_webhook(drop_pending_updates=True)
        except Exception as exc:
            logger.warning("تعذر حذف الويب هوك: %s", exc)

        # [R6-NEW] تنبيه الأدمن إذا كان التشغيل السابق قد انهار
        if notify_crash and ADMIN_USER_ID:
            try:
                await bot.send_message(
                    ADMIN_USER_ID,
                    "⚠️ <b>تنبيه تشغيل</b>\n\n"
                    "التشغيل السابق توقف فجأة (انهيار أو إيقاف قسري).\n"
                    "البوت يعمل الآن بشكل طبيعي ✅",
                )
            except Exception as exc:
                logger.warning("تعذر إرسال تنبيه الانهيار: %s", exc)

        try:
            print("\n" + "=" * 46, flush=True)
            print("✅  BOT IS RUNNING  —  البوت يعمل الآن", flush=True)
            print("    اترك هذه النافذة مفتوحة — للإيقاف: Ctrl+C", flush=True)
            print("=" * 46 + "\n", flush=True)
        except Exception:
            pass  # لو كان الإخراج موجهاً بترميز محدود

        # [FIX 6] start_polling يغلق جلسة البوت تلقائياً
        await dp.start_polling(
            bot,
            allowed_updates=dp.resolve_used_update_types(),
        )
    finally:
        periodic_task.cancel()

        if ka_task:
            ka_task.cancel()

        if ka_server:
            ka_server.close()


if __name__ == "__main__":
    # إظهار سجلات التشغيل في النافذة (كانت INFO مخفية فبدت النافذة صامتة)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)-7s | %(message)s",
        datefmt="%H:%M:%S",
    )
    # [R6-NEW] كشف الانهيار: علامة تُكتب عند الإقلاع وتُحذف عند
    # الإيقاف النظيف — بقاءها يعني انهياراً في الجولة السابقة
    _crash_flag = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), ".crash_flag",
    )
    _prev_crash = os.path.exists(_crash_flag)

    try:
        with open(_crash_flag, "w") as _f:
            _f.write(now_iso())

        asyncio.run(main(notify_crash=_prev_crash))
    except KeyboardInterrupt:
        logger.info("Bot stopped.")
    finally:
        try:
            os.remove(_crash_flag)
        except OSError:
            pass
