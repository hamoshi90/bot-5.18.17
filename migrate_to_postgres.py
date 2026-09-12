#!/usr/bin/env python3
"""
ترحيل قاعدة البيانات من SQLite إلى PostgreSQL [NEW 18]
=====================================================
تصدير كل الجداول من bot.db إلى قاعدة PostgreSQL موجودة.

الاستخدام:
    1. ثبّت مكتبة psycopg:  pip install "psycopg[binary]"
    2. اضبط المتغير:        export POSTGRES_DSN="postgresql://user:pass@host:5432/dbname"
    3. شغّل:                python migrate_to_postgres.py

ملاحظة مهمة:
    هذا السكربت يرحّل *البيانات* فقط. لتشغيل البوت نفسه على PostgreSQL
    يجب استبدال طبقة الوصول في bot.py من aiosqlite إلى asyncpg
    (نفس الاستعلامات تعمل تقريباً مع تغيير ? إلى $1، $2...)
    — راجع قسم PostgreSQL في DEPLOY.md.
"""

import os
import sqlite3
import sys

import psycopg

SQLITE_PATH = os.getenv("DB_PATH", "bot.db")
POSTGRES_DSN = os.getenv("POSTGRES_DSN", "")

TABLES = {
    "users": """
        CREATE TABLE IF NOT EXISTS users (
            id BIGSERIAL PRIMARY KEY,
            telegram_id BIGINT UNIQUE NOT NULL,
            username TEXT DEFAULT '',
            full_name TEXT DEFAULT '',
            site_username TEXT,
            site_password TEXT,
            balance DOUBLE PRECISION DEFAULT 0,
            is_banned INTEGER DEFAULT 0,
            referrer_id BIGINT,
            lang TEXT DEFAULT 'ar',
            created_at TEXT NOT NULL
        )
    """,
    "transactions": """
        CREATE TABLE IF NOT EXISTS transactions (
            id BIGSERIAL PRIMARY KEY,
            user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            type TEXT NOT NULL,
            amount DOUBLE PRECISION DEFAULT 0,
            note TEXT DEFAULT '',
            created_at TEXT NOT NULL
        )
    """,
    "admin_settings": """
        CREATE TABLE IF NOT EXISTS admin_settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    """,
    "gift_codes": """
        CREATE TABLE IF NOT EXISTS gift_codes (
            code TEXT PRIMARY KEY,
            amount DOUBLE PRECISION NOT NULL,
            used_by BIGINT DEFAULT NULL,
            created_by BIGINT DEFAULT 0,
            created_at TEXT NOT NULL,
            used_at TEXT DEFAULT NULL
        )
    """,
    "supervisors": """
        CREATE TABLE IF NOT EXISTS supervisors (
            telegram_id BIGINT PRIMARY KEY,
            permissions TEXT DEFAULT '[]',
            suspended INTEGER DEFAULT 0,
            daily_quota DOUBLE PRECISION DEFAULT 0,
            created_at TEXT NOT NULL
        )
    """,
    "finance_requests": """
        CREATE TABLE IF NOT EXISTS finance_requests (
            id BIGSERIAL PRIMARY KEY,
            telegram_id BIGINT NOT NULL,
            type TEXT NOT NULL,
            amount DOUBLE PRECISION NOT NULL,
            status TEXT DEFAULT 'pending',
            promo_code TEXT DEFAULT '',
            note TEXT DEFAULT '',
            created_at TEXT NOT NULL,
            processed_at TEXT DEFAULT NULL,
            processed_by BIGINT DEFAULT NULL
        )
    """,
    "admin_audit": """
        CREATE TABLE IF NOT EXISTS admin_audit (
            id BIGSERIAL PRIMARY KEY,
            admin_id BIGINT NOT NULL,
            action TEXT NOT NULL,
            target TEXT DEFAULT '',
            details TEXT DEFAULT '',
            created_at TEXT NOT NULL
        )
    """,
    "bot_texts": """
        CREATE TABLE IF NOT EXISTS bot_texts (
            key TEXT PRIMARY KEY,
            value TEXT DEFAULT '',
            updated_at TEXT
        )
    """,
    # [NEW 35/36] سجل أحداث الويب هوك (منع الشحن المزدوج)
    "webhook_events": """
        CREATE TABLE IF NOT EXISTS webhook_events (
            event_id TEXT PRIMARY KEY,
            source TEXT DEFAULT 'payment_webhook',
            payload_hash TEXT DEFAULT '',
            result TEXT DEFAULT '',
            user_tid BIGINT,
            amount DOUBLE PRECISION,
            created_at TEXT NOT NULL
        )
    """,
    # [NEW 35/36] أوامر الدفع الصادرة
    "payouts": """
        CREATE TABLE IF NOT EXISTS payouts (
            id BIGSERIAL PRIMARY KEY,
            user_tid BIGINT NOT NULL,
            amount DOUBLE PRECISION NOT NULL,
            method TEXT DEFAULT 'manual',
            destination TEXT DEFAULT '',
            status TEXT DEFAULT 'pending',
            external_id TEXT DEFAULT '',
            error TEXT DEFAULT '',
            created_by BIGINT DEFAULT 0,
            created_at TEXT NOT NULL,
            processed_at TEXT
        )
    """,
    # [USR2-4] أكواد إعفاء العمولة
    "promo_codes": """
        CREATE TABLE IF NOT EXISTS promo_codes (
            code TEXT PRIMARY KEY,
            uses_left INTEGER DEFAULT 1,
            created_by BIGINT DEFAULT 0,
            created_at TEXT NOT NULL
        )
    """,
    # [ADM3-6] سجل تعديلات الرصيد (للتراجع)
    "balance_adjustments": """
        CREATE TABLE IF NOT EXISTS balance_adjustments (
            id BIGSERIAL PRIMARY KEY,
            admin_id BIGINT NOT NULL,
            target_tid BIGINT NOT NULL,
            amount DOUBLE PRECISION NOT NULL,
            note TEXT DEFAULT '',
            undone INTEGER DEFAULT 0,
            created_at TEXT NOT NULL
        )
    """,
    # [ADM4-1] وسوم المستخدمين (CRM)
    "user_tags": """
        CREATE TABLE IF NOT EXISTS user_tags (
            id BIGSERIAL PRIMARY KEY,
            telegram_id BIGINT NOT NULL,
            tag TEXT NOT NULL,
            created_at TEXT NOT NULL,
            UNIQUE(telegram_id, tag)
        )
    """,
    # [ADM4-4] الإعلانات + تتبع القراءة
    "announcements": """
        CREATE TABLE IF NOT EXISTS announcements (
            id BIGSERIAL PRIMARY KEY,
            text TEXT NOT NULL,
            created_by BIGINT DEFAULT 0,
            created_at TEXT NOT NULL,
            expires_at TEXT NOT NULL
        )
    """,
    "announcement_reads": """
        CREATE TABLE IF NOT EXISTS announcement_reads (
            announcement_id BIGINT NOT NULL,
            telegram_id BIGINT NOT NULL,
            read_at TEXT NOT NULL,
            UNIQUE(announcement_id, telegram_id)
        )
    """,
    # [USR4-3] الحضور اليومي
    "checkins": """
        CREATE TABLE IF NOT EXISTS checkins (
            id BIGSERIAL PRIMARY KEY,
            telegram_id BIGINT NOT NULL,
            day TEXT NOT NULL,
            streak INTEGER DEFAULT 1,
            amount DOUBLE PRECISION DEFAULT 0,
            created_at TEXT NOT NULL,
            UNIQUE(telegram_id, day)
        )
    """,
    # [ADM4-3] قائمة الثقة للاعتماد التلقائي
    "auto_wd_whitelist": """
        CREATE TABLE IF NOT EXISTS auto_wd_whitelist (
            telegram_id BIGINT PRIMARY KEY,
            created_by BIGINT DEFAULT 0,
            created_at TEXT NOT NULL
        )
    """,
    # [USR4-2] دفتر وجهات السحب
    "payout_accounts": """
        CREATE TABLE IF NOT EXISTS payout_accounts (
            id BIGSERIAL PRIMARY KEY,
            telegram_id BIGINT NOT NULL,
            label TEXT DEFAULT '',
            destination TEXT NOT NULL,
            created_at TEXT NOT NULL,
            UNIQUE(telegram_id, destination)
        )
    """,
    # [USR4-6] سجل التصدير الذاتي
    "my_exports": """
        CREATE TABLE IF NOT EXISTS my_exports (
            telegram_id BIGINT PRIMARY KEY,
            created_at TEXT NOT NULL
        )
    """,
    # [ADM3-9] ردود جاهزة للتذاكر
    "canned_replies": """
        CREATE TABLE IF NOT EXISTS canned_replies (
            id BIGSERIAL PRIMARY KEY,
            title TEXT DEFAULT '',
            body TEXT DEFAULT '',
            created_at TEXT NOT NULL
        )
    """,
    # [ADM2-2] ملاحظات الإدارة على المستخدمين
    "user_notes": """
        CREATE TABLE IF NOT EXISTS user_notes (
            id BIGSERIAL PRIMARY KEY,
            target_tid BIGINT NOT NULL,
            author_id BIGINT NOT NULL,
            note TEXT DEFAULT '',
            created_at TEXT NOT NULL
        )
    """,
    # [NEW 38] تذاكر الدعم
    "support_tickets": """
        CREATE TABLE IF NOT EXISTS support_tickets (
            id BIGSERIAL PRIMARY KEY,
            user_tid BIGINT NOT NULL,
            message TEXT DEFAULT '',
            status TEXT DEFAULT 'open',
            created_at TEXT NOT NULL,
            answered_at TEXT,
            answered_by BIGINT,
            rating INTEGER
        )
    """,
    # [R6-PLUS2] تقييم ⭐ بعد السحب
    "payout_ratings": """
        CREATE TABLE IF NOT EXISTS payout_ratings (
            id BIGSERIAL PRIMARY KEY,
            payout_id BIGINT UNIQUE NOT NULL,
            telegram_id BIGINT NOT NULL,
            stars INTEGER DEFAULT 5,
            created_at TEXT NOT NULL
        )
    """,
}

# فهارس مطابقة لما ينشئه bot.py عند الإقلاع
INDEXES = {
    "transactions": [
        "CREATE INDEX IF NOT EXISTS idx_transactions_user"
        " ON transactions(user_id)",
    ],
    "payouts": [
        "CREATE INDEX IF NOT EXISTS idx_payouts_status ON payouts(status)",
    ],
    "support_tickets": [
        "CREATE INDEX IF NOT EXISTS idx_tickets_status"
        " ON support_tickets(status)",
    ],
    "user_notes": [
        "CREATE INDEX IF NOT EXISTS idx_notes_target"
        " ON user_notes(target_tid)",
    ],
}


def main():
    if not POSTGRES_DSN:
        sys.exit("❌ اضبط POSTGRES_DSN أولاً.")

    lite = sqlite3.connect(SQLITE_PATH)
    lite.row_factory = sqlite3.Row

    tables = {
        r[0]
        for r in lite.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        ).fetchall()
    }

    with psycopg.connect(POSTGRES_DSN) as pg:
        with pg.cursor() as cur:
            total_rows = 0

            for name, ddl in TABLES.items():
                if name not in tables:
                    print(f"⏭  {name}: غير موجودة في SQLite — تخطي")
                    continue

                cur.execute(ddl)

                for idx_sql in INDEXES.get(name, []):
                    cur.execute(idx_sql)

                # ترقية قواعد Postgres أقدم نسخةً (أعمدة أضيفت لاحقاً) —
                # بعد CREATE مباشرة وقبل INSERT وإلا فشل على القواعد القديمة
                if name == "supervisors":
                    cur.execute(
                        "ALTER TABLE supervisors ADD COLUMN IF NOT EXISTS"
                        " suspended INTEGER DEFAULT 0"
                    )
                    cur.execute(
                        "ALTER TABLE supervisors ADD COLUMN IF NOT EXISTS"
                        " daily_quota DOUBLE PRECISION DEFAULT 0"
                    )
                elif name == "finance_requests":
                    cur.execute(
                        "ALTER TABLE finance_requests"
                        " ADD COLUMN IF NOT EXISTS promo_code"
                        " TEXT DEFAULT ''"
                    )
                    cur.execute(
                        "ALTER TABLE finance_requests"
                        " ADD COLUMN IF NOT EXISTS note"
                        " TEXT DEFAULT ''"
                    )
                    cur.execute(  # [R6-PLUS2] تذكير الطلبات العالقة
                        "ALTER TABLE finance_requests"
                        " ADD COLUMN IF NOT EXISTS remind_at TEXT"
                    )
                elif name == "announcements":
                    cur.execute(  # [R6-PLUS2] صورة الإعلان
                        "ALTER TABLE announcements"
                        " ADD COLUMN IF NOT EXISTS photo_file_id"
                        " TEXT DEFAULT ''"
                    )
                elif name == "support_tickets":
                    cur.execute(
                        "ALTER TABLE support_tickets"
                        " ADD COLUMN IF NOT EXISTS rating INTEGER"
                    )
                elif name == "gift_codes":
                    cur.execute(
                        "ALTER TABLE gift_codes"
                        " ADD COLUMN IF NOT EXISTS created_by BIGINT DEFAULT 0"
                    )
                elif name == "users":
                    cur.execute(
                        "ALTER TABLE users"
                        " ADD COLUMN IF NOT EXISTS referrer_id BIGINT"
                    )
                    cur.execute(
                        "ALTER TABLE users"
                        " ADD COLUMN IF NOT EXISTS lang TEXT DEFAULT 'ar'"
                    )
                    # [R6-PLUS2] أعمدة جولة الاقتراحات
                    cur.execute(
                        "ALTER TABLE users ADD COLUMN IF NOT EXISTS"
                        " wd_daily_cap DOUBLE PRECISION DEFAULT 0"
                    )
                    cur.execute(
                        "ALTER TABLE users ADD COLUMN IF NOT EXISTS"
                        " points INTEGER DEFAULT 0"
                    )
                    cur.execute(
                        "ALTER TABLE users ADD COLUMN IF NOT EXISTS"
                        " hide_balance INTEGER DEFAULT 0"
                    )
                    cur.execute(
                        "ALTER TABLE users ADD COLUMN IF NOT EXISTS"
                        " last_winback TEXT"
                    )
                    cur.execute(  # [R6-PLUS3] جولة التحسينات
                        "ALTER TABLE users ADD COLUMN IF NOT EXISTS"
                        " ban_until TEXT"
                    )
                    cur.execute(
                        "ALTER TABLE users ADD COLUMN IF NOT EXISTS"
                        " digest_enabled INTEGER DEFAULT 0"
                    )
                    cur.execute(
                        "ALTER TABLE users ADD COLUMN IF NOT EXISTS"
                        " ann_notify INTEGER DEFAULT 0"
                    )
                    cur.execute(
                        "ALTER TABLE users ADD COLUMN IF NOT EXISTS"
                        " last_dep_method TEXT DEFAULT ''"
                    )
                    cur.execute(
                        "ALTER TABLE users ADD COLUMN IF NOT EXISTS"
                        " last_wd_method TEXT DEFAULT ''"
                    )

                rows = lite.execute(
                    f"SELECT * FROM {name}"
                ).fetchall()

                if not rows:
                    print(f"⏭  {name}: فارغة")
                    continue

                cols = rows[0].keys()
                placeholders = ", ".join(["%s"] * len(cols))
                col_list = ", ".join(cols)

                # تصفير العدادات للجداول ذات المفتاح التلقائي
                has_id = "id" in cols

                for row in rows:
                    cur.execute(
                        f"INSERT INTO {name} ({col_list})"
                        f" VALUES ({placeholders})"
                        + (
                            " ON CONFLICT (id) DO NOTHING"
                            if has_id
                            else " ON CONFLICT DO NOTHING"
                        ),
                        tuple(row),
                    )

                if has_id:
                    cur.execute(
                        f"SELECT setval(pg_get_serial_sequence('{name}', 'id'),"
                        f" COALESCE((SELECT MAX(id) FROM {name}), 1))"
                    )

                total_rows += len(rows)
                print(f"✅ {name}: {len(rows)} صف")

        pg.commit()

    lite.close()
    print(f"\n🎉 تم ترحيل {total_rows} صف بنجاح.")


if __name__ == "__main__":
    main()
