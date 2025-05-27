from sqlalchemy.future import select
from sqlalchemy import func
import logging
from app.database import connection
from app.models.fundraising_model import Fundraising
from app.schemas.fundraising_schema import *
from app.errors_custom_types import *

logger = logging.getLogger("app.fundraising_crud")


class FundraisingCRUD:
    @connection
    async def create_fundraising(self, fundraising: FundraisingCreate, session):
        logger.info("Creating a new fundraising")
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
            await session.refresh(new_fundraising)
            logger.info(f"Fundraising created successfully with ID: {new_fundraising.id}")
            return new_fundraising
        except Exception as e:
            logger.error("Error occurred while creating fundraising", exc_info=True)
            raise

    @connection
    async def get_fundraising(self, fundraising_id: int, session):
        logger.info(f"Fetching fundraising with ID: {fundraising_id}")
        try:
            fundraising = await session.get(Fundraising, fundraising_id)
            if fundraising:
                logger.info(f"Fundraising with ID {fundraising_id} retrieved successfully")
                return fundraising
            else:
                logger.warning(f"Fundraising with ID {fundraising_id} not found")
                raise NotFoundError('Fundraising', fundraising_id)
        except Exception as e:
            logger.error(f"Error occurred while fetching fundraising with ID {fundraising_id}", exc_info=True)
            raise

    @connection
    async def patch_fundraising(self, fundraising_id: int, session, params):
        try:
            fundraising_to_patch = await session.get(Fundraising, fundraising_id)
            if fundraising_to_patch:
                for key, value in params.params.items():
                    if hasattr(fundraising_to_patch, key):
                        setattr(fundraising_to_patch, key, value)
                        logger.debug(f"Updated field {key} to {value} for fundraising ID {fundraising_id}")
                    else:
                        logger.warning(f"Field {key} not found in Fundraising model")
                        raise FundraisingUpdateError(f"FIELD_NOT_FOUND: {key}")
                await session.commit()
                await session.refresh(fundraising_to_patch)
                logger.info(f"Fundraising with ID {fundraising_id} patched successfully")
                return fundraising_to_patch
            else:
                logger.warning(f"Fundraising with ID {fundraising_id} not found")
                raise NotFoundError('Fundraising', fundraising_id)
        except Exception as e:
            logger.error(f"Error occurred while patching fundraising with ID {fundraising_id}", exc_info=True)
            raise

    @connection
    async def delete_fundraising(self, fundraising_id: int, session):
        logger.info(f"Deleting fundraising with ID: {fundraising_id}")
        try:
            fundraising_to_delete = await session.get(Fundraising, fundraising_id)
            if fundraising_to_delete:
                await session.delete(fundraising_to_delete)
                await session.commit()
                logger.info(f"Fundraising with ID {fundraising_id} deleted successfully")
                return True
            else:
                logger.warning(f"Fundraising with ID {fundraising_id} not found")
                raise NotFoundError('Fundraising', fundraising_id)
        except Exception as e:
            logger.error(f"Error occurred while deleting fundraising with ID {fundraising_id}", exc_info=True)
            raise