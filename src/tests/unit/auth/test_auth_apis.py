from base.integrations import mailjet


def test_read_users_works(client, user):
    response = client.get('/auth/users')

    assert response.status_code == 200


def test_get_user_by_id(client, user):
    response = client.get('/auth/users')

    assert response.status_code == 200
    assert response.json()[0]['email'] == user.email
    assert response.json()[0]['username'] == user.username


def test_protected_endpoint(auth_client, user):
    response = auth_client.get(f'/auth/users/{user.pk}')

    assert response.status_code == 200
    assert response.json()['email'] == user.email
    assert response.json()['username'] == user.username


def test_refresh_token_with_email(client, user):
    response = client.post('/auth/users/refresh/', json={
        'email': user.email,
        'password': '1234'
    })

    assert response.status_code == 200
    assert response.json()['token']


def test_refresh_token_with_username(client, user):
    response = client.post('/auth/users/refresh/', json={
        'username': user.username,
        'password': '1234'
    })

    assert response.status_code == 200
    assert response.json()['token']

def test_create_user(client):
    response = client.post('/auth/users/', json={
        'username': 'test',
        'email': 'test@py.com',
        'password': 'assword'
    })

    assert response.status_code == 201
    assert response.json()['token']


def test_get_me(auth_client):
    response = auth_client.get('/auth/users/me/')

    assert response.status_code == 200


def test_send_email_after_create_user(client, mocker):
    mocker.patch('base.integrations.mailjet.send')
    response = client.post('/auth/users/', json={
        'username': 'test',
        'email': 'test@py.com',
        'password': 'assword'
    })

    assert response.status_code == 201
    mailjet.send.assert_called_once()
