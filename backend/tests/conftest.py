import os
import pytest
from sqlalchemy import create_engine

os.environ["DATABASE_URL"] = "sqlite:///test.db"

from backend import main
from backend.src.adapters.out.persistence.orm import Base

@pytest.fixture(scope="session")
def cleanup_db_file():
    yield
    if os.path.exists("test.db"):
        os.remove("test.db")

@pytest.fixture
def app(cleanup_db_file):
    app = main.create_app()
    app.config.update({
        "TESTING": True,
    })
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def init_database():
    Base.metadata.drop_all(bind=main.engine)
    Base.metadata.create_all(bind=main.engine)
    yield
    Base.metadata.drop_all(bind=main.engine)
    main.db_session.remove()
