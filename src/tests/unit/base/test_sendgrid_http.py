from base.integrations.sendgrid.http import SendgridHTTP
from base.integrations.sendgrid.exceptions import SendgridAuthenticationFailed, SendgridWrongResponse
import pytest


@pytest.mark.asyncio
async def test_http_works():
    async with SendgridHTTP() as http:
        resp = await http.get('user/profile')
        assert resp.status_code == 200


@pytest.mark.asyncio
async def test_http_wrong_response():
    async with SendgridHTTP() as http:
        with pytest.raises(SendgridWrongResponse):
            await http.get('bla-bla')


@pytest.mark.asyncio
async def test_http_wrong_credentials():
    async with SendgridHTTP(token='bla-bla') as http:
        with pytest.raises(SendgridAuthenticationFailed):
            await http.post('mail/send')


@pytest.mark.asyncio
async def test_http_send_email():
    async with SendgridHTTP() as http:
        resp = await http.post('mail/send', json={
            "personalizations": [{
                "to": [{'email': 'stepan.bandera@example.com', 'name': 'Oleh'}],
                "dynamic_template_data": {
                    'first_name': 'Oleh',
                    'verification_link': 'http://loalhost:8080/verify/123121wefdsfdgd'
                },
                "subject": "Test message",
            }],
            "template_id": 'd-c0dc70b630b54c1d8214de6dc02d8d38',
            "from": {
                "email": 'pragmatic.once.lviv@gmail.com',
                "name": "Oleh Pykulytsky"
            }
        }
        )

        assert resp.status_code == 202
