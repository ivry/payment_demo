from uuid import uuid4
from decimal import Decimal

from kafka import KafkaProducer
from models import PaymentRequest, APIPaymentRequest


producer = KafkaProducer(bootstrap_servers=['localhost:9092'])


def create_payment_request():
    payment_request_id = uuid4()
    for i in range(5):
        r = PaymentRequest(
            payment_request_id=payment_request_id,
            amount=Decimal(i*10),
            currency='USD',
            user_id=uuid4(),
            payee_id=uuid4(),
            payment_method_id=uuid4()
        )
        future = producer.send('payment_request', bytes(r.json(), 'utf-8'))
        producer.flush()
        print(r.json())


if __name__ == '__main__':
    create_payment_request()
