from auth import crud


def test_get_user(user, db):
    assert crud.get_user(db, user.id) == user


def test_get_user_by_email(user, db):
    assert crud.get_user_by_email(db, user.email) == user


def test_login(user, db):
    assert crud.
