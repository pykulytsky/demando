import pytest

from quiz.webocket import quiz_manager
from tests.tests_websocket import TestWebcocket


@pytest.mark.asyncio
async def test_connect_to_room(quiz, user, db):
    websocket = TestWebcocket({"type": "websocket"}, None, None)
    await quiz_manager.connect_to_room(websocket, quiz.enter_code, user.token, db)

    assert len(quiz_manager.rooms) == 1
    assert quiz_manager.rooms[0].active_connections[0].member == user

    quiz_manager.disconnect_from_room(quiz.enter_code, websocket)


@pytest.mark.asyncio
async def test_disconnect_from_room(quiz, user, db):
    websocket = TestWebcocket({"type": "websocket"}, None, None)
    await quiz_manager.connect_to_room(websocket, quiz.enter_code, user.token, db)
    quiz_manager.disconnect_from_room(quiz.enter_code, websocket)

    assert quiz_manager.get_room(quiz.enter_code).active_connections == []


@pytest.mark.asyncio
async def test_many_connections(quiz, user, db):
    websocket = TestWebcocket({"type": "websocket"}, None, None)
    for _ in range(5):
        await quiz_manager.connect_to_room(websocket, quiz.enter_code, user.token, db)

    assert len(quiz_manager.get_room(quiz.enter_code).active_connections) == 5
