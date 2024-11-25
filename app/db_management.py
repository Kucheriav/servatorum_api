from app.database import Base, engine

# говорят, в асинхронном контексте не нужно инициализировать таблдицы ((((
def init_db():
    Base.metadata.create_all(bind=engine)


def drop_db():
    Base.metadata.drop_all(bind=engine)


def recreate_db():
    drop_db()
    print('db dropped!')
    init_db()

