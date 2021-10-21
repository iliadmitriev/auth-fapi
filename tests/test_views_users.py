import uuid

import pytest
from starlette import status

from schemas import UserCreate, UserUpdate
from utils.password import password_hash_ctx


@pytest.mark.asyncio
async def test_get_users_list(get_client, get_app, add_some_user):
    res = await get_client.get(get_app.url_path_for('users:get'))
    data = res.json()
    assert res.status_code == status.HTTP_200_OK
    user = next(item for item in data if item["id"] == add_some_user.id)
    assert user.get('id') == add_some_user.id
    assert user.get('email') == add_some_user.email
    assert user.get('is_active') == add_some_user.is_active
    assert user.get('confirmed') == add_some_user.confirmed
    assert user.get('is_superuser') == add_some_user.is_superuser


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
async def test_get_user_by_id_not_exists(get_client, add_some_user, get_app):
    res = await get_client.get(get_app.url_path_for('users:get-by-id', user_id=9999))
    assert res.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_post_user_create_201_created(get_client, get_app):
    random_email = f'{uuid.uuid4().hex}@example.com'
    user = UserCreate(email=random_email, password='password')
    user_created = await create_new_user(get_app, get_client, user)
    assert not user_created.get('is_superuser')
    return user_created


async def create_new_user(get_app, get_client, user) -> dict:
    """
    Creates a new user using API post method

    :param get_app: application instance, which is used to get path for user creation url
    :param get_client: AsyncClient instance is performing http request
    :param user: user to be posted to API method
    :return: dict created user
    """
    res = await get_client.post(get_app.url_path_for('users:post'), content=user.json())
    assert res.status_code == status.HTTP_201_CREATED
    assert not res.json().get('confirmed')
    assert res.json().get('is_active')
    assert res.json().get('email') == user.email
    assert password_hash_ctx.verify(user.password, res.json().get('password'))
    assert 'created' in res.json()
    assert 'last_login' in res.json()
    return res.json()


@pytest.mark.asyncio
async def test_post_user_create_400_bad_request(get_client, get_app, add_some_user):
    random_email = f'myuserwithid@example.com'
    user = UserCreate(email=random_email, password='password')
    res = await get_client.post(get_app.url_path_for('users:post'), content=user.json())
    assert res.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio
@pytest.mark.parametrize('data', [
    {
        'confirmed': True,
        'is_active': False,
        'password': 'new_password',
        'is_superuser': True,
        'email': f'{uuid.uuid4().hex}@example.com'
    },
    {
        'confirmed': True,
        'is_active': False,
        'is_superuser': True,
    }
])
async def test_put_user_update_200_ok(get_client, get_app, data):
    user = await test_post_user_create_201_created(get_client, get_app)
    new_user = UserUpdate(**data)
    res = await get_client.put(get_app.url_path_for('users:put', user_id=user['id']), content=new_user.json())
    assert res.status_code == status.HTTP_200_OK
    assert res.json().get('confirmed') == data.get('confirmed')
    assert res.json().get('is_active') == data.get('is_active')
    assert res.json().get('is_superuser') == data.get('is_superuser')
    assert res.json().get('id') == user['id']
    assert res.json().get('email') == (data.get('email') or user['email'])
    if not data.get('password') is None:
        assert password_hash_ctx.verify(
            data.get('password'),
            res.json().get('password')
        )
    assert 'created' in res.json()
    assert 'last_login' in res.json()


@pytest.mark.asyncio
async def test_put_user_update_404_not_found(get_client, get_app):
    user = await test_post_user_create_201_created(get_client, get_app)
    new_user = UserUpdate(**user)
    res = await get_client.put(get_app.url_path_for('users:put', user_id=9999), content=new_user.json())
    assert res.status_code == status.HTTP_404_NOT_FOUND
    assert res.json() == {'detail': f"User with id '9999' not found"}


@pytest.mark.asyncio
@pytest.mark.parametrize('data', [
    {
        'email': f'{uuid.uuid4().hex}@example.com'
    },
    {
        'confirmed': True,
    },
    {
        'password': 'absolutely_new_pass',
    },
])
async def test_patch_user_update_200_ok(get_client, get_app, data):
    user = await test_post_user_create_201_created(get_client, get_app)
    new_user = UserUpdate(**data)
    res = await get_client.patch(
        get_app.url_path_for('users:patch', user_id=user['id']),
        content=new_user.json(exclude_defaults=True, exclude_unset=True)
    )
    assert res.status_code == status.HTTP_200_OK
    assert res.json().get('id') == user['id']
    assert res.json().get('confirmed') == (data.get('confirmed') or user['confirmed'])
    assert res.json().get('is_active') == (data.get('is_active') or user['is_active'])
    assert res.json().get('is_superuser') == (data.get('is_superuser') or user['is_superuser'])
    if not data.get('password') is None:
        assert password_hash_ctx.verify(
            data.get('password'),
            res.json().get('password')
        )
    assert res.json().get('email') == (data.get('email') or user['email'])
    assert 'last_login' in res.json()
    assert 'created' in res.json()


@pytest.mark.asyncio
async def test_patch_user_update_404_not_found(get_client, get_app):
    user = await test_post_user_create_201_created(get_client, get_app)
    new_user = UserUpdate(**user)
    res = await get_client.patch(get_app.url_path_for('users:patch', user_id=9999), content=new_user.json())
    assert res.status_code == status.HTTP_404_NOT_FOUND
    assert res.json() == {'detail': f"User with id '9999' not found"}


@pytest.mark.asyncio
async def test_delete_user_200_ok(get_client, get_app):
    user = await test_post_user_create_201_created(get_client, get_app)
    res = await get_client.delete(
        get_app.url_path_for('users:delete', user_id=user['id']),
    )
    assert res.status_code == status.HTTP_200_OK
    assert res.json().get('id') == user['id']
    assert res.json().get('confirmed') == user['confirmed']
    assert res.json().get('is_active') == user['is_active']
    assert res.json().get('is_superuser') == user['is_superuser']
    assert res.json().get('password') == user['password']
    assert res.json().get('email') == user['email']
    assert 'last_login' in res.json()
    assert 'created' in res.json()


@pytest.mark.asyncio
async def test_delete_user_404_not_found(get_client, get_app):
    res = await get_client.delete(get_app.url_path_for('users:patch', user_id=9999))
    assert res.status_code == status.HTTP_404_NOT_FOUND
    assert res.json() == {'detail': f"User with id '9999' not found"}
