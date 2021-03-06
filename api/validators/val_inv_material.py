from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel, conint, confloat
from pydantic.types import UUID4
from . classes import cls_universal
from . val_user import UserInclude
from . val_commodities import CommodityInclude


class InvMaterialCreate(BaseModel):
    total_pallets: conint(ge=0)
    total_units: confloat(ge=0)
    total_per_unit: confloat(ge=0)
    total_end: confloat(ge=0)
    note: Optional[cls_universal.UniversalNote] = None
    id_commodity: int


class InvMaterialOut(BaseModel):
    id: int
    total_pallets: conint(ge=0)
    total_units: confloat(ge=0)
    total_per_unit: confloat(ge=0)
    total_end: confloat(ge=0)
    note: str
    creator: UserInclude
    parent: CommodityInclude

    class Config:
        orm_mode = True


class InvMaterialDatesOut(BaseModel):
    inv_date: date
    inv_uuid: UUID4

    class Config:
        orm_mode = True


class InvMaterialSumOut(BaseModel):
    name_local: str
    name_bit: str
    sap: str
    inventory: str
    total_pallets: conint(ge=0)
    total_units: confloat(ge=0)
    total_end: confloat(ge=0)
    inv_date: date
    inv_uuid: UUID4

    class Config:
        orm_mode = True


class InvMaterialCompleteOut(BaseModel):
    name_local: str
    name_bit: str
    sap: str
    inventory: str
    total_pallets: conint(ge=0)
    total_units: confloat(ge=0)
    total_end: confloat(ge=0)
    note: str
    name: str
    inv_date: datetime
    inv_uuid: UUID4

    class Config:
        orm_mode = True
