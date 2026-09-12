"""[Windows helper] يجهز .env: يولّد API_KEY و PAYMENT_WEBHOOK_SECRET الفارغين.

يُشغَّل من start_bot.bat مرة واحدة قبل أول تشغيل. لا يلمس أي قيمة معبأة.
"""
import pathlib
import secrets

p = pathlib.Path(".env")
if not p.exists():
    raise SystemExit(0)

s = p.read_text(encoding="utf-8")
changed = False

for key in ("API_KEY", "PAYMENT_WEBHOOK_SECRET"):
    marker = key + "="
    idx = s.find(marker)

    if idx == -1:  # المفتاح غير موجود إطلاقاً بأ env قديم -> أضفه
        s = s.rstrip("\n") + f"\n{key}={secrets.token_hex(32)}\n"
        changed = True
        continue

    rest = s[idx + len(marker):]
    lines = rest.splitlines()
    value = lines[0].strip() if lines else ""

    if value == "":  # فارغ -> ولّد مفتاحاً قوياً
        s = (s[: idx + len(marker)] + secrets.token_hex(32)
             + s[idx + len(marker):])
        changed = True

p.write_text(s, encoding="utf-8")
print("OK" if changed else "ALREADY")
