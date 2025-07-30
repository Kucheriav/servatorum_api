from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.exc import IntegrityError
from app.crud.foundation_crud import FoundationCRUD
from app.schemas.foundation_schema import *
from app.errors_custom_types import *
from app.scripts_utils.dependencies import get_current_user, foundation_owner_or_admin
import logging

router = APIRouter()
foundation_crud = FoundationCRUD()


logger = logging.getLogger("app.foundation_router")


@router.post("/create_foundation", response_model=FoundationResponse)
async def create_foundation(foundation: FoundationCreate, current_user=Depends(get_current_user)):
    logger.info(f"{current_user} creates a foundation")
    try:
        result = await foundation_crud.create_foundation(foundation=foundation)
        return result
    except ConstrictionViolatedError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail='Internal Server Error')


@router.get("/get_foundation/{foundation_id}", response_model=FoundationResponse)
async def get_foundation(foundation_id: int):
    logger.info(f"Request received to get foundation with ID: {foundation_id}")
    try:
        foundation = await foundation_crud.get_foundation(foundation_id=foundation_id)
        return foundation
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail='Internal Server Error')


@router.patch("/patch_foundation/{foundation_id}", response_model=FoundationResponse)
async def patch_foundation(foundation_id: int, foundation_to_patch: FoundationPatch, current_actor=Depends(foundation_owner_or_admin)):
    logger.info(f"{current_actor.phone} patches foundation with ID: {foundation_id}")
    try:
        patched_foundation = await foundation_crud.patch_foundation(foundation_id=foundation_id,
                                                                    params=foundation_to_patch)
        return patched_foundation
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail='Internal Server Error')

@router.post("/foundation/{foundation_id}/add_account", response_model=FoundationAccountDetailsAddResponse)
async def add_account_details(foundation_id: int, details: FoundationAccountDetailsAdd, current_actor=Depends(foundation_owner_or_admin)):
    logger.info(f"{current_actor.phone} adds a new account to a foundation with ID: {foundation_id}")
    try:
        return await foundation_crud.add_account_details(foundation_id, details)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/delete_foundation/{foundation_id}")
async def delete_foundation(foundation_id: int, current_actor=Depends(foundation_owner_or_admin)):
    logger.info(f"{current_actor.phone} deletes foundation with ID: {foundation_id}")
    try:
        await foundation_crud.delete_foundation(foundation_id=foundation_id)
        return {"message": "Foundation deleted"}
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail='Internal Server Error')