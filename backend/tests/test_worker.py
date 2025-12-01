import pytest
from backend import worker, models, database
import io

def test_process_csv_task():
    """Test CSV processing logic"""
    csv_content = "id,date,type,amount\n1,2024-01-01,debit,100.00\n2,2024-01-02,credit,200.00\n3,2024-01-03,debit,50.00"
    
    # Create a test transaction
    database.init_db()
    session = database.db_session()
    transaction = models.Transaction(status="pending")
    session.add(transaction)
    session.commit()
    transaction_id = transaction.id
    session.close()
    
    # Process the CSV
    worker.process_csv_task(transaction_id, csv_content)
    
    # Verify results
    session = database.db_session()
    processed_transaction = session.query(models.Transaction).filter(
        models.Transaction.id == transaction_id
    ).first()
    
    assert processed_transaction.status == "done"
    assert processed_transaction.num_records == 3
    assert processed_transaction.total_debit == 150.00
    assert processed_transaction.total_credit == 200.00
    
    session.close()
    database.Base.metadata.drop_all(bind=database.engine)

def test_process_csv_empty():
    """Test processing empty CSV"""
    csv_content = "id,date,type,amount"
    
    database.init_db()
    session = database.db_session()
    transaction = models.Transaction(status="pending")
    session.add(transaction)
    session.commit()
    transaction_id = transaction.id
    session.close()
    
    worker.process_csv_task(transaction_id, csv_content)
    
    session = database.db_session()
    processed_transaction = session.query(models.Transaction).filter(
        models.Transaction.id == transaction_id
    ).first()
    
    assert processed_transaction.status == "done"
    assert processed_transaction.num_records == 0
    assert processed_transaction.total_debit == 0.0
    assert processed_transaction.total_credit == 0.0
    
    session.close()
    database.Base.metadata.drop_all(bind=database.engine)
