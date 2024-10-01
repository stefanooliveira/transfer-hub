import pytest
import json

from fastapi.responses import JSONResponse, PlainTextResponse
from api.handler import handle_reset, handle_get_balance, handle_deposit, handle_withdraw, handle_transfer

@pytest.fixture(autouse=True)
def setup_and_teardown():
    handle_reset()

def test_handle_reset():
    response = handle_reset()
    assert response.status_code == 200
    response_content = json.loads(response.body.decode())
    assert response_content == "OK"

def test_handle_get_balance_non_existing():
    response = handle_get_balance("-1")
    assert response.status_code == 404
    assert response.body.decode() == "0"

def test_handle_deposit():
    response = handle_deposit("100", 10)
    assert response.status_code == 201
    response_content = json.loads(response.body.decode())
    assert response_content == {"destination": {"id": "100", "balance": 10}}


def test_handle_withdraw_non_existing():
    response = handle_withdraw("200", 10)
    assert response.status_code == 404
    assert response.body.decode() == "0"

def test_handle_withdraw_existing():
    handle_deposit("100", 10) 
    response = handle_withdraw("100", 5)
    assert response.status_code == 201
    response_content = json.loads(response.body.decode())
    assert response_content == {"origin": {"id": "100", "balance": 5}}

def test_handle_transfer_existing():
    handle_deposit("100", 20) 
    response = handle_transfer("100", "300", 15)
    assert response.status_code == 201
    response_content = json.loads(response.body.decode())
    assert response_content == {
        "origin": {"id": "100", "balance": 5},
        "destination": {"id": "300", "balance": 15}
    }

def test_handle_transfer_non_existing():
    response = handle_transfer("200", "300", 15)
    assert response.status_code == 404
    assert response.body.decode() == "0"