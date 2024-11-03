from sqlalchemy.orm import Session
from . import models, schemas


def authorize_user(db: Session, phone_number, pin_code):
    user = db.query(models.User).filter_by(phone_number=phone_number).first()
    if user and user.verify_pin_code(pin_code):
        print("Авторизация успешна")
        return True
    else:
        print("Неправильный пин-код")
        return False


def get_user_by_phone(db: Session, phone: str):
    return db.query(models.User).filter(models.User.phone == phone).first()


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserBase):
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user: schemas.UserBase):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        for key, value in user.model_dump().items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()


def update_profile_picture(db: Session, user_id: int, profile_picture: str):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db_user.profile_picture = profile_picture
        db.commit()
        db.refresh(db_user)
    return db_user
###################


def get_funds(db: Session):
    return db.query(models.Fund).all()


def get_fund(db: Session, fund_id: int):
    return db.query(models.Fund).filter(models.Fund.id == fund_id).first()


def create_fund(db: Session, fund: schemas.FundBase):
    db_fund = models.Fund(**fund.dict())
    db.add(db_fund)
    db.commit()
    db.refresh(db_fund)
    return db_fund


def update_fund(db: Session, db_fund: models.Fund, fund: schemas.FundBase):
    db_fund.name = fund.name
    db_fund.description = fund.description
    db.commit()
    db.refresh(db_fund)
    return db_fund


def delete_fund(db: Session, db_fund: models.Fund):
    db.delete(db_fund)
    db.commit()


def get_charity_spheres(db: Session):
    return db.query(models.CharitySphere).all()


def get_charity_sphere(db: Session, charity_sphere_id: int):
    return db.query(models.CharitySphere).filter(models.CharitySphere.id == charity_sphere_id).first()


def create_charity_sphere(db: Session, charity_sphere: schemas.CharitySphereBase):
    db_charity_sphere = models.CharitySphere(**charity_sphere.dict())
    db.add(db_charity_sphere)
    db.commit()
    db.refresh(db_charity_sphere)
    return db_charity_sphere


def get_accounts(db: Session):
    return db.query(models.Account).all()


def get_account(db: Session, account_id: int):
    return db.query(models.Account).filter(models.Account.id == account_id).first()


def create_account(db: Session, account: schemas.AccountBase):
    db_account = models.Account(**account.dict())
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account