from pydantic import BaseModel
from typing import Optional

class TransactionInputSchema(BaseModel):
    user_id: Optional[str]
    account_id: Optional[str]
    amount: Optional[int]
    signature: Optional[str]
    transaction_id: Optional[str]


    class Config:
        from_attributes = True