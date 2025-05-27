from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import IntegrityError
from app.crud.company_crud import CompanyCRUD
from app.schemas.company_schema import *
from app.errors_custom_types import *
import logging

router = APIRouter()
company_crud = CompanyCRUD()


logger = logging.getLogger("app.company_router")


@router.post("/create_company", response_model=CompanyResponse)
async def create_company(company: CompanyCreate):
    logger.info("Request received to create a company")
    try:
        result = await company_crud.create_company(company=company)
        return result
    except ConstrictionViolatedError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/get_company/{company_id}", response_model=CompanyResponse)
async def get_company(company_id: int):
    logger.info(f"Request received to get company with ID: {company_id}")
    try:
        company = await company_crud.get_company(company_id=company_id)
        return company
    except CompanyNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/patch_company/{company_id}", response_model=CompanyResponse)
async def patch_company(company_id: int, company_params_to_patch: CompanyPatch):
    logger.info(f"Request received to patch company with ID: {company_id}")
    try:
        patched_company = await company_crud.patch_company(company_id=company_id,
                                                                      params=company_params_to_patch)
        return patched_company
    except CompanyNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/delete_company/{company_id}")
async def delete_company(company_id: int):
    logger.info(f"Request received to delete company with ID: {company_id}")
    try:
        await company_crud.delete_company(company_id=company_id)
        return {"message": "Company deleted"}
    except CompanyNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))