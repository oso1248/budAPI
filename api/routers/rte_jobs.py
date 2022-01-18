from fastapi import status, Response, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from .. database.database import cursor, conn, get_db
from .. validators import val_jobs, val_user
from .. models import mdl_jobs
from .. oauth2.oauth2 import get_current_user

router = APIRouter(prefix='/jobs', tags=['Jobs'])


# Validaton: api/validators/val_jobs.py
# Model: api/models/mdl_jobs.py


# Create New Job
@router.post('', status_code=status.HTTP_201_CREATED, response_model=val_jobs.JobOut)
def create_job(job: val_jobs.JobCreate, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):

    does_exist_name = db.query(mdl_jobs.Jobs).filter(
        mdl_jobs.Jobs.name == job.name).first()
    if does_exist_name:
        raise HTTPException(status_code=status.HTTP_226_IM_USED,
                            detail=f'job: {job.name} already exists')

    db_data = mdl_jobs.Jobs(created_by=current_user.id,
                            updated_by=current_user.id, **job.dict())
    db.add(db_data)
    db.commit()
    db.refresh(db_data)

    return db_data


# Return List Of All Jobs
@router.get('', status_code=status.HTTP_200_OK, response_model=List[val_jobs.JobOut])
def get_jobs(db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):

    db_data = db.query(mdl_jobs.Jobs).order_by(
        mdl_jobs.Jobs.area, mdl_jobs.Jobs.name).all()
    if not db_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='jobs do not exist')

    return db_data


# Return Single Job By ID
@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=val_jobs.JobOut)
def get_job(id: int, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):

    db_data = db.query(mdl_jobs.Jobs).filter(
        mdl_jobs.Jobs.id == id).first()
    if not db_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'job with id: {id} does not exist')

    return db_data


# Update Job By ID
@router.put('/{id}', status_code=status.HTTP_200_OK, response_model=val_jobs.JobOut)
def update_job(id: int, job: val_jobs.JobUpdate, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):

    query = db.query(mdl_jobs.Jobs).filter(mdl_jobs.Jobs.id == id)
    update = query.first()
    if not update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'user with id: {id} does not exist')

    new_dict = job.dict()
    new_dict['updated_by'] = current_user.id
    query.update(new_dict, synchronize_session=False)

    db.commit()

    return query.first()


# Delete User By ID
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_job(id: int, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):

    query = db.query(mdl_jobs.Jobs).filter(mdl_jobs.Jobs.id == id)
    if not query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'job with id: {id} does not exist')

    query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_205_RESET_CONTENT)
