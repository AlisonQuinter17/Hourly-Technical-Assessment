from flask import Flask
from flask_cors import CORS
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import os

# Adapters
import importlib
from .src.adapters.out.persistence.transaction_repository_adapter import SqlAlchemyTransactionRepository
from .src.adapters.out.persistence.orm import Base

_controller = importlib.import_module("backend.src.adapters.in.web.transactions_controller")
api_bp = _controller.api_bp

# Use Cases
from .src.application.use_cases.create_transaction_use_case import CreateTransactionUseCase
from .src.application.use_cases.get_transaction_use_case import GetTransactionUseCase
from .src.application.use_cases.list_transactions_use_case import ListTransactionsUseCase
from .src.application.use_cases.process_transaction_use_case import ProcessTransactionUseCase
from .src.application.use_cases.ingest_transaction_use_case import IngestTransactionUseCase

# Database Setup
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/transactions_db")
engine = create_engine(DATABASE_URL)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

def create_app():
    app = Flask(__name__)
    CORS(app)

    Base.metadata.create_all(bind=engine)

    repository = SqlAlchemyTransactionRepository(db_session)
    
    process_uc = ProcessTransactionUseCase(repository)
    create_uc = CreateTransactionUseCase(repository)
    get_uc = GetTransactionUseCase(repository)
    list_uc = ListTransactionsUseCase(repository)
    ingest_uc = IngestTransactionUseCase(create_uc, process_uc)

    app.config["USE_CASES"] = {
        "create_transaction_use_case": create_uc,
        "get_transaction_use_case": get_uc,
        "list_transactions_use_case": list_uc,
        "process_transaction_use_case": process_uc,
        "ingest_transaction_use_case": ingest_uc,
    }

    app.register_blueprint(api_bp)
    
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()
        
    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
