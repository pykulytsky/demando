import pytest

from core import settings
from core.integrations.sendgrid.client import SendgridApp


@pytest.mark.asyncio
async def test_client_send_email(db, user):

    client = SendgridApp(db=db)
    resp = await client._send_email(
        user_pk=user.pk,
        template_id=settings.SENDGRID_VERIFY_EMAIL_TEMPLATE_ID,
        dynamic_template_data={},
        subject="hello world",
    )

    assert resp
