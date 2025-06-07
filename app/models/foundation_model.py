from app.models.legal_entity_base import LegalEntityBase
from sqlalchemy.orm import relationship
from app.models.sphere_model import foundation_spheres


class Foundation(LegalEntityBase):
    __tablename__ = "foundations"
    spheres = relationship("Sphere", secondary=foundation_spheres, backref="foundations")

    # Можно добавить специфические поля для фондов тут