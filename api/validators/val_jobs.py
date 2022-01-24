from typing import Optional
from pydantic import BaseModel, conint
from datetime import datetime
from . classes import cls_jobs
from .val_user import UserInclude


class JobInclude(BaseModel):
    id: int
    name: cls_jobs.Name
    area: cls_jobs.Area

    class Config:
        orm_mode = True


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
    is_active: bool
    is_work_restriction: bool
    created_at: datetime
    updated_at: datetime
    creator: UserInclude
    updater: UserInclude

    class Config:
        orm_mode = True


class UserJobAdd(BaseModel):
    id_users: int
    id_jobs: int
    skap: conint(ge=1, le=6)


class UserJobUpdateSkap(BaseModel):
    id_users: int
    id_jobs: int
    skap: conint(ge=1, le=6)


class UserJobDelete(BaseModel):
    id_users: int
    id_jobs: int


class UserJobOut(BaseModel):
    brewer: UserInclude
    job: JobInclude
    skap: conint(ge=1, le=6)

    class Config:
        orm_mode = True
