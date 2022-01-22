from .. regx import regex_brands
from ... utils.utils import uppercase


class BrandName(str):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(
            pattern='^[A-Z0-9]{4,4}$b',
            examples='Must Be: Alphanumeric characters, 4 characters in length, Uppercase Only',
        )

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError('string required')
        v = uppercase(v)
        m = regex_brands.brands_name_regex.fullmatch(v)
        if not m:
            raise ValueError(
                'Must Be: Alphanumeric characters, 4 characters in length, Uppercase Only')

        return cls(f'{m.group()}')

    def __repr__(self):
        return f'Role({super().__repr__()})'


class MethodAcx(str):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(
            pattern='Use: replace single quotes with double quotes, parsons to JSON, use, parse to string replacing double quotes with single quotes',
            examples="{'pre':{'Vertical Fermenter':{'method':'','note':''},'ACX Lines':{'method':'','note':''},'Chip Tank':{'method':'','note':''},'Uni Tank':{'method':'','note':''}},'post':{'Vertical Fermenter':{'method':'','note':''},'ACX Lines':{'method':'','note':''},'Chip Tank':{'method':'','note':''},'Uni Tank':{'method':'','note':''}}}",
        )

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError('string required')

        m = regex_brands.brands_methods_acx_regex.fullmatch(v)
        if not m:
            raise ValueError(
                'Must match regex. See docs.')

        return cls(f'{m.group()}')

    def __repr__(self):
        return f'Role({super().__repr__()})'


class MethodCsx(str):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(
            pattern='Use: replace single quotes with double quotes, parsons to JSON, use, parse to string replacing double quotes with single quotes',
            examples="{'pre':{'Chip Tank':{'method':'','note':''},'Uni Tank':{'method':'','note':''},'Schoene Train':{'method':'','note':''},'Schoene Receiver':{'method':'','note':''},'Schoene Fill Banks':{'method':'','note':''},'Separators':{'method':'','note':''},'ACP Addition':{'method':'','note':''},'Bypass Pre cooler':{'method':'','note':''},'Schoene Tank':{'method':'','note':''}},'post':{'Chip Tank':{'method':'','note':''},'Uni Tank':{'method':'','note':''},'Schoene Train':{'method':'','note':''},'Schoene Receiver':{'method':'','note':''},'Schoene Fill Banks':{'method':'','note':''},'Separators':{'method':'','note':''},'Schoene Tank':{'method':'','note':''}}}",
        )

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError('string required')

        m = regex_brands.brands_methods_csx_regex.fullmatch(v)
        if not m:
            raise ValueError(
                'Must match regex. See docs.')

        return cls(f'{m.group()}')

    def __repr__(self):
        return f'Role({super().__repr__()})'


class MethodFilters(str):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(
            pattern='Use: replace single quotes with double quotes, parsons to JSON, use, parse to string replacing double quotes with single quotes',
            examples="{'pre':{'Schoene Tank':{'method':'','note':''},'Schoene Release Bank':{'method':'','note':''},'Filter':{'method':'','note':''},'Balance Tanks':{'method':'','note':''},'Trap Filter':{'method':'','note':''},'Filter Beer Supply Bank':{'method':'','note':''},'Filter Beer Tank':{'method':'','note':''},'Filter Control':{'method':'','note':''},'G Beer':{'method':'','note':''},'Brand Changes':{'method':'','note':''},'Pre Injection':{'Ingredient 1':{'commodity':'','note':''},'Ingredient 2':{'commodity':'','note':''}},'Post Injection':{'Ingredient 1':{'commodity':'','note':''},'Ingredient 2':{'commodity':'','note':''},'Ingredient 3':{'commodity':'','note':''},'Ingredient 4':{'commodity':'','note':''},'Ingredient 5':{'commodity':'','note':''},'Ingredient 6':{'commodity':'','note':''},'Ingredient 7':{'commodity':'','note':''},'Ingredient 8':{'commodity':'','note':''}}},'post':{'Schoene Tank':{'method':'','note':''},'Schoene Release Bank':{'method':'','note':''},'Filter':{'method':'','note':''},'Balance Tanks':{'method':'','note':''},'Trap Filter':{'method':'','note':''},'Filter Beer Supply Bank':{'method':'','note':''},'Filter Beer Tank':{'method':'','note':''},'Beer Recovery':{'method':'','note':''}}}",
        )

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError('string required')

        m = regex_brands.brands_methods_filters_regex.fullmatch(v)
        if not m:
            raise ValueError(
                'Must match regex. See docs.')

        return cls(f'{m.group()}')

    def __repr__(self):
        return f'Role({super().__repr__()})'


class MethodReleasing(str):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(
            pattern='Use: replace single quotes with double quotes, parsons to JSON, use, parse to string replacing double quotes with single quotes',
            examples="{'pre':{'Filter Beer Tank':{'method':'','note':''},'Release Bank':{'method':'','note':''},'Package Line':{'method':'','note':''},'Draught Line':{'method':'','note':''},'Release Control':{'method':'','note':''},'Beer Recovery':{'method':'','note':''}},'post':{'Filter Beer Tank':{'method':'','note':''},'Release Bank':{'method':'','note':''},'Package Line':{'method':'','note':''},'Draught Line':{'method':'','note':'this is a test'}}}",
        )

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError('string required')

        m = regex_brands.brands_methods_releasing_regex.fullmatch(v)
        if not m:
            raise ValueError(
                'Must match regex. See docs.')

        return cls(f'{m.group()}')

    def __repr__(self):
        return f'Role({super().__repr__()})'
