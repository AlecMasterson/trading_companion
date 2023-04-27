FROM python:3.10.4
RUN apt-get update

COPY requirements.txt /requirements.txt
RUN pip install --user --upgrade pip
RUN pip install --no-cache-dir --user -r /requirements.txt

RUN mkdir /scripts

CMD cd /scripts && PYTHONPATH=PYTHONPATH:/scripts/src python -m uvicorn src.api:App --host 0.0.0.0 --port 8000 --reload
