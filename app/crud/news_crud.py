from app.database import connection
from app.models.news_model import News
from app.schemas.news_schema import *  # Импортируйте ваши схемы для валидации
from app.errors_custom_types import *  # Импортируйте ваши пользовательские ошибки
from sqlalchemy import func
import logging

# Create a logger specific to this module
logger = logging.getLogger("app.news_crud")


class NewsCRUD:
    @connection
    async def create_news(self, news: NewsCreate, session):
        logger.info("Creating a new news entry")
        try:
            new_news = News(
                title=news.title,
                description=news.description,
                publication_date=news.publication_date,
                photo=news.photo
            )
            session.add(new_news)
            await session.commit()
            logger.info(f"News created successfully with ID: {new_news.id}")
            return new_news
        except Exception as e:
            logger.error("Error occurred while creating news", exc_info=True)
            raise

    @connection
    async def get_news(self, news_id: int, session):
        logger.info(f"Fetching news with ID: {news_id}")
        news_item = session.select(News).filter(News.id == news_id).first()
        if news_item:
            logger.info(f"News with ID {news_id} retrieved successfully")
            return news_item
        else:
            logger.warning(f"News with ID {news_id} not found")
            raise NewsNotFoundError(f"NEWS_NOT_FOUND: {news_id}")

    @connection
    async def get_news_paginated(self, page: int = 1, page_size: int = 10, session=None):
        logger.info(f"Fetching paginated news: Page {page}, Page Size {page_size}")
        try:
            offset = (page - 1) * page_size
            total_items = session.query(func.count(News.id)).scalar()
            total_pages = (total_items + page_size - 1) // page_size
            news_items = session.query(News).offset(offset).limit(page_size).all()
            news_get = [NewsResponse(**news.__dict__()) for news in news_items]
            response = {
                "page": page,
                "page_size": page_size,
                "total_items": total_items,
                "total_pages": total_pages,
                "has_next": page < total_pages,
                "has_previous": page > 1,
                "news": news_get
            }
            logger.info(f"Paginated news retrieved successfully: Page {page}")
            return response
        except Exception as e:
            logger.error("Error occurred while fetching paginated news", exc_info=True)
            raise

    @connection
    async def patch_news(self, news_id: int, session, **params):
        logger.info(f"Patching news with ID: {news_id}")
        news_to_patch = session.select(News).filter(News.id == news_id).first()
        if news_to_patch:
            try:
                for key, value in params.items():
                    if hasattr(news_to_patch, key):
                        setattr(news_to_patch, key, value)
                        logger.debug(f"Updated field {key} to {value} for news ID {news_id}")
                    else:
                        logger.warning(f"Field {key} not found in News model")
                        raise NewsUpdateError(f"FIELD_NOT_FOUND: {key}")
                await session.commit()
                logger.info(f"News with ID {news_id} patched successfully")
                return news_to_patch
            except Exception as e:
                logger.error("Error occurred while patching news", exc_info=True)
                raise
        else:
            logger.warning(f"News with ID {news_id} not found")
            raise NewsNotFoundError(f"NEWS_NOT_FOUND: {news_id}")

    @connection
    async def delete_news(self, news_id: int, session):
        logger.info(f"Deleting news with ID: {news_id}")
        news_to_delete = session.select(News).filter(News.id == news_id).first()
        if news_to_delete:
            try:
                session.delete(news_to_delete)
                await session.commit()
                logger.info(f"News with ID {news_id} deleted successfully")
                return True
            except Exception as e:
                logger.error("Error occurred while deleting news", exc_info=True)
                raise
        else:
            logger.warning(f"News with ID {news_id} not found")
            raise NewsNotFoundError(f"NEWS_NOT_FOUND: {news_id}")