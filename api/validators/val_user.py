from typing import Optional
from pydantic import BaseModel, conint
from datetime import datetime
from . classes import cls_user


class UserInclude(BaseModel):
    id: int
    name: cls_user.Name

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    name: cls_user.Name
    username: cls_user.UserName
    password: cls_user.Password
    is_active: bool = True
    role: cls_user.Role = 'Brewer'
    brewery: cls_user.Brewery = 'FTC'
    permissions: conint(ge=0, le=6) = 1


class UserUpdate(BaseModel):
    name: cls_user.Name
    is_active: bool = True
    role: cls_user.Role = 'Brewer'
    brewery: cls_user.Brewery = 'FTC'
    permissions: conint(ge=1, le=6) = 1


class UserOut(BaseModel):
    id: int
    name: cls_user.Name
    is_active: bool
    role: cls_user.Role
    brewery: cls_user.Brewery
    permissions: int
    created_at: datetime
    updated_at: datetime
    creator: UserInclude
    updater: UserInclude

    class Config:
        orm_mode = True


class UserPasswordReset(BaseModel):
    id: int
    password_reset: cls_user.Password


class UserPasswordChange(BaseModel):
    username: cls_user.UserName
    password: cls_user.Password
    password_reset: cls_user.Password
