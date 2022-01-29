from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel, conint, confloat, UUID4
from . classes import cls_universal, cls_inv
from . val_user import UserInclude
from . val_commodities import CommodityInclude


class InvHopLastBrewsIn(BaseModel):
    bh_1: cls_inv.LastBrew
    bh_2: cls_inv.LastBrew


class InvHopLastBrewsOut(BaseModel):
    bh_1: cls_inv.LastBrew
    bh_2: cls_inv.LastBrew
    inv_uuid: UUID4

    class Config:
        orm_mode = True


class InvHopCreate(BaseModel):
    total_pallets: conint(ge=0)
    total_units: confloat(ge=0)
    total_per_unit: confloat(ge=0)
    total_end: confloat(ge=0)
    note: Optional[cls_universal.UniversalNote] = None
    id_commodity: int


class InvHopOut(BaseModel):
    id: int
    total_pallets: conint(ge=0)
    total_units: confloat(ge=0)
    total_per_unit: confloat(ge=0)
    total_end: confloat(ge=0)
    note: str
    creator: UserInclude
    parent: CommodityInclude
    lastbrews: InvHopLastBrewsOut

    class Config:
        orm_mode = True


class InvHopDatesOut(BaseModel):
    inv_date: date
    inv_uuid: str

    class Config:
        orm_mode = True


class InvHopSumOut(BaseModel):
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


class InvHopCompleteOut(BaseModel):
    id: int
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
