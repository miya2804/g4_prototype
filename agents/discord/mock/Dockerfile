FROM python:3.7.8-stretch

WORKDIR /tmp

COPY requirements.txt /tmp/

RUN pip install -r requirements.txt

WORKDIR /opt/app

CMD ["python", "app.py"]
