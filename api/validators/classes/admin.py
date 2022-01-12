from regx import regx


class Password(str):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(
            pattern='^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$',
            examples='Valid: 8 characters minimun, Uppercase, Lowercase, Number, Special Character',
        )

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError('string required')
        m = regx.user_password_regex.fullmatch(v)
        if not m:
            raise ValueError('invalid password format')
        return m

    def __repr__(self):
        return f'Password({super().__repr__()})'
