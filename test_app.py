import pytest
from flask import Flask
from app import app, db
from alembic.config import Config
from alembic import command


@pytest.fixture
def client():
    app.config['TESTING'] = True

    # Load Alembic configuration and point it to the correct location
    alembic_cfg = Config("alembic.ini")

    with app.test_client() as client:
        with app.app_context():
            # Run Alembic migrations instead of db.create_all()
            command.upgrade(alembic_cfg, "head")  # Apply migrations

        yield client

        with app.app_context():
            db.session.remove()
            # Optionally, you can use Alembic to downgrade and clean up the database if needed
            command.downgrade(alembic_cfg, "base")  # Revert all migrations


def test_generate_answer(client):
    response = client.post('/ask', json={'question': 'What is Python?'})
    assert response.status_code == 200
    data = response.get_json()
    assert 'question' in data
    assert 'answer' in data
    assert data['question'] == 'What is Python?'
