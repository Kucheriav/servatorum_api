from app.database import connection
from app.models.fundraising_model import Fundraising
from app.schemas.fundraising_schema import *
from app.errors_custom_types import *
from sqlalchemy import func
import logging

# Create a logger specific to this module
logger = logging.getLogger("app.fundraising_crud")

# TODO manage with raised amount. must be zero as created
# TODO manage with foreign keys


class FundraisingCRUD:
    @connection
    async def create_fundraising(self, fundraising: FundraisingCreate, session):
        logger.info("Creating a new fundraising entry")
        try:
            new_fundraising = Fundraising(
                title=fundraising.title,
                description=fundraising.description,
                goal_amount=fundraising.goal_amount,
                start_date=fundraising.start_date,
                finish_date=fundraising.finish_date
            )
            session.add(new_fundraising)
            await session.commit()
            logger.info(f"Fundraising created successfully with ID: {new_fundraising.id}")
            return new_fundraising
        except Exception as e:
            logger.error("Error occurred while creating fundraising", exc_info=True)
            raise

    @connection
    async def get_fundraising(self, fundraising_id: int, session):
        logger.info(f"Fetching fundraising with ID: {fundraising_id}")
        fundraising = session.select(Fundraising).filter(Fundraising.id == fundraising_id).first()
        if fundraising:
            logger.info(f"Fundraising with ID {fundraising_id} retrieved successfully")
            return fundraising
        else:
            logger.warning(f"Fundraising with ID {fundraising_id} not found")
            raise FundraisingNotFoundError(f"FUNDRAISING_NOT_FOUND: {fundraising_id}")

    @connection
    async def get_fundraisings_paginated(self, page: int = 1, page_size: int = 10, session=None):
        logger.info(f"Fetching paginated fundraisings: Page {page}, Page Size {page_size}")
        try:
            offset = (page - 1) * page_size
            total_items = session.query(func.count(Fundraising.id)).scalar()
            total_pages = (total_items + page_size - 1) // page_size
            fundraisings = session.query(Fundraising).offset(offset).limit(page_size).all()
            fundraisings_get = [FundraisingResponce(**fundraising.__dict__) for fundraising in fundraisings]
            response = {
                "page": page,
                "page_size": page_size,
                "total_items": total_items,
                "total_pages": total_pages,
                "has_next": page < total_pages,
                "has_previous": page > 1,
                "fundraisings": fundraisings_get
            }
            logger.info(f"Paginated fundraisings retrieved successfully: Page {page}")
            return response
        except Exception as e:
            logger.error("Error occurred while fetching paginated fundraisings", exc_info=True)
            raise

    @connection
    async def patch_fundraising(self, fundraising_id: int, session, **params):
        logger.info(f"Patching fundraising with ID: {fundraising_id}")
        fundraising_to_patch = session.select(Fundraising).filter(Fundraising.id == fundraising_id).first()
        if fundraising_to_patch:
            try:
                for key, value in params.items():
                    if hasattr(fundraising_to_patch, key):
                        setattr(fundraising_to_patch, key, value)
                        logger.debug(f"Updated field {key} to {value} for fundraising ID {fundraising_id}")
                    else:
                        logger.warning(f"Field {key} not found in Fundraising model")
                        raise FundraisingUpdateError(f"FIELD_NOT_FOUND: {key}")
                await session.commit()
                logger.info(f"Fundraising with ID {fundraising_id} patched successfully")
                return fundraising_to_patch
            except Exception as e:
                logger.error("Error occurred while patching fundraising", exc_info=True)
                raise
        else:
            logger.warning(f"Fundraising with ID {fundraising_id} not found")
            raise FundraisingNotFoundError(f"FUNDRAISING_NOT_FOUND: {fundraising_id}")

    @connection
    async def delete_fundraising(self, fundraising_id: int, session):
        logger.info(f"Deleting fundraising with ID: {fundraising_id}")
        fundraising_to_delete = session.select(Fundraising).filter(Fundraising.id == fundraising_id).first()
        if fundraising_to_delete:
            try:
                session.delete(fundraising_to_delete)
                await session.commit()
                logger.info(f"Fundraising with ID {fundraising_id} deleted successfully")
                return True
            except Exception as e:
                logger.error("Error occurred while deleting fundraising", exc_info=True)
                raise
        else:
            logger.warning(f"Fundraising with ID {fundraising_id} not found")
            raise FundraisingNotFoundError(f"FUNDRAISING_NOT_FOUND: {fundraising_id}")