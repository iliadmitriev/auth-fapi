from fastapi import APIRouter, HTTPException
from sqlalchemy.future import select
from starlette import status
from starlette.requests import Request

from models import User
from schemas import Register, UserCreate
from schemas.users import UserOut
from utils.password import password_hash_ctx


router = APIRouter()


@router.post(
    '/login/register/',
    name="login:register",
    summary="Register a new user",
    status_code=status.HTTP_200_OK,
    description="Registers new user",
    response_model=UserOut
)
async def login_register(register: Register, request: Request):
    db = request.app.state.db
    res = await db.execute(select(User).filter(User.email == register.email))
    found_users = res.scalar_one_or_none()
    if found_users:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with email '{register.email}' already exists"
        )
    user = UserCreate.parse_obj(register)
    user.password = password_hash_ctx.hash(register.password)
    user_db = User(**user.dict())
    db.add(user_db)
    await db.commit()
    await db.refresh(user_db)
    return user_db
