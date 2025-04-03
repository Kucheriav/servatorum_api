from fastapi import APIRouter, HTTPException
from pydantic import ValidationError
from sqlalchemy import exc
from app.crud.legal_entity_crud import LegalEntityCRUD
from app.schemas.legal_entity_schema import *

router = APIRouter()
legal_entity_crud = LegalEntityCRUD()
# TODO optimize exceptions chain


@router.post("/create_legal_entity", response_model=LegalEntityResponse)
async def create_legal_entity(legal_entity: LegalEntityCreate):
    try:
        return await legal_entity_crud.create_legal_entity(legal_entity)
    # если не проходим по схеме Pydantic
    except ValidationError as e:
        errors = e.errors()
        error_messages = []
        for error in errors:
            field = error['loc'][-1]
            message = error['msg']
            error_messages.append(f"Ошибка в поле '{field}': {message}")
        raise HTTPException(status_code=422, detail=error_messages)
    # TODO think about unique constrictions
    except exc.IntegrityError:
        raise HTTPException(status_code=400, detail="Email already exists")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/get_legal_entity/{legal_entity_id}", response_model=LegalEntityResponse)
async def get_legal_entity(legal_entity_id: int):
    legal_entity = await legal_entity_crud.get_legal_entity(legal_entity_id)
    if legal_entity:
        return legal_entity
    raise HTTPException(status_code=404, detail="Legal entity not found")


@router.patch("/patch_legal_entity/{legal_entity_id}", response_model=LegalEntityResponse)
async def patch_legal_entity(legal_entity_id: int, legal_entity_params_to_patch: LegalEntityPatch):
    patched_legal_entity = await legal_entity_crud.patch_legal_entity(legal_entity_id, legal_entity_params_to_patch)
    if patched_legal_entity:
        return patched_legal_entity
    raise HTTPException(status_code=404, detail="Legal entity not found")


@router.delete("/delete_legal_entity/{legal_entity_id}")
async def delete_legal_entity(legal_entity_id: int):
    if await legal_entity_crud.delete_legal_entity(legal_entity_id):
        return {"message": "Legal entity deleted"}
    raise HTTPException(status_code=404, detail="Legal entity not found")
