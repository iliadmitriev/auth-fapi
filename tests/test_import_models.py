from models import Base


def test_import_models_user():
    from models.users import User
    assert issubclass(User, Base)
