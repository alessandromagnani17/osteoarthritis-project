import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../backend")))
from app import app

@pytest.fixture
def client():
    """Fixture per il client Flask."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    """Test per l'endpoint home."""
    response = client.get('/')
    assert response.status_code == 200
    assert response.json["message"] == "Welcome to the API!"
