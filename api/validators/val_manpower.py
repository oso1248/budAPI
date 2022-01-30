from datetime import datetime
from pydantic import BaseModel, conint
from . val_user import UserInclude
from . val_jobs import JobInclude
from .classes import cls_universal


class ManPowerIndividualIn(BaseModel):
    shift: conint(ge=1, le=3)
    id_users: int
    id_jobs: int
    note: cls_universal.UniversalNote


class ManPowerIndividualOut(BaseModel):
    id: int
    shift: conint(ge=1, le=3)
    brewer: UserInclude
    job: JobInclude
    note: cls_universal.UniversalNote
    created_at: datetime
    creator: UserInclude

    class Config:
        orm_mode = True


class ManPowerIndividualDatesIn(BaseModel):
    start: datetime
    stop: datetime
    shift: conint(ge=1, le=3)


class ManPowerGroupIn(BaseModel):
    shift: conint(ge=1, le=3)
    note: cls_universal.UniversalNote


class ManPowerGroupOut(BaseModel):
    id: int
    shift: conint(ge=1, le=3)
    note: cls_universal.UniversalNote
    created_at: datetime
    creator: UserInclude

    class Config:
        orm_mode = True


class ManPowerGroupDatesIn(BaseModel):
    start: datetime
    stop: datetime
    shift: conint(ge=1, le=3)
