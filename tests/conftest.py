import asyncio
import pathlib
import sys
from unittest import mock

import aioredis
import pytest
from aioredis import Redis
from alembic.config import Config
from alembic.operations import Operations
from alembic.runtime.environment import EnvironmentContext
from alembic.script import ScriptDirectory
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine, AsyncConnection
from sqlalchemy.orm import sessionmaker

from models import Base, User
from schemas.items import Item

BASE_PATH = pathlib.Path(__file__).parent.parent
sys.path.append(str(BASE_PATH))


@pytest.fixture
def item() -> Item:
    """
    create test item object
    """
    return Item(name='Banana', price=2.99, tax=0.25, description='One pound of banana')


def do_upgrade(revision, context):
    alembic_script = context.script
    return alembic_script._upgrade_revs(alembic_script.get_heads(), revision)  # noqa


def do_run_migrations(connection, alembic_env):
    alembic_env.configure(
        connection=connection, target_metadata=Base.metadata,
        fn=do_upgrade, render_as_batch=True
    )
    migration_context = alembic_env.get_context()

    with migration_context.begin_transaction():
        with Operations.context(migration_context):
            migration_context.run_migrations()


async def async_migrate(engine: AsyncEngine, alembic_env):
    async with engine.begin() as conn:
        await conn.run_sync(do_run_migrations, alembic_env)


async def migrate(engine: AsyncEngine, url: str):
    alembic_cfg = Config()
    alembic_cfg.set_main_option("script_location", "alembic")
    alembic_cfg.set_main_option("url", url)
    alembic_script = ScriptDirectory.from_config(alembic_cfg)
    alembic_env = EnvironmentContext(alembic_cfg, alembic_script)

    await async_migrate(engine, alembic_env)


async def disconnect(engine: AsyncEngine):
    """
    Disposes a database engine
    For sqlite3 in memory db this means destroying database with data
    :param engine: async sqlalchemy engine to be disposed
    :return: None
    """
    await engine.dispose()


@pytest.fixture(scope='session')
def database_test_url() -> str:
    """
    generate in memory sqlite db connect url for test purposes
    :return: url string for test database connection
    """
    return "sqlite+aiosqlite://?cache=shared"  # noqa


@pytest.fixture(scope='session')
def redis_test_url() -> str:
    """
    generate test string for redis connection
    :return: url string for redis test database connection
    """
    return "redis://127.0.0.1:6379/0"


@pytest.fixture(scope='session')
async def engine(database_test_url: str) -> AsyncEngine:
    """
    create async engine and run alembic migrations on database
    :return: sqlalchemy async engine
    """
    url = database_test_url
    engine = create_async_engine(url, echo=False)
    await migrate(engine, url)
    yield engine
    await engine.dispose()


@pytest.fixture(scope='session')
async def get_redis(redis_test_url: str) -> Redis:
    """
    create redis test connection pool with url connection string provided
    :param redis_test_url: url string
    :return: Redis instance
    """
    return aioredis.from_url(
        redis_test_url
    )


@pytest.fixture(scope='session')
async def get_app(
        engine: AsyncEngine,
        database_test_url: str,
        get_redis: Redis,
        redis_test_url: str
) -> FastAPI:
    """
    create FastApi test application with initialized database
    :param engine: async database engine instance
    :param database_test_url: db connection url
    :param get_redis: redis instance
    :param redis_test_url: redis connection instance
    :return: FastAPI wsgi application instance
    """
    from config import connection
    connection.DATABASE_URL = database_test_url
    connection.REDIS_URL = redis_test_url
    with mock.patch('sqlalchemy.ext.asyncio.create_async_engine') as create_eng:
        with mock.patch('aioredis.from_url') as create_redis:
            create_redis.return_value = get_redis
            create_eng.return_value = engine
            from main import app
            async with LifespanManager(app):
                yield app


@pytest.fixture()
async def get_client(get_app: FastAPI) -> AsyncClient:
    """
    create a custom async http client based on httpx AsyncClient
    :param: get_app: FastAPI wsgi application instance
    :return: httpx async client
    """
    async with AsyncClient(app=get_app, base_url="http://testserver") as client:
        yield client


@pytest.fixture(scope='session')
async def add_some_user(engine: AsyncEngine) -> User:
    """
    add test user to database and return it
    :param engine: async database engine is used for db connection session
    :return: a model.User instance
    """
    async_session = sessionmaker(engine, expire_on_commit=False, autoflush=False, class_=AsyncSession)

    user_db = User(email="myuserwithid@example.com", password="password", is_active=True)
    async with async_session(bind=engine) as session:
        # add user
        session.add(user_db)
        await session.commit()
        await session.refresh(user_db)

    return user_db


@pytest.fixture(scope='session')
def event_loop():
    """
    Redefinition of base pytest-asyncio event_loop fixture,
    which returns the same value but with scope session
    """
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()

    yield loop
    loop.close()
