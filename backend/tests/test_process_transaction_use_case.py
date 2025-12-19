from unittest.mock import MagicMock
from ..src.application.use_cases.process_transaction_use_case import ProcessTransactionUseCase
from ..src.domain.transaction import Transaction
import tempfile
import os

def test_process_transaction_logic():
    mock_repo = MagicMock()
    use_case = ProcessTransactionUseCase(mock_repo)
    
    tx = Transaction(id="123", status="pending")
    mock_repo.get_by_id.return_value = tx
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
        f.write("id,date,type,amount\n1,2024-01-01,debit,100.00\n2,2024-01-02,credit,50.00")
        temp_path = f.name
        
    try:
        use_case._process("123", temp_path)
        
        assert tx.status == "done"
        assert tx.num_records == 2
        assert tx.total_debit == 100.00
        assert tx.total_credit == 50.00
        
        assert mock_repo.save.call_count >= 2
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
