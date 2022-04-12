def test_create_user(user_schema, manager):
    manager.create_user(user_schema)

    assert manager.exists(username=user_schema.username)


def test_create_user_password(user_schema, manager):
    user = manager.create_user(user_schema)

    assert manager.verify_password("1488", user)
