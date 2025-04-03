from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy import func, CheckConstraint
from app.database import Base

#TODO manage with logo
#TODO think about unique constrictions

class LegalEntity(Base):
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
    entity_type = Column(Enum('company', 'foundation', name='entity_type'))

    __table_args__ = (
        CheckConstraint("inn ~ '^[0-9]{9}$'", name='check_inn'),
        CheckConstraint('length(cor_account) = 20', name='check_cor_account'),
        CheckConstraint("phone ~ '^7[0-9]{9}$'", name='check_phone'),
        CheckConstraint("phone_helpdesk ~ '^7[0-9]{9}$'", name='check_phone_helpdesk')
    )