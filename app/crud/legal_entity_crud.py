from app.database import connection
from app.models.legal_entity_model import LegalEntity
from app.schemas.legal_entity_schema import *
from app.errors_custom_types import *


class LegalEntityCRUD:
    @connection
    async def create_legal_entity(self, legal_entity: LegalEntityCreate, session):
        new_legal_entity = LegalEntity(name=legal_entity.name,
                                       description=legal_entity.description,
                                       logo=legal_entity.logo,
                                       inn=legal_entity.inn,
                                       bik=legal_entity.bik,
                                       cor_account=legal_entity.cor_account,
                                       address=legal_entity.address,
                                       address_reg=legal_entity.address_reg,
                                       phone=legal_entity.phone,
                                       phone_helpdesk=legal_entity.phone_helpdesk,
                                       entity_type=legal_entity.entity_type,
                                       )
        session.add(new_legal_entity)
        session.commit()
        return new_legal_entity

    @connection
    async def get_legal_entity(self, legal_entity_id: int, session):
        legal_entity = session.select(LegalEntity).filter(LegalEntity.id == legal_entity_id).first()
        if legal_entity:
            return legal_entity
        else:
            raise LegalEntityNotFoundError(f"LEGAL_ENTITY_NOT_FOUND: {legal_entity_id}")

    @connection
    async def patch_legal_entity(self, legal_entity_id: int, session, **params):
        legal_entity_to_patch = session.select(LegalEntity).filter(LegalEntity.id == legal_entity_id).first()
        if legal_entity_to_patch:
            for key, value in params.items():
                if hasattr(legal_entity_to_patch, key):
                    setattr(legal_entity_to_patch, key, value)
                else:
                    raise LegalEntityUpdateError(f"FIELD_NOT_FOUND: {key}")
            session.commit()
            return legal_entity_to_patch
        else:
            raise LegalEntityNotFoundError(f"LEGAL_ENTITY_NOT_FOUND: {legal_entity_id}")

    @connection
    def delete_legal_entity(self, legal_entity_id: int, session):
        legal_entity_to_delete = session.select(LegalEntity).filter(LegalEntity.id == legal_entity_id).first()
        if legal_entity_to_delete:
            session.delete(legal_entity_to_delete)
            session.commit()
            return True
        else:
            raise LegalEntityNotFoundError(f"LEGAL_ENTITY_NOT_FOUND: {legal_entity_id}")