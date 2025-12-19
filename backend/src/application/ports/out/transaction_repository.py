from abc import ABC, abstractmethod
from typing import Optional, List
from ....domain.transaction import Transaction

class TransactionRepositoryPort(ABC):
    @abstractmethod
    def save(self, transaction: Transaction) -> None:
        pass

    @abstractmethod
    def get_by_id(self, transaction_id: str) -> Optional[Transaction]:
        pass

    @abstractmethod
    def list_all(self) -> List[Transaction]:
        pass
