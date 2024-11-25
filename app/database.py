from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy import Integer, func
from datetime import datetime
from app.config import settings


DATABASE_URL = settings.get_db_url()
engine = create_async_engine(url=DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


def connection(method):
    async def wrapper(*args, **kwargs):
        async with async_session_maker() as session:
            try:
                # Явно не открываем транзакции, так как они уже есть в контексте
                return await method(*args, session=session, **kwargs)
            except Exception as e:
                await session.rollback()
                raise e
            finally:
                await session.close()

    return wrapper

# Базовый класс для всех моделей
class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    @declared_attr.directive
    def __tablename__(self) -> str:
        return self.__name__.lower() + 's'


