import pytest
import sys
import os

from main import app

from fastapi.testclient import TestClient

from mixer.backend.sqlalchemy import mixer as _mixer


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def mixer():
    return _mixer


def user(mixer):
    return mixer.blend('auth.models.User')
