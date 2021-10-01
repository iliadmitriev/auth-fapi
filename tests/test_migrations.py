import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker

from models import User


@pytest.mark.asyncio
async def test_migrations_run(db_connection):
    connection, engine = db_connection
    async_session = sessionmaker(engine, expire_on_commit=False, autoflush=False, class_=AsyncSession)

    conn = await connection
    user_db = User(email="user@example.com", password="password", is_active=True)
    async with async_session(bind=engine) as session:
        # add user
        session.add(user_db)
        await session.commit()
        await session.refresh(user_db)
        assert user_db.id == 1

        query = select(User).where(User.email == "user@example.com")
        res = await conn.execute(query)

        user = res.fetchone()

        assert user.id == 1


