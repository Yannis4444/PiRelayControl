FROM python:3.11-alpine

ENV PYTHONUNBUFFERED=0

ENV RELAY_PIN=18

WORKDIR /app

RUN apk add build-base

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY *.py .

EXPOSE 8080

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]