from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy import Integer, func
from datetime import datetime
from app.config import settings
import logging

logger = logging.getLogger("app.database")

DATABASE_URL = settings.get_db_url()
logger.info(f"Initializing database engine with URL: {DATABASE_URL}")
engine = create_async_engine(url=DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


def connection(method):
    async def wrapper(*args, **kwargs):
        logger.info(f"Opening a new database session for method: {method.__name__}")
        async with async_session_maker() as session:
            try:
                result = await method(*args, session=session, **kwargs)
                logger.info(f"Method {method.__name__} completed successfully")
                return result
            finally:
                logger.info(f"Database session for method {method.__name__} closed")

    return wrapper

class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())