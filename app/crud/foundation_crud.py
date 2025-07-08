from sqlalchemy.future import select
import logging
from app.database import connection
from app.models.foundation_model import Foundation, FoundationAccountDetails
from app.models.user_model import UserEntityRelation
from app.schemas.foundation_schema import *
from app.errors_custom_types import *
from sqlalchemy.exc import IntegrityError

logger = logging.getLogger("app.foundation_crud")
FORBIDDEN_FIELDS = {"id", "created_at", "updated_at"}

class FoundationCRUD:
    @connection
    async def create_foundation(self, foundation: FoundationCreate, user_id: int, session):
        logger.info("Creating a new foundation")
        try:
            new_foundation = Foundation(
                administrator_name=foundation.administrator_name,
                administrator_surname=foundation.administrator_surname,
                administrator_lastname=foundation.administrator_lastname,
                name=foundation.name,
                description=foundation.description,
                address=foundation.address,
                phone=foundation.phone,
                email=foundation.email,
                site=foundation.site,
                logo=foundation.logo
            )
            session.add(new_foundation)
            await session.commit()
            await session.refresh(new_foundation)
            logger.info(f"Foundation created successfully with ID: {new_foundation.id}")
            details = foundation.account_details
            new_details = FoundationAccountDetails(
                company=new_foundation.id,
                inn=details.inn,
                kpp=details.kpp,
                account_name=details.account_name,
                bank_account=details.bank_account,
                cor_account=details.cor_account,
                bik=details.bik
            )
            session.add(new_details)
            await session.commit()
            await session.refresh(new_details)
            logger.info(f"Added account details for foundation: {new_foundation.id}")

            new_relation = UserEntityRelation(
                user_id=user_id,
                entity_id=new_foundation.id,
                entity_type="company"
            )
            session.add(new_relation)
            await session.commit()
            logger.info(f"Added data into UserEntityRelation table")
            accounts = [FoundationAccountDetailsResponse.model_validate(new_details)]
            resp = FoundationResponse(
                id=new_foundation.id,
                administrator_name=new_foundation.administrator_name,
                administrator_surname=new_foundation.administrator_surname,
                administrator_lastname=new_foundation.administrator_lastname,
                name=new_foundation.name,
                description=new_foundation.description,
                address=new_foundation.address,
                phone=new_foundation.phone,
                email=new_foundation.email,
                site=new_foundation.site,
                logo=new_foundation.logo,
                account_details=accounts
            )
            return resp
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
            if not foundation:
                logger.warning(f"Foundation with ID {foundation_id} not found")
                raise NotFoundError('Foundation', foundation_id)
                # Получаем счета
            details_query = select(FoundationAccountDetails).where(
                FoundationAccountDetails.foundation == foundation_id
            )
            details_result = await session.execute(details_query)
            accounts = details_result.scalars().all()
            accounts_list = [
                FoundationAccountDetailsResponse.model_validate(acc)
                for acc in accounts
            ]
            resp = FoundationResponse(
                id=foundation.id,
                administrator_name=foundation.administrator_name,
                administrator_surname=foundation.administrator_surname,
                administrator_lastname=foundation.administrator_lastname,
                name=foundation.name,
                description=foundation.description,
                address=foundation.address,
                phone=foundation.phone,
                email=foundation.email,
                site=foundation.site,
                logo=foundation.logo,
                account_details=accounts_list
            )
            logger.info(f"Foundation with ID {foundation_id} retrieved successfully")
            return resp
        except Exception as e:
            logger.error(f"Error occurred while fetching foundation with ID {foundation_id}", exc_info=True)
            raise

    @connection
    async def patch_foundation(self, foundation_id: int, session, params: FoundationPatch):
        try:
            foundation_to_patch = await session.get(Foundation, foundation_id)
            if not foundation_to_patch:
                logger.warning(f"Foundation with ID {foundation_id} not found")
                raise NotFoundError('Foundation', foundation_id)
            # Патчим базовые поля
            for key, value in params.params.items():
                if hasattr(foundation_to_patch, key):
                    if key in FORBIDDEN_FIELDS:
                        logger.warning(f"Attempt to patch forbidden field {key} for Foundation ID {foundation_id}")
                        continue
                    setattr(foundation_to_patch, key, value)
                    logger.debug(f"Updated field {key} to {value} for Foundation ID {foundation_id}")
                else:
                    logger.warning(f"Field {key} not found in Foundation model")
                    raise UpdateError('Foundation', foundation_id)
            # Патчим счета
            if params.account_details:
                for ac_patch in params.account_details:
                    if not ac_patch.id:
                        logger.warning("No id for account details patch, skipping...")
                        continue
                    account = await session.get(FoundationAccountDetails, ac_patch.id)
                    if not account or account.foundation != foundation_id:
                        logger.warning(f"Account {ac_patch.id} not found or not related to foundation {foundation_id}")
                        continue  # или raise
                    for key, value in ac_patch.dict(exclude_unset=True).items():
                        if key != "id" and hasattr(account, key):
                            setattr(account, key, value)
                            logger.debug(
                                f"Updated account_details field {key} to {value} for Foundation ID {foundation_id}")
            await session.commit()
            await session.refresh(foundation_to_patch)
            # Собираем response
            details_query = select(FoundationAccountDetails).where(
                FoundationAccountDetails.foundation == foundation_id
            )
            details_result = await session.execute(details_query)
            accounts = details_result.scalars().all()
            accounts_list = [
                FoundationAccountDetailsResponse.model_validate(acc)
                for acc in accounts
            ]
            resp = FoundationResponse(
                id=foundation_to_patch.id,
                administrator_name=foundation_to_patch.administrator_name,
                administrator_surname=foundation_to_patch.administrator_surname,
                administrator_lastname=foundation_to_patch.administrator_lastname,
                name=foundation_to_patch.name,
                description=foundation_to_patch.description,
                address=foundation_to_patch.address,
                phone=foundation_to_patch.phone,
                email=foundation_to_patch.email,
                site=foundation_to_patch.site,
                logo=foundation_to_patch.logo,
                account_details=accounts_list
            )
            logger.info(f"Foundation with ID {foundation_id} patched successfully")
            return resp
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
    async def add_account_details(self, foundation_id: int, details: FoundationAccountDetailsAdd, session):
        logger.info(f"Adding new account details to foundation {foundation_id}")
        try:
            foundation = await session.get(Foundation, foundation_id)
            if not foundation:
                raise NotFoundError('Foundation', foundation_id)
            new_details = FoundationAccountDetails(
                foundation=foundation_id,
                inn=details.inn,
                kpp=details.kpp,
                account_name=details.account_name,
                bank_account=details.bank_account,
                cor_account=details.cor_account,
                bik=details.bik,
            )
            session.add(new_details)
            await session.commit()
            await session.refresh(new_details)
            logger.info(f"New account details added for foundation: {foundation_id}")
            return FoundationAccountDetailsAddResponse.model_validate(new_details)
        except IntegrityError as e:
            logger.error("Integrity Error occurred while adding account details", exc_info=True)
            raise
        except Exception as e:
            logger.error("Error occurred while adding account details", exc_info=True)
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