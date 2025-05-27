from sqlalchemy import Column, Integer, String
from sqlalchemy import CheckConstraint
from app.database import Base

#TODO manage with logo
#TODO think about unique constrictions

class LegalEntityBase(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    logo = Column(String)
    inn = Column(String, unique=True)
    bik = Column(String)
    cor_account = Column(String)
    address = Column(String)
    address_reg = Column(String)
    phone = Column(String)
    phone_helpdesk = Column(String)

    __table_args__ = (
        CheckConstraint("inn ~ '^[0-9]{10}$'", name='check_inn'),
        CheckConstraint('length(cor_account) = 20', name='check_cor_account'),
        CheckConstraint("phone ~ '^7[0-9]{10}$'", name='check_phone'),
        CheckConstraint("phone_helpdesk ~ '^7[0-9]{10}$'", name='check_phone_helpdesk')
    )
