from fastapi import APIRouter, HTTPException
from pydantic import ValidationError
from sqlalchemy import exc
from app.crud.fundraising_crud import FundraisingCRUD
from app.schemas.fundraising_schema import *
import logging

router = APIRouter()
fundraising_crud = FundraisingCRUD()

# Create a logger specific to this module
logger = logging.getLogger("app.router")

# TODO optimize exceptions chain

@router.post("/create_fundraising", response_model=FundraisingResponce)
async def create_fundraising(fundraising: FundraisingCreate):
    logger.info("Request received to create fundraising")
    try:
        result = await fundraising_crud.create_fundraising(fundraising)
        logger.info("Fundraising created successfully")
        return result
    except ValidationError as e:
        logger.error("Validation error while creating fundraising", exc_info=True)
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
        logger.error("Unexpected error while creating fundraising", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/get_fundraising/{fundraising_id}", response_model=FundraisingResponce)
async def get_fundraising(fundraising_id: int):
    logger.info(f"Request received to get fundraising with ID: {fundraising_id}")
    fundraising = await fundraising_crud.get_fundraising(fundraising_id)
    if fundraising:
        logger.info(f"Fundraising with ID {fundraising_id} retrieved successfully")
        return fundraising
    logger.warning(f"Fundraising with ID {fundraising_id} not found")
    raise HTTPException(status_code=404, detail="Fundraising not found")


@router.get("/get_fundraisings_pages", response_model=FundraisingPaginationResponse)
async def get_fundraisings(page: int = 1, page_size: int = 10):
    logger.info(f"Request received to get fundraisings paginated: Page {page}, Page Size {page_size}")
    result = await fundraising_crud.get_fundraisings_paginated(page=page, page_size=page_size)
    if result:
        logger.info(f"Fundraisings page {page} retrieved successfully")
        return result
    logger.warning("No fundraisings found for the requested page")
    raise HTTPException(status_code=404, detail="Fundraising not found")


@router.patch("/patch_fundraising/{fundraising_id}", response_model=FundraisingResponce)
async def patch_fundraising(fundraising_id: int, fundraising_params_to_patch: FundraisingPatch):
    logger.info(f"Request received to patch fundraising with ID: {fundraising_id}")
    patched_fundraising = await fundraising_crud.patch_fundraising(fundraising_id, fundraising_params_to_patch)
    if patched_fundraising:
        logger.info(f"Fundraising with ID {fundraising_id} patched successfully")
        return patched_fundraising
    logger.warning(f"Fundraising with ID {fundraising_id} not found for patching")
    raise HTTPException(status_code=404, detail="Fundraising not found")


@router.delete("/delete_fundraising/{fundraising_id}")
async def delete_fundraising(fundraising_id: int):
    logger.info(f"Request received to delete fundraising with ID: {fundraising_id}")
    if await fundraising_crud.delete_fundraising(fundraising_id):
        logger.info(f"Fundraising with ID {fundraising_id} deleted successfully")
        return {"message": "Fundraising deleted"}
    logger.warning(f"Fundraising with ID {fundraising_id} not found for deletion")
    raise HTTPException(status_code=404, detail="Fundraising not found")