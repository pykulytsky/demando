import pytest


def test_read_users_works(client):
    response = client.get('/auth/users')

    assert response.status_code == 200
