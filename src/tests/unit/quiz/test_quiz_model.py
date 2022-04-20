from quiz.models import Quiz


def test_quiz_enter_code(db, user):
    quiz = Quiz.manager(db).create(name="test quiz", owner=user)

    assert len(quiz.enter_code) == 4
    assert isinstance(quiz.enter_code, str)
    assert int(quiz.enter_code) > 999


def test_quiz_add_member(db, user, another_user):
    quiz = Quiz.manager(db).create(name="test quiz", owner=user)
    quiz.members = [another_user]
    db.commit()
    db.refresh(quiz)

    assert len(quiz.members) == 1
    assert quiz.members[0] == another_user


def test_quiz_remove_member(db, user, another_user):
    quiz = Quiz.manager(db).create(name="test quiz", owner=user)
    quiz.members = [another_user]
    db.commit()
    db.refresh(quiz)

    assert len(quiz.members) == 1

    quiz.members.remove(another_user)
    db.commit()
    db.refresh(quiz)

    assert quiz.members == []
