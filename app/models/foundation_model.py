from app.models.legal_entity_base import LegalEntityBase
from sqlalchemy.orm import relationship
from app.models.sphere_model import foundation_spheres
from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base


class Foundation(LegalEntityBase):
    __tablename__ = "foundations"
    spheres = relationship("Sphere", secondary=foundation_spheres, back_populates="foundations")


class FoundationAccountDetails(Base):
    __tablename__ = "foundation_account_details"
    id = Column(Integer, primary_key=True, index=True)
    foundation = Column(Integer, ForeignKey('foundations.id'), unique=False)
    inn = Column(String, unique=True)
    kpp = Column(String)
    account_name = Column(String)
    bank_account = Column(String)
    cor_account = Column(String)
    bik = Column(String)