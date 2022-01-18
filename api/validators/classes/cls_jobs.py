from .. regx import regex_jobs
from ... utils.utils import titlecase


class Name(str):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(
            pattern='/^[a-zA-Z0-9\x20]{5,30}$/',
            examples='Must Be: 5-30 Characters, Alphanumeric Only',
        )

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError('string required')
        m = regex_jobs.jobs_name_regex.fullmatch(v)
        if not m:
            raise ValueError('Must Be: 5-30 Characters, Alphanumeric Only')

        converted_str = titlecase(cls(f'{m.group()}'))

        return converted_str

    def __repr__(self):
        return f'Role({super().__repr__()})'


class Area(str):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(
            pattern='\b(Brewhouse|Finishing)\b',
            examples='Must Be: Brewhouse, Finishing',
        )

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError('string required')
        m = regex_jobs.jobs_area_regex.fullmatch(v)
        if not m:
            raise ValueError('Must Be: Brewhouse, Finishing')

        return cls(f'{m.group(1)}')

    def __repr__(self):
        return f'Role({super().__repr__()})'
