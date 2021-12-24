import pytest
from auth.schemas import UserLogin
from pydantic import ValidationError

pytestmark = [pytest.mark.django_db]


def test_refresh_token_with_no_enought_fields():
    with pytest.raises(ValidationError):
        UserLogin(password=1234)


def test_refresh_token_with_too_many_fields():
    with pytest.raises(ValidationError):
        UserLogin(username="test12", email="test12@example.com", password=1234)
