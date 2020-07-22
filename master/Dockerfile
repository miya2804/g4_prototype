FROM python:3.7.8-stretch

RUN apt update \
    && apt install -y build-essential

WORKDIR /tmp
COPY requirements.txt /tmp/
RUN pip install -r requirements.txt

WORKDIR /work
