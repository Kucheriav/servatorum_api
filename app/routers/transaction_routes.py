from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.exc import IntegrityError
from app.crud.transaction_crud import TransactionCRUD
from app.schemas.transaction_schema import *
from app.errors_custom_types import *
from app.scripts_utlis.dependencies import get_current_user, owner_or_admin, get_current_admin
import logging

router = APIRouter()
transaction_crud = TransactionCRUD()
logger = logging.getLogger("app.transaction_router")

@router.post("/create_transaction", response_model=TransactionResponse)
async def create_transaction(transaction: TransactionCreate, current_user=Depends(get_current_user)):
    logger.info(f"{current_user.phone} creates a transaction")
    try:
        result = await transaction_crud.create_transaction(tx=transaction)
        return result
    except ValidationError as e:
        logger.error("Ошибка валидации при создании транзакции", exc_info=True)
        errors = e.errors()
        error_messages = []
        for error in errors:
            field = error['loc'][-1]
            message = error['msg']
            error_messages.append(f"Ошибка в поле '{field}': {message}")
        raise HTTPException(status_code=422, detail=error_messages)
    except NotFoundError as e:
        logger.warning(str(e))
        raise HTTPException(status_code=404, detail=str(e))
    except IntegrityError:
        logger.error("Ошибка уникальности/целостности при создании транзакции")
        raise HTTPException(status_code=400, detail="Ошибка уникальности или бизнес-правил")
    except Exception as e:
        logger.error("Непредвиденная ошибка при создании транзакции", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/get_transaction/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(transaction_id: int, current_actor=Depends(owner_or_admin)):
    logger.info(f"{current_actor.phone} requests transaction with ID: {transaction_id}")
    try:
        tx = await transaction_crud.get_transaction(transaction_id=transaction_id)
        logger.info(f"Транзакция с ID {transaction_id} найдена")
        return tx
    except NotFoundError:
        logger.warning(f"Транзакция с ID {transaction_id} не найдена")
        raise HTTPException(status_code=404, detail="Транзакция не найдена")
    except Exception as e:
        logger.error("Непредвиденная ошибка при получении транзакции", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/get_transactions_for_wallet/{wallet_id}", response_model=List[TransactionResponse])
async def get_transactions_for_wallet(wallet_id: int, limit: int = 30, offset: int = 0, current_actor=Depends(owner_or_admin)):
    logger.info(f"{current_actor.phone} requests transactions for wallet with ID: {wallet_id}")
    try:
        txs = await transaction_crud.get_transactions_for_wallet(wallet_id=wallet_id, limit=limit, offset=offset)
        logger.info(f"Найдено {len(txs)} транзакций для кошелька ID {wallet_id}")
        return txs
    except Exception as e:
        logger.error("Непредвиденная ошибка при получении истории транзакций", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.delete("/delete_transaction/{transaction_id}")
async def delete_transaction(transaction_id: int, current_admin=Depends(get_current_admin)):
    logger.info(f"{current_admin.username} requests delete transaction with ID: {transaction_id}")
    try:
        await transaction_crud.delete_transaction(transaction_id=transaction_id)
        logger.info(f"Транзакция с ID {transaction_id} успешно удалена")
        return {"message": "Транзакция удалена"}
    except NotFoundError:
        logger.warning(f"Транзакция с ID {transaction_id} не найдена для удаления")
        raise HTTPException(status_code=404, detail="Транзакция не найдена")
    except Exception as e:
        logger.error("Непредвиденная ошибка при удалении транзакции", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")