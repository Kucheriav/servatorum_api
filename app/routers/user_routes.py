from fastapi import APIRouter, HTTPException
from pydantic import ValidationError
from sqlalchemy import exc
from app.crud.user_crud import UserCRUD
from app.schemas.user_schema import *
import logging

router = APIRouter()
user_crud = UserCRUD()

# Create a logger specific to this module
logger = logging.getLogger("app.user_router")

# TODO optimize exceptions chain

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
            error_messages.append(f"Ошибка в поле '{field}': {message}")
        raise HTTPException(status_code=422, detail=error_messages)
    except exc.IntegrityError:
        logger.error("Integrity error: possibly duplicate email")
        raise HTTPException(status_code=400, detail="Email already exists")
    except Exception as e:
        logger.error("Unexpected error while creating user", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")


# TODO refactor all GET DELETE routes without using query-strings into Pydantic models (yes, with 1 parameter)
@router.get("/get_user/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    logger.info(f"Request received to get user with ID: {user_id}")
    user = await user_crud.get_user(user_id=user_id)
    if user:
        logger.info(f"User with ID {user_id} retrieved successfully")
        return user
    logger.warning(f"User with ID {user_id} not found")
    raise HTTPException(status_code=404, detail="User not found")


@router.patch("/patch_user/{user_id}", response_model=UserResponse)
async def patch_user(user_id: int, user_params_to_patch: UserPatch):
    logger.info(f"Request received to patch user with ID: {user_id}")
    patched_user = await user_crud.patch_user(user_id=user_id, params=user_params_to_patch)
    if patched_user:
        logger.info(f"User with ID {user_id} patched successfully")
        return patched_user
    logger.warning(f"User with ID {user_id} not found for patching")
    raise HTTPException(status_code=404, detail="User not found")


@router.delete("/delete_user/{user_id}")
async def delete_user(user_id: int):
    logger.info(f"Request received to delete user with ID: {user_id}")
    if await user_crud.delete_user(user_id=user_id):
        logger.info(f"User with ID {user_id} deleted successfully")
        return {"message": "User deleted"}
    logger.warning(f"User with ID {user_id} not found for deletion")
    raise HTTPException(status_code=404, detail="User not found")

