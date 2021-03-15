from auth import crud

from auth.schemas import UserLogin


def test_get_user(user, db):
    assert crud.get_user(db, user.pk) == user


def test_get_user_by_email(user, db):
    assert crud.get_user_by_email(db, user.email) == user


def test_login(user, db):
    user_login = UserLogin(email=user.email, password='1234')
    assert crud.login(db, user_login) == user
