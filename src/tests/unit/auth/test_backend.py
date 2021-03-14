from auth.backend import JWTAuthentication
import pytest


@pytest.fixture
def auth_request(user, auth_client):
    response = auth_client.get(f'/auth/users/{user.id}')
    return response.request


@pytest.mark.asyncio
async def test_backend_works(auth_request):

    backend = JWTAuthentication()
    result = await backend(auth_request)

    assert isinstance(result, str)
