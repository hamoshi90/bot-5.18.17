import os
import asyncio
import json
import secrets
import string
import sqlite3
import html
from datetime import datetime, timezone
from typing import Optional

import aiosqlite
from aiogram import Bot, Dispatcher, types, F
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

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()

try:
    ADMIN_USER_ID = int(os.getenv("ADMIN_USER_ID", "0"))
except ValueError:
    ADMIN_USER_ID = 0

DB_PATH = os.getenv("DB_PATH", "bot.db")


if not BOT_TOKEN:
    raise RuntimeError(
        "TELEGRAM_BOT_TOKEN غير موجود في ملف .env"
    )

if ADMIN_USER_ID <= 0:
    raise RuntimeError(
        "ADMIN_USER_ID غير صالح في ملف .env"
    )


bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML
    )
)

dp = Dispatcher()


# ============================================================
# CONSTANTS
# ============================================================

MAX_AMOUNT = 1_000_000

ALLOWED_SUPERVISOR_PERMISSIONS = {
    "users",
    "finance",
    "gifts",
    "all",
}


# ============================================================
# HELPERS
# ============================================================

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(
        timespec="seconds"
    )


def money(value) -> str:
    try:
        value = float(value)

        if value.is_integer():
            return str(int(value))

        return f"{value:.2f}"

    except Exception:
        return str(value)


def esc(value) -> str:
    """
    Escape HTML before sending user-controlled text
    with ParseMode.HTML.
    """
    return html.escape(str(value or ""))


def generate_password(length: int = 10) -> str:
    chars = (
        string.ascii_letters
        + string.digits
        + "!@#$%^&*"
    )

    return "".join(
        secrets.choice(chars)
        for _ in range(length)
    )


def generate_code(length: int = 8) -> str:
    chars = string.ascii_uppercase + string.digits

    return "".join(
        secrets.choice(chars)
        for _ in range(length)
    )


def valid_amount(value: float) -> bool:
    return (
        value > 0
        and value <= MAX_AMOUNT
    )


# ============================================================
# DATABASE
# ============================================================

def init_db():
    conn = sqlite3.connect(DB_PATH)

    try:
        cur = conn.cursor()

        # SQLite settings
        cur.execute("PRAGMA journal_mode=WAL")
        cur.execute("PRAGMA foreign_keys=ON")

        # ----------------------------------------------------
        # USERS
        # ----------------------------------------------------

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

        # ----------------------------------------------------
        # TRANSACTIONS
        # ----------------------------------------------------

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

        # ----------------------------------------------------
        # ADMIN SETTINGS
        # ----------------------------------------------------

        cur.execute("""
        CREATE TABLE IF NOT EXISTS admin_settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
        """)

        # ----------------------------------------------------
        # GIFT CODES
        # ----------------------------------------------------

        cur.execute("""
        CREATE TABLE IF NOT EXISTS gift_codes (
            code TEXT PRIMARY KEY,
            amount REAL NOT NULL,
            used_by INTEGER DEFAULT NULL,
            created_at TEXT NOT NULL,
            used_at TEXT DEFAULT NULL
        )
        """)

        # ----------------------------------------------------
        # SUPERVISORS
        # ----------------------------------------------------

        cur.execute("""
        CREATE TABLE IF NOT EXISTS supervisors (
            telegram_id INTEGER PRIMARY KEY,
            permissions TEXT DEFAULT '[]',
            created_at TEXT NOT NULL
        )
        """)

        # ----------------------------------------------------
        # FINANCE REQUESTS
        # ----------------------------------------------------

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

        # ----------------------------------------------------
        # INDEXES
        # ----------------------------------------------------

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

        # ----------------------------------------------------
        # DEFAULT SETTINGS
        # ----------------------------------------------------

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
            """
            SELECT *
            FROM users
            WHERE telegram_id = ?
            """,
            (telegram_id,)
        )

        row = await cur.fetchone()

        return dict(row) if row else None

    finally:
        await db.close()


async def create_user(
    telegram_id: int,
    username: str = "",
    full_name: str = ""
):
    db = await get_db()

    try:
        await db.execute(
            """
            INSERT OR IGNORE INTO users
            (
                telegram_id,
                username,
                full_name,
                created_at
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                telegram_id,
                username,
                full_name,
                now_iso()
            )
        )

        await db.execute(
            """
            UPDATE users
            SET username = ?,
                full_name = ?
            WHERE telegram_id = ?
            """,
            (
                username,
                full_name,
                telegram_id
            )
        )

        await db.commit()

    finally:
        await db.close()


async def update_user(
    telegram_id: int,
    **kwargs
):
    allowed_fields = {
        "username",
        "full_name",
        "site_username",
        "site_password",
        "balance",
        "is_banned",
    }

    if not kwargs:
        return

    invalid = set(kwargs) - allowed_fields

    if invalid:
        raise ValueError(
            "حقول غير مسموحة: "
            + ", ".join(invalid)
        )

    fields = ", ".join(
        f"{key} = ?"
        for key in kwargs
    )

    values = list(kwargs.values())
    values.append(telegram_id)

    db = await get_db()

    try:
        await db.execute(
            f"""
            UPDATE users
            SET {fields}
            WHERE telegram_id = ?
            """,
            values
        )

        await db.commit()

    finally:
        await db.close()


async def add_transaction(
    user_id: int,
    transaction_type: str,
    amount: float,
    note: str = ""
):
    db = await get_db()

    try:
        await db.execute(
            """
            INSERT INTO transactions
            (
                user_id,
                type,
                amount,
                note,
                created_at
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                user_id,
                transaction_type,
                amount,
                note,
                now_iso()
            )
        )

        await db.commit()

    finally:
        await db.close()


# ============================================================
# SETTINGS
# ============================================================

async def get_setting(
    key: str
) -> Optional[str]:

    db = await get_db()

    try:
        cur = await db.execute(
            """
            SELECT value
            FROM admin_settings
            WHERE key = ?
            """,
            (key,)
        )

        row = await cur.fetchone()

        return row["value"] if row else None

    finally:
        await db.close()


async def set_setting(
    key: str,
    value: str
):
    db = await get_db()

    try:
        await db.execute(
            """
            INSERT OR REPLACE INTO
            admin_settings(key, value)
            VALUES (?, ?)
            """,
            (key, value)
        )

        await db.commit()

    finally:
        await db.close()


async def is_bot_active() -> bool:
    value = await get_setting("bot_active")

    return value != "0"


# ============================================================
# PERMISSIONS
# ============================================================

async def is_admin_or_supervisor(
    telegram_id: int,
    required_perm: Optional[str] = None
) -> bool:

    # Main admin
    if telegram_id == ADMIN_USER_ID:
        return True

    db = await get_db()

    try:
        cur = await db.execute(
            """
            SELECT permissions
            FROM supervisors
            WHERE telegram_id = ?
            """,
            (telegram_id,)
        )

        row = await cur.fetchone()

    finally:
        await db.close()

    if not row:
        return False

    try:
        permissions = json.loads(
            row["permissions"] or "[]"
        )

    except Exception:
        permissions = []

    if required_perm is None:
        return True

    return (
        required_perm in permissions
        or "all" in permissions
    )


async def is_banned(
    telegram_id: int
) -> bool:

    user = await get_user(telegram_id)

    return bool(
        user
        and user["is_banned"]
    )


async def ensure_user(
    message: types.Message
):
    await create_user(
        message.from_user.id,
        message.from_user.username or "",
        message.from_user.full_name or ""
    )


async def user_allowed(
    telegram_id: int,
    notify_message: Optional[types.Message] = None
) -> bool:

    # Main admin can always access the bot
    if telegram_id == ADMIN_USER_ID:
        return True

    if await is_banned(telegram_id):

        if notify_message:
            await notify_message.answer(
                "🚫 تم حظر حسابك من استخدام البوت."
            )

        return False

    if not await is_bot_active():

        if notify_message:
            await notify_message.answer(
                "⛔ البوت متوقف حاليًا للصيانة."
            )

        return False

    return True


# ============================================================
# FINANCE
# ============================================================

async def has_pending_finance_request(
    telegram_id: int,
    request_type: str
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
            (
                telegram_id,
                request_type
            )
        )

        row = await cur.fetchone()

        return bool(row)

    finally:
        await db.close()


async def create_finance_request(
    telegram_id: int,
    request_type: str,
    amount: float
) -> int:

    db = await get_db()

    try:
        cur = await db.execute(
            """
            INSERT INTO finance_requests
            (
                telegram_id,
                type,
                amount,
                status,
                created_at
            )
            VALUES (?, ?, ?, 'pending', ?)
            """,
            (
                telegram_id,
                request_type,
                amount,
                now_iso()
            )
        )

        request_id = cur.lastrowid

        await db.commit()

        return request_id

    finally:
        await db.close()


async def process_finance_request(
    request_id: int,
    admin_id: int,
    approve: bool
):

    db = await get_db()

    try:
        await db.execute("BEGIN IMMEDIATE")

        cur = await db.execute(
            """
            SELECT *
            FROM finance_requests
            WHERE id = ?
            """,
            (request_id,)
        )

        request = await cur.fetchone()

        if not request:
            await db.rollback()
            return None, "not_found"

        if request["status"] != "pending":
            await db.rollback()
            return request, "already_processed"

        # ----------------------------------------------------
        # REJECT
        # ----------------------------------------------------

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
                (
                    now_iso(),
                    admin_id,
                    request_id
                )
            )

            await db.commit()

            return request, "rejected"

        # ----------------------------------------------------
        # GET USER
        # ----------------------------------------------------

        telegram_id = request["telegram_id"]
        amount = float(request["amount"])

        user_cur = await db.execute(
            """
            SELECT *
            FROM users
            WHERE telegram_id = ?
            """,
            (telegram_id,)
        )

        user = await user_cur.fetchone()

        if not user:
            await db.rollback()
            return request, "user_not_found"

        current_balance = float(
            user["balance"] or 0
        )

        # ----------------------------------------------------
        # DEPOSIT
        # ----------------------------------------------------

        if request["type"] == "deposit":

            new_balance = (
                current_balance + amount
            )

            await db.execute(
                """
                UPDATE users
                SET balance = ?
                WHERE telegram_id = ?
                """,
                (
                    new_balance,
                    telegram_id
                )
            )

            await db.execute(
                """
                INSERT INTO transactions
                (
                    user_id,
                    type,
                    amount,
                    note,
                    created_at
                )
                VALUES (?, 'deposit', ?, ?, ?)
                """,
                (
                    user["id"],
                    amount,
                    f"approved_request={request_id}",
                    now_iso()
                )
            )

        # ----------------------------------------------------
        # WITHDRAW
        # ----------------------------------------------------

        elif request["type"] == "withdraw":

            if current_balance < amount:

                await db.rollback()

                return request, "insufficient_balance"

            new_balance = (
                current_balance - amount
            )

            await db.execute(
                """
                UPDATE users
                SET balance = ?
                WHERE telegram_id = ?
                """,
                (
                    new_balance,
                    telegram_id
                )
            )

            await db.execute(
                """
                INSERT INTO transactions
                (
                    user_id,
                    type,
                    amount,
                    note,
                    created_at
                )
                VALUES (?, 'withdraw', ?, ?, ?)
                """,
                (
                    user["id"],
                    amount,
                    f"approved_request={request_id}",
                    now_iso()
                )
            )

        else:

            await db.rollback()

            return request, "invalid_type"

        # ----------------------------------------------------
        # MARK APPROVED
        # ----------------------------------------------------

        await db.execute(
            """
            UPDATE finance_requests
            SET status = 'approved',
                processed_at = ?,
                processed_by = ?
            WHERE id = ?
              AND status = 'pending'
            """,
            (
                now_iso(),
                admin_id,
                request_id
            )
        )

        await db.commit()

        return request, "approved"

    except Exception:

        try:
            await db.rollback()
        except Exception:
            pass

        raise

    finally:
        await db.close()


# ============================================================
# GIFT CODES
# ============================================================

async def generate_unique_gift_code(
    amount: float
) -> str:

    for _ in range(30):

        code = generate_code()

        db = await get_db()

        try:
            cur = await db.execute(
                """
                SELECT code
                FROM gift_codes
                WHERE code = ?
                """,
                (code,)
            )

            exists = await cur.fetchone()

            if exists:
                continue

            await db.execute(
                """
                INSERT INTO gift_codes
                (
                    code,
                    amount,
                    created_at
                )
                VALUES (?, ?, ?)
                """,
                (
                    code,
                    amount,
                    now_iso()
                )
            )

            await db.commit()

            return code

        finally:
            await db.close()

    raise RuntimeError(
        "تعذر إنشاء كود هدية فريد."
    )


async def redeem_gift_code(
    telegram_id: int,
    code: str
):

    db = await get_db()

    try:
        await db.execute("BEGIN IMMEDIATE")

        cur = await db.execute(
            """
            SELECT *
            FROM gift_codes
            WHERE code = ?
            """,
            (code,)
        )

        gift = await cur.fetchone()

        if not gift:

            await db.rollback()

            return False, "invalid", 0

        if gift["used_by"] is not None:

            await db.rollback()

            return False, "used", 0

        cur = await db.execute(
            """
            SELECT *
            FROM users
            WHERE telegram_id = ?
            """,
            (telegram_id,)
        )

        user = await cur.fetchone()

        if not user:

            await db.rollback()

            return False, "user_not_found", 0

        amount = float(
            gift["amount"]
        )

        current_balance = float(
            user["balance"] or 0
        )

        new_balance = (
            current_balance + amount
        )

        # Update gift first with condition
        cur = await db.execute(
            """
            UPDATE gift_codes
            SET used_by = ?,
                used_at = ?
            WHERE code = ?
              AND used_by IS NULL
            """,
            (
                telegram_id,
                now_iso(),
                code
            )
        )

        if cur.rowcount != 1:

            await db.rollback()

            return False, "used", 0

        await db.execute(
            """
            UPDATE users
            SET balance = ?
            WHERE telegram_id = ?
            """,
            (
                new_balance,
                telegram_id
            )
        )

        await db.execute(
            """
            INSERT INTO transactions
            (
                user_id,
                type,
                amount,
                note,
                created_at
            )
            VALUES (?, 'gift', ?, ?, ?)
            """,
            (
                user["id"],
                amount,
                f"code={code}",
                now_iso()
            )
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


class DepositFSM(StatesGroup):
    amount = State()


class WithdrawFSM(StatesGroup):
    amount = State()


class GiftFSM(StatesGroup):
    code = State()


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


# ============================================================
# KEYBOARDS
# ============================================================

def main_menu_kb():

    b = InlineKeyboardBuilder()

    b.button(
        text="👤 حسابي",
        callback_data="menu_profile"
    )

    b.button(
        text="🛠 الخدمات",
        callback_data="menu_services"
    )

    b.button(
        text="📊 الإحصائيات",
        callback_data="menu_stats"
    )

    b.button(
        text="🎁 كود هدية",
        callback_data="menu_gift"
    )

    b.adjust(2)

    return b.as_markup()


def services_kb():

    b = InlineKeyboardBuilder()

    b.button(
        text="🆕 إنشاء حساب جديد",
        callback_data="svc_create_account"
    )

    b.button(
        text="💰 شحن الرصيد",
        callback_data="svc_deposit"
    )

    b.button(
        text="🏦 سحب الأموال",
        callback_data="svc_withdraw"
    )

    b.button(
        text="🔙 رجوع",
        callback_data="menu_back"
    )

    b.adjust(2)

    return b.as_markup()


def back_kb(
    callback_data="menu_back"
):

    b = InlineKeyboardBuilder()

    b.button(
        text="🔙 رجوع",
        callback_data=callback_data
    )

    return b.as_markup()


def admin_kb():

    b = InlineKeyboardBuilder()

    b.button(
        text="🎛 لوحة الأدمن",
        callback_data="admin_panel"
    )

    return b.as_markup()


def admin_panel_kb():

    b = InlineKeyboardBuilder()

    b.button(
        text="⚙️ تشغيل/إيقاف البوت",
        callback_data="admin_toggle_bot"
    )

    b.button(
        text="👥 إدارة المستخدمين",
        callback_data="admin_users"
    )

    b.button(
        text="💳 الشحن والسحب",
        callback_data="admin_finance"
    )

    b.button(
        text="🎁 أكواد الهدايا",
        callback_data="admin_gifts"
    )

    b.button(
        text="🛡 المشرفين",
        callback_data="admin_supervisors"
    )

    b.button(
        text="📈 إحصائيات الأدمن",
        callback_data="admin_statistics"
    )

    b.button(
        text="🔙 رجوع",
        callback_data="menu_back"
    )

    b.adjust(2)

    return b.as_markup()


def admin_users_kb():

    b = InlineKeyboardBuilder()

    b.button(
        text="➕ إنشاء حساب لمستخدم",
        callback_data="admin_user_create"
    )

    b.button(
        text="🚫 حظر / فك الحظر",
        callback_data="admin_user_ban"
    )

    b.button(
        text="🔙 رجوع",
        callback_data="admin_panel"
    )

    b.adjust(1)

    return b.as_markup()


def admin_finance_kb():

    b = InlineKeyboardBuilder()

    b.button(
        text="💵 تعديل رصيد مستخدم",
        callback_data="admin_finance_adjust"
    )

    b.button(
        text="📋 الطلبات المعلقة",
        callback_data="admin_finance_pending"
    )

    b.button(
        text="📊 سجل الشحن والسحب",
        callback_data="admin_finance_logs"
    )

    b.button(
        text="🔙 رجوع",
        callback_data="admin_panel"
    )

    b.adjust(1)

    return b.as_markup()


def admin_gifts_kb():

    b = InlineKeyboardBuilder()

    b.button(
        text="➕ إنشاء كود هدية",
        callback_data="admin_gift_create"
    )

    b.button(
        text="📋 قائمة الأكواد",
        callback_data="admin_gift_list"
    )

    b.button(
        text="🔙 رجوع",
        callback_data="admin_panel"
    )

    b.adjust(1)

    return b.as_markup()


def admin_supervisors_kb():

    b = InlineKeyboardBuilder()

    b.button(
        text="➕ إضافة / تحديث مشرف",
        callback_data="admin_sup_add"
    )

    b.button(
        text="📋 قائمة المشرفين",
        callback_data="admin_sup_list"
    )

    b.button(
        text="🗑 حذف مشرف",
        callback_data="admin_sup_delete"
    )

    b.button(
        text="🔙 رجوع",
        callback_data="admin_panel"
    )

    b.adjust(1)

    return b.as_markup()


def finance_request_kb(
    request_id: int
):

    b = InlineKeyboardBuilder()

    b.button(
        text="✅ موافقة",
        callback_data=f"finance_approve:{request_id}"
    )

    b.button(
        text="❌ رفض",
        callback_data=f"finance_reject:{request_id}"
    )

    b.adjust(2)

    return b.as_markup()


def gift_item_kb(code: str):

    b = InlineKeyboardBuilder()

    b.button(
        text="🗑 حذف",
        callback_data=f"gift_delete:{code}"
    )

    return b.as_markup()


# ============================================================
# START
# ============================================================

@dp.message(Command("start"))
async def cmd_start(
    message: types.Message,
    state: FSMContext
):

    await state.clear()

    await ensure_user(message)

    if not await user_allowed(
        message.from_user.id,
        message
    ):
        return

    name = esc(
        message.from_user.first_name
        or "صديقي"
    )

    await message.answer(
        f"أهلاً {name}! 👋\n\n"
        "اختر من القائمة:",
        reply_markup=main_menu_kb()
    )

    if await is_admin_or_supervisor(
        message.from_user.id
    ):

        await message.answer(
            "🎛 لديك صلاحية إدارية.",
            reply_markup=admin_kb()
        )


# ============================================================
# MAIN MENU
# ============================================================

@dp.callback_query(F.data == "menu_back")
async def menu_back(
    cb: types.CallbackQuery,
    state: FSMContext
):

    await state.clear()

    if not await user_allowed(
        cb.from_user.id
    ):

        await cb.answer(
            "البوت متوقف أو الحساب محظور.",
            show_alert=True
        )

        return

    await cb.answer()

    try:

        await cb.message.edit_text(
            "🏠 القائمة الرئيسية:",
            reply_markup=main_menu_kb()
        )

    except Exception:

        await cb.message.answer(
            "🏠 القائمة الرئيسية:",
            reply_markup=main_menu_kb()
        )


@dp.callback_query(F.data == "menu_profile")
async def menu_profile(
    cb: types.CallbackQuery
):

    if not await user_allowed(
        cb.from_user.id
    ):

        await cb.answer(
            "غير مسموح باستخدام البوت.",
            show_alert=True
        )

        return

    user = await get_user(
        cb.from_user.id
    )

    if not user:

        await create_user(
            cb.from_user.id,
            cb.from_user.username or "",
            cb.from_user.full_name or ""
        )

        user = await get_user(
            cb.from_user.id
        )

    text = (
        "👤 <b>حسابك</b>\n\n"
        f"الاسم: {esc(user['full_name'])}\n"
        f"Telegram ID: "
        f"<code>{user['telegram_id']}</code>\n"
        f"اسم الموقع: "
        f"<code>{esc(user['site_username'] or 'غير مرتبط')}</code>\n"
        f"الرصيد: "
        f"<b>{money(user['balance'])}</b>"
    )

    await cb.answer()

    await cb.message.edit_text(
        text,
        reply_markup=back_kb()
    )


@dp.callback_query(F.data == "menu_services")
async def menu_services(
    cb: types.CallbackQuery
):

    if not await user_allowed(
        cb.from_user.id
    ):

        await cb.answer(
            "غير مسموح باستخدام البوت.",
            show_alert=True
        )

        return

    await cb.answer()

    await cb.message.edit_text(
        "🛠 <b>الخدمات</b>\n\n"
        "اختر الخدمة المطلوبة:",
        reply_markup=services_kb()
    )


@dp.callback_query(F.data == "menu_stats")
async def menu_stats(
    cb: types.CallbackQuery
):

    if not await user_allowed(
        cb.from_user.id
    ):

        await cb.answer(
            "غير مسموح باستخدام البوت.",
            show_alert=True
        )

        return

    db = await get_db()

    try:

        cur = await db.execute(
            """
            SELECT COUNT(*) AS count
            FROM users
            """
        )

        total_users = (
            await cur.fetchone()
        )["count"]

        cur = await db.execute(
            """
            SELECT COALESCE(
                SUM(balance), 0
            ) AS total
            FROM users
            """
        )

        total_balance = (
            await cur.fetchone()
        )["total"]

    finally:

        await db.close()

    text = (
        "📊 <b>الإحصائيات العامة</b>\n\n"
        f"👥 إجمالي المستخدمين: "
        f"{total_users}\n"
        f"💰 إجمالي الأرصدة: "
        f"{money(total_balance)}"
    )

    await cb.answer()

    await cb.message.edit_text(
        text,
        reply_markup=back_kb()
    )


# ============================================================
# GIFT USER
# ============================================================

@dp.callback_query(F.data == "menu_gift")
async def menu_gift(
    cb: types.CallbackQuery,
    state: FSMContext
):

    if not await user_allowed(
        cb.from_user.id
    ):

        await cb.answer(
            "غير مسموح باستخدام البوت.",
            show_alert=True
        )

        return

    await cb.answer()

    await state.set_state(
        GiftFSM.code
    )

    await cb.message.answer(
        "🎁 أرسل كود الهدية "
        "المكون من 8 أحرف/أرقام:"
    )


@dp.message(GiftFSM.code)
async def gift_code_submit(
    message: types.Message,
    state: FSMContext
):

    if not await user_allowed(
        message.from_user.id,
        message
    ):
        return

    raw_code = (
        message.text or ""
    ).strip().upper()

    if (
        len(raw_code) != 8
        or not all(
            char in string.ascii_uppercase
            + string.digits
            for char in raw_code
        )
    ):

        await message.answer(
            "❌ الكود غير صالح.\n"
            "يجب أن يكون 8 أحرف أو أرقام."
        )

        return

    success, status, amount = (
        await redeem_gift_code(
            message.from_user.id,
            raw_code
        )
    )

    if not success:

        messages = {
            "invalid": "❌ كود غير صالح.",
            "used": "⚠️ هذا الكود مستخدم مسبقًا.",
            "user_not_found":
                "❌ المستخدم غير موجود.",
        }

        await message.answer(
            messages.get(
                status,
                "❌ تعذر استخدام الكود."
            )
        )

        return

    user = await get_user(
        message.from_user.id
    )

    await message.answer(
        "🎉 <b>تم استخدام كود الهدية بنجاح!</b>\n\n"
        f"💰 المبلغ المضاف: "
        f"{money(amount)}\n"
        f"💳 رصيدك الجديد: "
        f"{money(user['balance'])}",
        reply_markup=main_menu_kb()
    )

    await state.clear()


# ============================================================
# CREATE SITE ACCOUNT
# ============================================================

@dp.callback_query(F.data == "svc_create_account")
async def svc_create_account(
    cb: types.CallbackQuery,
    state: FSMContext
):

    if not await user_allowed(
        cb.from_user.id
    ):

        await cb.answer(
            "غير مسموح باستخدام البوت.",
            show_alert=True
        )

        return

    await cb.answer()

    await state.set_state(
        RegisterFSM.site_username
    )

    await cb.message.answer(
        "🆕 أرسل اسم المستخدم "
        "الذي تريد ربطه بحساب الموقع:"
    )


@dp.message(RegisterFSM.site_username)
async def reg_site_username(
    message: types.Message,
    state: FSMContext
):

    if not await user_allowed(
        message.from_user.id,
        message
    ):
        return

    username = (
        message.text or ""
    ).strip()

    if len(username) < 3 or len(username) > 32:

        await message.answer(
            "❌ اسم المستخدم يجب أن يكون "
            "بين 3 و32 حرفًا."
        )

        return

    if any(
        char.isspace()
        for char in username
    ):

        await message.answer(
            "❌ اسم المستخدم لا يجب "
            "أن يحتوي على مسافات."
        )

        return

    existing = await get_user(
        message.from_user.id
    )

    if (
        existing
        and existing["site_username"]
    ):

        await message.answer(
            "⚠️ لديك حساب موقع مرتبط بالفعل.\n"
            f"اسم المستخدم: "
            f"<code>{esc(existing['site_username'])}</code>\n\n"
            "لاستبداله، استخدم لوحة الإدارة."
        )

        await state.clear()

        return

    password = generate_password()

    await update_user(
        message.from_user.id,
        site_username=username,
        site_password=password
    )

    user = await get_user(
        message.from_user.id
    )

    await add_transaction(
        user["id"],
        "register",
        0,
        f"site_user={username}"
    )

    await message.answer(
        "✅ <b>تم إنشاء بيانات الحساب بنجاح!</b>\n\n"
        f"👤 اسم المستخدم: "
        f"<code>{esc(username)}</code>\n"
        f"🔑 كلمة المرور: "
        f"<code>{esc(password)}</code>\n\n"
        "⚠️ احتفظ بكلمة المرور في مكان آمن.",
        reply_markup=main_menu_kb()
    )

    await state.clear()


# ============================================================
# DEPOSIT
# ============================================================

@dp.callback_query(F.data == "svc_deposit")
async def svc_deposit(
    cb: types.CallbackQuery,
    state: FSMContext
):

    if not await user_allowed(
        cb.from_user.id
    ):

        await cb.answer(
            "غير مسموح باستخدام البوت.",
            show_alert=True
        )

        return

    await cb.answer()

    await state.set_state(
        DepositFSM.amount
    )

    await cb.message.answer(
        "💰 أرسل المبلغ الذي تريد شحنه:"
    )


@dp.message(DepositFSM.amount)
async def deposit_amount(
    message: types.Message,
    state: FSMContext
):

    if not await user_allowed(
        message.from_user.id,
        message
    ):
        return

    try:

        amount = float(
            (message.text or "").strip()
        )

        if not valid_amount(amount):
            raise ValueError

    except Exception:

        await message.answer(
            "❌ مبلغ غير صالح.\n"
            f"أرسل مبلغًا أكبر من 0 "
            f"ولا يتجاوز {MAX_AMOUNT}."
        )

        return

    if await has_pending_finance_request(
        message.from_user.id,
        "deposit"
    ):

        await message.answer(
            "⚠️ لديك بالفعل طلب شحن "
            "معلق قيد المراجعة."
        )

        return

    request_id = await create_finance_request(
        message.from_user.id,
        "deposit",
        amount
    )

    await message.answer(
        "📨 <b>تم إرسال طلب الشحن.</b>\n\n"
        f"💰 المبلغ: <b>{money(amount)}</b>\n"
        f"🆔 رقم الطلب: #{request_id}\n\n"
        "سيتم إضافة المبلغ بعد موافقة الإدارة.",
        reply_markup=main_menu_kb()
    )

    try:

        await bot.send_message(
            ADMIN_USER_ID,
            "💰 <b>طلب شحن جديد</b>\n\n"
            f"👤 المستخدم: "
            f"<code>{message.from_user.id}</code>\n"
            f"💵 المبلغ: "
            f"<b>{money(amount)}</b>\n"
            f"🆔 الطلب: #{request_id}",
            reply_markup=finance_request_kb(
                request_id
            )
        )

    except Exception as exc:

        print(
            "تعذر إرسال إشعار الشحن للأدمن:",
            exc
        )

    await state.clear()


# ============================================================
# WITHDRAW
# ============================================================

@dp.callback_query(F.data == "svc_withdraw")
async def svc_withdraw(
    cb: types.CallbackQuery,
    state: FSMContext
):

    if not await user_allowed(
        cb.from_user.id
    ):

        await cb.answer(
            "غير مسموح باستخدام البوت.",
            show_alert=True
        )

        return

    await cb.answer()

    await state.set_state(
        WithdrawFSM.amount
    )

    await cb.message.answer(
        "🏦 أرسل المبلغ الذي تريد سحبه:"
    )


@dp.message(WithdrawFSM.amount)
async def withdraw_amount(
    message: types.Message,
    state: FSMContext
):

    if not await user_allowed(
        message.from_user.id,
        message
    ):
        return

    try:

        amount = float(
            (message.text or "").strip()
        )

        if not valid_amount(amount):
            raise ValueError

    except Exception:

        await message.answer(
            "❌ مبلغ غير صالح."
        )

        return

    user = await get_user(
        message.from_user.id
    )

    if not user:

        await message.answer(
            "❌ تعذر العثور على حسابك."
        )

        await state.clear()

        return

    if float(user["balance"] or 0) < amount:

        await message.answer(
            "❌ الرصيد غير كافٍ.\n"
            f"رصيدك الحالي: "
            f"{money(user['balance'])}"
        )

        return

    if await has_pending_finance_request(
        message.from_user.id,
        "withdraw"
    ):

        await message.answer(
            "⚠️ لديك بالفعل طلب سحب "
            "معلق قيد المراجعة."
        )

        return

    request_id = await create_finance_request(
        message.from_user.id,
        "withdraw",
        amount
    )

    await message.answer(
        "📨 <b>تم إرسال طلب السحب.</b>\n\n"
        f"💵 المبلغ: <b>{money(amount)}</b>\n"
        f"🆔 رقم الطلب: #{request_id}\n\n"
        "سيتم خصم المبلغ بعد موافقة الإدارة.",
        reply_markup=main_menu_kb()
    )

    try:

        await bot.send_message(
            ADMIN_USER_ID,
            "🏦 <b>طلب سحب جديد</b>\n\n"
            f"👤 المستخدم: "
            f"<code>{message.from_user.id}</code>\n"
            f"💵 المبلغ: "
            f"<b>{money(amount)}</b>\n"
            f"🆔 الطلب: #{request_id}",
            reply_markup=finance_request_kb(
                request_id
            )
        )

    except Exception as exc:

        print(
            "تعذر إرسال إشعار السحب للأدمن:",
            exc
        )

    await state.clear()


# ============================================================
# ADMIN PANEL
# ============================================================

@dp.callback_query(F.data == "admin_panel")
async def admin_panel(
    cb: types.CallbackQuery
):

    if not await is_admin_or_supervisor(
        cb.from_user.id
    ):

        await cb.answer(
            "غير مصرّح.",
            show_alert=True
        )

        return

    await cb.answer()

    await cb.message.edit_text(
        "🎛 <b>لوحة الإدارة</b>\n\n"
        "اختر القسم:",
        reply_markup=admin_panel_kb()
    )


# ============================================================
# TOGGLE BOT
# ============================================================

@dp.callback_query(F.data == "admin_toggle_bot")
async def admin_toggle_bot(
    cb: types.CallbackQuery
):

    if not await is_admin_or_supervisor(
        cb.from_user.id,
        "all"
    ):

        await cb.answer(
            "غير مصرّح.",
            show_alert=True
        )

        return

    current = await is_bot_active()

    new_value = (
        "0"
        if current
        else "1"
    )

    await set_setting(
        "bot_active",
        new_value
    )

    await cb.answer(
        (
            "تم إيقاف البوت."
            if new_value == "0"
            else "تم تشغيل البوت."
        ),
        show_alert=True
    )


# ============================================================
# ADMIN USERS
# ============================================================

@dp.callback_query(F.data == "admin_users")
async def admin_users(
    cb: types.CallbackQuery
):

    if not await is_admin_or_supervisor(
        cb.from_user.id
    ):

        await cb.answer(
            "غير مصرّح.",
            show_alert=True
        )

        return

    await cb.answer()

    await cb.message.edit_text(
        "👥 <b>إدارة المستخدمين</b>",
        reply_markup=admin_users_kb()
    )


@dp.callback_query(F.data == "admin_user_create")
async def admin_user_create(
    cb: types.CallbackQuery,
    state: FSMContext
):

    if not await is_admin_or_supervisor(
        cb.from_user.id,
        "users"
    ):

        await cb.answer(
            "غير مصرّح.",
            show_alert=True
        )

        return

    await cb.answer()

    await state.set_state(
        AdminCreateUserFSM.telegram_id
    )

    await cb.message.answer(
        "أرسل Telegram ID للمستخدم:"
    )


@dp.message(AdminCreateUserFSM.telegram_id)
async def admin_create_user_tid(
    message: types.Message,
    state: FSMContext
):

    if not await is_admin_or_supervisor(
        message.from_user.id,
        "users"
    ):

        await state.clear()

        return

    try:

        telegram_id = int(
            (message.text or "").strip()
        )

        if telegram_id <= 0:
            raise ValueError

    except Exception:

        await message.answer(
            "❌ Telegram ID غير صالح."
        )

        return

    await state.update_data(
        telegram_id=telegram_id
    )

    await state.set_state(
        AdminCreateUserFSM.site_username
    )

    await message.answer(
        "أرسل اسم المستخدم للموقع:"
    )


@dp.message(AdminCreateUserFSM.site_username)
async def admin_create_user_uname(
    message: types.Message,
    state: FSMContext
):

    if not await is_admin_or_supervisor(
        message.from_user.id,
        "users"
    ):

        await state.clear()

        return

    site_username = (
        message.text or ""
    ).strip()

    if (
        len(site_username) < 3
        or len(site_username) > 32
        or any(
            char.isspace()
            for char in site_username
        )
    ):

        await message.answer(
            "❌ اسم المستخدم يجب أن يكون "
            "بين 3 و32 حرفًا وبدون مسافات."
        )

        return

    data = await state.get_data()

    telegram_id = data["telegram_id"]

    existing = await get_user(
        telegram_id
    )

    if (
        existing
        and existing["site_username"]
    ):

        await message.answer(
            "⚠️ هذا المستخدم لديه "
            "حساب موقع بالفعل."
        )

        await state.clear()

        return

    await create_user(
        telegram_id,
        "",
        f"User-{telegram_id}"
    )

    password = generate_password()

    await update_user(
        telegram_id,
        site_username=site_username,
        site_password=password
    )

    user = await get_user(
        telegram_id
    )

    await add_transaction(
        user["id"],
        "register",
        0,
        f"admin_created site_user={site_username}"
    )

    await message.answer(
        "✅ <b>تم إنشاء الحساب.</b>\n\n"
        f"🆔 Telegram ID: "
        f"<code>{telegram_id}</code>\n"
        f"👤 Username: "
        f"<code>{esc(site_username)}</code>\n"
        f"🔑 Password: "
        f"<code>{esc(password)}</code>",
        reply_markup=admin_users_kb()
    )

    await state.clear()


# ============================================================
# ADMIN BAN
# ============================================================

@dp.callback_query(F.data == "admin_user_ban")
async def admin_user_ban(
    cb: types.CallbackQuery,
    state: FSMContext
):

    if not await is_admin_or_supervisor(
        cb.from_user.id,
        "users"
    ):

        await cb.answer(
            "غير مصرّح.",
            show_alert=True
        )

        return

    await cb.answer()

    await state.set_state(
        AdminBanFSM.telegram_id
    )

    await cb.message.answer(
        "أرسل Telegram ID للحظر "
        "أو فك الحظر:"
    )


@dp.message(AdminBanFSM.telegram_id)
async def admin_ban_user(
    message: types.Message,
    state: FSMContext
):

    if not await is_admin_or_supervisor(
        message.from_user.id,
        "users"
    ):

        await state.clear()

        return

    try:

        telegram_id = int(
            (message.text or "").strip()
        )

    except Exception:

        await message.answer(
            "❌ ID غير صالح."
        )

        return

    if telegram_id == ADMIN_USER_ID:

        await message.answer(
            "❌ لا يمكن حظر الأدمن الرئيسي."
        )

        await state.clear()

        return

    user = await get_user(
        telegram_id
    )

    if not user:

        await message.answer(
            "❌ المستخدم غير موجود."
        )

        return

    new_status = (
        0
        if user["is_banned"]
        else 1
    )

    await update_user(
        telegram_id,
        is_banned=new_status
    )

    if new_status:

        status_text = (
            "تم حظر المستخدم 🚫"
        )

    else:

        status_text = (
            "تم فك حظر المستخدم ✅"
        )

    await message.answer(
        f"{status_text}\n"
        f"Telegram ID: "
        f"<code>{telegram_id}</code>",
        reply_markup=admin_users_kb()
    )

    await state.clear()


# ============================================================
# ADMIN FINANCE
# ============================================================

@dp.callback_query(F.data == "admin_finance")
async def admin_finance(
    cb: types.CallbackQuery
):

    if not await is_admin_or_supervisor(
        cb.from_user.id
    ):

        await cb.answer(
            "غير مصرّح.",
            show_alert=True
        )

        return

    await cb.answer()

    await cb.message.edit_text(
        "💳 <b>الشحن والسحب</b>",
        reply_markup=admin_finance_kb()
    )


@dp.callback_query(F.data == "admin_finance_adjust")
async def admin_finance_adjust(
    cb: types.CallbackQuery,
    state: FSMContext
):

    if not await is_admin_or_supervisor(
        cb.from_user.id,
        "finance"
    ):

        await cb.answer(
            "غير مصرّح.",
            show_alert=True
        )

        return

    await cb.answer()

    await state.set_state(
        AdminAdjustBalanceFSM.telegram_id
    )

    await cb.message.answer(
        "أرسل Telegram ID للمستخدم:"
    )


@dp.message(AdminAdjustBalanceFSM.telegram_id)
async def admin_adjust_tid(
    message: types.Message,
    state: FSMContext
):

    if not await is_admin_or_supervisor(
        message.from_user.id,
        "finance"
    ):

        await state.clear()

        return

    try:

        telegram_id = int(
            (message.text or "").strip()
        )

    except Exception:

        await message.answer(
            "❌ ID غير صالح."
        )

        return

    user = await get_user(
        telegram_id
    )

    if not user:

        await message.answer(
            "❌ المستخدم غير موجود."
        )

        return

    await state.update_data(
        telegram_id=telegram_id
    )

    await state.set_state(
        AdminAdjustBalanceFSM.amount
    )

    await message.answer(
        "أرسل مقدار التعديل.\n\n"
        "مثال:\n"
        "<code>+100</code> لإضافة 100\n"
        "<code>-50</code> لخصم 50"
    )


@dp.message(AdminAdjustBalanceFSM.amount)
async def admin_adjust_amount(
    message: types.Message,
    state: FSMContext
):

    if not await is_admin_or_supervisor(
        message.from_user.id,
        "finance"
    ):

        await state.clear()

        return

    try:

        amount = float(
            (message.text or "").strip()
        )

        if amount == 0:
            raise ValueError

        if abs(amount) > MAX_AMOUNT:
            raise ValueError

    except Exception:

        await message.answer(
            "❌ أرسل رقمًا صحيحًا "
            f"ولا يتجاوز {MAX_AMOUNT}."
        )

        return

    data = await state.get_data()

    telegram_id = data["telegram_id"]

    db = await get_db()

    try:

        await db.execute(
            "BEGIN IMMEDIATE"
        )

        cur = await db.execute(
            """
            SELECT *
            FROM users
            WHERE telegram_id = ?
            """,
            (telegram_id,)
        )

        user = await cur.fetchone()

        if not user:

            await db.rollback()

            await message.answer(
                "❌ المستخدم غير موجود."
            )

            await state.clear()

            return

        old_balance = float(
            user["balance"] or 0
        )

        new_balance = (
            old_balance + amount
        )

        if new_balance < 0:

            await db.rollback()

            await message.answer(
                "❌ لا يمكن أن يصبح "
                "الرصيد سالبًا."
            )

            return

        await db.execute(
            """
            UPDATE users
            SET balance = ?
            WHERE telegram_id = ?
            """,
            (
                new_balance,
                telegram_id
            )
        )

        await db.execute(
            """
            INSERT INTO transactions
            (
                user_id,
                type,
                amount,
                note,
                created_at
            )
            VALUES (
                ?,
                'admin_adjust',
                ?,
                ?,
                ?
            )
            """,
            (
                user["id"],
                amount,
                f"admin={message.from_user.id}",
                now_iso()
            )
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

    await message.answer(
        "✅ <b>تم تعديل الرصيد.</b>\n\n"
        f"الرصيد السابق: "
        f"{money(old_balance)}\n"
        f"التعديل: "
        f"{money(amount)}\n"
        f"الرصيد الجديد: "
        f"{money(new_balance)}",
        reply_markup=admin_finance_kb()
    )

    try:

        await bot.send_message(
            telegram_id,
            "💳 <b>تم تعديل رصيدك من الإدارة.</b>\n\n"
            f"التعديل: "
            f"{money(amount)}\n"
            f"الرصيد الجديد: "
            f"{money(new_balance)}"
        )

    except Exception as exc:

        print(
            "تعذر إرسال إشعار تعديل الرصيد:",
            exc
        )

    await state.clear()


# ============================================================
# PENDING FINANCE
# ============================================================

@dp.callback_query(F.data == "admin_finance_pending")
async def admin_finance_pending(
    cb: types.CallbackQuery
):

    if not await is_admin_or_supervisor(
        cb.from_user.id,
        "finance"
    ):

        await cb.answer(
            "غير مصرّح.",
            show_alert=True
        )

        return

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

        await cb.message.edit_text(
            "📭 لا توجد طلبات مالية معلقة.",
            reply_markup=back_kb(
                "admin_finance"
            )
        )

        return

    await cb.answer()

    await cb.message.edit_text(
        f"📋 <b>الطلبات المعلقة:</b> "
        f"{len(rows)}"
    )

    for row in rows:

        request_type = (
            "💰 شحن"
            if row["type"] == "deposit"
            else "🏦 سحب"
        )

        text = (
            f"{request_type}\n"
            f"🆔 الطلب: #{row['id']}\n"
            f"👤 User ID: "
            f"<code>{row['telegram_id']}</code>\n"
            f"💵 المبلغ: "
            f"<b>{money(row['amount'])}</b>\n"
            f"🕐 {esc(row['created_at'])}"
        )

        try:

            await cb.message.answer(
                text,
                reply_markup=finance_request_kb(
                    row["id"]
                )
            )

        except Exception as exc:

            print(
                "تعذر عرض طلب مالي:",
                exc
            )


# ============================================================
# APPROVE FINANCE
# ============================================================

@dp.callback_query(
    F.data.startswith("finance_approve:")
)
async def finance_approve(
    cb: types.CallbackQuery
):

    if not await is_admin_or_supervisor(
        cb.from_user.id,
        "finance"
    ):

        await cb.answer(
            "غير مصرّح.",
            show_alert=True
        )

        return

    try:

        request_id = int(
            cb.data.split(":")[1]
        )

    except Exception:

        await cb.answer(
            "طلب غير صالح.",
            show_alert=True
        )

        return

    request, status = (
        await process_finance_request(
            request_id,
            cb.from_user.id,
            True
        )
    )

    if status == "approved":

        await cb.answer(
            "تمت الموافقة.",
            show_alert=True
        )

        try:

            await cb.message.edit_reply_markup(
                reply_markup=None
            )

        except Exception:
            pass

        request_type = (
            "شحن"
            if request["type"] == "deposit"
            else "سحب"
        )

        try:

            await bot.send_message(
                request["telegram_id"],
                f"✅ تمت الموافقة على "
                f"طلب {request_type}.\n"
                f"💵 المبلغ: "
                f"{money(request['amount'])}\n"
                f"🆔 الطلب: #{request_id}"
            )

        except Exception as exc:

            print(
                "تعذر إرسال إشعار الموافقة:",
                exc
            )

    elif status == "already_processed":

        await cb.answer(
            "تمت معالجة الطلب مسبقًا.",
            show_alert=True
        )

    elif status == "insufficient_balance":

        await cb.answer(
            "رصيد المستخدم لم يعد كافيًا.",
            show_alert=True
        )

    else:

        await cb.answer(
            "تعذر معالجة الطلب.",
            show_alert=True
        )


# ============================================================
# REJECT FINANCE
# ============================================================

@dp.callback_query(
    F.data.startswith("finance_reject:")
)
async def finance_reject(
    cb: types.CallbackQuery
):

    if not await is_admin_or_supervisor(
        cb.from_user.id,
        "finance"
    ):

        await cb.answer(
            "غير مصرّح.",
            show_alert=True
        )

        return

    try:

        request_id = int(
            cb.data.split(":")[1]
        )

    except Exception:

        await cb.answer(
            "طلب غير صالح.",
            show_alert=True
        )

        return

    request, status = (
        await process_finance_request(
            request_id,
            cb.from_user.id,
            False
        )
    )

    if status == "rejected":

        await cb.answer(
            "تم رفض الطلب.",
            show_alert=True
        )

        try:

            await cb.message.edit_reply_markup(
                reply_markup=None
            )

        except Exception:
            pass

        try:

            await bot.send_message(
                request["telegram_id"],
                "❌ تم رفض طلبك المالي.\n"
                f"💵 المبلغ: "
                f"{money(request['amount'])}\n"
                f"🆔 الطلب: #{request_id}"
            )

        except Exception as exc:

            print(
                "تعذر إرسال إشعار الرفض:",
                exc
            )

    elif status == "already_processed":

        await cb.answer(
            "تمت معالجة الطلب مسبقًا.",
            show_alert=True
        )

    else:

        await cb.answer(
            "تعذر معالجة الطلب.",
            show_alert=True
        )


# ============================================================
# FINANCE LOGS
# ============================================================

@dp.callback_query(F.data == "admin_finance_logs")
async def admin_finance_logs(
    cb: types.CallbackQuery
):

    if not await is_admin_or_supervisor(
        cb.from_user.id,
        "finance"
    ):

        await cb.answer(
            "غير مصرّح.",
            show_alert=True
        )

        return

    db = await get_db()

    try:

        cur = await db.execute(
            """
            SELECT
                t.*,
                u.telegram_id
            FROM transactions t
            JOIN users u
                ON u.id = t.user_id
            WHERE t.type IN (
                'deposit',
                'withdraw',
                'admin_adjust'
            )
            ORDER BY t.id DESC
            LIMIT 30
            """
        )

        rows = await cur.fetchall()

    finally:

        await db.close()

    if not rows:

        text = (
            "📭 لا توجد عمليات مالية."
        )

    else:

        lines = [
            "📊 <b>آخر العمليات المالية</b>\n"
        ]

        for row in rows:

            type_name = {
                "deposit": "💰 شحن",
                "withdraw": "🏦 سحب",
                "admin_adjust":
                    "🛠 تعديل إداري"
            }.get(
                row["type"],
                row["type"]
            )

            lines.append(
                f"{type_name} | "
                f"<code>{row['telegram_id']}</code> | "
                f"{money(row['amount'])}\n"
                f"🕐 {esc(row['created_at'])}"
            )

        text = "\n\n".join(lines)

    await cb.answer()

    await cb.message.edit_text(
        text,
        reply_markup=back_kb(
            "admin_finance"
        )
    )


# ============================================================
# ADMIN GIFTS
# ============================================================

@dp.callback_query(F.data == "admin_gifts")
async def admin_gifts(
    cb: types.CallbackQuery
):

    if not await is_admin_or_supervisor(
        cb.from_user.id
    ):

        await cb.answer(
            "غير مصرّح.",
            show_alert=True
        )

        return

    await cb.answer()

    await cb.message.edit_text(
        "🎁 <b>أكواد الهدايا</b>",
        reply_markup=admin_gifts_kb()
    )


@dp.callback_query(F.data == "admin_gift_create")
async def admin_gift_create(
    cb: types.CallbackQuery,
    state: FSMContext
):

    if not await is_admin_or_supervisor(
        cb.from_user.id,
        "gifts"
    ):

        await cb.answer(
            "غير مصرّح.",
            show_alert=True
        )

        return

    await cb.answer()

    await state.set_state(
        AdminGiftCodeFSM.amount
    )

    await cb.message.answer(
        "🎁 أرسل قيمة كود الهدية:"
    )


@dp.message(AdminGiftCodeFSM.amount)
async def admin_gift_create_amount(
    message: types.Message,
    state: FSMContext
):

    if not await is_admin_or_supervisor(
        message.from_user.id,
        "gifts"
    ):

        await state.clear()

        return

    try:

        amount = float(
            (message.text or "").strip()
        )

        if not valid_amount(amount):
            raise ValueError

    except Exception:

        await message.answer(
            "❌ مبلغ غير صالح."
        )

        return

    code = await generate_unique_gift_code(
        amount
    )

    await message.answer(
        "🎁 <b>تم إنشاء كود الهدية.</b>\n\n"
        f"🔑 الكود: <code>{code}</code>\n"
        f"💰 القيمة: "
        f"<b>{money(amount)}</b>",
        reply_markup=admin_gifts_kb()
    )

    await state.clear()


@dp.callback_query(F.data == "admin_gift_list")
async def admin_gift_list(
    cb: types.CallbackQuery
):

    if not await is_admin_or_supervisor(
        cb.from_user.id,
        "gifts"
    ):

        await cb.answer(
            "غير مصرّح.",
            show_alert=True
        )

        return

    db = await get_db()

    try:

        cur = await db.execute(
            """
            SELECT *
            FROM gift_codes
            ORDER BY created_at DESC
            LIMIT 50
            """
        )

        rows = await cur.fetchall()

    finally:

        await db.close()

    if not rows:

        await cb.answer()

        await cb.message.edit_text(
            "📭 لا توجد أكواد.",
            reply_markup=back_kb(
                "admin_gifts"
            )
        )

        return

    await cb.answer()

    await cb.message.edit_text(
        "📋 <b>قائمة أكواد الهدايا</b>"
    )

    for row in rows:

        if row["used_by"]:

            status = (
                "❌ مستخدم بواسطة "
                f"<code>{row['used_by']}</code>"
            )

        else:

            status = "✅ غير مستخدم"

        text = (
            f"🎁 <code>{esc(row['code'])}</code>\n"
            f"💰 القيمة: "
            f"{money(row['amount'])}\n"
            f"{status}\n"
            f"🕐 {esc(row['created_at'])}"
        )

        await cb.message.answer(
            text,
            reply_markup=gift_item_kb(
                row["code"]
            )
        )


@dp.callback_query(
    F.data.startswith("gift_delete:")
)
async def gift_delete(
    cb: types.CallbackQuery
):

    if not await is_admin_or_supervisor(
        cb.from_user.id,
        "gifts"
    ):

        await cb.answer(
            "غير مصرّح.",
            show_alert=True
        )

        return

    code = cb.data.split(
        ":",
        1
    )[1]

    db = await get_db()

    try:

        cur = await db.execute(
            """
            SELECT used_by
            FROM gift_codes
            WHERE code = ?
            """,
            (code,)
        )

        row = await cur.fetchone()

        if not row:

            await cb.answer(
                "الكود غير موجود.",
                show_alert=True
            )

            return

        if row["used_by"]:

            await cb.answer(
                "لا يمكن حذف كود مستخدم.",
                show_alert=True
            )

            return

        await db.execute(
            """
            DELETE FROM gift_codes
            WHERE code = ?
              AND used_by IS NULL
            """,
            (code,)
        )

        await db.commit()

    finally:

        await db.close()

    await cb.answer(
        "تم حذف الكود.",
        show_alert=True
    )

    try:

        await cb.message.edit_reply_markup(
            reply_markup=None
        )

    except Exception:
        pass


# ============================================================
# ADMIN SUPERVISORS
# ============================================================

@dp.callback_query(F.data == "admin_supervisors")
async def admin_supervisors(
    cb: types.CallbackQuery
):

    if cb.from_user.id != ADMIN_USER_ID:

        await cb.answer(
            "هذه الخاصية للأدمن الرئيسي فقط.",
            show_alert=True
        )

        return

    await cb.answer()

    await cb.message.edit_text(
        "🛡 <b>إدارة المشرفين</b>",
        reply_markup=admin_supervisors_kb()
    )


@dp.callback_query(F.data == "admin_sup_add")
async def admin_sup_add(
    cb: types.CallbackQuery,
    state: FSMContext
):

    if cb.from_user.id != ADMIN_USER_ID:

        await cb.answer(
            "للأدمن الرئيسي فقط.",
            show_alert=True
        )

        return

    await cb.answer()

    await state.set_state(
        AdminSupervisorFSM.telegram_id
    )

    await cb.message.answer(
        "أرسل Telegram ID للمشرف:"
    )


@dp.message(AdminSupervisorFSM.telegram_id)
async def admin_sup_tid(
    message: types.Message,
    state: FSMContext
):

    if message.from_user.id != ADMIN_USER_ID:

        await state.clear()

        return

    try:

        telegram_id = int(
            (message.text or "").strip()
        )

        if telegram_id <= 0:
            raise ValueError

    except Exception:

        await message.answer(
            "❌ ID غير صالح."
        )

        return

    if telegram_id == ADMIN_USER_ID:

        await message.answer(
            "ℹ️ هذا هو الأدمن الرئيسي بالفعل."
        )

        await state.clear()

        return

    await state.update_data(
        telegram_id=telegram_id
    )

    await state.set_state(
        AdminSupervisorFSM.permissions
    )

    await message.answer(
        "أرسل الصلاحيات مفصولة بفاصلة.\n\n"
        "الصلاحيات المتاحة:\n"
        "<code>users</code> - المستخدمين\n"
        "<code>finance</code> - المالية\n"
        "<code>gifts</code> - الهدايا\n"
        "<code>all</code> - كل الصلاحيات\n\n"
        "مثال:\n"
        "<code>users,finance</code>"
    )


@dp.message(AdminSupervisorFSM.permissions)
async def admin_sup_permissions(
    message: types.Message,
    state: FSMContext
):

    if message.from_user.id != ADMIN_USER_ID:

        await state.clear()

        return

    raw = (
        message.text or ""
    ).strip().lower()

    permissions = [
        p.strip()
        for p in raw.split(",")
        if p.strip()
    ]

    if not permissions:

        await message.answer(
            "❌ يجب تحديد صلاحية واحدة على الأقل."
        )

        return

    if any(
        p not in ALLOWED_SUPERVISOR_PERMISSIONS
        for p in permissions
    ):

        await message.answer(
            "❌ توجد صلاحية غير صحيحة.\n"
            "المتاح: "
            "users, finance, gifts, all"
        )

        return

    # Remove duplicates
    permissions = list(
        dict.fromkeys(permissions)
    )

    # If all exists, use all only
    if "all" in permissions:
        permissions = ["all"]

    data = await state.get_data()

    telegram_id = data["telegram_id"]

    db = await get_db()

    try:

        await db.execute(
            """
            INSERT OR REPLACE INTO supervisors
            (
                telegram_id,
                permissions,
                created_at
            )
            VALUES (?, ?, ?)
            """,
            (
                telegram_id,
                json.dumps(
                    permissions,
                    ensure_ascii=False
                ),
                now_iso()
            )
        )

        await db.commit()

    finally:

        await db.close()

    await message.answer(
        "✅ تم إضافة/تحديث المشرف.\n\n"
        f"🆔 ID: "
        f"<code>{telegram_id}</code>\n"
        f"🛡 الصلاحيات: "
        f"{esc(', '.join(permissions))}",
        reply_markup=admin_supervisors_kb()
    )

    await state.clear()


@dp.callback_query(F.data == "admin_sup_list")
async def admin_sup_list(
    cb: types.CallbackQuery
):

    if cb.from_user.id != ADMIN_USER_ID:

        await cb.answer(
            "للأدمن الرئيسي فقط.",
            show_alert=True
        )

        return

    db = await get_db()

    try:

        cur = await db.execute(
            """
            SELECT *
            FROM supervisors
            ORDER BY created_at DESC
            """
        )

        rows = await cur.fetchall()

    finally:

        await db.close()

    if not rows:

        await cb.answer()

        await cb.message.edit_text(
            "📭 لا يوجد مشرفون.",
            reply_markup=back_kb(
                "admin_supervisors"
            )
        )

        return

    lines = [
        "🛡 <b>قائمة المشرفين</b>\n"
    ]

    for row in rows:

        try:

            perms = json.loads(
                row["permissions"] or "[]"
            )

        except Exception:

            perms = []

        lines.append(
            f"👤 <code>{row['telegram_id']}</code>\n"
            f"🔐 {esc(', '.join(perms))}"
        )

    await cb.answer()

    await cb.message.edit_text(
        "\n\n".join(lines),
        reply_markup=back_kb(
            "admin_supervisors"
        )
    )


@dp.callback_query(F.data == "admin_sup_delete")
async def admin_sup_delete(
    cb: types.CallbackQuery,
    state: FSMContext
):

    if cb.from_user.id != ADMIN_USER_ID:

        await cb.answer(
            "للأدمن الرئيسي فقط.",
            show_alert=True
        )

        return

    await cb.answer()

    await state.set_state(
        AdminDeleteSupervisorFSM.telegram_id
    )

    await cb.message.answer(
        "أرسل Telegram ID للمشرف "
        "الذي تريد حذفه:"
    )


@dp.message(AdminDeleteSupervisorFSM.telegram_id)
async def admin_delete_supervisor_by_id(
    message: types.Message,
    state: FSMContext
):

    if message.from_user.id != ADMIN_USER_ID:

        await state.clear()

        return

    try:

        telegram_id = int(
            (message.text or "").strip()
        )

    except Exception:

        await message.answer(
            "❌ ID غير صالح."
        )

        return

    if telegram_id == ADMIN_USER_ID:

        await message.answer(
            "❌ لا يمكن حذف الأدمن الرئيسي."
        )

        await state.clear()

        return

    db = await get_db()

    try:

        cur = await db.execute(
            """
            SELECT telegram_id
            FROM supervisors
            WHERE telegram_id = ?
            """,
            (telegram_id,)
        )

        row = await cur.fetchone()

        if not row:

            await message.answer(
                "❌ لم يتم العثور على المشرف."
            )

            return

        await db.execute(
            """
            DELETE FROM supervisors
            WHERE telegram_id = ?
            """,
            (telegram_id,)
        )

        await db.commit()

    finally:

        await db.close()

    await message.answer(
        "✅ تم حذف المشرف:\n"
        f"<code>{telegram_id}</code>",
        reply_markup=admin_supervisors_kb()
    )

    await state.clear()


# ============================================================
# ADMIN STATISTICS
# ============================================================

@dp.callback_query(F.data == "admin_statistics")
async def admin_statistics(
    cb: types.CallbackQuery
):

    if not await is_admin_or_supervisor(
        cb.from_user.id
    ):

        await cb.answer(
            "غير مصرّح.",
            show_alert=True
        )

        return

    db = await get_db()

    try:

        cur = await db.execute(
            """
            SELECT COUNT(*) AS c
            FROM users
            """
        )

        users_count = (
            await cur.fetchone()
        )["c"]

        cur = await db.execute(
            """
            SELECT COALESCE(
                SUM(balance), 0
            ) AS total
            FROM users
            """
        )

        total_balance = (
            await cur.fetchone()
        )["total"]

        cur = await db.execute(
            """
            SELECT COUNT(*) AS c
            FROM finance_requests
            WHERE status = 'pending'
            """
        )

        pending = (
            await cur.fetchone()
        )["c"]

        cur = await db.execute(
            """
            SELECT COUNT(*) AS c
            FROM gift_codes
            WHERE used_by IS NULL
            """
        )

        unused_gifts = (
            await cur.fetchone()
        )["c"]

        cur = await db.execute(
            """
            SELECT COUNT(*) AS c
            FROM users
            WHERE is_banned = 1
            """
        )

        banned = (
            await cur.fetchone()
        )["c"]

    finally:

        await db.close()

    text = (
        "📈 <b>إحصائيات الإدارة</b>\n\n"
        f"👥 المستخدمون: {users_count}\n"
        f"🚫 المحظورون: {banned}\n"
        f"💰 إجمالي الأرصدة: "
        f"{money(total_balance)}\n"
        f"📨 طلبات مالية معلقة: {pending}\n"
        f"🎁 أكواد غير مستخدمة: "
        f"{unused_gifts}"
    )

    await cb.answer()

    await cb.message.edit_text(
        text,
        reply_markup=back_kb(
            "admin_panel"
        )
    )


# ============================================================
# COMMANDS
# ============================================================

@dp.message(Command("admin"))
async def admin_command(
    message: types.Message
):

    if not await is_admin_or_supervisor(
        message.from_user.id
    ):

        await message.answer(
            "❌ ليس لديك صلاحية "
            "للوصول إلى لوحة الإدارة."
        )

        return

    await message.answer(
        "🎛 <b>لوحة الإدارة</b>",
        reply_markup=admin_panel_kb()
    )


@dp.message(Command("cancel"))
async def cancel_command(
    message: types.Message,
    state: FSMContext
):

    current_state = await state.get_state()

    if current_state is None:

        await message.answer(
            "لا توجد عملية قيد التنفيذ.",
            reply_markup=main_menu_kb()
        )

        return

    await state.clear()

    await message.answer(
        "❌ تم إلغاء العملية.",
        reply_markup=main_menu_kb()
    )


# ============================================================
# FALLBACK
# ============================================================

@dp.message()
async def fallback_message(
    message: types.Message
):

    if not await user_allowed(
        message.from_user.id,
        message
    ):
        return

    await message.answer(
        "استخدم أزرار القائمة للمتابعة 👇",
        reply_markup=main_menu_kb()
    )


# ============================================================
# ERROR HANDLER
# ============================================================

@dp.errors()
async def global_error_handler(
    event
):

    print(
        "حدث خطأ غير متوقع:",
        repr(event.exception)
    )

    return True


# ============================================================
# MAIN
# ============================================================

async def main():

    print(
        "===================================="
    )

    print(
        "Bot is starting..."
    )

    print(
        f"Database: {DB_PATH}"
    )

    print(
        f"Admin ID: {ADMIN_USER_ID}"
    )

    print(
        "===================================="
    )

    try:

        await bot.delete_webhook(
            drop_pending_updates=True
        )

        await dp.start_polling(
            bot,
            allowed_updates=(
                dp.resolve_used_update_types()
            )
        )

    finally:

        await bot.session.close()


if __name__ == "__main__":

    try:

        asyncio.run(main())

    except KeyboardInterrupt:

        print(
            "Bot stopped."
        )
