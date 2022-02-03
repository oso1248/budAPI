from . val_brands_packaging import BrandPackagingInclude
from . val_brands_brewing import BrandBrewingInclude
from . classes import cls_universal, cls_brands
from . val_user import UserInclude
from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime


class BrandFinishingInclude(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class BrandFinishingCreate(BaseModel):
    name: cls_brands.BrandName
    is_pre_injection: bool = False
    is_post_injection: bool = False
    is_bypass: bool = False
    is_organic: bool = False
    note: Optional[cls_universal.UniversalNote] = None
    is_active: bool = True
    id_brewing: int


class BrandFinishingUpdate(BaseModel):
    name: cls_brands.BrandName
    is_pre_injection: bool = False
    is_post_injection: bool = False
    is_bypass: bool = False
    is_organic: bool = False
    note: Optional[cls_universal.UniversalNote] = None
    is_active: bool = True
    id_brewing: int


class MethodNote(BaseModel):
    method: cls_brands.BrandMethod
    note: Optional[cls_universal.UniversalNote] = None


class BrandsFinishingFiltersPreInjection(BaseModel):
    Ingredient_1: Optional[MethodNote]
    Ingredient_2: Optional[MethodNote]


class BrandsFinishingFiltersPostInjection(BaseModel):
    Ingredient_1: Optional[MethodNote]
    Ingredient_2: Optional[MethodNote]
    Ingredient_3: Optional[MethodNote]
    Ingredient_4: Optional[MethodNote]
    Ingredient_5: Optional[MethodNote]
    Ingredient_6: Optional[MethodNote]
    Ingredient_7: Optional[MethodNote]
    Ingredient_8: Optional[MethodNote]


class EquipmentFilters(BaseModel):
    Schoene_Tank: MethodNote
    Schoene_Release_Bank: MethodNote
    Filter: MethodNote
    Balance_Tanks: MethodNote
    Trap_Filter: MethodNote
    Filter_Beer_Supply_Bank: MethodNote
    Filter_Beer_Tank: MethodNote
    Filter_Control: MethodNote
    Brand_Changes: MethodNote
    Pre_Injection: Optional[List[BrandsFinishingFiltersPreInjection]]
    Post_Injection: Optional[List[BrandsFinishingFiltersPostInjection]]
    Beer_recovery: Optional[MethodNote]


class PrePostFilters(BaseModel):
    pre: EquipmentFilters
    post: EquipmentFilters


class BrandFinishingMethodsFilters(BaseModel):
    methods_filters: PrePostFilters


class BrandFinishingMethodsFiltersOut(BaseModel):
    id: int
    name: cls_brands.BrandName
    parent: BrandBrewingInclude
    methods_filters: PrePostFilters

    class Config:
        orm_mode = True


class EquipmentReleasing(BaseModel):
    Filter_Beer_Tank: MethodNote
    Release_Bank: MethodNote
    Package_Line: MethodNote
    Draught_Line: MethodNote
    Release_Control: MethodNote
    Beer_Recovery: MethodNote


class PrePostReleasing(BaseModel):
    pre: EquipmentReleasing
    post: EquipmentReleasing


class BrandFinishingMethodsReleasing(BaseModel):
    methods_releasing: PrePostReleasing


class BrandFinishingMethodsReleasingOut(BaseModel):
    id: int
    name: str
    methods_releasing: PrePostReleasing

    class Config:
        orm_mode = True


class BrandFinishingMethodsOut(BaseModel):
    id: int
    name: cls_brands.BrandName
    is_pre_injection: bool
    is_post_injection: bool
    is_bypass: bool
    is_organic: bool
    note: Optional[cls_universal.UniversalNote] = None
    is_active: bool
    updated_at: datetime
    parent: BrandBrewingInclude
    children: List[BrandPackagingInclude]
    methods_filters: PrePostFilters
    methods_releasing: PrePostReleasing

    class Config:
        orm_mode = True


class BrandFinishingOut(BaseModel):
    id: int
    name: cls_brands.BrandName
    is_pre_injection: bool
    is_post_injection: bool
    is_bypass: bool
    is_organic: bool
    note: Optional[cls_universal.UniversalNote] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    creator: UserInclude
    updater: UserInclude
    parent: BrandBrewingInclude
    children: List[BrandPackagingInclude]

    class Config:
        orm_mode = True
