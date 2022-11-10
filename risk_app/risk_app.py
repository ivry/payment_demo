import json
import random
import os
import psycopg2.errors
from kafka import KafkaConsumer
from common.models import PaymentRequest, AuthRequest

from common import postgres_utils


def process():
    bootstrap_server = (
            f'{os.environ.get("KAFKA_BOOTSTRAP_HOST")}:{os.environ.get("KAFKA_BOOTSTRAP_PORT")}' or
            'localhost:9092'
    )

    bootstrap_server = 'broker:9092'
    print(bootstrap_server)

    consumer = KafkaConsumer('payment_request', bootstrap_servers=[bootstrap_server])

    for message in consumer:
        r = PaymentRequest(**json.loads(message.value))

        auth_request_id = r.payment_request_id
        auth_request = AuthRequest(**(r.dict(exclude={'payment_request_id'}) | {'auth_request_id': auth_request_id}))
        random.seed(hash(str(auth_request_id)))
        auth_request.risk_score = int(random.random() * 100)

        with postgres_utils.get_connection(db_schema='risk_schema') as conn:
            try:
                postgres_utils.insert(conn, 'auth_request', auth_request.dict())
            except psycopg2.errors.UniqueViolation as e:
                # ignore duplicate message
                pass
            except Exception as e:
                # Other error
                pass

        print(r)


if __name__ == '__main__':
    process()
