# [NEW 17] تشغيل البوت داخل Docker
FROM python:3.12-slim

WORKDIR /app

# مكتبات النظام اللازمة (matplotlib تعتمد عليها)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libfreetype6 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY bot.py api.py ./

# قاعدة البيانات والمفتاح في مجلد مُثبَّت (volume)
ENV DB_PATH=/data/bot.db
VOLUME ["/data"]

CMD ["python", "bot.py"]
