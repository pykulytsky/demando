def test_get_events_empty(client):
    response = client.get('/qa/events/')

    assert response.status_code == 200
    assert response.json() == []


def test_get_events(client, event):
    response = client.get('/qa/events/')

    assert response.status_code == 200
    assert response.json()[0]['name'] == event.name
    assert response.json()[0]['owner']['username'] == event.owner.username


def test_get_event(client, event):
    response = client.get(f'/qa/events/{event.pk}')

    assert response.status_code == 200
    assert response.json()['name'] == event.name


def test_create_event(auth_client):
    response = auth_client.post('/qa/events/', json={
        'name': 'why i am so good?',
    })

    assert response.status_code == 201
