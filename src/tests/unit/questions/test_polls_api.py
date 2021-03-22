def test_get_polls(client):
    response = client.get('/qa/polls/')

    assert response.status_code == 200


def test_get_poll(client, poll):
    response = client.get(f'/qa/polls/{poll.pk}')

    assert response.status_code == 200
    assert response.json()['name'] == poll.name


def test_create_poll(auth_client, user):
    response = auth_client.post('/qa/polls/', json={
        'name': 'test poll'
    })

    assert response.status_code == 201
    assert response.json()['owner']['pk'] == user.pk
