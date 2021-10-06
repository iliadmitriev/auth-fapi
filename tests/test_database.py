import pytest
from unittest import mock


@pytest.mark.asyncio
async def test_database_get_db(engine):
    with mock.patch('sqlalchemy.ext.asyncio.create_async_engine') as create_eng:
        create_eng.return_value = engine
        from db.database import get_db
        res = await get_db()
    create_eng.assert_called_once()
