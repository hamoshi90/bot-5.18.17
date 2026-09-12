#!/usr/bin/env bash
# ============================================================
# deploy.sh — نشر آمن لمشروع البوت (تحديث الكود دون لمس البيانات)
#
# الاستخدام:
#   bash deploy.sh <المصدر> [خيارات]
#
#   <المصدر>  إما ملف bot.py جديد، أو حزمة .zip تحتوي المشروع
#
# الخيارات:
#   --unit NAME    اسم وحدة systemd (افتراضي: bot)
#   --docker       استخدام docker compose بدل systemd
#   --plain        تشغيل مباشر (بدون مدير خدمات) — pgrep/pkill + nohup
#   --pip          تثبيت requirements.txt بعد نسخ الملفات وقبل التشغيل
#   --app DIR      مجلد التطبيق (افتراضي: المجلد الحالي)
#   --yes          بدون سؤال تأكيد
#   --wait N       ثوانٍ الانتظار في فحص الصحة (افتراضي 12)
#
# يحمي دائماً: .env و bot.db و secret.key — لا ينسخها ولا يحذفها
# على أي حال، حتى لو كانت داخل الحزمة.
#
# عند أي فشل بعد مرحلة الإيقاف: رجوع تلقائي (rollback) للنسخة السابقة.
# ============================================================

set -uo pipefail

APP_DIR="."
UNIT="bot"
MODE=""          # systemd | docker | plain  (يُكتشف تلقائياً إن تُرك فارغاً)
SRC=""
ASSUME_YES=0
DO_PIP=0
WAIT_SEC=12
TS="$(date +%Y%m%d_%H%M%S)"
BACKUP_DIR=""
STAGE=""
PHASE="pre"      # pre -> stopped -> started (يحدد ما إذا كان الرجوع ضرورياً)

log()  { echo "[deploy] $*"; }
warn() { echo "[deploy][تحذير] $*" >&2; }
die()  { echo "[deploy][فشل] $*" >&2; exit 1; }

# ---------- تحليل الوسائط ----------
while [ $# -gt 0 ]; do
  case "$1" in
    --unit)  UNIT="$2";  shift 2 ;;
    --docker) MODE="docker"; shift ;;
    --plain) MODE="plain";   shift ;;
    --app)   APP_DIR="$2";   shift 2 ;;
    --pip)   DO_PIP=1;       shift ;;
    --yes)   ASSUME_YES=1;   shift ;;
    --wait)  WAIT_SEC="$2";  shift 2 ;;
    -h|--help) sed -n '2,25p' "$0"; exit 0 ;;
    -*)      die "خيار غير معروف: $1 (استخدم --help)" ;;
    *)       SRC="$1"; shift ;;
  esac
done

[ -n "$SRC" ] || { sed -n '2,25p' "$0"; die "حدد المصدر: ملف bot.py أو حزمة .zip"; }
[ -d "$APP_DIR" ] || die "مجلد التطبيق غير موجود: $APP_DIR"
APP_DIR="$(cd "$APP_DIR" && pwd)"
[ -f "$APP_DIR/bot.py" ] || die "لا يوجد bot.py في $APP_DIR — هل هذا مجلد التطبيق الصحيح؟"

command -v python3 >/dev/null 2>&1 || die "python3 غير متوفر في PATH"

# ---------- اكتشاف نمط التشغيل ----------
detect_mode() {
  [ -n "$MODE" ] && return 0
  if command -v systemctl >/dev/null 2>&1 \
     && systemctl list-unit-files 2>/dev/null | grep -q "^${UNIT}\.service"; then
    MODE="systemd"
  elif [ -f "$APP_DIR/docker-compose.yml" ] && command -v docker >/dev/null 2>&1; then
    MODE="docker"
  else
    MODE="plain"
  fi
  return 0
}

svc_stop() {
  case "$MODE" in
    systemd)
      if [ "$(id -u)" = "0" ]; then systemctl stop "$UNIT"
      elif sudo -n systemctl stop "$UNIT" 2>/dev/null; then :
      else systemctl stop "$UNIT"; fi
      ;;
    docker) (cd "$APP_DIR" && docker compose stop) ;;
    plain)
      pkill -f "python3? +(\./)?bot\.py" 2>/dev/null || true
      sleep 1
      pkill -9 -f "python3? +(\./)?bot\.py" 2>/dev/null || true
      ;;
  esac
}

svc_start() {
  case "$MODE" in
    systemd)
      if [ "$(id -u)" = "0" ]; then systemctl start "$UNIT"
      elif sudo -n systemctl start "$UNIT" 2>/dev/null; then :
      else systemctl start "$UNIT"; fi
      ;;
    docker) (cd "$APP_DIR" && docker compose up -d) ;;
    plain)
      # عزل كامل: جلسة جديدة + stdin مغلق حتى لا ينتظر السكربت العملية
      if command -v setsid >/dev/null 2>&1; then
        ( cd "$APP_DIR" && setsid nohup python3 bot.py \
            >> bot_console.log 2>&1 < /dev/null & )
      else
        ( cd "$APP_DIR" && nohup python3 bot.py \
            >> bot_console.log 2>&1 < /dev/null & )
      fi
      pkill -0 -f "python3? +(\./)?bot\.py" 2>/dev/null || true
      ;;
  esac
}

svc_alive() {
  case "$MODE" in
    systemd) [ "$(systemctl is-active "$UNIT" 2>/dev/null)" = "active" ] ;;
    docker)  [ -n "$(cd "$APP_DIR" && docker compose ps -q 2>/dev/null)" ] \
             && [ "$(cd "$APP_DIR" && docker compose ps --format '{{.State}}' 2>/dev/null | grep -c running)" != "0" ] ;;
    plain)   pgrep -f "python3? +(\./)?bot\.py" >/dev/null 2>&1 ;;
  esac
}

# ---------- تجهيز المصدر في مجلد مرحلي ----------
STAGE="$(mktemp -d /tmp/deploy_stage_XXXXXX)"
trap 'rm -rf "$STAGE" 2>/dev/null || true' EXIT

if [ -f "$SRC" ] && echo "$SRC" | grep -qi '\.zip$'; then
  log "فك الحزمة: $SRC"
  python3 - "$SRC" "$STAGE" << 'PY'
import sys, zipfile
zip_path, dest = sys.argv[1], sys.argv[2]
with zipfile.ZipFile(zip_path) as z:
    bad = z.testzip()
    if bad:
        sys.exit(f"ملف تالف داخل الحزمة: {bad}")
    z.extractall(dest)
print("تم الفك بنجاح")
PY
  [ $? -eq 0 ] || die "الحزمة تالفة أو لا يمكن فكها"
elif [ -f "$SRC" ]; then
  case "$(basename "$SRC")" in
    bot.py) cp "$SRC" "$STAGE/bot.py" ;;
    *) die "المصدر يجب أن يكون bot.py أو حزمة .zip" ;;
  esac
else
  die "المصدر غير موجود: $SRC"
fi

[ -f "$STAGE/bot.py" ] || die "لا يوجد bot.py داخل المصدر"

# ---------- فحص الصيغة قبل لمس أي شيء ----------
log "فحص صيغة Python لكل الملفات المرشحة..."
COMPILE_FAIL=""
while IFS= read -r pyfile; do
  rel="${pyfile#"$STAGE"/}"
  if ! python3 -m py_compile "$pyfile" 2> "$STAGE/compile_err.txt"; then
    COMPILE_FAIL="$rel"
    break
  fi
done < <(find "$STAGE" -maxdepth 1 -name '*.py' -type f | sort)

if [ -n "$COMPILE_FAIL" ]; then
  echo "----- خطأ الصيغة في $COMPILE_FAIL -----" >&2
  cat "$STAGE/compile_err.txt" >&2
  echo "---------------------------------------" >&2
  die "فحص الصيغة فشل — لم يُعدَّل أي شيء، والبوت يعمل كما هو"
fi
log "فحص الصيغة: نظيف ✓"

# ---------- قائمة الملفات للنسخ (مع الحماية) ----------
FILES_TO_COPY=()
for f in bot.py api.py migrate_to_postgres.py requirements.txt \
         Dockerfile docker-compose.yml bot.service README.txt; do
  [ -f "$STAGE/$f" ] && FILES_TO_COPY+=("$f")
done
[ ${#FILES_TO_COPY[@]} -gt 0 ] || die "لا ملفات صالحة للنسخ داخل المصدر"

# قص نهائي: ممنوع نسخ أي بيانات/أسرار حتى لو وُجدت بالمصدر
for f in "${FILES_TO_COPY[@]}"; do
  case "$f" in
    .env|*.db|*.db-wal|*.db-shm|secret.key|*.key|bot.db.backup)
      die "رفض نسخ '$f' — ملف بيانات/سر (خطأ في بناء الحزمة؟)" ;;
  esac
done

# ---------- خطة + تأكيد ----------
detect_mode
echo "======================================================"
echo " خطة النشر"
echo "------------------------------------------------------"
echo " مجلد التطبيق : $APP_DIR"
echo " نمط التشغيل  : $MODE${MODE:-}${MODE:+ (وحدة: $UNIT)}"
echo " الملفات      : ${FILES_TO_COPY[*]}"
echo " pip install  : $([ $DO_PIP = 1 ] && echo نعم || echo لا)"
echo " فحص الصحة    : حتى $(( WAIT_SEC + 6 )) ثانية"
echo " محمي دائماً  : .env / bot.db / secret.key / backups"
echo "======================================================"

if [ "$ASSUME_YES" != "1" ]; then
  printf "متابعة؟ [y/N] "
  read -r answer
  case "$answer" in
    y|Y|نعم|n3m) : ;;
    *) die "أُلغي بواسطة المستخدم — لم يتغير أي شيء" ;;
  esac
fi

# ---------- النسخ الاحتياطي ----------
BACKUP_DIR="$APP_DIR/backups/pre_deploy_$TS"
mkdir -p "$BACKUP_DIR"
log "نسخ احتياطي إلى: $BACKUP_DIR"

cp -a "$APP_DIR/bot.py" "$BACKUP_DIR/"
for f in "${FILES_TO_COPY[@]}"; do
  [ -f "$APP_DIR/$f" ] && cp -a "$APP_DIR/$f" "$BACKUP_DIR/"
done
# البيانات الحرجة
[ -f "$APP_DIR/bot.db" ]        && cp -a "$APP_DIR/bot.db" "$BACKUP_DIR/"
[ -f "$APP_DIR/bot.db-wal" ]    && cp -a "$APP_DIR/bot.db-wal" "$BACKUP_DIR/" 2>/dev/null || true
[ -f "$APP_DIR/bot.db-shm" ]    && cp -a "$APP_DIR/bot.db-shm" "$BACKUP_DIR/" 2>/dev/null || true
[ -f "$APP_DIR/secret.key" ]    && cp -a "$APP_DIR/secret.key" "$BACKUP_DIR/"
[ -f "$APP_DIR/.env" ]          && cp -a "$APP_DIR/.env" "$BACKUP_DIR/"
log "النسخ الاحتياطي تم ✓ (يشمل bot.db و secret.key و .env)"

# ---------- الرجوع التلقائي عند أي فشل لاحق ----------
rollback() {
  echo "" >&2
  warn "بدء الرجوع التلقائي (rollback)..."
  svc_stop || true
  for f in "${FILES_TO_COPY[@]}"; do
    if [ -f "$BACKUP_DIR/$f" ]; then
      cp -a "$BACKUP_DIR/$f" "$APP_DIR/$f"
    else
      warn "الملف $f كان غير موجود قبل النشر — أزالته؟ (احذفه يدوياً إن ظهرت مشكلة)"
    fi
  done
  svc_start || true
  sleep 3
  if svc_alive; then
    warn "تمت استعادة النسخة السابقة والبوت يعمل ✓"
    warn "ملفات النشر الفاشلة محفوظة في: $STAGE (للفحص)"
  else
    warn "الرجوع تم للملفات لكن الخدمة لا تستجيب — راجع: journalctl -u $UNIT -n 50"
  fi
  exit 1
}

# ---------- التنفيذ ----------
log "إيقاف الخدمة ($MODE)..."
svc_stop || die "تعذر إيقاف الخدمة — أوقفها يدوياً وأعد المحاولة (لم يُعدَّل شيء)"
PHASE="stopped"

log "نسخ الملفات الجديدة..."
for f in "${FILES_TO_COPY[@]}"; do
  cp -a "$STAGE/$f" "$APP_DIR/$f"
  log "  + $f"
done

if [ "$DO_PIP" = "1" ] && [ -f "$APP_DIR/requirements.txt" ]; then
  log "تثبيت المتطلبات..."
  python3 -m pip install -r "$APP_DIR/requirements.txt" \
    || { warn "pip فشل"; rollback; }
fi

log "تشغيل الخدمة..."
svc_start || { warn "أمر التشغيل فشل"; rollback; }
PHASE="started"

# ---------- فحص الصحة ----------
log "فحص الصحة (${WAIT_SEC} ثانية)..."
sleep 3
CHECKS=$(( (WAIT_SEC / 3) + 1 ))
i=1
while [ $i -le $CHECKS ]; do
  if ! svc_alive; then
    warn "الخدمة توقفت بعد التشغيل (المحاولة $i/$CHECKS)"
    rollback
  fi
  sleep 3
  i=$((i + 1))
done

# في نمط plain تأكد إضافي: العملية نفسها لا تزال نفسها
if [ "$MODE" = "plain" ]; then
  sleep 2
  svc_alive || { warn "فحص أخير: العملية سقطت"; rollback; }
fi

echo ""
log "============================================="
log "✅ النشر نجح — البوت يعمل بالنسخة الجديدة"
log "   مجلد التطبيق : $APP_DIR"
log "   نسخ احتياطية : $BACKUP_DIR"
log "   للرجوع اليدوي:"
log "     cp -a $BACKUP_DIR/bot.py $APP_DIR/bot.py"
log "     ثم أعد تشغيل الخدمة (systemctl restart $UNIT)"
log "============================================="
exit 0
