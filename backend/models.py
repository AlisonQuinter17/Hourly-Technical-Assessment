from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from .database import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="pending")
    num_records = Column(Integer, default=0)
    total_debit = Column(Float, default=0.0)
    total_credit = Column(Float, default=0.0)

    def to_dict(self):
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "status": self.status,
            "num_records": self.num_records,
            "total_debit": self.total_debit,
            "total_credit": self.total_credit
        }
