import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from backend import database
from backend.main import app

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    # Use SQLite for tests
    test_engine = create_engine("sqlite:///:memory:")
    database.engine = test_engine
    database.db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=test_engine))
    database.Base.metadata.bind = test_engine
    database.Base.query = database.db_session.query_property()

@pytest.fixture(autouse=True)
def init_database(setup_test_db):
    # Create tables
    database.Base.metadata.create_all(bind=database.engine)
    yield
    # Drop tables
    database.Base.metadata.drop_all(bind=database.engine)
    database.db_session.remove()

@pytest.fixture
def client(init_database):
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
