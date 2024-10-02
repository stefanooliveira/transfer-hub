from fastapi.responses import JSONResponse, PlainTextResponse
from loguru import logger
from api.account import Account

accounts = {}

def handle_reset():
    accounts.clear()
    logger.info("All accounts reset.")
    return JSONResponse(content="OK", status_code=200)

def handle_get_balance(account_id: str):
    if account_id not in accounts:
        logger.warning(f"Account {account_id} not found.")
        return PlainTextResponse(content="0", status_code=404)
    account = accounts[account_id]
    logger.info(f"Account {account_id} balance queried: {account.balance}.")
    return PlainTextResponse(content=str(account.balance), status_code=200)

def handle_deposit(destination: str, amount: float):
    if destination not in accounts:
        accounts[destination] = Account(account_id=destination, balance=0)
        logger.info(f"New account created: {destination} with initial balance 0")

    account = accounts[destination]
    account.deposit(amount)
    logger.info(f"Deposited {amount} to account {destination}")
    
    return JSONResponse(content={"destination": {"id": destination, "balance": account.balance}}, status_code=201)

def handle_withdraw(origin: str, amount: float):
    if origin not in accounts:
        logger.warning(f"Attempted withdrawal from non-existing account: {origin}.")
        return PlainTextResponse(content="0", status_code=404)
    
    account = accounts[origin]
    try:
        account.withdraw(amount)
        logger.info(f"Withdrew {amount} from account {origin}")
    except ValueError as e:
        logger.error(f"Failed withdrawal from account {origin}: {str(e)}")
        return PlainTextResponse(content="0", status_code=404)
    
    return JSONResponse(content={"origin": {"id": origin, "balance": account.balance}}, status_code=201)

def handle_transfer(origin: str, destination: str, amount: float):
    if origin not in accounts:
        logger.warning(f"Attempted transfer from non-existing account: {origin}.")
        return PlainTextResponse(content="0", status_code=404)
    
    if destination not in accounts:
        accounts[destination] = Account(account_id=destination, balance=0)
        logger.info(f"New account created: {destination} with initial balance 0")

    origin_account = accounts[origin]
    destination_account = accounts[destination]
    
    try:
        origin_account.transfer(destination_account, amount)
        logger.info(f"Transferred {amount} from account {origin} to account {destination}.")
    except ValueError as e:
        logger.error(f"Failed transfer from account {origin} to {destination}: {str(e)}")
        return PlainTextResponse(content="0", status_code=404)
    
    return JSONResponse(content={
                                "origin": {"id": origin, "balance": origin_account.balance},
                                "destination": {"id": destination, "balance": destination_account.balance}
                        }, status_code=201)
