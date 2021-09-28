import os


def test_import_config():
    os.environ["POSTGRES_DB"] = 'database'
    os.environ["POSTGRES_USER"] = 'user'
    os.environ["POSTGRES_PASSWORD"] = 'pass'
    os.environ["POSTGRES_HOST"] = 'host'
    os.environ["POSTGRES_PORT"] = '5432'
    import config
    assert config.POSTGRES_DB == 'database'
    assert config.POSTGRES_USER == 'user'
    assert config.POSTGRES_PASSWORD == 'pass'
    assert config.POSTGRES_HOST == 'host'
    assert config.POSTGRES_PORT == '5432'
