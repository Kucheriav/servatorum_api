from dotenv import load_dotenv

load_dotenv()


from logging.config import fileConfig

from app.models import Base

from urllib.parse import quote_plus
import os

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.
DB_USER = os.getenv("DB_USER", "")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "")
DB_PORT = os.getenv("DB_PORT", "")
DB_NAME = os.getenv("DB_NAME", "")


URL_TEMPLATE = "postgresql+asyncpg://%s:%s@%s:%s/%s"
quoted_password = quote_plus(DB_PASSWORD)
config.set_main_option(
    "sqlalchemy.url",
    URL_TEMPLATE % (
        DB_USER,
        quoted_password,
        DB_HOST,
        DB_PORT,
        DB_NAME
    )
)


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

#
# def run_migrations_online() -> None:
#     """Run migrations in 'online' mode.
#
#     In this scenario we need to create an Engine
#     and associate a connection with the context.
#
#     """
#     connectable = create_async_engine(config.get_main_option("sqlalchemy.url"))
#
#     with connectable.connect() as connection:
#         context.configure(
#             connection=connection,
#             target_metadata=target_metadata,
#             compare_type=True,
#             render_as_batch=True
#         )
#
#         with context.begin_transaction():
#             context.run_migrations()

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncConnection, create_async_engine
from typing import Optional
async def run_migrations_online_async(connection: Optional[AsyncConnection] = None) -> None:
    """Run migrations in 'online' mode."""
    if connection is None:
        connectable = AsyncEngine(create_async_engine(config.get_main_option("sqlalchemy.url")))
    else:
        connectable = connection

    async with connectable.begin() as conn:
        await conn.run_sync(context.configure, connection=conn, target_metadata=target_metadata, compare_type=True, render_as_batch=True)
        await conn.run_sync(context.run_migrations)


# def run_migrations_offline_automized() -> None:
#     import os
#     from alembic import op
#     from sqlalchemy.engine.reflection import Inspector
#
#     # Функция для записи миграций в SQL-файл
#     def write_sql_to_file(filename, sql):
#         with open(filename, 'w') as f:
#             f.write(sql)
#
#     # Основной метод для запуска миграций в оффлайне
#
#     def run_migrations_offline():
#         # Определяем путь для хранения SQL-файлов
#         migrations_dir = config.get_main_option('migrations_directory')
#         if not os.path.exists(migrations_dir):
#             os.makedirs(migrations_dir)
#
#         # Получаем список таблиц из существующей схемы
#         inspector = Inspector.from_engine(op.get_bind())
#         existing_tables = set(inspector.get_table_names())
#
#         # Генерируем команды для новых таблиц/колонок
#         for table_name in target_metadata.tables.keys():
#             if table_name not in existing_tables:
#                 print(f'Creating table {table_name}')
#                 # Генерируем команду CREATE TABLE
#                 create_table_command = str(target_metadata.tables[table_name].create(op.get_bind()))
#                 filename = os.path.join(migrations_dir, f'{table_name}_create.sql')
#                 write_sql_to_file(filename, create_table_command)
#
#         # Остальные необходимые операции также записываются в отдельные файлы
from pprint import pprint

pprint(target_metadata.tables)

if context.is_offline_mode():
    run_migrations_offline()
else:
    # import asyncio
    # asyncio.run(run_migrations_online_async())
    run_migrations_online_async()

# alembic revision --autogenerate -m "Initial migration for async database support"
# этот черт плюется пустыми файлами миграций, хотя все модели видны.
# я что-то не понимаю, за какой конец держать этот молоток