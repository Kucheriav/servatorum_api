from fastapi import APIRouter, HTTPException, Depends
from app.errors_custom_types import *
from pydantic import ValidationError
from sqlalchemy import exc
from app.crud.admin_crud import AdminCRUD
from app.schemas.admin_schema import *
from app.models.admin_model import *
from app.scripts_utils.dependencies import get_current_admin, superadmin_required
import logging
from app.scripts_utils.bot_sms_code_sender import bot


router = APIRouter()
admin_crud = AdminCRUD()


logger = logging.getLogger("app.admin_router")

async def send_via_tg(phone: str, code: str):
    logger.info("into sending func")
    chat_id_list = await admin_crud.get_chat_id_for_bot()
    for chat_id in chat_id_list:
        await bot.send_message(chat_id=chat_id, text=f'sent code {code} to {phone}')


def send_sms_mock(phone: str, code: str):
    logger.info(f"MOCK SMS: sent code {code} to {phone}")

@router.post("/request_code")
async def request_code(data: RequestCodeSchema):
    try:
        code = await admin_crud.create_verification_code(phone=data.phone)
        send_sms_mock(data.phone, code)
        await send_via_tg(data.phone, code)
        return {"success": True}
    except Exception as e:
        logger.error("Ошибка при создании кода", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post("/verify_code", response_model=AuthResponse)
async def verify_code(data: VerifyCodeSchema):
    try:
        result = await admin_crud.verify_code(phone=data.phone, code=data.code)
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


@router.post("/create_admin", response_model=AuthResponse)
async def create_admin(admin: AdminCreate, superadmin: Admin=Depends(superadmin_required)):
    logger.info(f"{superadmin.username} creates an admin")
    try:
        result = await admin_crud.create_admin(admin=admin)
        logger.info("Admin created successfully")
        return result
    except ValidationError as e:
        logger.error("Validation error while creating admin", exc_info=True)
        errors = e.errors()
        error_messages = []
        for error in errors:
            field = error['loc'][-1]
            message = error['msg']
            error_messages.append(f"Error in field '{field}': {message}")
        raise HTTPException(status_code=422, detail=error_messages)
    except exc.IntegrityError:
        logger.error("Integrity error: Email or phone already exists")
        raise HTTPException(status_code=400, detail="Email or phone already exists")
    except Exception as e:
        logger.error("Unexpected error while creating admin", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/get_admin/{admin_id}", response_model=AdminResponse)
async def get_admin(admin_id: int, current_admin: Admin=Depends(get_current_admin)):
    logger.info(f"{current_admin.username} gets admin with ID: {admin_id}")
    try:
        admin = await admin_crud.get_admin(admin_id=admin_id)
        logger.info(f"Admin with ID {admin_id} retrieved successfully")
        return admin
    except NotFoundError:
        logger.warning(f"Admin with ID {admin_id} not found")
        raise HTTPException(status_code=404, detail="Admin not found")
    except Exception as e:
        logger.error("Unexpected error while getting admin", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.patch("/patch_admin/{admin_id}", response_model=AdminResponse)
async def patch_admin(admin_id: int, admin_params_to_patch: AdminPatch, superadmin=Depends(superadmin_required)):
    logger.info(f"{superadmin.username} patches admin with ID: {admin_id}")
    try:
        patched_admin = await admin_crud.patch_admin(admin_id=admin_id, params=admin_params_to_patch)
        logger.info(f"Admin with ID {admin_id} patched successfully")
        return patched_admin
    except NotFoundError:
        logger.warning(f"Admin with ID {admin_id} not found")
        raise HTTPException(status_code=404, detail="Admin not found")
    except Exception as e:
        logger.error("Unexpected error while patching admin", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.delete("/delete_admin/{admin_id}")
async def delete_admin(admin_id: int, superadmin=Depends(superadmin_required)):
    logger.info(f"{superadmin.username} deletes admin with ID: {admin_id}")
    try:
        await admin_crud.delete_admin(admin_id=admin_id)
        logger.info(f"Admin with ID {admin_id} deleted successfully")
        return {"message": "Admin deleted"}
    except NotFoundError:
        logger.warning(f"Admin with ID {admin_id} not found")
        raise HTTPException(status_code=404, detail="Admin not found")
    except Exception as e:
        logger.error("Unexpected error while patching admin", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post("/token/refresh")
async def refresh_token(refresh_token_in: str):
    logger.info(f"Request received to refresh token: {refresh_token_in}")
    try:
        result = await admin_crud.refresh_access_token(refresh_token_in)
        return {"access_token": result}
    except NotFoundError:
        logger.warning(f"Token {refresh_token_in} not found")
        raise HTTPException(status_code=404, detail="Token not found")
    except RefreshTokenExpired:
        raise HTTPException(status_code=401, detail="Expired refresh token")