import pytest

from auth.backend import JWTAuthentication


@pytest.fixture
def auth_request(user, auth_client):
    response = auth_client.get(f"/auth/users/{user.pk}")
    return response.request


@pytest.mark.asyncio
async def test_backend_works(auth_request, db):

    backend = JWTAuthentication()
    result = await backend(auth_request, db=db)

    assert isinstance(result, str)


@pytest.mark.asyncio
async def test_backend_verify_token(auth_request, mocker, db):
    mocker.patch("auth.backend.JWTAuthentication._verify_jwt_token")
    backend = JWTAuthentication()
    result = await backend(auth_request, db=db)

    backend._verify_jwt_token.assert_called_once_with(result)
