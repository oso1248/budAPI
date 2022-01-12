from typing import Optional, ParamSpecArgs
from pydantic import BaseModel, EmailStr, constr
from datetime import datetime
from typing import Optional
import re
from classes import admin

# user_password_regex = re.compile(
#     r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$')


# class Password(str):

#     @classmethod
#     def __get_validators__(cls):
#         yield cls.validate

#     @classmethod
#     def __modify_schema__(cls, field_schema):
#         field_schema.update(
#             pattern='^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$',
#             examples='Valid: 8 characters minimun, Uppercase, Lowercase, Number, Special Character',
#         )

#     @classmethod
#     def validate(cls, v):
#         if not isinstance(v, str):
#             raise TypeError('string required')
#         m = user_password_regex.fullmatch(v)
#         if not m:
#             raise ValueError('invalid password format')
#         return m

#     def __repr__(self):
#         return f'Password({super().__repr__()})'


# class Model(BaseModel):
#     post_code: Password


# model = Model(post_code='Oso1978x!')
# print(model)


class User(BaseModel):
    name: constr(strip_whitespace=True, min_length=5, max_length=20)
    is_active: bool = True
    email: EmailStr
    role: constr(
        regex=r'\b(Admin|Brew Master|Assist Brew Master|BPM|PE Brewhouse|PE Finishing|Maintenance|Material Handler|Lead Brewer|Brewer)\b')
    brewery: constr(
        regex=r'\b(FTC)\b') = 'FTC'


class UserCreate(User):
    password: admin.Password
    pass


class UserPatch(User):
    id: int
    pass


class UserOut(User):
    id: int = 1

    class Config:
        orm_mode = True
