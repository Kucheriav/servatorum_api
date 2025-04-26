from app.database import connection
from app.models.legal_entity_model import LegalEntity
from app.schemas.legal_entity_schema import *
from app.errors_custom_types import *
import logging

# Create a logger specific to this module
logger = logging.getLogger("app.legal_entity_crud")


class LegalEntityCRUD:
    @connection
    async def create_legal_entity(self, legal_entity: LegalEntityCreate, session):
        logger.info("Creating a new legal entity")
        try:
            new_legal_entity = LegalEntity(
                name=legal_entity.name,
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
            await session.commit()
            logger.info(f"Legal entity created successfully with ID: {new_legal_entity.id}")
            return new_legal_entity
        except Exception as e:
            logger.error("Error occurred while creating legal entity", exc_info=True)
            raise

    @connection
    async def get_legal_entity(self, legal_entity_id: int, session):
        logger.info(f"Fetching legal entity with ID: {legal_entity_id}")
        legal_entity = session.select(LegalEntity).filter(LegalEntity.id == legal_entity_id).first()
        if legal_entity:
            logger.info(f"Legal entity with ID {legal_entity_id} retrieved successfully")
            return legal_entity
        else:
            logger.warning(f"Legal entity with ID {legal_entity_id} not found")
            raise LegalEntityNotFoundError(f"LEGAL_ENTITY_NOT_FOUND: {legal_entity_id}")

    @connection
    async def patch_legal_entity(self, legal_entity_id: int, session, **params):
        logger.info(f"Patching legal entity with ID: {legal_entity_id}")
        legal_entity_to_patch = session.select(LegalEntity).filter(LegalEntity.id == legal_entity_id).first()
        if legal_entity_to_patch:
            try:
                for key, value in params.items():
                    if hasattr(legal_entity_to_patch, key):
                        setattr(legal_entity_to_patch, key, value)
                        logger.debug(f"Updated field {key} to {value} for legal entity ID {legal_entity_id}")
                    else:
                        logger.warning(f"Field {key} not found in LegalEntity model")
                        raise LegalEntityUpdateError(f"FIELD_NOT_FOUND: {key}")
                await session.commit()
                logger.info(f"Legal entity with ID {legal_entity_id} patched successfully")
                return legal_entity_to_patch
            except Exception as e:
                logger.error("Error occurred while patching legal entity", exc_info=True)
                raise
        else:
            logger.warning(f"Legal entity with ID {legal_entity_id} not found")
            raise LegalEntityNotFoundError(f"LEGAL_ENTITY_NOT_FOUND: {legal_entity_id}")

    @connection
    async def delete_legal_entity(self, legal_entity_id: int, session):
        logger.info(f"Deleting legal entity with ID: {legal_entity_id}")
        legal_entity_to_delete = session.select(LegalEntity).filter(LegalEntity.id == legal_entity_id).first()
        if legal_entity_to_delete:
            try:
                session.delete(legal_entity_to_delete)
                await session.commit()
                logger.info(f"Legal entity with ID {legal_entity_id} deleted successfully")
                return True
            except Exception as e:
                logger.error("Error occurred while deleting legal entity", exc_info=True)
                raise
        else:
            logger.warning(f"Legal entity with ID {legal_entity_id} not found")
            raise LegalEntityNotFoundError(f"LEGAL_ENTITY_NOT_FOUND: {legal_entity_id}")