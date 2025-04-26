from sqlalchemy.future import select
from sqlalchemy import func
import logging
from app.database import connection
from app.models.news_model import News
from app.schemas.news_schema import *
from app.errors_custom_types import *

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
            await session.refresh(new_news)
            logger.info(f"News created successfully with ID: {new_news.id}")
            return new_news
        except Exception as e:
            logger.error("Error occurred while creating news", exc_info=True)
            raise

    @connection
    async def get_news(self, news_id: int, session):
        logger.info(f"Fetching news with ID: {news_id}")
        try:
            query = select(News).where(News.id == news_id)
            result = await session.execute(query)
            news_item = result.scalar_one_or_none()
            if news_item:
                logger.info(f"News with ID {news_id} retrieved successfully")
                return news_item
            else:
                logger.warning(f"News with ID {news_id} not found")
                raise NewsNotFoundError(f"NEWS_NOT_FOUND: {news_id}")
        except Exception as e:
            logger.error(f"Error occurred while fetching news with ID {news_id}", exc_info=True)
            raise

    @connection
    async def get_news_paginated(self, page: int = 1, page_size: int = 10, session=None):
        logger.info(f"Fetching paginated news: Page {page}, Page Size {page_size}")
        try:
            offset = (page - 1) * page_size
            query = select(News).offset(offset).limit(page_size)
            result = await session.execute(query)
            news_items = result.scalars().all()
            total_items_query = await session.execute(select(func.count(News.id)))
            total_items = total_items_query.scalar()
            total_pages = (total_items + page_size - 1) // page_size
            response = {
                "page": page,
                "page_size": page_size,
                "total_items": total_items,
                "total_pages": total_pages,
                "has_next": page < total_pages,
                "has_previous": page > 1,
                "news": [news.__dict__ for news in news_items]
            }
            logger.info(f"Paginated news retrieved successfully: Page {page}")
            return response
        except Exception as e:
            logger.error(f"Error occurred while fetching paginated news", exc_info=True)
            raise

    @connection
    async def delete_news(self, news_id: int, session):
        logger.info(f"Deleting news with ID: {news_id}")
        try:
            query = select(News).where(News.id == news_id)
            result = await session.execute(query)
            news_to_delete = result.scalar_one_or_none()
            if news_to_delete:
                await session.delete(news_to_delete)
                await session.commit()
                logger.info(f"News with ID {news_id} deleted successfully")
                return True
            else:
                logger.warning(f"News with ID {news_id} not found")
                raise NewsNotFoundError(f"NEWS_NOT_FOUND: {news_id}")
        except Exception as e:
            logger.error(f"Error occurred while deleting news with ID {news_id}", exc_info=True)
            raise