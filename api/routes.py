from fastapi import APIRouter, HTTPException, status, Request
from fastapi.responses import JSONResponse

router = APIRouter()

state = {}

@router.get("/")
async def root():
    return {"message": "Welcome to transfer-hub"}

@router.post("/reset", status_code=status.HTTP_200_OK)
def reset():
    state.clear()
    return JSONResponse(content={"status": "reset"}, status_code=status.HTTP_200_OK)

@router.get("/balance", status_code=status.HTTP_200_OK)
def get_balance(account_id: str):
    if account_id not in state:
        raise HTTPException(status_code=404, detail="Account not found")
    return JSONResponse(content={"balance": state[account_id]}, status_code=status.HTTP_200_OK)
