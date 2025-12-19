from typing import List, Optional
from sqlalchemy.orm import Session
from ....application.ports.out.transaction_repository import TransactionRepositoryPort
from ....domain.transaction import Transaction
from .orm import TransactionModel

class SqlAlchemyTransactionRepository(TransactionRepositoryPort):
    def __init__(self, session: Session):
        self.session = session

    def _to_domain(self, model: TransactionModel) -> Transaction:
        return Transaction(
            id=model.id,
            status=model.status,
            created_at=model.created_at,
            num_records=model.num_records,
            total_debit=model.total_debit,
            total_credit=model.total_credit
        )

    def _to_model(self, entity: Transaction) -> TransactionModel:
        return TransactionModel(
            id=entity.id,
            status=entity.status,
            created_at=entity.created_at,
            num_records=entity.num_records,
            total_debit=entity.total_debit,
            total_credit=entity.total_credit
        )

    def save(self, transaction: Transaction) -> None:
        model = self.session.query(TransactionModel).filter_by(id=transaction.id).first()
        if model:
            # Update
            model.status = transaction.status
            model.num_records = transaction.num_records
            model.total_debit = transaction.total_debit
            model.total_credit = transaction.total_credit
        else:
            # Create
            model = self._to_model(transaction)
            self.session.add(model)
        
        self.session.commit()

    def get_by_id(self, transaction_id: str) -> Optional[Transaction]:
        model = self.session.query(TransactionModel).filter_by(id=transaction_id).first()
        if model:
            return self._to_domain(model)
        return None

    def list_all(self) -> List[Transaction]:
        models = self.session.query(TransactionModel).all()
        return [self._to_domain(m) for m in models]
