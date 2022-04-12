import json

import pytest


def test_client_receives_poll_data_after_connect(client, poll):
    with client.websocket_connect(f"/ws/vote/{poll.pk}") as websocket:
        data = websocket.receive_json()
        assert data["pk"] == poll.pk


@pytest.mark.xfail(strict=True)
def test_vote_without_a12n(client, poll, option):
    with client.websocket_connect(f"/ws/vote/{poll.pk}") as websocket:
        data = websocket.receive_json()
        assert data["pk"] == poll.pk
        websocket.send_json(
            json.dumps(
                {"poll_id": poll.pk, "option_id": option.pk},
            )
        )
