import pytest
from pydantic import ValidationError

from schemas import UserBase, UserCreate, UserDB, UserUpdate


def test_user_base():
    user = UserBase(email="test@example.com")
    assert user.email == "test@example.com"
    assert user.is_active
    assert not user.is_superuser
    assert not user.confirmed
    assert user.dict(exclude_unset=True) == {"email": "test@example.com"}
    assert user.dict() == {
        "email": "test@example.com",
        "is_active": True,
        "is_superuser": False,
        "confirmed": False,
    }


def test_user_base_email_empty():
    user = UserBase()
    assert user.email is None
    assert user.dict(exclude_unset=True) == {}
    assert user.dict() == {
        "email": None,
        "is_active": True,
        "is_superuser": False,
        "confirmed": False,
    }


def test_user_base_email_not_valid():
    with pytest.raises(ValidationError):
        UserBase(email="not_valid_email")


def test_user_create():
    user = UserCreate(email="test@example.com", password="password")
    assert user.email == "test@example.com"
    assert user.password == "password"
    assert user.is_active
    assert not user.is_superuser
    assert not user.confirmed


def test_user_create_password_empty():
    with pytest.raises(ValidationError):
        UserCreate(user="test@example.com")


def test_user_update():
    user = UserUpdate(email="test@example.com")
    assert user.email == "test@example.com"
    assert user.password is None
    assert user.is_active
    assert not user.is_superuser
    assert not user.confirmed


def test_user_update_with_password():
    user = UserUpdate(email="test@example.com", password="password")
    assert user.email == "test@example.com"
    assert user.password == "password"
    assert user.is_active
    assert not user.is_superuser
    assert not user.confirmed


def test_user_db():
    user = UserDB(email="test@example.com", password="secret")
    assert user.email == "test@example.com"
    assert user.password == "secret"
    assert user.is_active
    assert not user.is_superuser
    assert not user.confirmed
    assert user.id is None
    assert user.last_login is None
    assert user.created is None
