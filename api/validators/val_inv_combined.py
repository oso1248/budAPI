from datetime import date
from pydantic import BaseModel, conint, confloat, UUID4


class InvCombinedIn(BaseModel):
    uuid_hop: UUID4
    uuid_material: UUID4


class InvCombinedOut(BaseModel):
    name_local: str
    name_bit: str
    sap: str
    inventory: str
    total_pallets: conint(ge=0)
    total_units: confloat(ge=0)
    total_end: confloat(ge=0)
    inv_date: date

    class Config:
        orm_mode = True
