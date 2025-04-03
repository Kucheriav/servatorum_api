from fastapi import APIRouter, HTTPException
from pydantic import ValidationError
from sqlalchemy import exc
from app.crud.user_crud import UserCRUD
from app.schemas.user_schema import *

router = APIRouter()
user_crud = UserCRUD()
# TODO optimize exceptions chain


@router.post("/create_user", response_model=UserResponse)
async def create_user(user: UserCreate):
    try:
        return await user_crud.create_user(user)
    # если не проходим по схеме Pydantic
    except ValidationError as e:
        errors = e.errors()
        error_messages = []
        for error in errors:
            field = error['loc'][-1]
            message = error['msg']
            error_messages.append(f"Ошибка в поле '{field}': {message}")
        raise HTTPException(status_code=422, detail=error_messages)
    except exc.IntegrityError:
        raise HTTPException(status_code=400, detail="Email already exists")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

#TODO refactor all GET DELETE routes witout using query-strings into Pydantic models (yes, with 1 parameter)
@router.get("/get_user/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    user = await user_crud.get_user(user_id)
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found")


@router.patch("/patch_user/{user_id}", response_model=UserResponse)
async def patch_user(user_id: int, user_params_to_patch: UserPatch):
    patched_user = await user_crud.patch_user(user_id, user_params_to_patch)
    if patched_user:
        return patched_user
    raise HTTPException(status_code=404, detail="User not found")


@router.delete("/delete_user/{user_id}")
async def delete_user(user_id: int):
    if await user_crud.delete_user(user_id):
        return {"message": "User deleted"}
    raise HTTPException(status_code=404, detail="User not found")
