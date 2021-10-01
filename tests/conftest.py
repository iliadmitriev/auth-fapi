import asyncio
import pathlib
import sys

from alembic.config import Config
from alembic.operations import Operations
from alembic.runtime.environment import EnvironmentContext
from alembic.script import ScriptDirectory
from sqlalchemy.ext.asyncio import create_async_engine

from models import Base

import pytest
from main import Item

BASE_PATH = pathlib.Path(__file__).parent.parent
sys.path.append(BASE_PATH)

TEST_DATABASE_URL = "sqlite+aiosqlite://?cache=shared"


@pytest.fixture
def item():
    return Item(name='Banana', price=2.99, tax=0.25, description='One pound of banana')


def do_upgrade(revision, context):
    alembic_script = context.script
    return alembic_script._upgrade_revs(alembic_script.get_heads(), revision)


def do_run_migrations(connection, alembic_env):
    alembic_env.configure(connection=connection, target_metadata=Base.metadata, fn=do_upgrade)
    migration_context = alembic_env.get_context()

    with migration_context.begin_transaction():
        with Operations.context(migration_context):
            migration_context.run_migrations()


async def async_migrate(engine, alembic_env):
    # migrate
    async with engine.begin() as conn:
        await conn.run_sync(do_run_migrations, alembic_env)


def migrate(engine, url):
    alembic_cfg = Config()
    alembic_cfg.set_main_option("script_location", "alembic")
    alembic_cfg.set_main_option("url", url)

    alembic_script = ScriptDirectory.from_config(alembic_cfg)
    alembic_env = EnvironmentContext(alembic_cfg, alembic_script)

    asyncio.run(async_migrate(engine, alembic_env))

    return engine.connect()


def drop_database(db_conn):
    pass


@pytest.fixture
def db_connection():
    url = TEST_DATABASE_URL
    engine = create_async_engine(url, echo=False)
    connection = migrate(engine, url)
    yield connection, engine
    drop_database(connection)
    