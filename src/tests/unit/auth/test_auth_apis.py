from pprint import pprint


def test_read_users_works(client, user):
    response = client.get('/auth/users')

    assert response.status_code == 200


def test_get_user_by_id(client, user):
    response = client.get('/auth/users')

    assert response.status_code == 200
    assert response.json()[0]['email'] == user.email
    assert response.json()[0]['username'] == user.username


def test_auth_endpoint(auth_client, user):
    response = auth_client.get(f'/auth/users/{user.id}')

    assert response.status_code == 200
    assert response.json()['email'] == user.email
    assert response.json()['username'] == user.username
