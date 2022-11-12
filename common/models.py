from uuid import UUID, uuid4
from decimal import Decimal
from pydantic import BaseModel


class APIPaymentRequest(BaseModel):
    user_id: UUID
    payee_id: UUID
    payment_method_id: UUID
    amount: Decimal
    currency: str


class PaymentRequest(BaseModel):
    payment_request_id: UUID
    user_id: UUID
    payee_id: UUID
    payment_method_id: UUID
    amount: Decimal
    currency: str


class AuthRequest(BaseModel):
    auth_request_id: UUID
    user_id: UUID
    payee_id: UUID
    payment_method_id: UUID
    amount: Decimal
    currency: str
    risk_score: float = 0


class APIPaymentMethod(BaseModel):
    name: str = None


class PaymentMethod(BaseModel):
    payment_method_id: UUID
    name: str = None


class APIUser(BaseModel):
    first_name: str = None
    last_name: str = None


class User(BaseModel):
    user_id: UUID
    first_name: str = None
    last_name: str = None

