import uuid

import pytest
from schemas import UserCreate

@pytest.mark.asyncio
async def test_get_user_by_id(get_client, add_some_user):

    res = await get_client.get(f'/users/{add_some_user.id}')
    assert res.status_code == 200
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
    assert res.status_code == 404


@pytest.mark.asyncio
async def test_post_user_create(get_client):
    random_email = f'{uuid.uuid4().hex}@example.com'
    user = UserCreate(email=random_email, password='password')
    res = await get_client.post('/users/', content=user.json())
    assert res.status_code == 201
