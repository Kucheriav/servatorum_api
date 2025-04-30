from sqlalchemy.future import select
import logging
from app.database import connection
from app.models.legal_entity_model import LegalEntity
from app.schemas.legal_entity_schema import *
from app.errors_custom_types import *
from sqlalchemy.exc import IntegrityError

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
            await session.refresh(new_legal_entity)
            logger.info(f"Legal entity created successfully with ID: {new_legal_entity.id}")
            return new_legal_entity
        except IntegrityError as e:
            logger.error("Integrity Error occurred while creating legal entity", exc_info=True)
            constraint_name = None
            if hasattr(e.orig, "diag") and e.orig.diag.constraint_name:
                constraint_name = e.orig.diag.constraint_name
            constraint_error_messages = {
                "check_inn": "The INN field violates format constraints.",
                "check_cor_account": "The Correspondent Account must be exactly 20 digits.",
                "check_phone": "The Phone number must follow the format '7XXXXXXXXXX'.",
                "check_phone_helpdesk": "The Helpdesk Phone number must follow the format '7XXXXXXXXXX'.",
            }
            error_message = constraint_error_messages.get(
                constraint_name, str(e.orig)
            )
            raise ConstrictionViolatedError(error_message)
        except Exception as e:
            logger.error("Error occurred while creating legal entity", exc_info=True)
            raise

    @connection
    async def get_legal_entity(self, legal_entity_id: int, session):
        logger.info(f"Fetching legal entity with ID: {legal_entity_id}")
        try:
            query = select(LegalEntity).where(LegalEntity.id == legal_entity_id)
            result = await session.execute(query)
            legal_entity = result.scalar_one_or_none()
            if legal_entity:
                logger.info(f"Legal entity with ID {legal_entity_id} retrieved successfully")
                return legal_entity
            else:
                logger.warning(f"Legal entity with ID {legal_entity_id} not found")
                raise LegalEntityNotFoundError(f"LEGAL_ENTITY_NOT_FOUND: {legal_entity_id}")
        except Exception as e:
            logger.error(f"Error occurred while fetching legal entity with ID {legal_entity_id}", exc_info=True)
            raise

    @connection
    async def patch_legal_entity(self, legal_entity_id: int, session, params):
        try:
            query = select(LegalEntity).where(LegalEntity.id == legal_entity_id)
            result = await session.execute(query)
            legal_entity_to_patch = result.scalar_one_or_none()
            if legal_entity_to_patch:
                for key, value in params.params.items():
                    if hasattr(legal_entity_to_patch, key):
                        setattr(legal_entity_to_patch, key, value)
                        logger.debug(f"Updated field {key} to {value} for LegalEntity ID {legal_entity_id}")
                    else:
                        logger.warning(f"Field {key} not found in LegalEntity model")
                        raise LegalEntityUpdateError(f"FIELD_NOT_FOUND: {key}")
                await session.commit()
                logger.info(f"LegalEntity with ID {legal_entity_id} patched successfully")
                return legal_entity_to_patch
            else:
                logger.warning(f"LegalEntity with ID {legal_entity_id} not found")
                raise LegalEntityNotFoundError(f"LEGAL_ENTITY_NOT_FOUND: {legal_entity_id}")
        except IntegrityError as e:
            logger.error("Integrity Error occurred while creating legal entity", exc_info=True)
            constraint_name = None
            if hasattr(e.orig, "diag") and e.orig.diag.constraint_name:
                constraint_name = e.orig.diag.constraint_name
            constraint_error_messages = {
                "check_inn": "The INN field violates format constraints.",
                "check_cor_account": "The Correspondent Account must be exactly 20 digits.",
                "check_phone": "The Phone number must follow the format '7XXXXXXXXXX'.",
                "check_phone_helpdesk": "The Helpdesk Phone number must follow the format '7XXXXXXXXXX'.",
            }
            error_message = constraint_error_messages.get(
                constraint_name, str(e.orig)
            )
            raise ConstrictionViolatedError(error_message)
        except Exception as e:
            logger.error(f"Error occurred while patching legal_entity with ID {legal_entity_id}", exc_info=True)
            raise

    @connection
    async def delete_legal_entity(self, legal_entity_id: int, session):
        logger.info(f"Deleting legal entity with ID: {legal_entity_id}")
        try:
            query = select(LegalEntity).where(LegalEntity.id == legal_entity_id)
            result = await session.execute(query)
            legal_entity_to_delete = result.scalar_one_or_none()
            if legal_entity_to_delete:
                await session.delete(legal_entity_to_delete)
                await session.commit()
                logger.info(f"Legal entity with ID {legal_entity_id} deleted successfully")
                return True
            else:
                logger.warning(f"Legal entity with ID {legal_entity_id} not found")
                raise LegalEntityNotFoundError(f"LEGAL_ENTITY_NOT_FOUND: {legal_entity_id}")
        except Exception as e:
            logger.error(f"Error occurred while deleting legal entity with ID {legal_entity_id}", exc_info=True)
            raise