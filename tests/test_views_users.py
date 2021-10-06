import uuid

import pytest
from starlette import status

from schemas import UserCreate


@pytest.mark.asyncio
async def test_get_user_by_id(get_client, add_some_user, get_app):
    res = await get_client.get(get_app.url_path_for('users:get-by-id', user_id=add_some_user.id))
    assert res.status_code == status.HTTP_200_OK
    assert {
               'confirmed': False,
               'email': 'myuserwithid@example.com',
               'id': add_some_user.id,
               'is_active': True,
               'password': 'password'
           }.items() <= res.json().items()


@pytest.mark.asyncio
async def test_get_user_by_id_not_exists(get_client, add_some_user):
    res = await get_client.get('/users/9999')
    assert res.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_post_user_create(get_client, get_app):
    random_email = f'{uuid.uuid4().hex}@example.com'
    user = UserCreate(email=random_email, password='password')
    res = await get_client.post(get_app.url_path_for('users:post'), content=user.json())
    assert res.status_code == status.HTTP_201_CREATED
