from app.database import connection
from app.models.news_model import News
from app.schemas.news_schema import *  # Импортируйте ваши схемы для валидации
from app.errors_custom_types import *  # Импортируйте ваши пользовательские ошибки
from sqlalchemy import func


class NewsCRUD:
    @connection
    async def create_news(self, news: NewsCreate, session):
        new_news = News(title=news.title,
                        description=news.description,
                        publication_date=news.publication_date,
                        photo=news.photo
                        )
        session.add(new_news)
        session.commit()
        return new_news

    @connection
    async def get_news(self, news_id: int, session):
        news_item = session.select(News).filter(News.id == news_id).first()
        if news_item:
            return news_item
        else:
            raise NewsNotFoundError(f"NEWS_NOT_FOUND: {news_id}")

    @connection
    async def get_news_paginated(self, page: int = 1, page_size: int = 10, session=None):
        offset = (page - 1) * page_size
        total_items = session.query(func.count(News.id)).scalar()
        total_pages = (total_items + page_size - 1) // page_size
        news_items = session.query(News).offset(offset).limit(page_size).all()
        news_get = [NewsResponse(**news.__dict__()) for news in news_items]  # Предполагается, что у вас есть схема NewsResponse
        response = {
            "page": page,
            "page_size": page_size,
            "total_items": total_items,
            "total_pages": total_pages,
            "has_next": page < total_pages,
            "has_previous": page > 1,
            "news": news_get
        }
        return response

    @connection
    async def patch_news(self, news_id: int, session, **params):
        news_to_patch = session.select(News).filter(News.id == news_id).first()
        if news_to_patch:
            for key, value in params.items():
                if hasattr(news_to_patch, key):
                    setattr(news_to_patch, key, value)
                else:
                    raise NewsUpdateError(f"FIELD_NOT_FOUND: {key}")
            session.commit()
            return news_to_patch
        else:
            raise NewsNotFoundError(f"NEWS_NOT_FOUND: {news_id}")

    @connection
    def delete_news(self, news_id: int, session):
        news_to_delete = session.select(News).filter(News.id == news_id).first()
        if news_to_delete:
            session.delete(news_to_delete)
            session.commit()
            return True
        else:
            raise NewsNotFoundError(f"NEWS_NOT_FOUND: {news_id}")
