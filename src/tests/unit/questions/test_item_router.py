import pytest

from auth.models import User
from questions.models import Event, Question
from questions.router import ItemRouter
from questions.schemas import questions


@pytest.fixture
def item_router():
    return ItemRouter(
        model=Question,
        get_schema=questions.Question,
        create_schema=questions.QuestionCreateTest,
        update_schema=questions.QuestionPatch,
        prefix="/test",
    )


def test_get_schemas_diff(item_router: ItemRouter):
    assert len(item_router._get_schemas_diff()) == 2
    assert "event" in item_router._get_schemas_diff()
    assert "author" in item_router._get_schemas_diff()


def test_get_schemas_diff_models(item_router: ItemRouter):
    models = item_router._get_schema_diff_models()

    assert [Event, User] == models


def test_get_schemas_diff_models_exclude_user(item_router: ItemRouter):
    models = item_router._get_schema_diff_models_exclude_user()

    assert [Event] == models
