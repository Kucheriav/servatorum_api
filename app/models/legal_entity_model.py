from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy import func, check
from app.database import Base

#TODO manage with logo
#TODO think about unique constrictions

class LegalEntity(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    logo = Column(String)
    inn = Column(String, check='inn REGEXP ^[0-9]{9}$')
    bik = Column(String, check='bik REGEXP ^[0-9]{9}$')
    cor_account = Column(String, check='length(cor_account) = 20')
    address = Column(String)
    address_reg = Column(String)
    phone = Column(String, check='phone REGEXP ^7[0-9]{9}$')
    phone_helpdesk = Column(String, check='phone_helpdesk REGEXP ^7[0-9]{9}$')
    entity_type = Column(Enum('company', 'foundation', name='entity_type'))

