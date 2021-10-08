from fastapi import APIRouter, HTTPException
from sqlalchemy.future import select
from starlette import status
from starlette.requests import Request

from models.users import User
from schemas.users import UserCreate, UserDB

router = APIRouter()


@router.post(
    '/users/',
    name="users:post",
    summary="create a new user",
    status_code=status.HTTP_201_CREATED,
    description="Creates a new user with post query",
    response_model=UserDB
)
async def user_post(user: UserCreate, request: Request):
    db = request.app.state.db
    res = await db.execute(select(User).filter(User.email == user.email))
    found_users = res.scalar_one_or_none()
    if found_users:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with email '{user.email}' already exists"
        )
    user_db = User(**user.dict())  # type: ignore
    db.add(user_db)
    await db.commit()
    await db.refresh(user_db)
    return user_db


@router.get(
    '/users/{user_id}',
    name="users:get-by-id",
    summary="get user by id",
    response_model=UserDB
)
async def user_get(user_id: int, request: Request):
    res = await request.app.state.db.execute(select(User).filter(User.id == user_id))
    db_user = res.scalar()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user
