from fastapi import APIRouter, HTTPException
from app.schemas.registration_schema import RegistrationStepSchema
from app.crud.user_crud import UserCRUD
from app.crud.foundation_crud import FoundationCRUD
from app.crud.company_crud import CompanyCRUD
from app.crud.auth_crud import AuthCRUD
import logging

router = APIRouter()
user_crud = UserCRUD()
fund_crud = FoundationCRUD()
company_crud = CompanyCRUD()
auth_crud = AuthCRUD()
logger = logging.getLogger("app.registration_router")


@router.post("/registration_step")
async def registration_step(data: RegistrationStepSchema):
    # data: {phone, user_type, step, ...fields}
    if data.user_type == "user":
        if data.step == 1:
            # имя и фото, можно сохранить частично
            user = await user_crud.create_user_step1(data.phone, data.name, data.profile_picture)
        elif data.step == 2:
            # остальное (city, email, ...), патчим юзера
            user = await user_crud.update_user_step2(data.phone, data.other_fields)
    elif data.user_type in ("fund", "company"):
        # создаём юзера, потом сразу фонд/компанию
        user = await user_crud.create_user_minimal(data.phone)
        if data.user_type == "fund":
            await fund_crud.create_fund(user.id, data.fund_fields)
        else:
            await company_crud.create_company(user.id, data.company_fields)
    else:
        raise HTTPException(status_code=400, detail="Unknown user_type")
    # После финального шага выдаём токен
    token = auth_crud.generate_token(user)
    return {"token": token}