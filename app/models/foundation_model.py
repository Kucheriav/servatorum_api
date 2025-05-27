from app.models.legal_entity_base import LegalEntityBase

class Foundation(LegalEntityBase):
    __tablename__ = "foundations"
    # Можно добавить специфические поля для фондов тут