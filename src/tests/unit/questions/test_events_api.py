import pytest


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


def test_get_events_by_user(client, event, user):
    response = client.get(f'/qa/events/user/{user.pk}')

    assert response.status_code == 200
    assert response.json()[0]['name'] == event.name


def test_get_my_events(auth_client, event):
    response = auth_client.get('/qa/events/my/')

    assert response.status_code == 200
    assert response.json()[0]['name'] == event.name


def test_create_event_not_allowed_by_anon(client):
    response = client.post('/qa/events/', json={'name': 'don`t matter'})

    assert response.status_code == 403


def test_create_event(auth_client):
    response = auth_client.post('/qa/events/', json={
        'name': 'why i am so good?',
    })

    assert response.status_code == 201


@pytest.mark.xfail(strict=True)
def test_patch(client, event):
    response = client.patch(
        f'/qa/events/{event.pk}',
        json={
            'name': "Changed"
        }
    )

    assert response.status_code == 200
    assert event.name == 'Changed'
