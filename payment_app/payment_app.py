import psycopg2.errorcodes
from fastapi import FastAPI, HTTPException
import uvicorn
import os
from uuid import uuid4
from kafka import KafkaProducer
from common.models import PaymentRequest, User, PaymentMethod
from common import postgres_utils
from psycopg2 import connect, sql
from psycopg2.extras import RealDictCursor, execute_values

payment_app = FastAPI()


@payment_app.post('/users')
async def create_user(user: User):
    if not user.user_id:
        user.user_id = uuid4()
    with postgres_utils.get_connection(db_schema='payment_schema') as conn:
        insert_raises(conn, 'user', user.dict())

    return user


@payment_app.get('/users')
async def get_users():
    return select_all('user')


@payment_app.post('/payment_methods')
async def create_payment_method(payment_method: PaymentMethod):
    if not payment_method.payment_method_id:
        payment_method.payment_method_id = uuid4()
    with postgres_utils.get_connection(db_schema='payment_schema') as conn:
        insert_raises(conn, 'payment_method', payment_method.dict())

    return payment_method


@payment_app.get('/payment_methods')
async def get_payment_methods():
    return select_all('payment_method')


@payment_app.post('/payments')
async def create_payment(payment_request: PaymentRequest):
    if not payment_request.payment_request_id:
        payment_request.payment_request_id = uuid4()

    with postgres_utils.get_connection(db_schema='payment_schema') as conn:
        # Check that user, payee and payment method exist
        raise_is_not_exist(
            conn=conn,
            table_name='user',
            id_name='user_id',
            id_value=payment_request.user_id
        )
        raise_is_not_exist(
            conn=conn,
            table_name='user',
            id_name='user_id',
            id_value=payment_request.payee_id
        )
        raise_is_not_exist(
            conn=conn,
            table_name='payment_method',
            id_name='payment_method_id',
            id_value=payment_request.payment_method_id
        )

        insert_raises(conn, 'payment_request', payment_request.dict())

    bootstrap_server = (
            f'{os.environ.get("KAFKA_BOOTSTRAP_HOST")}:{os.environ.get("KAFKA_BOOTSTRAP_PORT")}' or
            'localhost:9092'
    )

    producer = KafkaProducer(bootstrap_servers=[bootstrap_server])
    producer.send('payment_request', bytes(payment_request.json(), 'utf-8'))

    return payment_request


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


def raise_is_not_exist(conn, table_name, id_name, id_value):
    query = sql.SQL('SELECT * FROM {table_name} WHERE {id_name} = %s').format(
        table_name=sql.Identifier(table_name),
        id_name=sql.Identifier(id_name)
    )

    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(query, (str(id_value), ))
        out = cur.fetchone()
        if out is None:
            raise HTTPException(status_code=400, detail=f"{id_name} not found")


def insert_raises(conn, table_name, data):
    try:
        postgres_utils.insert(conn, table_name, data)
    except psycopg2.errors.UniqueViolation as e:
        raise HTTPException(status_code=400, detail=f"{e.pgerror}")
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"db error")


if __name__ == '__main__':
    uvicorn.run(payment_app, host="0.0.0.0", port=int(os.environ['PAYMENT_APP_PORT']))
