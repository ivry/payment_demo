from fastapi import FastAPI
import uvicorn
import os
from uuid import uuid4
from kafka import KafkaProducer
from common.models import PaymentRequest, APIPaymentRequest, User, APIUser, PaymentMethod, APIPaymentMethod
from common import postgres_utils
from psycopg2 import connect, sql
from psycopg2.extras import RealDictCursor, execute_values

"""
/Users/ivry/development/projects/intuit_p2p/venv/bin/uvicorn --app-dir ./app payment_service:app
"""

payment_app = FastAPI()


@payment_app.post('/users')
async def create_user(user: APIUser):
    user = User(**(user.dict() | {'user_id': uuid4()}))
    with postgres_utils.get_connection(db_schema='payment_schema') as conn:
        postgres_utils.insert(conn, 'user', user.dict())

    return user


@payment_app.get('/users')
async def get_users():
    return select_all('user')


@payment_app.post('/payment_methods')
async def create_payment_method(payment_method: APIPaymentMethod):
    user = PaymentMethod(**(payment_method.dict() | {'payment_method_id': uuid4()}))
    with postgres_utils.get_connection(db_schema='payment_schema') as conn:
        postgres_utils.insert(conn, 'payment_method', user.dict())

    return payment_method


@payment_app.get('/payment_methods')
async def get_payment_methods():
    return select_all('payment_method')


@payment_app.post('/payments')
async def create_payment(payment_api_request: APIPaymentRequest):
    # return payment_api_request
    payment_request = PaymentRequest(**(payment_api_request.dict() | {'payment_request_id': uuid4()}))
    with postgres_utils.get_connection(db_schema='payment_schema') as conn:
        postgres_utils.insert(conn, 'payment_request', payment_request.dict())

    bootstrap_server = (
            f'{os.environ.get("KAFKA_BOOTSTRAP_HOST")}:{os.environ.get("KAFKA_BOOTSTRAP_PORT")}' or
            'localhost:9092'
    )

    bootstrap_server = 'broker:9092'
    print(bootstrap_server)

    producer = KafkaProducer(bootstrap_servers=[bootstrap_server])
    future = producer.send('payment_request', bytes(payment_request.json(), 'utf-8'))

    return payment_api_request


@payment_app.get('/payments')
async def get_payment_requests():
    return select_all('payment_request')


def select_all(table_name):
    query = sql.SQL('SELECT * FROM {tbl}').format(
        tbl=sql.Identifier(table_name)
    )

    with postgres_utils.get_connection(db_schema='payment_schema') as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query)
            out = cur.fetchall()

    return out


if __name__ == '__main__':
    uvicorn.run(payment_app, host="0.0.0.0", port=8000)
