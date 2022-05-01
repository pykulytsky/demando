from random import randint

from core.exceptions import ImproperlyConfigured
from core.manager import BaseManager


def _generate_enter_code() -> str:
    resulted_code = ""
    for _ in range(4):
        resulted_code += str(randint(1, 9))

    return resulted_code


class QuizManager(BaseManager):
    def create(self, disable_check: bool = False, **fields):
        if not fields.get("enter_code"):
            fields["enter_code"] = _generate_enter_code()
        return super(QuizManager, self).create(disable_check, **fields)


class OptionManager(BaseManager):
    def create(self, disable_check: bool = False, **fields):
        existing_options = fields.get("step").options
        if fields.get("is_right"):
            for option in existing_options:
                if option.is_right:
                    raise ImproperlyConfigured()
        return super(OptionManager, self).create(disable_check, **fields)


class OptionManagerMixin:
    @classmethod
    def manager(cls, db):
        return OptionManager(cls, db)


class QuizManagerMixin:
    @classmethod
    def manager(cls, db):
        return QuizManager(cls, db)
