from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import crud, models, schemas
from ..database import get_db

router = APIRouter()


@router.get("/funds/", response_model=List[schemas.Fund])
def read_funds(db: Session = Depends(get_db)):
    return crud.get_funds(db)


@router.get("/funds/{fund_id}", response_model=schemas.Fund)
def read_fund(fund_id: int, db: Session = Depends(get_db)):
    db_fund = crud.get_fund(db, fund_id=fund_id)
    if db_fund is None:
        raise HTTPException(status_code=404, detail="Фонд не найден")
    return db_fund


@router.post("/funds/", response_model=schemas.Fund)
def create_fund(fund: schemas.FundBase, db: Session = Depends(get_db)):
    return crud.create_fund(db, fund=fund)


@router.put("/funds/{fund_id}", response_model=schemas.Fund)
def update_fund(fund_id: int, fund: schemas.FundBase, db: Session = Depends(get_db)):
    db_fund = crud.get_fund(db, fund_id=fund_id)
    if db_fund is None:
        raise HTTPException(status_code=404, detail="Фонд не найден")
    return crud.update_fund(db, db_fund, fund)


@router.delete("/funds/{fund_id}")
def delete_fund(fund_id: int, db: Session = Depends(get_db)):
    db_fund = crud.get_fund(db, fund_id=fund_id)
    if db_fund is None:
        raise HTTPException(status_code=404, detail="Фонд не найден")
    crud.delete_fund(db, db_fund)
    return {"message": "Фонд удален"}


@router.get("/charity_spheres/", response_model=List[schemas.CharitySphere])
def read_charity_spheres(db: Session = Depends(get_db)):
    return crud.get_charity_spheres(db)


@router.get("/charity_spheres/{charity_sphere_id}", response_model=schemas.CharitySphere)
def read_charity_sphere(charity_sphere_id: int, db: Session = Depends(get_db)):
    db_charity_sphere = crud.get_charity_sphere(db, charity_sphere_id=charity_sphere_id)
    if db_charity_sphere is None:
        raise HTTPException(status_code=404, detail="Сфера благотворительности не найдена")
    return db_charity_sphere


@router.post("/charity_spheres/", response_model=schemas.CharitySphere)
def create_charity_sphere(charity_sphere: schemas.CharitySphereBase, db: Session = Depends(get_db)):
    return crud.create_charity_sphere(db, charity_sphere=charity_sphere)


@router.get("/accounts/", response_model=List[schemas.Account])
def read_accounts(db: Session = Depends(get_db)):
    return crud.get_accounts(db)


@router.get("/accounts/{account_id}", response_model=schemas.Account)
def read_account(account_id: int, db: Session = Depends(get_db)):
    db_account = crud.get_account(db, account_id=account_id)
    if db_account is None:
        raise HTTPException(status_code=404, detail="Счет не найден")
    return db_account


@router.post("/accounts/", response_model=schemas.Account)
def create_account(account: schemas.AccountBase, db: Session = Depends(get_db)):
    return crud.create_account(db, account=account)
