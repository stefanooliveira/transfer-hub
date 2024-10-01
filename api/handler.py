from fastapi.responses import JSONResponse, PlainTextResponse

accounts = {}

def handle_reset():
    accounts.clear()
    return JSONResponse(content="OK", status_code=200)

def handle_get_balance(account_id: str):
    if account_id not in accounts:
        return PlainTextResponse(content="0", status_code=404)
    return PlainTextResponse(content=str(accounts[account_id]), status_code=200)

def handle_deposit(destination: str, amount: int):
    if destination not in accounts:
        accounts[destination] = 0
    accounts[destination] += amount
    return JSONResponse(content={"destination": {"id": destination, "balance": accounts[destination]}}, status_code=201)

def handle_withdraw(origin: str, amount: int):
    if origin not in accounts or accounts[origin] < amount:
        return PlainTextResponse(content="0", status_code=404)
    accounts[origin] -= amount
    return JSONResponse(content={"origin": {"id": origin, "balance": accounts[origin]}}, status_code=201)

def handle_transfer(origin: str, destination: str, amount: int):
    if origin not in accounts or accounts[origin] < amount:
        return PlainTextResponse(content="0", status_code=404)
    accounts[origin] -= amount
    if destination not in accounts:
        accounts[destination] = 0


    accounts[destination] += amount

    return JSONResponse(content={
        "origin": {"id": origin, "balance": accounts[origin]},
        "destination": {"id": destination, "balance": accounts[destination]}
    }, status_code=201)
