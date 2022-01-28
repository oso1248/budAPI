from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime
from . classes import cls_universal, cls_brands
from . val_user import UserInclude


class BrandBrewingInclude(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class BrandFinishingInclude(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class BrandPackagingInclude(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


# Brand Brewing
class BrandBrewingCreate(BaseModel):
    name: cls_brands.BrandName
    is_organic: bool = False
    is_hop_kettle: bool = True
    is_hop_dry: bool = False
    is_addition: bool = False
    note: Optional[cls_universal.UniversalNote] = None
    is_active: bool = True


class BrandBrewingUpdate(BaseModel):
    name: cls_brands.BrandName
    is_organic: bool
    is_hop_kettle: bool
    is_hop_dry: bool
    is_addition: bool
    note: Optional[cls_universal.UniversalNote] = None
    is_active: bool


class BrandBrewingMethodsAcx(BaseModel):
    methods_acx: cls_brands.MethodAcx


class BrandBrewingMethodsAcxOut(BaseModel):
    id: int
    name: str
    methods_acx: cls_brands.MethodAcx

    class Config:
        orm_mode = True


class BrandBrewingMethodsCsx(BaseModel):
    methods_csx: cls_brands.MethodCsx


class BrandBrewingMethodsCsxOut(BaseModel):
    id: int
    name: str
    methods_csx: cls_brands.MethodCsx

    class Config:
        orm_mode = True


class BrandBrewingMethodsOut(BaseModel):
    id: int
    name: str
    methods_acx: cls_brands.MethodAcx = None
    methods_csx: cls_brands.MethodCsx = None

    class Config:
        orm_mode = True


class BrandBrewingOut(BaseModel):
    id: int
    name: str
    is_organic: bool
    is_hop_kettle: bool
    is_hop_dry: bool
    is_addition: bool
    note: cls_universal.UniversalNote
    is_active: bool
    created_at: datetime
    updated_at: datetime
    creator: UserInclude
    updater: UserInclude
    children: List[BrandFinishingInclude]

    class Config:
        orm_mode = True


# Brand Finishing
class BrandFinishingCreate(BaseModel):
    name: cls_brands.BrandName
    is_pre_injection: bool = False
    is_post_injection: bool = False
    is_bypass: bool = False
    is_organic: bool = False
    note: cls_universal.UniversalNote
    is_active: bool = True
    id_brewing: int


class BrandFinishingUpdate(BaseModel):
    name: cls_brands.BrandName
    is_pre_injection: bool = False
    is_post_injection: bool = False
    is_bypass: bool = False
    is_organic: bool = False
    note: cls_universal.UniversalNote
    is_active: bool = True
    id_brewing: int


class BrandFinishingMethodsFilters(BaseModel):
    methods_filters: cls_brands.MethodFilters


class BrandFinishingMethodsFiltersOut(BaseModel):
    id: int
    name: str
    methods_filters: cls_brands.MethodFilters

    class Config:
        orm_mode = True


class BrandFinishingMethodsReleasing(BaseModel):
    methods_releasing: cls_brands.MethodReleasing


class BrandFinishingMethodsReleasingOut(BaseModel):
    id: int
    name: str
    methods_releasing: cls_brands.MethodReleasing

    class Config:
        orm_mode = True


class BrandFinishingMethodsOut(BaseModel):
    id: int
    name: str
    methods_filters: cls_brands.MethodFilters
    methods_releasing: cls_brands.MethodReleasing

    class Config:
        orm_mode = True


class BrandFinishingOut(BaseModel):
    id: int
    name: cls_brands.BrandName
    is_pre_injection: bool
    is_post_injection: bool
    is_bypass: bool
    is_organic: bool
    note: cls_universal.UniversalNote
    is_active: bool
    created_at: datetime
    updated_at: datetime
    creator: UserInclude
    updater: UserInclude
    parent: BrandBrewingInclude
    children: List[BrandPackagingInclude]

    class Config:
        orm_mode = True


# Brand Packaging
class BrandPackagingCreate(BaseModel):
    name: cls_brands.BrandName
    is_organic: bool = False
    note: cls_universal.UniversalNote
    is_active: bool = False
    id_finishing: int


class BrandPackagingUpdate(BaseModel):
    name: cls_brands.BrandName
    is_organic: bool = False
    note: cls_universal.UniversalNote
    is_active: bool = False
    id_finishing: int


class BrandPackagingOut(BaseModel):
    id: int
    name: cls_brands.BrandName
    is_organic: bool
    note: cls_universal.UniversalNote
    is_active: bool
    created_at: datetime
    updated_at: datetime
    creator: UserInclude
    updater: UserInclude
    parent: BrandFinishingInclude

    class Config:
        orm_mode = True
