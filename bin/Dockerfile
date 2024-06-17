FROM python:3.12-slim

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y --no-install-recommends build-essential gcc make wget
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

RUN wget https://github.com/ta-lib/ta-lib/releases/download/v0.6.4/ta-lib-0.6.4-src.tar.gz
RUN tar -xzf ta-lib-0.6.4-src.tar.gz && \
cd ta-lib-0.6.4 && \
./configure --prefix=/usr && \
make && make install

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
