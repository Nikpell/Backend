import uuid

from sqlalchemy import Column, DateTime, func, ForeignKey, BigInteger
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from postgres import Base

class Count(Base):
    __tablename__ = "count_table"
    account_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user_table.id"), nullable=False)
    balance = Column(BigInteger)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    user = relationship("User", foreign_keys=[user_id])