from .. regx import regex_commodities
from ... utils.utils import titlecase


class CommoditiesName(str):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(
            pattern='^[a-zA-Z0-9\x20]{5,50}$b',
            examples='Must Be: Alphanumeric characters, 5-50 characters in length',
        )

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError('string required')
        m = regex_commodities.commodity_name_regex.fullmatch(v)
        if not m:
            raise ValueError(
                'Must Be: Alphanumeric characters, 5-50 characters in length')

        converted_str = titlecase(cls(f'{m.group()}'))

        return converted_str

    def __repr__(self):
        return f'Role({super().__repr__()})'


class Location(str):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(
            pattern='\b(Grains|Brewhouse|Fermenting|Unitanks|Chips|Finishing)\b',
            examples='Must Be: Grains|Brewhouse|Fermenting|Unitanks|Chips|Finishing',
        )

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError('string required')
        m = regex_commodities.commodity_location_regex.fullmatch(v)
        if not m:
            raise ValueError(
                'Must Be: Grains|Brewhouse|Fermenting|Unitanks|Chips|Finishing')

        return cls(f'{m.group()}')

    def __repr__(self):
        return f'Role({super().__repr__()})'


class Inventory(str):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(
            pattern='\b(Brw|Fin|Log)\b',
            examples='Must Be: Brw|Fin|Log',
        )

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError('string required')
        m = regex_commodities.commodity_inventory_regex.fullmatch(v)
        if not m:
            raise ValueError(
                'Must Be: Brw|Fin|Log')

        return cls(f'{m.group()}')

    def __repr__(self):
        return f'Role({super().__repr__()})'


class Sap(str):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(
            pattern='^[0-9]{8, 8}$',
            examples='Must Be: Numeric only, 8 Digits only',
        )

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError('string required')
        m = regex_commodities.commodity_sap_regex.fullmatch(v)
        print(v)
        if not m:
            raise ValueError(
                'Must Be: Numeric only, 8 Digits only')

        return cls(f'{m.group()}')

    def __repr__(self):
        return f'Role({super().__repr__()})'


class Type(str):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(
            pattern='\b(Chemical|Filter|Hop|BH_Injection|FIN_Injection|BK_Addition|MC_Addition)\b',
            examples='Must Be: Chemical|Filter|Hop|BH_Injection|FIN_Injection|BK_Addition|MC_Addition',
        )

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError('string required')
        m = regex_commodities.commodity_type_regex.fullmatch(v)
        print(v)
        if not m:
            raise ValueError(
                'Must Be: Chemical|Filter|Hop|BH_Injection|FIN_Injection|BK_Addition|MC_Addition')

        return cls(f'{m.group()}')

    def __repr__(self):
        return f'Role({super().__repr__()})'
