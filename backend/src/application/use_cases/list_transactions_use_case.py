from typing import List
from ...domain.transaction import Transaction
from ..ports.out.transaction_repository import TransactionRepositoryPort

class ListTransactionsUseCase:
    def __init__(self, repo: TransactionRepositoryPort):
        self.repo = repo

    def execute(self) -> List[Transaction]:
        return self.repo.list_all()
