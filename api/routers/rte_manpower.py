from fastapi import status, Response, Depends, APIRouter
from .. database.database import cursor, conn, get_db
from .. validators import val_user, val_manpower
from .. oauth2.oauth2 import get_current_user
from fastapi.responses import JSONResponse
from .. models import mdl_manpower
from sqlalchemy.orm import Session
from loguru import logger
from typing import List


router = APIRouter(prefix='/manpower', tags=['Manpower'])


# Validaton: api/validators/val_manpower.py
# Model: api/models/mdl_manpower.py


# Create New Manpower Individual Entry
@router.post('/individual', status_code=status.HTTP_201_CREATED, response_model=val_manpower.ManPowerIndividualOut)
@logger.catch()
def create_individual_entry(job_assignment: val_manpower.ManPowerIndividualIn, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):
    if current_user.permissions < 5:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={'detail': 'unauthorized'})

    try:
        db_data = mdl_manpower.ManpowerIndividual(
            created_by=current_user.id, **job_assignment.dict())
        db.add(db_data)
        db.commit()
        db.refresh(db_data)

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return db_data


# Get Manpower Individual
@router.get('/individual', status_code=status.HTTP_200_OK, response_model=List[val_manpower.ManPowerIndividualOut])
@logger.catch()
def get_individual_entries(dt: val_manpower.ManPowerIndividualDatesIn, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):
    if current_user.permissions < 1:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={'detail': 'unauthorized'})
    try:
        db_data = db.query(mdl_manpower.ManpowerIndividual).filter(
            mdl_manpower.ManpowerIndividual.created_at > dt.start,
            mdl_manpower.ManpowerIndividual.created_at < dt.stop,
            mdl_manpower.ManpowerIndividual.shift == dt.shift).order_by(
            mdl_manpower.ManpowerIndividual.id).all()

        if not db_data:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND)

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return db_data


# Delete Entry Manpower Individual Entry
@router.delete('/individual/{id}', status_code=status.HTTP_204_NO_CONTENT)
@logger.catch()
def delete_individual_entry(id: int, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):
    if current_user.permissions < 5:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={'detail': 'unauthorized'})

    try:
        query = db.query(mdl_manpower.ManpowerIndividual).filter(
            mdl_manpower.ManpowerIndividual.id == id)
        does_exist = query.first()
        if not does_exist:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'detail': f'Key (id)=({id}) is not present in table manpower_individual'})

        query.delete(synchronize_session=False)
        db.commit()

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(status_code=status.HTTP_205_RESET_CONTENT)


# Create New Manpower Group Entry
@router.post('/group', status_code=status.HTTP_201_CREATED, response_model=val_manpower.ManPowerGroupOut)
@logger.catch()
def create_group_entry(group_assignment: val_manpower.ManPowerGroupIn, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):
    if current_user.permissions < 5:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={'detail': 'unauthorized'})

    try:
        db_data = mdl_manpower.ManpowerGroup(
            created_by=current_user.id, **group_assignment.dict())
        db.add(db_data)
        db.commit()
        db.refresh(db_data)

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return db_data


# Get Manpower Group
@router.get('/group', status_code=status.HTTP_200_OK, response_model=List[val_manpower.ManPowerGroupOut])
@logger.catch()
def get_group_entries(dt: val_manpower.ManPowerGroupDatesIn, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):
    if current_user.permissions < 1:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={'detail': 'unauthorized'})

    try:
        db_data = db.query(mdl_manpower.ManpowerGroup).filter(
            mdl_manpower.ManpowerGroup.created_at > dt.start,
            mdl_manpower.ManpowerGroup.created_at < dt.stop,
            mdl_manpower.ManpowerGroup.shift == dt.shift).order_by(
            mdl_manpower.ManpowerGroup.id).all()

        if not db_data:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND)

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return db_data


# Delete Manpower Group Entry
@router.delete('/group/{id}', status_code=status.HTTP_204_NO_CONTENT)
@logger.catch()
def delete_group_entry(id: int, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):
    if current_user.permissions < 5:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={'detail': 'unauthorized'})

    try:
        query = db.query(mdl_manpower.ManpowerGroup).filter(
            mdl_manpower.ManpowerGroup.id == id)

        does_exist = query.first()
        if not does_exist:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'detail': f'Key (id)=({id}) is not present in table manpower_group'})

        query.delete(synchronize_session=False)
        db.commit()

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(status_code=status.HTTP_205_RESET_CONTENT)
