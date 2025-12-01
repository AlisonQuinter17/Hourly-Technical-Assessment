import csv
import io
import threading
from . import models, database

def process_csv_task(transaction_id: str, file_content: str):
    session = database.db_session()
    try:
        transaction = session.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()
        if not transaction:
            return

        transaction.status = "processing"
        session.commit()

        csv_reader = csv.DictReader(io.StringIO(file_content))

        num_records = 0
        total_debit = 0.0
        total_credit = 0.0

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
        session.commit()

    except Exception as e:
        import logging
        logging.error(f"Error processing CSV: {e}")
    finally:
        session.close()
        database.db_session.remove()

def start_processing(transaction_id: str, file_content: str):
    thread = threading.Thread(target=process_csv_task, args=(transaction_id, file_content))
    thread.start()
