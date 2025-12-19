from ...domain.transaction import Transaction
from .create_transaction_use_case import CreateTransactionUseCase
from .process_transaction_use_case import ProcessTransactionUseCase

class IngestTransactionUseCase:
    def __init__(self, create_use_case: CreateTransactionUseCase, process_use_case: ProcessTransactionUseCase):
        self.create_use_case = create_use_case
        self.process_use_case = process_use_case

    def execute(self, file_path: str) -> Transaction:
        transaction = self.create_use_case.execute()
        self.process_use_case.execute(transaction.id, file_path)

        return transaction
