import threading
from loguru import logger

class Account:
    def __init__(self, account_id: str, balance: float = 0.0) -> None:
        self._account_id = account_id
        self._balance = balance
        self._lock = threading.Lock()
        logger.info(f"Account created with id {self._account_id} and balance {self._balance}")

    @property
    def account_id(self):
        return self._account_id
    
    @property
    def balance(self):
        return self._balance
    
    def deposit(self, amount: float):
        if amount < 0.0:
            raise ValueError("Amount should be positive for deposit")
        self._balance += amount
        logger.info(f"Deposited {amount} to account {self._account_id}")
    
    def withdraw(self, amount: float):
        if amount > self._balance:
            logger.error(f"Insufficient funds for withdrawal from account {self._account_id}.")
            raise ValueError("Don't have enough balance for withdraw")
        if amount < 0.0:
            logger.error(f"Invalid withdrawal amount: {amount} for account {self._account_id}")
            raise ValueError("Withdraw must be greater than zero")
        
        self._balance -= amount
        logger.info(f"Withdraw {amount} from account {self._account_id}")
    
    def transfer(self, destination: 'Account', amount: float):
        if amount > self.balance:
            logger.error(f"Insufficient funds for transfer from account {self._account_id} to account {destination.account_id}")
            raise ValueError("Insufficient funds for transfer")
        if amount < 0:
            logger.error(f"Invalid transfer amount: {amount} from account {self._account_id}"\
                          "to {destination.account_id}. Transfer amount must be positive")
            raise ValueError("Transfer amount must be positive")

        with self._lock, destination._lock:
            self.withdraw(amount)
            destination.deposit(amount)
        logger.info(f"Transferred {amount} from account {self._account_id} to account {destination.account_id}.")

    def __repr__(self) -> str:
        return f'Account Id={self._account_id} has balance: {self._balance}'



if __name__ == '__main__':
    acc = Account(100)
    acc2 = Account(101)
    logger.debug(acc)
    acc.deposit(10)
    acc.withdraw(5)
    acc.transfer(destination=acc2, amount=3)
    logger.debug(acc)
    logger.debug(acc2)