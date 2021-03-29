import pytest


@pytest.mark.asyncio
async def test_read_users_works(client, user):
    response = await client.get('/auth/users')

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_user_by_id(client, user):
    response = await client.get('/auth/users')

    assert response.status_code == 200
    assert response.json()[0]['email'] == user.email
    assert response.json()[0]['username'] == user.username


@pytest.mark.asyncio
async def test_protected_endpoint(auth_client, user):
    response = await auth_client.get(f'/auth/users/{user.pk}')

    assert response.status_code == 200
    assert response.json()['email'] == user.email
    assert response.json()['username'] == user.username


@pytest.mark.asyncio
async def test_login(client, user):
    response = await client.post('/auth/users/refresh/', json={
        'email': user.email,
        'password': '1234'
    })

    assert response.status_code == 200
    assert response.json()['token']


@pytest.mark.asyncio
async def test_create_user(client):
    response = await client.post('/auth/users/', json={
        'username': 'test',
        'email': 'test@py.com',
        'password': 'assword'
    })

    assert response.status_code == 201
    assert response.json()['token']


@pytest.mark.asyncio
async def test_get_me(auth_client):
    response = await auth_client.get('/auth/users/me/')

    assert response.status_code == 200
