FROM python:3.10-slim

WORKDIR /app
# 必要なシステムパッケージをインストール
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./app /app/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--log-level", "debug"]
