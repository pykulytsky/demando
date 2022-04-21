import pytest
from fastapi import WebSocket
from starlette.types import Message


class TestWebcocket(WebSocket):
    async def receive(self) -> Message:
        return "CONNECTED"

    async def send(self, message: Message) -> None:
        return "SENDED"


@pytest.fixture
def websocket():
    return TestWebcocket({"type": "websocket"}, None, None)
