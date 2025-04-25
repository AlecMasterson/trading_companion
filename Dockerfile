FROM python:3.12-slim AS base

RUN apt-get update && apt-get install -y --no-install-recommends build-essential gcc make wget
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

RUN wget https://github.com/ta-lib/ta-lib/releases/download/v0.6.4/ta-lib-0.6.4-src.tar.gz && \
    tar -xzf ta-lib-0.6.4-src.tar.gz && \
    cd ta-lib-0.6.4 && \
    ./configure --prefix=/usr && \
    make && make install && \
    cd .. && \
    rm -rf ta-lib-0.6.4-src.tar.gz ta-lib-0.6.4

WORKDIR /app

COPY bin/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY bin/ .

FROM node:23.11.0-slim AS development_ui

WORKDIR /app/web

COPY web/package*.json .
RUN npm install
COPY web/ .
RUN npm run build

FROM base AS development

WORKDIR /app

FROM base AS production

WORKDIR /app

COPY --from=development_ui /app/web/dist/ ./dist/
