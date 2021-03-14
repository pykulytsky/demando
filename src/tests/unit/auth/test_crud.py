from auth import crud

from auth.schemas import UserLogin, User


def test_get_user(user, db):
    assert crud.get_user(db, user.id) == user


def test_get_user_by_email(user, db):
    assert crud.get_user_by_email(db, user.email) == user


def test_login(user, db):
    user_login = UserLogin(email=user.email, password='1234')
    assert crud.login(db, user_login) == user


def test_delete_user(user, db):
    _user = User(id=user.id, email=user.email, username=user.username)
    crud.delete_user(db, _user)

    assert crud.get_user(db, user.id) is None


def get_users(user, another_user, db):
    assert len(crud.get_users(db)) == 2


def test_user_or_false(db, user):
    _user = User(id=user.id, email=user.email, username=user.username)
    crud.delete_user(db, _user)

    assert crud.get_user_or_false(db, user.id) is False
