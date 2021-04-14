from tortoise.validators import Validator
from tortoise.exceptions import ValidationError

import httpx
from base import settings


class EmailValidator(Validator):

    def __call__(self, email: str):
        if not settings.DEBUG:
            resp = httpx.get(
                settings.MAILBOXLAYER_API_KEY + \
                f'?access_key={settings.MAILBOXLAYER_API_KEY}' + \
                f'&email={email}&smtp=1&format=1'
            )

            if resp.status_code != 200:
                raise ValidationError(f'[{resp.status_code}] {resp.text}')

            data = resp.json()

            if data['format_valid']:
                if not data['mx_found'] or not data['smtp_check']:
                    raise ValidationError(f"Email [{email}] not valid.")
                raise ValidationError("Invalid email format")
