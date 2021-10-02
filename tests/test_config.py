import os


def test_import_config():
    os.environ["DATABASE_NAME"] = 'database'
    os.environ["DATABASE_USER"] = 'user'
    os.environ["DATABASE_PASSWORD"] = 'pass'
    os.environ["DATABASE_HOST"] = 'host'
    os.environ["DATABASE_PORT"] = '5432'
    os.environ["DATABASE_DRIVER"] = 'postgresql+asyncpg'
    import config
    assert config.DATABASE_NAME == 'database'
    assert config.DATABASE_USER == 'user'
    assert config.DATABASE_PASSWORD == 'pass'
    assert config.DATABASE_HOST == 'host'
    assert config.DATABASE_PORT == '5432'
    assert config.DATABASE_DRIVER == 'postgresql+asyncpg'


def test_db_url():
    os.environ["DATABASE_NAME"] = 'database'
    os.environ["DATABASE_USER"] = 'user'
    os.environ["DATABASE_PASSWORD"] = 'pass'
    os.environ["DATABASE_HOST"] = 'host'
    os.environ["DATABASE_PORT"] = '5432'
    os.environ["DATABASE_DRIVER"] = 'postgresql+asyncpg'
    import config
    assert config.DATABASE_URL == 'postgresql+asyncpg://user:pass@host:5432/database'
