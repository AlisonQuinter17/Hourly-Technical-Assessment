from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import uuid

@dataclass
class Transaction:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    status: str = "pending"
    created_at: datetime = field(default_factory=datetime.utcnow)
    num_records: int = 0
    total_debit: float = 0.0
    total_credit: float = 0.0

    def calculate_totals(self, records: list[dict]):
        self.num_records = 0
        self.total_debit = 0.0
        self.total_credit = 0.0
        
        for record in records:
            self.num_records += 1
            amount = float(record.get("amount", 0))
            type_ = record.get("type")
            
            if type_ == "debit":
                self.total_debit += amount
            elif type_ == "credit":
                self.total_credit += amount
        
        self.status = "done"

    def mark_failed(self):
        self.status = "failed"
