from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.exc import IntegrityError
from app.crud.wallet_crud import WalletCRUD
from app.schemas.wallet_schema import *
from app.errors_custom_types import *
from app.scripts_utlis.dependencies import get_current_user, owner_or_admin
import logging

router = APIRouter()
wallet_crud = WalletCRUD()
logger = logging.getLogger("app.wallet_router")

@router.post("/create_wallet", response_model=WalletResponse)
async def create_wallet(wallet: WalletCreate, current_user=Depends(get_current_user)):
    logger.info(f"{current_user.phone} creates a wallet")
    try:
        result = await wallet_crud.create_wallet(wallet=wallet)
        logger.info("Кошелек успешно создан")
        return result
    except ValueError as e:
        logger.error("Ошибка валидации при создании кошелька", exc_info=True)
        errors = e.errors()
        error_messages = []
        for error in errors:
            field = error["loc"][-1]
            message = error["msg"]
            error_messages.append(f"Ошибка в поле '{field}': {message}")
        raise HTTPException(status_code=422, detail=error_messages)
    except IntegrityError:
        logger.error("Ошибка уникальности: Кошелек для этого владельца уже существует")
        raise HTTPException(status_code=400, detail="Кошелек для этого владельца уже существует")
    except Exception as e:
        logger.error("Непредвиденная ошибка при создании кошелька", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/get_wallet/{wallet_id}", response_model=WalletResponse)
async def get_wallet(wallet_id: int, current_actor=Depends(owner_or_admin)):
    logger.info(f"{current_actor.phone} requests wallet with ID: {wallet_id}")
    try:
        wallet = await wallet_crud.get_wallet(wallet_id=wallet_id)
        logger.info(f"Кошелек с ID {wallet_id} успешно найден")
        return wallet
    except NotFoundError:
        logger.warning(f"Кошелек с ID {wallet_id} не найден")
        raise HTTPException(status_code=404, detail="Кошелек не найден")
    except Exception as e:
        logger.error("Непредвиденная ошибка при получении кошелька", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/get_wallet_by_owner", response_model=WalletResponse)
async def get_wallet_by_owner(owner_type: str, owner_id: int, current_actor=Depends(owner_or_admin)):
    logger.info(f"{current_actor.phone} requests wallet with owner_type={owner_type}, owner_id={owner_id}")
    try:
        wallet = await wallet_crud.get_wallet_by_owner(owner_type=owner_type, owner_id=owner_id)
        logger.info(f"Кошелек для {owner_type} с owner_id={owner_id} найден")
        return wallet
    except NotFoundError:
        logger.warning(f"Кошелек для {owner_type} c owner_id={owner_id} не найден")
        raise HTTPException(status_code=404, detail="Кошелек не найден")
    except Exception as e:
        logger.error("Непредвиденная ошибка при получении кошелька", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.patch("/patch_wallet/{wallet_id}", response_model=WalletResponse)
async def patch_wallet(wallet_id: int, wallet_params_to_patch: WalletPatch, current_actor=Depends(owner_or_admin)):
    logger.info(f"{current_actor.phone} patches wallet: {wallet_id}")
    try:
        patched_wallet = await wallet_crud.patch_wallet(wallet_id=wallet_id, params=wallet_params_to_patch.params)
        logger.info(f"Кошелек ID {wallet_id} успешно обновлен")
        return patched_wallet
    except NotFoundError:
        logger.warning(f"Кошелек с ID {wallet_id} не найден для patch")
        raise HTTPException(status_code=404, detail="Кошелек не найден")
    except Exception as e:
        logger.error("Непредвиденная ошибка при patch кошелька", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.delete("/delete_wallet/{wallet_id}")
async def delete_wallet(wallet_id: int, current_actor=Depends(owner_or_admin)):
    logger.info(f"{current_actor.phone} deletes wallet: {wallet_id}")
    try:
        await wallet_crud.delete_wallet(wallet_id=wallet_id)
        logger.info(f"Кошелек с ID {wallet_id} успешно удален")
        return {"message": "Кошелек удален"}
    except NotFoundError:
        logger.warning(f"Кошелек с ID {wallet_id} не найден для удаления")
        raise HTTPException(status_code=404, detail="Кошелек не найден")
    except Exception as e:
        logger.error("Непредвиденная ошибка при удалении кошелька", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")