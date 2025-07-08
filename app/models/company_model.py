from app.models.legal_entity_base import LegalEntityBase
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey
from app.models.sphere_model import company_spheres
from app.database import Base

class Company(LegalEntityBase):
    __tablename__ = "companies"
    spheres = relationship("Sphere", secondary=company_spheres, back_populates="companies")

class CompanyAccountDetails(Base):
    __tablename__ = "company_account_details"
    id = Column(Integer, primary_key=True, index=True)
    company = Column(Integer, ForeignKey('companies.id'), unique=True)
    inn = Column(String, unique=True)
    kpp = Column(String)
    account_name = Column(String)
    bank_account = Column(String)
    cor_account = Column(String)
    bik = Column(String)