from uuid import UUID, uuid4
from decimal import Decimal
from pydantic import BaseModel
from typing import Optional


class PaymentRequest(BaseModel):
    payment_request_id: Optional[UUID]
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


class PaymentMethod(BaseModel):
    payment_method_id: Optional[UUID]
    name: str = None


class User(BaseModel):
    user_id: Optional[UUID] = None
    first_name: str = None
    last_name: str = None

