from auth import crud

from auth.schemas import UserLogin, User


def test_get_user(user, db):
    assert crud.get_user(db, user.pk) == user


def test_get_user_by_email(user, db):
    assert crud.get_user_by_email(db, user.email) == user


def test_delete_user(user, db):
    _user = User(pk=user.pk, email=user.email, username=user.username)
    crud.delete_user(db, _user)

    assert crud.get_user(db, user.pk) is None


def get_users(user, another_user, db):
    assert len(crud.get_users(db)) == 2


def test_user_or_false(db, user):
    _user = User(pk=user.pk, email=user.email, username=user.username)
    crud.delete_user(db, _user)

    assert crud.get_user_or_false(db, user.pk) is False
