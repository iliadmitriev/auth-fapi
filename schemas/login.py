from pydantic import BaseModel, EmailStr


class Register(BaseModel):
    email: EmailStr
    password: str


class Auth(Register):
    pass


class Token(BaseModel):
    access_token: str
    refresh_token: str

    class Config:
        orm_mode = True
