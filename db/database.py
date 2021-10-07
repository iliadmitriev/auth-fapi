from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from config import DATABASE_URL


async def app_init_db(app: FastAPI):
    engine = create_async_engine(url=DATABASE_URL, echo=False, pool_size=50, pool_pre_ping=True)
    async_session = sessionmaker(engine, expire_on_commit=False, autoflush=False, class_=AsyncSession)
    session = async_session(bind=engine)
    app.state.db = session


async def app_dispose_db(app: FastAPI):
    session = app.state.db
    await session.close()
