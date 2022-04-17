from uuid import uuid4

from base import settings
from base.integrations.mailjet import MailService


def test_mail_was_sent(mocker):
    settings.SEND_VERIFICATION_MAIL = True
    mocker.patch("base.integrations.mailjet.MailService.send")
    service = MailService()

    service.send_verification_mail("test", uuid4(), "test@test.com")

    service.send.assert_called_once()

    settings.SEND_VERIFICATION_MAIL = False


def test_mail_was_send_and_response_ok(mocker):
    settings.SEND_VERIFICATION_MAIL = True
    mocker.patch("base.integrations.mailjet.MailService.send")
    service = MailService()
    code = uuid4()

    service.send_verification_mail("test", code, "test@test.com")

    service.send.assert_called_once_with(
        {
            "To": [{"Email": "test@test.com", "Name": "test"}],
            "Subject": "Thank you for joining our service!",
            "HTMLPart": f'<h3>Hello dear test, welcome to our service! </h3><br /><h4>In order to fully use our service, you need to confirm your mail.</h4><br />To do this, just follow the link below:<br /><a href="http://localhost:8080/verify/{code}">Verify your email</a>',  # noqa
            "CustomID": "AppGettingStartedTest",
        }
    )

    settings.SEND_VERIFICATION_MAIL = False
