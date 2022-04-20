from core.exceptions import ImproperlyConfigured
from core.manager import BaseManager


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
