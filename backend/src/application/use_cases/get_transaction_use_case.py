from ...domain.transaction import Transaction
from ..ports.out.transaction_repository import TransactionRepositoryPort

class GetTransactionUseCase:
    def __init__(self, repo: TransactionRepositoryPort):
        self.repo = repo

    def execute(self, transaction_id: str) -> Transaction:
        return self.repo.get_by_id(transaction_id)
