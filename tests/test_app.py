import pytest
from app import app
from unittest.mock import patch


@pytest.fixture
def client():
    with app.app_context():
        with app.test_client() as client:
            yield client


@pytest.fixture
def mock_save_password_fail(request):
    with patch('app.save_password', return_value=False):
        yield request


def test_change_password_wrong_path(client):
    response = client.get('/')
    assert response.status_code == 404


def test_change_password_wrong_method(client):
    response = client.get('/change_password')
    assert response.status_code == 405


def test_change_password_no_data_provided(client):
    response = client.post('/change_password')
    assert response.status_code == 400


def test_change_password_with_invalid_password(client):
    response = client.post(
        '/change_password',
        data={
            'old_password': 'old_password',
            'new_password': 'new_password'
        }
    )
    assert response.status_code == 400
    assert response.data == b'At least 18 alphanumeric characters and list of special chars !@#$&*.'


def test_change_password_success(client):
    response = client.post(
        '/change_password',
        data={
            'old_password': 'new_password',
            'new_password': '1qaz@WSX3edc$RFV5tgb'
        }
    )
    assert response.status_code == 200


@pytest.mark.usefixtures("mock_save_password_fail")
def test_change_password_save_failed(client):
    response = client.post(
        '/change_password',
        data={
            'old_password': 'new_password',
            'new_password': '1qaz@WSX3edc$RFV5tgb'
        }
    )
    assert response.status_code == 500
