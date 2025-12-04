FROM python:3.9-slim

WORKDIR /app

# requirements.txt ZUERST kopieren und installieren
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Danach erst app kopieren
COPY app.py .

EXPOSE 5000

CMD ["python", "app.py"]
