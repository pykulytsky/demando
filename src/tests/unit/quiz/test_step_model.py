import pytest
from core.exceptions import ImproperlyConfigured
from quiz import models


def test_add_step(quiz, db):
    step = models.Step.manager(db).create(quiz=quiz, title="test")

    assert quiz.steps[0] == step


def test_add_and_finish_steps(quiz, db):
    for _ in range(10):
        models.Step.manager(db).create(quiz=quiz, title="test")

    assert len(quiz.steps) == 10

    for step in quiz.steps:
        step.done = True

    db.commit()
    db.refresh(quiz)

    assert all([step.done for step in quiz.steps])


def test_add_option(quiz, db):
    step = models.Step.manager(db).create(quiz=quiz, title="test")

    option = models.StepOption.manager(db).create(
        title="option",
        step=step,
        is_right=True
    )

    assert option.step == step
    assert len(step.options) == 1


def test_only_one_right_option(quiz, db):
    step = models.Step.manager(db).create(quiz=quiz, title="test")

    models.StepOption.manager(db).create(
        title="option",
        step=step,
        is_right=True
    )

    with pytest.raises(ImproperlyConfigured):
        models.StepOption.manager(db).create(
            title="second right option",
            step=step,
            is_right=True
        )
