from auth.backend import JWTAuthentication
import pytest


@pytest.fixture
def auth_request(user, auth_client):
    response = auth_client.get(f'/auth/users/{user.pk}')
    return response.request


@pytest.mark.asyncio
async def test_backend_works(auth_request):

    backend = JWTAuthentication()
    result = await backend(auth_request)

    assert isinstance(result, str)


@pytest.mark.asyncio
async def test_backend_verify_token(auth_request, mocker):
    mocker.patch('auth.backend.JWTAuthentication._verify_jwt_token')
    backend = JWTAuthentication()
    result = await backend(auth_request)

    backend._verify_jwt_token.assert_called_once_with(result)
