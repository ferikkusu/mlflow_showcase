FROM python:3.8-slim

RUN apt update \
  && apt install -y libpq-dev build-essential \
  && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir mlflow==1.27.0 psycopg2 boto3

# CMD ["mlflow", "ui", "--backend-store-uri", "postgresql://postgres:password@db:5432/postgres", "--default-artifact-root", "/mlruns", "--host", "0.0.0.0"]