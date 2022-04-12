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
