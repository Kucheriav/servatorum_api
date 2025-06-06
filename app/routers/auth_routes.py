from fastapi import APIRouter, HTTPException
from app.schemas.auth_schema import RequestCodeSchema, VerifyCodeSchema, AuthTokenResponse
from app.crud.auth_crud import AuthCRUD
import logging

router = APIRouter()
auth_crud = AuthCRUD()
logger = logging.getLogger("app.auth_router")

def send_sms_mock(phone: str, code: str):
    logger.info(f"MOCK SMS: sent code {code} to {phone}")

@router.post("/request_code")
async def request_code(data: RequestCodeSchema):
    try:
        code = await auth_crud.create_verification_code(phone=data.phone)
        send_sms_mock(data.phone, code)
        return {"success": True}
    except Exception as e:
        logger.error("Ошибка при создании кода", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post("/verify_code", response_model=AuthTokenResponse)
async def verify_code(data: VerifyCodeSchema):
    try:
        status = await auth_crud.verify_code(phone=data.phone, code=data.code)
        if status == "ok":
            user = await auth_crud.get_or_create_user(phone=data.phone)
            token = auth_crud.generate_token(user)
            return {"access_token": token, "token_type": "bearer"}
        elif status == "expired":
            raise HTTPException(status_code=400, detail="Код истек")
        elif status == "locked":
            raise HTTPException(status_code=400, detail="Превышено количество попыток. Запросите новый код.")
        else:
            raise HTTPException(status_code=400, detail="Неверный код")
    except Exception as e:
        logger.error("Ошибка при верификации кода", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")