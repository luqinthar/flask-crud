FROM python:3.10-slim

WORKDIR /app

COPY app/ .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python3", "app.py"]
