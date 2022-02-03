from . classes import cls_universal, cls_brands
from . val_user import UserInclude
from typing import Optional, List
from pydantic import BaseModel, Json
from datetime import datetime


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


class MethodNote(BaseModel):
    method: cls_brands.BrandMethod
    note: Optional[cls_universal.UniversalNote] = None


class EquipmentAcx(BaseModel):
    Vertical_Fermenter: MethodNote
    ACX_Lines: MethodNote
    Chip_Tank: MethodNote


class PrePostAcx(BaseModel):
    pre: EquipmentAcx
    post: EquipmentAcx


class BrandBrewingMethodsAcx(BaseModel):
    methods_acx: PrePostAcx


class BrandBrewingMethodsAcxOut(BaseModel):
    id: int
    name: str
    methods_acx: PrePostAcx

    class Config:
        orm_mode = True


class EquipmentCsx(BaseModel):
    Chip_Tank: MethodNote
    Uni_Tank: MethodNote
    Schoene_Train: MethodNote
    Schoene_Receiver: MethodNote
    Schoene_Fill_Bank: MethodNote
    Seperators: MethodNote
    ACP_Addition: MethodNote
    Bypass_Pre_Cooler: MethodNote
    Schoene_Tank: MethodNote


class PrePostCsx(BaseModel):
    pre: EquipmentCsx
    post: EquipmentCsx


class BrandBrewingMethodsCsx(BaseModel):
    methods_csx: PrePostCsx


class BrandBrewingMethodsCsxOut(BaseModel):
    id: int
    name: str
    methods_csx: PrePostCsx

    class Config:
        orm_mode = True


class BrandBrewingMethodsOut(BaseModel):
    id: int
    name: str
    methods_acx: PrePostAcx
    methods_csx: PrePostCsx

    class Config:
        orm_mode = True


class BrandBrewingOut(BaseModel):
    id: int
    name: str
    is_organic: bool
    is_hop_kettle: bool
    is_hop_dry: bool
    is_addition: bool
    note: Optional[cls_universal.UniversalNote] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    creator: UserInclude
    updater: UserInclude
    children: List[BrandFinishingInclude]

    class Config:
        orm_mode = True
