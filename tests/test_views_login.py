import uuid

import pytest
from sqlalchemy.future import select
from starlette import status

from models import User
from schemas import Register
from utils.password import password_hash_ctx


@pytest.mark.asyncio
async def test_login_register_success(get_client, get_app):
    email = f'{uuid.uuid4().hex}@example.com'
    password = uuid.uuid4().hex
    register = Register(email=email, password=password)
    res = await get_client.post(get_app.url_path_for('login:register'), content=register.json())
    assert res.status_code == status.HTTP_200_OK
    db = get_app.state.db
    res = await db.execute(select(User).filter(User.email == email))
    found_user = res.scalar_one_or_none()
    assert found_user
    assert password_hash_ctx.verify(password, found_user.password)


@pytest.mark.asyncio
async def test_login_register_fail_exists(get_client, get_app, add_some_user):
    register_exists = Register(email=add_some_user.email, password=uuid.uuid4().hex)
    res = await get_client.post(get_app.url_path_for('login:register'), content=register_exists.json())
    assert res.status_code == status.HTTP_400_BAD_REQUEST

