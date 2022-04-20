from sqlalchemy.dialects import postgresql

from quiz.types import QuizEnterCode


def test_enter_code_returns_string():
    code = QuizEnterCode()

    assert isinstance(code.process_result_value(None, postgresql), str)


def test_enter_code_generates_unique_code():
    code = QuizEnterCode().process_result_value(None, postgresql)

    assert len(code) == 4
    assert isinstance(int(code), int)
    assert int(code) > 999
