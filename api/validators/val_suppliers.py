from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime
from . classes import cls_suppliers, cls_universal
from . val_user import UserInclude


class SupplierInclude(BaseModel):
    id: int
    name: cls_suppliers.SupplierName
    contact: cls_suppliers.SupplierName
    email: EmailStr
    phone: cls_universal.UniversalPhone
    note: Optional[cls_universal.UniversalNote] = None

    class Config:
        orm_mode = True


class SupplierCreate(BaseModel):
    name: cls_suppliers.SupplierName
    contact: cls_suppliers.SupplierName
    email: EmailStr
    phone: cls_universal.UniversalPhone
    note: Optional[cls_universal.UniversalNote] = None
    is_active: bool = True


class SupplierUpdate(BaseModel):
    name: cls_suppliers.SupplierName
    contact: cls_suppliers.SupplierName
    email: EmailStr
    phone: cls_universal.UniversalPhone
    note: Optional[cls_universal.UniversalNote] = None
    is_active: bool = True


class SupplierOut(BaseModel):
    id: int
    name: cls_suppliers.SupplierName
    contact: cls_suppliers.SupplierName
    email: EmailStr
    phone: cls_universal.UniversalPhone
    note: Optional[cls_universal.UniversalNote] = None
    is_active: bool = True
    created_at: datetime
    updated_at: datetime
    creator: UserInclude
    updater: UserInclude

    class Config:
        orm_mode = True
