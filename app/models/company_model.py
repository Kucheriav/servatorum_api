from app.models.legal_entity_base import LegalEntityBase
from sqlalchemy.orm import relationship
from app.models.sphere_model import company_spheres

class Company(LegalEntityBase):
    __tablename__ = "companies"
    spheres = relationship("Sphere", secondary=company_spheres, back_populates="companies")
