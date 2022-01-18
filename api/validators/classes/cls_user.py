from .. regx import regex_user
from ... utils.utils import titlecase


class Password(str):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(
            pattern='^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$',
            examples='Must Be: 8 characters minimun, Uppercase, Lowercase, Number, Special Character [#?!@$%^&*-]',
        )

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError('string required')
        m = regex_user.user_password_regex.fullmatch(v)
        if not m:
            raise ValueError(
                'Must Be: 8 characters minimun, Uppercase, Lowercase, Number, Special Character [#?!@$%^&*-]')
        return cls(m.group())

    def __repr__(self):
        return f'Password({super().__repr__()})'


class Role(str):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(
            pattern='\b(Admin|Brew Master|Assist Brew Master|BPM|PE Brewhouse|PE Finishing|Maintenance|Material Handler|Lead Brewer|Brewer|Apprentice|Weekender|Seasonal)\b',
            examples='Must Be: Admin, Brew Master, Assist Brew Master, BPM, PE Brewhouse, PE Finishing, Maintenance, Material Handler, Lead Brewer, Brewer, Apprentice, Weekender, Seasonal',
        )

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError('string required')
        m = regex_user.user_role_regex.fullmatch(v)
        if not m:
            raise ValueError(
                'Must Be: Admin, Brew Master, Assist Brew Master, BPM, PE Brewhouse, PE Finishing, Maintenance, Material Handler, Lead Brewer, Brewer, Apprentice, Weekender, Seasonal')
        return cls(f'{m.group()}')

    def __repr__(self):
        return f'Role({super().__repr__()})'


class Brewery(str):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(
            pattern='\b(FTC)\b',
            examples='Must Be: FTC',
        )

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError('string required')
        m = regex_user.user_brewery_regex.fullmatch(v)
        if not m:
            raise ValueError('Must Be: FTC')

        return cls(f'{m.group()}')

    def __repr__(self):
        return f'Brewery({super().__repr__()})'


class Name(str):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(
            pattern='^[a-zA-Z0-9\x20]{5,50}$',
            examples='Must Be: Alphanumeric characters, 5-50 characters in length',
        )

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError('string required')
        m = regex_user.user_name_regex.fullmatch(v)
        if not m:
            raise ValueError(
                'Must Be: Alphanumeric characters, 5-50 characters in length')

        m = titlecase(cls(f'{m.group()}'))

        return m

    def __repr__(self):
        return f'Brewery({super().__repr__()})'


class UserName(str):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(
            pattern='^[a-zA-Z0-9]{5,50}$',
            examples='Must Be: Alphanumeric characters, 5-50 characters in length, no spaces',
        )

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError('string required')
        m = regex_user.user_username_regex.fullmatch(v)
        if not m:
            raise ValueError(
                'Must Be: Alphanumeric characters, 5-50 characters in length, no spaces')

        return cls(f'{m.group()}')

    def __repr__(self):
        return f'Brewery({super().__repr__()})'
