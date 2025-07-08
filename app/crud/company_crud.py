import logging
from app.database import connection
from app.models.user_model import UserEntityRelation
from app.models.company_model import Company, CompanyAccountDetails
from app.schemas.company_schema import *
from app.errors_custom_types import *
from sqlalchemy.exc import IntegrityError

logger = logging.getLogger("app.company_crud")


class CompanyCRUD:
    @connection
    async def create_company(self, company: CompanyCreate, user_id: int,  session):
        logger.info("Creating a new company")
        try:
            new_company = Company(
                administrator_name = company.administrator_name,
                administrator_surname = company.administrator_surname,
                administrator_lastname = company.administrator_lastname,
                name=company.name,
                description=company.description,
                address=company.address,
                phone=company.phone,
                email=company.email,
                site=company.site,
                logo = company.logo
            )
            session.add(new_company)
            await session.commit()
            await session.refresh(new_company)
            logger.info(f"Company created successfully with ID: {new_company.id}")
            details = company.account_details
            new_details = CompanyAccountDetails(
                company=new_company.id,
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
            logger.info(f"Added account details for company: {new_company.id}")
            new_relation = UserEntityRelation(
                user_id=user_id,
                entity_id=new_company.id,
                entity_type="company"
            )
            session.add(new_relation)
            await session.commit()
            logger.info(f"Added data into UserEntityRelation table")
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
                        raise UpdateError('Company', company_id)
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