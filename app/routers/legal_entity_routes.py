from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import IntegrityError
from app.crud.legal_entity_crud import LegalEntityCRUD
from app.schemas.legal_entity_schema import *
from app.errors_custom_types import *
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
        return result
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/get_legal_entity/{legal_entity_id}", response_model=LegalEntityResponse)
async def get_legal_entity(legal_entity_id: int):
    logger.info(f"Request received to get legal entity with ID: {legal_entity_id}")
    try:
        legal_entity = await legal_entity_crud.get_legal_entity(legal_entity_id=legal_entity_id)
        return legal_entity
    except LegalEntityNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/patch_legal_entity/{legal_entity_id}", response_model=LegalEntityResponse)
async def patch_legal_entity(legal_entity_id: int, legal_entity_params_to_patch: LegalEntityPatch):
    logger.info(f"Request received to patch legal entity with ID: {legal_entity_id}")
    try:
        patched_legal_entity = await legal_entity_crud.patch_legal_entity(legal_entity_id=legal_entity_id,
                                                                      params=legal_entity_params_to_patch)
        return patched_legal_entity
    except LegalEntityNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/delete_legal_entity/{legal_entity_id}")
async def delete_legal_entity(legal_entity_id: int):
    logger.info(f"Request received to delete legal entity with ID: {legal_entity_id}")
    try:
        await legal_entity_crud.delete_legal_entity(legal_entity_id=legal_entity_id)
        return {"message": "Legal entity deleted"}
    except LegalEntityNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))