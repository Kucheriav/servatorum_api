import logging
from app.database import connection
from app.models.company_model import Company
from app.schemas.company_schema import *
from app.errors_custom_types import *
from sqlalchemy.exc import IntegrityError

logger = logging.getLogger("app.company_crud")


class CompanyCRUD:
    @connection
    async def create_company(self, company: CompanyCreate, session):
        logger.info("Creating a new company")
        try:
            new_company = Company(
                name=company.name,
                description=company.description,
                logo=company.logo,
                inn=company.inn,
                bik=company.bik,
                cor_account=company.cor_account,
                address=company.address,
                address_reg=company.address_reg,
                phone=company.phone,
                phone_helpdesk=company.phone_helpdesk,
            )
            session.add(new_company)
            await session.commit()
            await session.refresh(new_company)
            logger.info(f"Company created successfully with ID: {new_company.id}")
            return new_company
        except IntegrityError as e:
            logger.error("Integrity Error occurred while creating company", exc_info=True)
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
            logger.error("Error occurred while creating company", exc_info=True)
            raise

    @connection
    async def get_company(self, company_id: int, session):
        logger.info(f"Fetching company with ID: {company_id}")
        try:
            company = await session.get(Company, company_id)
            if company:
                logger.info(f"Company with ID {company_id} retrieved successfully")
                return company
            else:
                logger.warning(f"Company with ID {company_id} not found")
                raise NotFoundError('Company', company_id)
        except Exception as e:
            logger.error(f"Error occurred while fetching company with ID {company_id}", exc_info=True)
            raise

    @connection
    async def patch_company(self, company_id: int, session, params):
        try:
            company_to_patch = await session.get(Company, company_id)
            if company_to_patch:
                for key, value in params.params.items():
                    if hasattr(company_to_patch, key):
                        setattr(company_to_patch, key, value)
                        logger.debug(f"Updated field {key} to {value} for Company ID {company_id}")
                    else:
                        logger.warning(f"Field {key} not found in Company model")
                        raise CompanyUpdateError(f"FIELD_NOT_FOUND: {key}")
                await session.commit()
                await session.refresh(company_to_patch)
                logger.info(f"Company with ID {company_id} patched successfully")
                return company_to_patch
            else:
                logger.warning(f"Company with ID {company_id} not found")
                raise NotFoundError('Company', company_id)
        except IntegrityError as e:
            logger.error("Integrity Error occurred while patching company", exc_info=True)
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
            logger.error(f"Error occurred while patching company with ID {company_id}", exc_info=True)
            raise

    @connection
    async def delete_company(self, company_id: int, session):
        logger.info(f"Deleting company with ID: {company_id}")
        try:
            company_to_delete = await session.get(Company, company_id)
            if company_to_delete:
                await session.delete(company_to_delete)
                await session.commit()
                logger.info(f"Company with ID {company_id} deleted successfully")
                return True
            else:
                logger.warning(f"Company with ID {company_id} not found")
                raise NotFoundError('Company', company_id)
        except Exception as e:
            logger.error(f"Error occurred while deleting company with ID {company_id}", exc_info=True)
            raise