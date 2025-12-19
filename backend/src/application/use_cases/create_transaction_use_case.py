from ...domain.transaction import Transaction
from ..ports.out.transaction_repository import TransactionRepositoryPort

class CreateTransactionUseCase:
    def __init__(self, repo: TransactionRepositoryPort):
        self.repo = repo

    def execute(self) -> Transaction:
        transaction = Transaction(status="pending")
        self.repo.save(transaction)
        return transaction
