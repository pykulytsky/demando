from base import settings


def test_event_create_not_allowed(unverified_auth_client):
    response = unverified_auth_client.post(
        'qa/events/',
        json={
            'name': 'event by unverified user'
        }
    )

    assert response.status_code == 403


def test_event_create_by_verified_user(auth_client):
    response = auth_client.post(
        'qa/events/',
        json={
            'name': 'event by unverified user'
        }
    )

    assert response.status_code == 201


def test_create_question_is_always_allowed(unverified_auth_client, event):
    response = unverified_auth_client.post(
        '/qa/questions/',
        json={
            'body': 'Can i ask a question?',
            'event': event.pk
        }
    )

    assert response.status_code == 201


def test_allow_create_for_all(unverified_auth_client):
    settings.ALLOW_EVERYONE_CREATE_ITEMS = True

    response = unverified_auth_client.post(
        'qa/events/',
        json={
            'name': 'event by unverified user, but its allowed'
        }
    )

    assert response.status_code == 201
