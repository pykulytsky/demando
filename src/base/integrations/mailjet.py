from mailjet_rest import Client

from base import settings


def send(username, verification_link, email):

    if not settings.SEND_EMAILS:
        return

    mailjet = Client(
        auth=(settings.MAILJET_API_KEY, settings.MAILJET_SECRET), version="v3.1"
    )
    data = {
        "Messages": [
            {
                "From": {"Email": "pykulytsky@gmail.com", "Name": "Oleh"},
                "To": [{"Email": email, "Name": username}],
                "Subject": "Thank you for joining our service!",
                "TextPart": "",
                "HTMLPart": f'<h3>Hello dear {username}, welcome to our service! </h3><br /><h4>In order to fully use our service, you need to confirm your mail.</h4><br />To do this, just follow the link below:<br /><a href="{verification_link}">Verify your email</a>',  # noqa
                "CustomID": "AppGettingStartedTest",
            }
        ]
    }
    mailjet.send.create(data=data)


class MailService:
    def __init__(
        self,
        api_key: str = settings.MAILJET_API_KEY,
        secret: str = settings.MAILJET_SECRET,
    ) -> None:
        self.api_key = api_key
        self.secret = secret
        self.client = Client(auth=(api_key, secret), version="v3.1")

    def send_verification_mail(self, username, email_verification_code, email):
        if not settings.SEND_VERIFICATION_MAIL:
            return

        data = {
            "To": [{"Email": email, "Name": username}],
            "Subject": "Thank you for joining our service!",
            "HTMLPart": f'<h3>Hello dear {username}, welcome to our service! </h3><br /><h4>In order to fully use our service, you need to confirm your mail.</h4><br />To do this, just follow the link below:<br /><a href="http://localhost:8080/verify/{email_verification_code}">Verify your email</a>',  # noqa
            "CustomID": "AppGettingStartedTest",
        }

        return self.send(data)

    def send(self, data: dict):
        if not settings.SEND_EMAILS:
            return

        _data = {
            "Messages": [
                {
                    "From": {
                        "Email": settings.SENDER_EMAIL,
                        "Name": settings.SEND_VERIFICATION_MAIL,
                    },
                    **data,
                }
            ]
        }

        return self.client.send.create(data=_data)
