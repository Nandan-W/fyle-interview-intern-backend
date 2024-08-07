import pytest
import json
from unittest.mock import patch
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import HTTPException
from core import db
from core.server import app

def test_ready_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.json['status'] == 'ready'
    assert 'time' in response.json


def test_page_not_found(client):
    response = client.get('/nonexistent-endpoint')
    assert response.status_code == 404
    assert response.json['error'] == 'NotFoundError'
    assert response.json['message'] == 'No such api'


def test_integrity_error_handling(client):
    response = client.get('/trigger-integrity-error')
    assert response.status_code == 400
    assert response.json['error'] == 'IntegrityError'
    assert response.json['message'] == 'mock orig'


@pytest.fixture(scope='function')
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_http_exception_handling(client):
    response = client.get('/trigger-http-exception')
    assert response.status_code == 403
    assert response.json['error'] == 'Forbidden'
    assert response.json['message'] == '403 Forbidden: mock HTTPException'


def test_unhandled_exception_handling(client):
    response = client.get('/trigger-unhandled-exception')
    assert response.status_code == 500
    assert response.json['error'] == 'InternalServerError'
    assert response.json['message'] == 'An unexpected error occurred.'