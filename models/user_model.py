import uuid

from sqlalchemy import Column, String, DateTime, func, Enum, Boolean
from sqlalchemy.dialects.postgresql import UUID

from postgres import Base



class User(Base):
    __tablename__ = "user_table"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    e_mail = Column(String, nullable=False)
    password = Column(String, nullable=False, unique=True)
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


    def __str__(self):
        return str(self.id)

    def to_dict(self):
        return {"user_id": str(self.id), "is_admin": str(self.is_admin)}