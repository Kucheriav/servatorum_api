from fastapi import APIRouter, HTTPException
from pydantic import ValidationError
from sqlalchemy import exc
from app.crud.user_crud import UserCRUD
from app.schemas.user import UserCreate

router = APIRouter()
user_crud = UserCRUD()

@router.post("/create_user")
async def create_user(user: UserCreate):
    try:
        return user_crud.create_user(user)
    except exc.IntegrityError:
        raise HTTPException(status_code=400, detail="Email already exists")
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/get_user/{user_id}")
async def get_user(user_id: int):
    user = user_crud.get_user(user_id)
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found")

@router.put("/update_user/{user_id}")
async def update_user(user_id: int, user: UserCreate):
    updated_user = user_crud.update_user(user_id, user)
    if updated_user:
        return updated_user
    raise HTTPException(status_code=404, detail="User not found")

@router.delete("/delete_user/{user_id}")
async def delete_user(user_id: int):
    if user_crud.delete_user(user_id):
        return {"message": "User deleted"}
    raise HTTPException(status_code=404, detail="User not found")
