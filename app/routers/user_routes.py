from fastapi import APIRouter, HTTPException
from app.errors_custom_types import *
from pydantic import ValidationError
from sqlalchemy import exc
from app.crud.user_crud import UserCRUD
from app.schemas.user_schema import *
import logging

from app.scripts_utlis.jwt_utils import generate_access_token

router = APIRouter()
user_crud = UserCRUD()


logger = logging.getLogger("app.user_router")
def send_sms_mock(phone: str, code: str):
    logger.info(f"MOCK SMS: sent code {code} to {phone}")

@router.post("/request_code")
async def request_code(data: RequestCodeSchema):
    try:
        code = await user_crud.create_verification_code(phone=data.phone)
        send_sms_mock(data.phone, code)
        return {"success": True}
    except Exception as e:
        logger.error("Ошибка при создании кода", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post("/verify_code")
async def verify_code(data: VerifyCodeSchema):
    try:
        result = await user_crud.verify_code(phone=data.phone, code=data.code)
        return result
    except CodeExpired:
        raise HTTPException(status_code=400, detail="Код истек")
    except CodeLocked:
        raise HTTPException(status_code=400, detail="Превышено количество попыток. Запросите новый код.")
    except CodeInvalid:
        raise HTTPException(status_code=400, detail="Неверный код")
    except Exception as e:
        logger.error("Ошибка при верификации кода", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/create_user", response_model=UserResponse)
async def create_user(user: UserCreate):
    logger.info("Request received to create a user")
    try:
        result = await user_crud.create_user(user=user)
        logger.info("User created successfully")
        return result
    except ValidationError as e:
        logger.error("Validation error while creating user", exc_info=True)
        errors = e.errors()
        error_messages = []
        for error in errors:
            field = error['loc'][-1]
            message = error['msg']
            error_messages.append(f"Error in field '{field}': {message}")
        raise HTTPException(status_code=422, detail=error_messages)
    except exc.IntegrityError:
        logger.error("Integrity error: Email already exists")
        raise HTTPException(status_code=400, detail="Email already exists")
    except Exception as e:
        logger.error("Unexpected error while creating user", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/get_user/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    logger.info(f"Request received to get user with ID: {user_id}")
    try:
        user = await user_crud.get_user(user_id=user_id)
        logger.info(f"User with ID {user_id} retrieved successfully")
        return user
    except NotFoundError:
        logger.warning(f"User with ID {user_id} not found")
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        logger.error("Unexpected error while getting user", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.patch("/patch_user/{user_id}", response_model=UserResponse)
async def patch_user(user_id: int, user_params_to_patch: UserPatch):
    logger.info(f"Request received to patch user with ID: {user_id}")
    try:
        patched_user = await user_crud.patch_user(user_id=user_id, params=user_params_to_patch)
        logger.info(f"User with ID {user_id} patched successfully")
        return patched_user
    except NotFoundError:
        logger.warning(f"User with ID {user_id} not found")
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        logger.error("Unexpected error while patching user", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.delete("/delete_user/{user_id}")
async def delete_user(user_id: int):
    logger.info(f"Request received to delete user with ID: {user_id}")
    try:
        await user_crud.delete_user(user_id=user_id)
        logger.info(f"User with ID {user_id} deleted successfully")
        return {"message": "User deleted"}
    except NotFoundError:
        logger.warning(f"User with ID {user_id} not found")
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        logger.error("Unexpected error while patching user", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post("/token/refresh")
async def refresh_token(refresh_token_in: str):
    token_obj = await user_crud.get_refresh_token(refresh_token_in)
    if not token_obj or token_obj.valid_before < datetime.utcnow():
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")
    access_token = generate_access_token(token_obj.user_id)
    return {"access_token": access_token}