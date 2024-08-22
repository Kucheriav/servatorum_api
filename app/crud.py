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



def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user