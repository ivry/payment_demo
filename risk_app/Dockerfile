#FROM alpine
FROM python:3.9.12-slim AS builder

ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2

ENV PATH="./venv/bin:$PATH"

WORKDIR /usr/app

RUN python -m venv /opt/venv
COPY ./risk_app/requirements.txt /usr/app/requirements.txt
RUN pip install -r requirements.txt

COPY ./risk_app .
COPY ./common /usr/app/common
ENV PYTHONPATH="$PYTHONPATH:/usr/app:..:."
ENV DB_HOST=postgres_db
ENV DB_NAME=demo_db
ENV DB_USER=demo_user
ENV DB_PASSWORD=1234
ENV DB_PORT=5432
ENV DB_SCHEMA_PAYMENT=payment_schema
ENV DB_SCHEMA_RISK=risk_schema

ENV KAFKA_BOOTSTRAP_HOST=broker
ENV KAFKA_BOOTSTRAP_PORT=9092

EXPOSE 8000

CMD ["python3", "risk_app.py"]
#CMD ["python3", "risk_app.py"]
