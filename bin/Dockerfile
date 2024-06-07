FROM python:3.10.4

WORKDIR /app
COPY requirements.txt /app/requirements.txt

RUN pip install --upgrade pip
RUN pip install --no-cache-dir --user -r requirements.txt
