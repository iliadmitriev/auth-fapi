from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from db import Base


class User(Base):
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    email = Column('email', String(100), nullable=False, index=True, unique=True)
    password = Column('password', String(200))
    is_active = Column('is_active', Boolean(), default=False)
    is_superuser = Column('is_superuser', Boolean(), default=False)
    created = Column('created', DateTime(timezone=True), server_default=func.now())
    last_login = Column('last_login', DateTime(timezone=True))
    confirmed = Column('confirmed', Boolean, default=False)
