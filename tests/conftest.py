import pytest

from fastapi.testclient import TestClient
from app import app

from mixer.backend.sqlalchemy import mixer as _mixer


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def mixer():
    return _mixer


def user(mixer):
    return mixer.blend('auth.models.User')
