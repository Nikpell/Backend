import uuid

from pydantic import BaseModel

from schemas.transaction_schema import TransactionInputSchema


class TransactionConfirmSchema(TransactionInputSchema):
    signature: str
    transaction_id: uuid.UUID
    user_id: uuid.UUID


class PaymentSchema(BaseModel):
    product_id: uuid.UUID
    bill_id: uuid.UUID