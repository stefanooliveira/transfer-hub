import pytest
from api.account import Account

@pytest.fixture
def account():
    return Account(account_id="100", balance=50.0)

@pytest.fixture
def another_account():
    return Account(account_id="101", balance=30.0)

def test_account_creation(account):
    assert account.account_id == "100"
    assert account.balance == 50.0

def test_deposit(account):
    account.deposit(20.0)
    assert account.balance == 70.0

def test_deposit_negative(account):
    with pytest.raises(ValueError, match="Amount should be positive for deposit"):
        account.deposit(-10.0)

def test_withdraw(account):
    account.withdraw(30.0)
    assert account.balance == 20.0

def test_withdraw_insufficient_funds(account):
    with pytest.raises(ValueError, match="Don't have enough balance for withdraw"):
        account.withdraw(60.0)

def test_withdraw_negative_amount(account):
    with pytest.raises(ValueError, match="Withdraw must be greater than zero"):
        account.withdraw(-5.0)

def test_transfer(account, another_account):
    account.transfer(destination=another_account, amount=20.0)
    assert account.balance == 30.0
    assert another_account.balance == 50.0

def test_transfer_insufficient_funds(account, another_account):
    with pytest.raises(ValueError, match="Insufficient funds for transfer"):
        account.transfer(destination=another_account, amount=60.0)

def test_transfer_negative_amount(account, another_account):
    with pytest.raises(ValueError, match="Transfer amount must be positive"):
        account.transfer(destination=another_account, amount=-5.0)
