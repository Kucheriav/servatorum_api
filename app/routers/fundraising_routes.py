from fastapi import APIRouter, HTTPException
from pydantic import ValidationError
from sqlalchemy import exc
from app.crud.fundraising_crud import FundraisingCRUD
from app.schemas.fundraising_schema import *

router = APIRouter()
fundraising_crud = FundraisingCRUD()
# TODO optimize exceptions chain


@router.post("/create_fundraising", response_model=FundraisingCreate)
async def create_fundraising(fundraising: FundraisingCreate):
    try:
        return fundraising_crud.create_fundraising(fundraising)
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


@router.get("/get_fundraising/{fundraising_id}")
async def get_fundraising(fundraising_id: int):
    fundraising = fundraising_crud.get_fundraising(fundraising_id)
    if fundraising:
        return fundraising
    raise HTTPException(status_code=404, detail="Fundraising not found")


@router.patch("/patch_fundraising/{fundraising_id}", response_model=FundraisingPatch)
async def patch_fundraising(fundraising_id: int, fundraising_params_to_patch: FundraisingPatch):
    patched_fundraising = fundraising_crud.patch_fundraising(fundraising_id, fundraising_params_to_patch)
    if patched_fundraising:
        return patched_fundraising
    raise HTTPException(status_code=404, detail="Fundraising not found")


@router.delete("/delete_fundraising/{fundraising_id}")
async def delete_fundraising(fundraising_id: int):
    if fundraising_crud.delete_fundraising(fundraising_id):
        return {"message": "Fundraising deleted"}
    raise HTTPException(status_code=404, detail="Fundraising not found")
