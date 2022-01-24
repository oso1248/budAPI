from typing import Optional
from pydantic import BaseModel, confloat, conint, constr
from datetime import datetime
from . classes import cls_universal, cls_commodities
from . val_suppliers import SupplierInclude
from . val_user import UserInclude


class CommodityInclude(BaseModel):
    id: int
    name_local: cls_commodities.CommoditiesName

    class Config:
        orm_mode = True


class CommodityCreate(BaseModel):
    name_bit: constr(min_length=5, max_length=50)
    name_local: cls_commodities.CommoditiesName
    location: cls_commodities.Location
    sap: cls_commodities.Sap
    inventory: cls_commodities.Inventory
    threshold: conint(ge=0) = 0
    per_pallet: conint(ge=0)
    per_unit: conint(ge=0)
    unit_of_measurement: str
    note: Optional[cls_universal.UniversalNote]
    is_active: bool = True
    id_supplier: int


class CommodityUpdate(BaseModel):
    name_bit: constr(min_length=5, max_length=50)
    name_local: cls_commodities.CommoditiesName
    location: cls_commodities.Location
    sap: cls_commodities.Sap
    inventory: cls_commodities.Inventory
    threshold: conint(ge=0) = 0
    per_pallet: conint(ge=0)
    per_unit: conint(ge=0)
    unit_of_measurement: str
    note: Optional[cls_universal.UniversalNote] = None
    balance_inactive: confloat(ge=0) = None
    is_active: bool = True
    id_supplier: int


class CommodityOut(BaseModel):
    id: int
    name_bit: constr(min_length=5, max_length=50)
    name_local: cls_commodities.CommoditiesName
    location: cls_commodities.Location
    sap: cls_commodities.Sap
    inventory: cls_commodities.Inventory
    threshold: conint(ge=0) = 0
    per_pallet: conint(ge=0)
    per_unit: conint(ge=0)
    unit_of_measurement: str
    note: Optional[cls_universal.UniversalNote] = None
    balance_inactive: confloat(ge=0) = None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    creator: UserInclude
    updater: UserInclude
    supplier: SupplierInclude

    class Config:
        orm_mode = True
