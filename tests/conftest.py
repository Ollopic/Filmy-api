import pytest
import os
import tempfile
from app.app import app
from app.db.fixtures.generate_test_data import generate_test_data

@pytest.fixture
def client():
    db_fd, db_path = tempfile.mkstemp()

    app.config['TESTING'] = True
    app.config['DATABASE'] = db_path

    with app.test_client() as client:
        with app.app_context():
            generate_test_data()
        yield client

    os.close(db_fd)
    os.unlink(db_path)

