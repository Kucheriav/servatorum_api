from sqlalchemy.future import select
import logging
from app.database import connection
from app.models.foundation_model import Foundation
from app.schemas.foundation_schema import *
from app.errors_custom_types import *
from sqlalchemy.exc import IntegrityError

logger = logging.getLogger("app.foundation_crud")


class FoundationCRUD:
    @connection
    async def create_foundation(self, foundation: FoundationCreate, session):
        logger.info("Creating a new foundation")
        try:
            new_foundation = Foundation(
                name=foundation.name,
                description=foundation.description,
                logo=foundation.logo,
                inn=foundation.inn,
                bik=foundation.bik,
                cor_account=foundation.cor_account,
                address=foundation.address,
                address_reg=foundation.address_reg,
                phone=foundation.phone,
                phone_helpdesk=foundation.phone_helpdesk,
            )
            session.add(new_foundation)
            await session.commit()
            await session.refresh(new_foundation)
            logger.info(f"Foundation created successfully with ID: {new_foundation.id}")
            return new_foundation
        except IntegrityError as e:
            logger.error("Integrity Error occurred while creating foundation", exc_info=True)
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
            logger.error("Error occurred while foundation", exc_info=True)
            raise

    @connection
    async def get_foundation(self, foundation_id: int, session):
        logger.info(f"Fetching foundation with ID: {foundation_id}")
        try:
            foundation = await session.get(Foundation, foundation_id)
            if foundation:
                logger.info(f"Foundation with ID {foundation_id} retrieved successfully")
                return foundation
            else:
                logger.warning(f"Foundation with ID {foundation_id} not found")
                raise NotFoundError('Foundation', foundation_id)
        except Exception as e:
            logger.error(f"Error occurred while fetching foundation with ID {foundation_id}", exc_info=True)
            raise

    @connection
    async def patch_foundation(self, foundation_id: int, session, params):
        try:
            foundation_to_patch = await session.get(Foundation, foundation_id)
            if foundation_to_patch:
                for key, value in params.params.items():
                    if hasattr(foundation_to_patch, key):
                        setattr(foundation_to_patch, key, value)
                        logger.debug(f"Updated field {key} to {value} for Foundation ID {foundation_id}")
                    else:
                        logger.warning(f"Field {key} not found in Foundation model")
                        raise FoundationUpdateError(f"FIELD_NOT_FOUND: {key}")
                await session.commit()
                await session.refresh(foundation_to_patch)
                logger.info(f"Foundation with ID {foundation_id} patched successfully")
                return foundation_to_patch
            else:
                logger.warning(f"Foundation with ID {foundation_id} not found")
                raise NotFoundError('Foundation', foundation_id)
        except IntegrityError as e:
            logger.error("Integrity Error occurred while patching foundation", exc_info=True)
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
            logger.error(f"Error occurred while patching foundation with ID {foundation_id}", exc_info=True)
            raise

    @connection
    async def delete_foundation(self, foundation_id: int, session):
        logger.info(f"Deleting foundation with ID: {foundation_id}")
        try:
            foundation_to_delete = await session.get(Foundation, foundation_id)
            if foundation_to_delete:
                await session.delete(foundation_to_delete)
                await session.commit()
                logger.info(f"Foundation with ID {foundation_id} deleted successfully")
                return True
            else:
                logger.warning(f"Foundation with ID {foundation_id} not found")
                raise NotFoundError('Foundation', foundation_id)
        except Exception as e:
            logger.error(f"Error occurred while deleting foundation with ID {foundation_id}", exc_info=True)
            raise