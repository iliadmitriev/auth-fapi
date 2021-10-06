from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from config import DATABASE_URL

engine = create_async_engine(url=DATABASE_URL, echo=False, pool_size=50, pool_pre_ping=True)
async_session = sessionmaker(engine, expire_on_commit=False, autoflush=False, class_=AsyncSession)
session = async_session(bind=engine)


async def get_db():
    global session
    return session
