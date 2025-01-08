import pytest
import sys
import os
from unittest import mock
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../backend")))

# Fixture per il client Flask
@pytest.fixture
def client():
    """Fixture per il client Flask."""
    from app import app
    #print("Registered routes:", app.url_map)
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
