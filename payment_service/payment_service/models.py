from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

class PaymentProvider(str, Enum):
    PAYFAST = "payfast"
    STRIPE = "stripe"

class PaymentStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"

class Payment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int
    amount: float
    currency: str
    provider: PaymentProvider
    status: PaymentStatus = Field(default=PaymentStatus.PENDING)
    transaction_id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now(datetime.UTC))
    updated_at: datetime = Field(default_factory=datetime.now(datetime.UTC))

class PaymentCreate(SQLModel):
    order_id: int
    amount: float
    currency: str
    provider: PaymentProvider