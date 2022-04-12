def test_verify_password(user, db):
    assert user.manager(db).verify_password("1234", user)
