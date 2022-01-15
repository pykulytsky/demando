from mailjet_rest import Client
import os
api_key = 'bb633c949705340d6cff042ffe8fe3b6'
api_secret = '316967d68a1c03efd6bcbf9134ec2871'

def send(username, verification_link, email):
    mailjet = Client(auth=(api_key, api_secret), version='v3.1')
    data = {
        'Messages': [
            {
                "From": {
                    "Email": "pykulytsky@gmail.com",
                    "Name": "Oleh"
                },
                "To": [
                    {
                        "Email": email,
                        "Name": username
                    }
                ],
                "Subject": "Thank you for joining Demando!",
                "TextPart": "",
                "HTMLPart": f'<h3>Hello dear {username}, welcome to Demando! </h3><br /><h4>In order to fully use our service, you need to confirm your mail.</h4><br />To do this, just follow the link below:<br /><a href="{verification_link}">Verify your email</a>',
                "CustomID": "AppGettingStartedTest"
            }
        ]
    }
    result = mailjet.send.create(data=data)
    print(result.status_code)
    print(result.json())
