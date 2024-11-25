from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from app.database import Base



class LegalEntity(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    daescription = Column(String)
    logo = Column(String)
    photo = Column(String)
    inn = Column(String)
    bik = Column(String)
    cor_account = Column(String)
    address = Column(String)
    address_reg = Column(String)
    phone = Column(String)
    phone_helpdesk = Column(String)
    entity_type = Column(Enum('company', 'foundation', name='entity_type'))


