# routes.py
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, PlainTextResponse
from api.handler import handle_reset, handle_get_balance, handle_deposit, handle_withdraw, handle_transfer

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Welcome to transfer-hub"}

@router.post("/reset")
def reset():
    return handle_reset()

@router.get("/balance")
def get_balance(account_id: str):
    return handle_get_balance(account_id)

@router.post("/event")
async def handle_event(request: Request):
    event = await request.json()
    if event['type'] == "deposit":
        return handle_deposit(event['destination'], event['amount'])
    elif event['type'] == "withdraw":
        return handle_withdraw(event['origin'], event['amount'])
    elif event['type'] == "transfer":
        return handle_transfer(event['origin'], event['destination'], event['amount'])
    else:
        return PlainTextResponse(content="Invalid event type", status_code=400)
