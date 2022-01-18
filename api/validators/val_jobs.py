from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from . classes import cls_jobs
from .val_user import UserInclude


class JobCreate(BaseModel):
    name: cls_jobs.Name
    area: cls_jobs.Area
    is_active: bool = True
    is_work_restriction: bool = False


class JobUpdate(BaseModel):
    name: cls_jobs.Name
    area: cls_jobs.Area
    is_active: bool = True
    is_work_restriction: bool = False


class JobOut(BaseModel):
    id: int
    name: cls_jobs.Name
    area: cls_jobs.Area
    is_active: bool = True
    is_work_restriction: bool = False
    created_at: datetime
    updated_at: datetime
    creator: UserInclude
    updater: UserInclude

    class Config:
        orm_mode = True
