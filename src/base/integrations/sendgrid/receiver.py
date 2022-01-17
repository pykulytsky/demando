from dataclasses import dataclass

from auth.models import User


@dataclass
class Receiver():
    """Class implements the user model for the service Sendgrid."""
    first_name: str
    last_name: str
    email: str

    @classmethod
    def from_user_model(cls, user: User):
        return cls(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
        )

    def to_json(self) -> dict:
        return {
            'name': f'{self.first_name} {self.last_name}',
            'email': self.email
        }
