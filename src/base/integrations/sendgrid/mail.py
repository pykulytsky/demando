from dataclasses import dataclass
from typing import List, Union

from base import settings
from base.integrations.sendgrid.receiver import Receiver


@dataclass
class SendgridMail:
    """Class for easy conversion of email data to json."""

    template_id: str
    receiver: Union[Receiver, List[Receiver]]
    subject: str
    dynamic_template_data: dict
    sender_email: str = settings.EMAIL_HOST_USER
    sender_name: str = settings.EMAIL_HOST_USER_NAME

    def to_json(self):
        data = {
            "personalizations": [
                {
                    "to": [self.receiver.to_json()]
                    if isinstance(self.receiver, Receiver)
                    else [user.to_json for user in self.receiver],
                    "dynamic_template_data": self.dynamic_template_data,
                    "subject": self.subject,
                }
            ],
            "template_id": self.template_id,
            "from": {"email": self.sender_email, "name": self.sender_email},
        }

        return data
