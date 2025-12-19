import csv
import os
import threading
from ..ports.out.transaction_repository import TransactionRepositoryPort

class ProcessTransactionUseCase:
    def __init__(self, repo: TransactionRepositoryPort):
        self.repo = repo

    def execute(self, transaction_id: str, file_path: str):
        thread = threading.Thread(target=self._process, args=(transaction_id, file_path))
        thread.start()

    def _process(self, transaction_id: str, file_path: str):
        transaction = self.repo.get_by_id(transaction_id)
        if not transaction:
             return

        transaction.status = "processing"
        self.repo.save(transaction)

        try:
            num_records = 0
            total_debit = 0.0
            total_credit = 0.0

            with open(file_path, 'r', encoding='utf-8') as f:
                csv_reader = csv.DictReader(f)
                for row in csv_reader:
                    num_records += 1
                    amount = float(row["amount"])
                    if row["type"] == "debit":
                        total_debit += amount
                    elif row["type"] == "credit":
                        total_credit += amount

            transaction.num_records = num_records
            transaction.total_debit = total_debit
            transaction.total_credit = total_credit
            transaction.status = "done"
            
            self.repo.save(transaction)

        except Exception as e:
            print(f"Error processing: {e}")
            transaction.mark_failed()
            self.repo.save(transaction)
        
        finally:
             if os.path.exists(file_path):
                os.remove(file_path)
