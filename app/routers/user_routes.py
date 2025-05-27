from fastapi import APIRouter, HTTPException
from app.errors_custom_types import *
from pydantic import ValidationError
from sqlalchemy import exc
from app.crud.user_crud import UserCRUD
from app.schemas.user_schema import *
import logging

router = APIRouter()
user_crud = UserCRUD()

logger = logging.getLogger("app.user_router")

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
    except UserNotFoundError:
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
    except UserNotFoundError:
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
    except UserNotFoundError:
        logger.warning(f"User with ID {user_id} not found")
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        logger.error("Unexpected error while patching user", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")

