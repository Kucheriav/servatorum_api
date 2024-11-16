from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost/servatorium_test_db"

# engine = create_async_engine(DATABASE_URL, echo=True)
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# AsyncSessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


Base = declarative_base()


class Database:
    def __init__(self):
        self.session = SessionLocal()

    def init_db(self):
        Base.metadata.create_all(bind=engine)

    def drop_db(self):
        Base.metadata.drop_all(bind=engine)

    def recreate_db(self):
        self.drop_db()
        print('db dropped!')
        self.init_db()

    def close(self):
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def add(self, obj):
        self.session.add(obj)

    def commit(self):
        self.session.commit()