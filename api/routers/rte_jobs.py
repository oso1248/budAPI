from fastapi import status, Response, Depends, APIRouter
from .. database.database import cursor, conn, get_db
from .. oauth2.oauth2 import get_current_user
from .. validators import val_jobs, val_user
from fastapi.responses import JSONResponse
from .. models import mdl_jobs, mdl_user
from sqlalchemy.orm import Session
from loguru import logger
from typing import List


router = APIRouter(prefix='/jobs', tags=['Jobs'])


# Validaton: api/validators/val_jobs.py
# Model: api/models/mdl_jobs.py


#  Add Job to User
@router.post('/userjobs', status_code=status.HTTP_201_CREATED, response_model=val_jobs.UserJobOut)
@logger.catch()
def add_job_to_user(job: val_jobs.UserJobAdd, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):
    try:
        does_exist = db.query(mdl_user.Users).filter(
            mdl_user.Users.id == job.id_users).first()
        if not does_exist:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'detail': f'Key (id_users)=({job.id_users}) id not present in table users'})

        does_exist = db.query(mdl_jobs.Jobs).filter(
            mdl_jobs.Jobs.id == job.id_jobs).first()
        if not does_exist:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'detail': f'Key (id_users)=({job.id_jobs}) id not present in table jobs'})

        does_exist = db.query(mdl_jobs.BridgeUsersJobs).filter(
            mdl_jobs.BridgeUsersJobs.id_jobs == job.id_jobs, mdl_jobs.BridgeUsersJobs.id_users == job.id_users).first()
        if does_exist:
            return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={'detail': f'Composite Key (id_users)=({job.id_users}) && (id_jobs)=({job.id_jobs}) violates unique constraint on table bridge_users_jobs'})

        db_data = mdl_jobs.BridgeUsersJobs(created_by=current_user.id,
                                           updated_by=current_user.id, **job.dict())

        db.add(db_data)
        db.commit()
        db.refresh(db_data)

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return db_data


# Update SKAP
@router.put('/userjobs', status_code=status.HTTP_200_OK, response_model=val_jobs.UserJobOut)
@logger.catch()
def update_skap(job: val_jobs.UserJobUpdateSkap, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):
    try:
        query = db.query(mdl_jobs.BridgeUsersJobs).filter(
            mdl_jobs.BridgeUsersJobs.id_jobs == job.id_jobs, mdl_jobs.BridgeUsersJobs.id_users == job.id_users)
        does_exist = query.first()
        if not does_exist:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'detail': f'Composite Key (id_users)=({job.id_users}) && (id_jobs)=({job.id_jobs}) is not present in table bridge_users_jobs'})

        new_dict = job.dict()
        new_dict['updated_by'] = current_user.id
        query.update(new_dict, synchronize_session=False)
        db.commit()

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return query.first()


# Delete Job From User
@router.delete('/userjobs', status_code=status.HTTP_204_NO_CONTENT)
def delete_job_from_user(job: val_jobs.UserJobDelete, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):
    try:
        query = db.query(mdl_jobs.BridgeUsersJobs).filter(
            mdl_jobs.BridgeUsersJobs.id_jobs == job.id_jobs, mdl_jobs.BridgeUsersJobs.id_users == job.id_users)
        does_exist = query.first()
        if not does_exist:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'detail': f'Composite Key (id_users)=({job.id_users}) && (id_jobs)=({job.id_jobs}) is not present in table bridge_users_jobs'})

        query.delete(synchronize_session=False)
        db.commit()

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(status_code=status.HTTP_205_RESET_CONTENT)


# Return List Of Job With Brewers
@router.get('/userjobs/jobs/{id}', status_code=status.HTTP_200_OK, response_model=List[val_jobs.UserJobOut])
@logger.catch()
def get_job_with_users(id: int, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):
    try:
        db_data = db.query(mdl_jobs.BridgeUsersJobs).join(
            mdl_user.Users, mdl_user.Users.id == mdl_jobs.BridgeUsersJobs.id_users).order_by(mdl_user.Users.name).filter(mdl_jobs.BridgeUsersJobs.id_jobs == id).all()
        if not db_data:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'detail': f'Key (id_jobs)=({id}) is not present in table bridge_users_jobs'})

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return db_data


# Return List Of Brewer With Jobs
@router.get('/userjobs/users/{id}', status_code=status.HTTP_200_OK, response_model=List[val_jobs.UserJobOut])
@logger.catch()
def get_user_with_jobs(id: int, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):
    try:
        db_data = db.query(mdl_jobs.BridgeUsersJobs).join(
            (mdl_user.Users, mdl_user.Users.id == mdl_jobs.BridgeUsersJobs.id_users), (mdl_jobs.Jobs, mdl_jobs.Jobs.id == mdl_jobs.BridgeUsersJobs.id_jobs)).order_by(mdl_jobs.Jobs.name).filter(mdl_jobs.BridgeUsersJobs.id_users == id).all()
        if not db_data:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'detail': f'Key (id_users)=({id}) is not present in table bridge_users_jobs'})

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return db_data


# Create New Job
@router.post('', status_code=status.HTTP_201_CREATED, response_model=val_jobs.JobOut)
@logger.catch()
def create_job(job: val_jobs.JobCreate, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):
    try:
        does_exist_name = db.query(mdl_jobs.Jobs).filter(
            mdl_jobs.Jobs.name == job.name).first()
        if does_exist_name:
            return JSONResponse(status_code=status.HTTP_226_IM_USED, content={'detail': f'Key (name)=({job.name}) violates unique constraint on column jobs.name'})

        db_data = mdl_jobs.Jobs(created_by=current_user.id,
                                updated_by=current_user.id, **job.dict())
        db.add(db_data)
        db.commit()
        db.refresh(db_data)

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return db_data


# Return List Of All Jobs
@router.get('', status_code=status.HTTP_200_OK, response_model=List[val_jobs.JobOut])
@logger.catch()
def get_jobs(active: str = True, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):
    try:
        db_data = db.query(mdl_jobs.Jobs).filter(mdl_jobs.Jobs.is_active == active).order_by(
            mdl_jobs.Jobs.area, mdl_jobs.Jobs.name).all()
        if not db_data:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'detail': f'Key (name)=(any) is not present in table jobs'})

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return db_data


# Return Single Job By ID
@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=val_jobs.JobOut)
@logger.catch()
def get_job(id: int, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):
    try:
        db_data = db.query(mdl_jobs.Jobs).filter(
            mdl_jobs.Jobs.id == id).first()
        if not db_data:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'detail': f'Key (id)=({id}) is not present in table jobs'})

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return db_data


# Update Job By ID
@router.put('/{id}', status_code=status.HTTP_200_OK, response_model=val_jobs.JobOut)
@logger.catch()
def update_job(id: int, job: val_jobs.JobUpdate, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):
    try:
        query = db.query(mdl_jobs.Jobs).filter(mdl_jobs.Jobs.id == id)
        does_exist = query.first()
        if not does_exist:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'detail': f'Key (id)=({id}) is not present in table jobs'})

        does_exist_name = db.query(mdl_jobs.Jobs).filter(
            mdl_jobs.Jobs.name == mdl_jobs.Jobs.name).first()
        if does_exist_name and does_exist_name.id != id:
            return JSONResponse(status_code=status.HTTP_226_IM_USED, content={'detail': f'Key (name)=({job.name}) violates unique constraint on column jobs.name'})

        new_dict = job.dict()
        new_dict['updated_by'] = current_user.id
        query.update(new_dict, synchronize_session=False)
        db.commit()
        db_data = query.first()

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return db_data


# Delete User By ID
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
@logger.catch()
def delete_job(id: int, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):
    try:
        query = db.query(mdl_jobs.Jobs).filter(mdl_jobs.Jobs.id == id)
        does_exist = query.first()
        if not does_exist:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'detail': f'Key (id)=({id}) is not present in table jobs'})

        query.delete(synchronize_session=False)
        db.commit()

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(status_code=status.HTTP_205_RESET_CONTENT)
