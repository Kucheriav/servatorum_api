from fastapi import APIRouter, HTTPException
from app.crud.wallet_crud import WalletCRUD
from app.schemas.wallet_schema import *
from app.errors_custom_types import *
import logging

router = APIRouter()
wallet_crud = WalletCRUD()
logger = logging.getLogger("app.wallet_routes")

@router.get("/wallet/balance/{user_id}", response_model=WalletBalanceResponse)
async def get_balance(user_id: int):
    logger.info(f"Request received to get balance for user ID: {user_id}")
    try:
        balance = await wallet_crud.get_balance(user_id=user_id)
        return WalletBalanceResponse(user_id=user_id, balance=balance)
    except UserNotFoundError:
        logger.warning(f"User with ID {user_id} not found")
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        logger.error("Unexpected error while getting balance", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/wallet/history/{user_id}", response_model=WalletHistoryResponse)
async def get_wallet_history(user_id: int):
    logger.info(f"Request received to get wallet history for user ID: {user_id}")
    try:
        history = await wallet_crud.get_history(user_id=user_id)
        return WalletHistoryResponse(
            user_id=user_id,
            history=history
        )
    except Exception as e:
        logger.error("Unexpected error while getting wallet history", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post("/wallet/deposit/{user_id}", response_model=UserWalletTransactionResponse)
async def deposit(user_id: int, amount: float, comment: str = "Пополнение"):
    logger.info(f"Request received to deposit {amount} for user ID: {user_id}")
    try:
        transaction = await wallet_crud.deposit(user_id=user_id, amount=amount, comment=comment)
        return transaction
    except UserNotFoundError:
        logger.warning(f"User with ID {user_id} not found")
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        logger.error("Unexpected error during deposit", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post("/wallet/withdraw/{user_id}", response_model=UserWalletTransactionResponse)
async def withdraw(user_id: int, amount: float, comment: str = "Списание"):
    logger.info(f"Request received to withdraw {amount} for user ID: {user_id}")
    try:
        transaction = await wallet_crud.withdraw(user_id=user_id, amount=amount, comment=comment)
        return transaction
    except UserNotFoundError:
        logger.warning(f"User with ID {user_id} not found")
        raise HTTPException(status_code=404, detail="User not found")
    except InsufficientFundsError:
        logger.warning(f"Insufficient funds for user ID {user_id}")
        raise HTTPException(status_code=400, detail="Insufficient funds")
    except Exception as e:
        logger.error("Unexpected error during withdrawal", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")