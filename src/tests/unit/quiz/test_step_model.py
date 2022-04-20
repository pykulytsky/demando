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
