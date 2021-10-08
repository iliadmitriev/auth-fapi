import importlib
import os
from unittest import mock


def test_import_config():
    with mock.patch.dict(os.environ, {
        'DATABASE_NAME': 'database',
        'DATABASE_USER': 'user',
        'DATABASE_PASSWORD': 'pass',
        'DATABASE_HOST': 'host',
        'DATABASE_PORT': '5432',
        'DATABASE_DRIVER': 'postgresql+asyncpg'
    }):
        from config import db
        importlib.reload(db)
        assert db.DATABASE_NAME == 'database'
        assert db.DATABASE_USER == 'user'
        assert db.DATABASE_PASSWORD == 'pass'
        assert db.DATABASE_HOST == 'host'
        assert db.DATABASE_PORT == '5432'
        assert db.DATABASE_DRIVER == 'postgresql+asyncpg'


def test_db_url():
    with mock.patch.dict(os.environ, {
        'DATABASE_NAME': 'database',
        'DATABASE_USER': 'user',
        'DATABASE_PASSWORD': 'pass',
        'DATABASE_HOST': 'host',
        'DATABASE_PORT': '5432',
        'DATABASE_DRIVER': 'postgresql+asyncpg'
    }):
        from config import db
        importlib.reload(db)
        assert db.DATABASE_URL == 'postgresql+asyncpg://user:pass@host:5432/database'
