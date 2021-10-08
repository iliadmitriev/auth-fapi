from typing import Optional
from datetime import datetime

from pydantic import BaseModel, EmailStr


# base shared properties
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False
    confirmed: bool = False


# user create query
class UserCreate(UserBase):
    email: EmailStr
    password: str


# update user query
class UserUpdate(UserBase):
    password: Optional[str] = None


# output user
class UserOut(UserBase):
    id: Optional[int] = None
    created: Optional[datetime] = None
    last_login: Optional[datetime] = None


# user attributes stored in db
class UserDB(UserBase):
    id: Optional[int] = None
    password: str
    created: Optional[datetime] = None
    last_login: Optional[datetime] = None

    class Config:
        orm_mode = True

