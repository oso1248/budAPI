from . classes import cls_universal, cls_brands
from . val_user import UserInclude
from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime


class BrandPackagingInclude(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class BrandFinishingInclude(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class BrandPackagingCreate(BaseModel):
    name: cls_brands.BrandName
    is_organic: bool = False
    note: Optional[cls_universal.UniversalNote] = None
    is_active: bool = True
    id_finishing: int


class BrandPackagingUpdate(BaseModel):
    name: cls_brands.BrandName
    is_organic: bool = False
    note: Optional[cls_universal.UniversalNote] = None
    is_active: bool = False
    id_finishing: int


class BrandPackagingOut(BaseModel):
    id: int
    name: cls_brands.BrandName
    is_organic: bool
    note: Optional[cls_universal.UniversalNote] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    creator: UserInclude
    updater: UserInclude
    parent: BrandFinishingInclude

    class Config:
        orm_mode = True
