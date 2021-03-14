def test_verify_password(user):
    assert user.verify_password('1234')
