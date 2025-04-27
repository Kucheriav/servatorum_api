from fastapi import APIRouter, HTTPException
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from app.crud.legal_entity_crud import LegalEntityCRUD
from app.schemas.legal_entity_schema import *
import logging

router = APIRouter()
legal_entity_crud = LegalEntityCRUD()

# Create a logger specific to this module
logger = logging.getLogger("app.legal_entity_router")

# TODO optimize exceptions chain

@router.post("/create_legal_entity", response_model=LegalEntityResponse)
async def create_legal_entity(legal_entity: LegalEntityCreate):
    logger.info("Request received to create a legal entity")
    try:
        result = await legal_entity_crud.create_legal_entity(legal_entity=legal_entity)
        logger.info("Legal entity created successfully")
        return result
    except ValidationError as e:
        logger.error("Validation error while creating legal entity", exc_info=True)
        errors = e.errors()
        error_messages = []
        for error in errors:
            field = error['loc'][-1]
            message = error['msg']
            error_messages.append(f"Ошибка в поле '{field}': {message}")
        raise HTTPException(status_code=422, detail=error_messages)
    except IntegrityError as e:
        constraint_error_messages = {
            "check_inn": "The INN field violates format constraints.",
            "check_cor_account": "The Correspondent Account must be exactly 20 digits.",
            "check_phone": "The Phone number must follow the format '7XXXXXXXXXX'.",
            "check_phone_helpdesk": "The Helpdesk Phone number must follow the format '7XXXXXXXXXX'.",
        }
        constraint_name = e.args[0]
        error_message = constraint_error_messages.get(constraint_name, "A database constraint was violated.")
        raise HTTPException(status_code=400, detail=error_message)
    except Exception as e:
        logger.error("Unexpected error while creating legal entity", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/get_legal_entity/{legal_entity_id}", response_model=LegalEntityResponse)
async def get_legal_entity(legal_entity_id: int):
    logger.info(f"Request received to get legal entity with ID: {legal_entity_id}")
    legal_entity = await legal_entity_crud.get_legal_entity(legal_entity_id=legal_entity_id)
    if legal_entity:
        logger.info(f"Legal entity with ID {legal_entity_id} retrieved successfully")
        return legal_entity
    logger.warning(f"Legal entity with ID {legal_entity_id} not found")
    raise HTTPException(status_code=404, detail="Legal entity not found")


@router.patch("/patch_legal_entity/{legal_entity_id}", response_model=LegalEntityResponse)
async def patch_legal_entity(legal_entity_id: int, legal_entity_params_to_patch: LegalEntityPatch):
    logger.info(f"Request received to patch legal entity with ID: {legal_entity_id}")
    patched_legal_entity = await legal_entity_crud.patch_legal_entity(legal_entity_id=legal_entity_id,
                                                                      params=legal_entity_params_to_patch)
    if patched_legal_entity:
        logger.info(f"Legal entity with ID {legal_entity_id} patched successfully")
        return patched_legal_entity
    logger.warning(f"Legal entity with ID {legal_entity_id} not found for patching")
    raise HTTPException(status_code=404, detail="Legal entity not found")


@router.delete("/delete_legal_entity/{legal_entity_id}")
async def delete_legal_entity(legal_entity_id: int):
    logger.info(f"Request received to delete legal entity with ID: {legal_entity_id}")
    if await legal_entity_crud.delete_legal_entity(legal_entity_id=legal_entity_id):
        logger.info(f"Legal entity with ID {legal_entity_id} deleted successfully")
        return {"message": "Legal entity deleted"}
    logger.warning(f"Legal entity with ID {legal_entity_id} not found for deletion")
    raise HTTPException(status_code=404, detail="Legal entity not found")