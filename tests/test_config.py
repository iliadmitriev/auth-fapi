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
        import config
        assert config.DATABASE_NAME == 'database'
        assert config.DATABASE_USER == 'user'
        assert config.DATABASE_PASSWORD == 'pass'
        assert config.DATABASE_HOST == 'host'
        assert config.DATABASE_PORT == '5432'
        assert config.DATABASE_DRIVER == 'postgresql+asyncpg'


def test_db_url():
    with mock.patch.dict(os.environ, {
        'DATABASE_NAME': 'database',
        'DATABASE_USER': 'user',
        'DATABASE_PASSWORD': 'pass',
        'DATABASE_HOST': 'host',
        'DATABASE_PORT': '5432',
        'DATABASE_DRIVER': 'postgresql+asyncpg'
    }):
        import config
        assert config.DATABASE_URL == 'postgresql+asyncpg://user:pass@host:5432/database'
