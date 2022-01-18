from ..regx import regex_universal
from ... utils.utils import convert_phone_number, titlecase, strip_non_numeric


class UniversalNote(str):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(
            pattern='^[a-zA-Z0-9\x20]{5,256}$b',
            examples='Must Be: Alphanumeric characters, [,.], 5-256 characters in length',
        )

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError('string required')
        if not v:
            return v
        m = regex_universal.universal_note_regex.fullmatch(v)
        if not m:
            raise ValueError(
                'Must Be: Alphanumeric characters, [,.], 5-256 characters in length')

        converted_str = titlecase(cls(f'{m.group()}'))
        return converted_str

    def __repr__(self):
        return f'Role({super().__repr__()})'


class UniversalPhone(str):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(
            pattern='^[0-9]{10,10}$b',
            examples='Must Be: Numeric Characters, 10 Digits',
        )

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError('string required')
        v = strip_non_numeric(v)
        m = regex_universal.universal_phone_regex.fullmatch(v)
        if not m:
            raise ValueError('Must Be: Numeric Characters, 10 Digits')

        converted_str = convert_phone_number(cls(f'{m.group()}'))

        return converted_str

    def __repr__(self):
        return f'Role({super().__repr__()})'
