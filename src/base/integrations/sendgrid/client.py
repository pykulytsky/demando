from auth.models import User
from base.database import get_db
from .http import SendgridHTTP
from fastapi import Depends
from base import settings

from .receiver import Receiver
from .mail import SendgridMail

from httpx import Response


class SendgridApp():
    def __init__(
        self,
        db: Depends(get_db),
        token: str = settings.SENDGRID_API_KEY
    ) -> None:
        self.http = SendgridHTTP(token=token)
        self.db = db

    async def send(self, mail: SendgridMail) -> Response:
        async with self.http as http:
            return await http.post('mail/send', json=mail.to_json())

    async def _send_email(
        self,
        user_pk: int,
        template_id: int,
        subject: str,
        dynamic_template_data: dict
    ):
        _user = User.manager(self.db).get(pk=user_pk)
        receiver = Receiver.from_user_model(_user)
        mail = SendgridMail(
            template_id=template_id,
            receiver=receiver,
            subject=subject,
            dynamic_template_data=dynamic_template_data
        )

        resp = await self.send(mail)

        if resp.status_code == 202:
            return True

        return False

    async def send_verification_mail(
        self,
        user_pk: int
    ):
        _user = User.manager(self.db).get(pk=user_pk)

        template_id = settings.SENDGRID_VERIFY_EMAIL_TEMPLATE_ID
        subject = 'Please verify your account'
        dynamic_template_data = {
            'first_name': _user.first_name,
            'verification_link': f'http://localhost:8000/verify/{_user.verification_code}'# noqa
        }

        return await self._send_email(
            user_pk,
            template_id,
            subject,
            dynamic_template_data
        )
