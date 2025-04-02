import uuid

from sqlalchemy import Column, DateTime, func, ForeignKey, BigInteger, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from postgres import Base


class Transaction(Base):
    __tablename__ = "transactions_table"
    transaction_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    transaction_number = Column(String, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user_table.id"), nullable=False)
    account_id = Column(UUID(as_uuid=True), ForeignKey("count_table.account_id"), nullable=False)
    amount = Column(BigInteger)
    signature = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    user = relationship("User", foreign_keys=[user_id])
    count = relationship("Count", foreign_keys=[account_id])