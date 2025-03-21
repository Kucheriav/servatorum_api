from app.database import connection
from app.models.fundraising_model import Fundraising
from app.schemas.fundraising_schema import *
from app.errors_custom_types import *
from sqlalchemy import func


#TODO manage with raised amount. must be zero as created
#TODO manage with foriegns keys


class FundraisingCRUD:
    @connection
    async def create_fundraising(self, fundraising: FundraisingCreate, session):
        new_fundraising = Fundraising(title=fundraising.title,
                                       description=fundraising.description,
                                       goal_amount=fundraising.goal_amount,
                                       start_date=fundraising.start_date,
                                       finish_date=fundraising.finish_date
                                       )
        session.add(new_fundraising)
        session.commit()
        return new_fundraising

    @connection
    async def get_fundraising(self, fundraising_id: int, session):
        fundraising = session.select(Fundraising).filter(Fundraising.id == fundraising_id).first()
        if fundraising:
            return fundraising
        else:
            raise FundraisingNotFoundError(f"FUNDRAISING_NOT_FOUND: {fundraising_id}")

    @connection
    async def get_fundraisings_paginated(self, page: int = 1, page_size: int = 10, session=None):
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
        return response

    @connection
    async def patch_fundraising(self, fundraising_id: int, session, **params):
        fundraising_to_patch = session.select(Fundraising).filter(Fundraising.id == fundraising_id).first()
        if fundraising_to_patch:
            for key, value in params.items():
                if hasattr(fundraising_to_patch, key):
                    setattr(fundraising_to_patch, key, value)
                else:
                    raise FundraisingUpdateError(f"FIELD_NOT_FOUND: {key}")
            session.commit()
            return fundraising_to_patch
        else:
            raise FundraisingNotFoundError(f"FUNDRAISING_NOT_FOUND: {fundraising_id}")

    @connection
    def delete_fundraising(self, fundraising_id: int, session):
        fundraising_to_delete = session.select(Fundraising).filter(Fundraising.id == fundraising_id).first()
        if fundraising_to_delete:
            session.delete(fundraising_to_delete)
            session.commit()
            return True
        else:
            raise FundraisingNotFoundError(f"FUNDRAISING_NOT_FOUND: {fundraising_id}")