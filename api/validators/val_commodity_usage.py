from datetime import datetime
from pydantic import BaseModel, confloat, conint
from . val_user import UserInclude
from . val_commodities import CommodityInclude
from . val_brands_brewing import BrandBrewingInclude


class CommodityUsageIn(BaseModel):
    id_commodity: int
    id_brand_brewing: int
    id_brewhouse: conint(ge=0, le=2) = 0
    amount_per_brew: confloat(ge=0)


class CommodityUsageDelete(BaseModel):
    id_commodity: int
    id_brand_brewing: int
    id_brewhouse: conint(ge=0, le=2) = 0


class CommodityUsageOut(BaseModel):
    id_brewhouse: conint(ge=0, le=2)
    amount_per_brew: confloat(ge=0)
    commodity: CommodityInclude
    brand: BrandBrewingInclude
    created_at: datetime
    updated_at: datetime
    creator: UserInclude
    updater: UserInclude

    class Config:
        orm_mode = True
