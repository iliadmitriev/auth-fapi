import asyncio
import pathlib
import sys
from unittest import mock

import pytest
from alembic.config import Config
from alembic.operations import Operations
from alembic.runtime.environment import EnvironmentContext
from alembic.script import ScriptDirectory
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from asgi_lifespan import LifespanManager

from models import Base, User
from schemas.items import Item

BASE_PATH = pathlib.Path(__file__).parent.parent
sys.path.append(BASE_PATH)  # type: ignore


@pytest.fixture
def item():
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


async def async_migrate(engine, alembic_env):
    async with engine.begin() as conn:
        await conn.run_sync(do_run_migrations, alembic_env)


async def migrate(engine, url):
    alembic_cfg = Config()
    alembic_cfg.set_main_option("script_location", "alembic")
    alembic_cfg.set_main_option("url", url)
    alembic_script = ScriptDirectory.from_config(alembic_cfg)
    alembic_env = EnvironmentContext(alembic_cfg, alembic_script)

    await async_migrate(engine, alembic_env)


async def disconnect(engine):
    await engine.dispose()


@pytest.fixture(scope='session')
def database_test_url():
    """
    generate in memory sqlite db connect url for test purposes
    """
    return "sqlite+aiosqlite://?cache=shared"  # noqa


@pytest.fixture(scope='session')
async def engine(database_test_url):
    """
    create async sqlalchemy engine and run alembic migrations
    """
    url = database_test_url
    engine = create_async_engine(url, echo=False)
    await migrate(engine, url)
    yield engine
    await engine.dispose()


@pytest.fixture(scope='session')
async def get_app(engine, database_test_url):
    """
    create FastApi test application with initialized database
    """
    from config import db
    db.DATABASE_URL = database_test_url
    with mock.patch('sqlalchemy.ext.asyncio.create_async_engine') as create_eng:
        create_eng.return_value = engine
        from main import app
        async with LifespanManager(app):
            yield app


@pytest.fixture()
async def get_client(get_app):
    """
    create a custom async http client based on httpx AsyncClient
    """
    async with AsyncClient(app=get_app, base_url="http://testserver") as client:
        yield client


@pytest.fixture(scope='session')
async def add_some_user(engine):
    """
    add test user to database and return it
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
    Create or get already created running default event loop for whole session
    """
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()

    yield loop
    loop.close()
