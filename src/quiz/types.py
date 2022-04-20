from random import randint

import sqlalchemy.types as types


class QuizEnterCode(types.TypeDecorator):

    impl = types.String

    cache_ok = True

    def process_bind_param(self, value, dialect):
        return self.enter_code

    def process_result_value(self, value, dialect):
        return self.enter_code

    def copy(self, **kw):
        return QuizEnterCode(self.impl.length)

    def _generate_code(self):
        resulted_code = ""
        for _ in range(4):
            resulted_code += str(randint(1, 9))

        return resulted_code

    def __init__(self, *args, **kwargs) -> None:
        if not kwargs.get("enter_code"):
            self.enter_code = self._generate_code()
