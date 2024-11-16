from app.database import Base, engine


def init_db():
    Base.metadata.create_all(bind=engine)


def drop_db():
    Base.metadata.drop_all(bind=engine)


def recreate_db():
    drop_db()
    print('db dropped!')
    init_db()

# from app.database import Base, engine
# from contextlib import asynccontextmanager
#
#
# @asynccontextmanager
# async def get_session():
#     async_session = AsyncSessionLocal()
#     async with async_session as session:
#         yield session
#         await session.commit()
#
# async def init_db():
#     """Инициализирует структуру базы данных."""
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#
# async def drop_db():
#     """Удаляет все таблицы из базы данных."""
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#
# async def recreate_db():
#     """Пересоздаёт всю структуру базы данных (удаляет и создаёт заново)."""
#     await drop_db()
#     print('db dropped!')
#     await init_db()