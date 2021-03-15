import pytest


@pytest.mark.bug('Fix validation')
def test_get_event(client, event):
    response = client.get(f'/qa/events/{event.pk}')

    assert response.status_code == 200
    assert response.json()['name'] == event.name
