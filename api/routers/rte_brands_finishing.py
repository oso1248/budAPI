from fastapi import status, Response, Depends, APIRouter
from .. database.database import cursor, conn, get_db
from .. validators import val_brands_finishing, val_user
from .. oauth2.oauth2 import get_current_user
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from .. models import mdl_brands
from loguru import logger
from typing import List


router = APIRouter(prefix='/brands/finishing', tags=['Finishing Brands'])


# Validaton: api/validators/val_brands.py
# Model: api/models/mdl_brands.py


# Create New Finishing Brand
@router.post('', status_code=status.HTTP_201_CREATED, response_model=val_brands_finishing.BrandFinishingOut)
@logger.catch()
def create_finishing_brand(brand: val_brands_finishing.BrandFinishingCreate, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):
    if current_user.permissions < 6:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={'detail': 'unauthorized'})

    try:
        does_exist = db.query(mdl_brands.BrandFin).filter(
            mdl_brands.BrandFin.name == brand.name).first()
        if does_exist:
            return JSONResponse(status_code=status.HTTP_226_IM_USED, content={'detail': f'Key (name)=({brand.name}) violates unique contraint on column brand_finishing.name'})

        does_exist = db.query(mdl_brands.BrandBrw).filter(
            mdl_brands.BrandBrw.id == brand.id_brewing).first()
        if not does_exist:
            return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content={'detail': f'Key (id_brewing)=({brand.id_brewing}) is not present in table brand_brewing'})

        db_data = mdl_brands.BrandFin(
            created_by=current_user.id, updated_by=current_user.id, **brand.dict())
        db.add(db_data)
        db.commit()
        db.refresh(db_data)

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return db_data


# Return List Of All Finishing Brands
@router.get('', status_code=status.HTTP_200_OK, response_model=List[val_brands_finishing.BrandFinishingOut])
@logger.catch()
def get_finishing_brands(active: bool = True, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):
    if current_user.permissions < 1:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={'detail': 'unauthorized'})
    try:
        db_data = db.query(mdl_brands.BrandFin).filter(mdl_brands.BrandFin.is_active == active).order_by(
            mdl_brands.BrandFin.name).all()
        if not db_data:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'detail': 'Key (name)=(all) are not present in table brand_finishing'})

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return db_data


# Return Single Finishing Brand By ID
@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=val_brands_finishing.BrandFinishingOut)
@logger.catch()
def get_finishing_brand(id: int, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):
    if current_user.permissions < 1:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={'detail': 'unauthorized'})
    try:
        db_data = db.query(mdl_brands.BrandFin).filter(
            mdl_brands.BrandFin.id == id).first()

        if not db_data:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'detail': f'Key (id)=({id}) is not present in table brand_finishing'})

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return db_data


# Update Finishing Brand By ID
@router.put('/{id}', status_code=status.HTTP_200_OK, response_model=val_brands_finishing.BrandFinishingOut)
@logger.catch()
def update_finishing_brand(id: int, brand: val_brands_finishing.BrandFinishingUpdate, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):
    if current_user.permissions < 6:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={'detail': 'unauthorized'})

    try:
        query = db.query(mdl_brands.BrandFin).filter(
            mdl_brands.BrandFin.id == id)
        update = query.first()
        if not update:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'detail': f'Key (id)=({id}) is not present in table brand_finishing'})

        does_exist = db.query(mdl_brands.BrandFin).filter(
            mdl_brands.BrandFin.name == brand.name).first()
        if does_exist and does_exist.id != id:
            return JSONResponse(status_code=status.HTTP_226_IM_USED, content={'detail': f'Key (name)=({brand.name}) violates unique constraint on column brand_finishing.name'})

        does_exist = db.query(mdl_brands.BrandBrw).filter(
            mdl_brands.BrandBrw.id == brand.id_brewing).first()
        if not does_exist:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'detail': f'Key (id_brewing)=({brand.id_brewing}) is not present in table brand_brewing'})

        new_dict = brand.dict()
        new_dict['updated_by'] = current_user.id
        query.update(new_dict, synchronize_session=False)
        db.commit()

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return query.first()


# Delete Finishing Brand By ID
@router.delete('/{id}', status_code=status.HTTP_205_RESET_CONTENT)
@logger.catch()
def delete_finishing_brand(id: int, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):
    if current_user.permissions < 7:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={'detail': 'unauthorized'})

    try:
        query = db.query(mdl_brands.BrandFin).filter(
            mdl_brands.BrandFin.id == id)
        if not query.first():
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'detail': f'Key (id)=({id}) is not present in table brand_finishing'})

        query.delete(synchronize_session=False)
        db.commit()

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(status_code=status.HTTP_205_RESET_CONTENT)


# Update Method Filters
@router.put('/method/filters/{id}', status_code=status.HTTP_200_OK, response_model=val_brands_finishing.BrandFinishingMethodsFiltersOut)
@logger.catch()
def update_finishing_brand_method_filters(id: int, brand: val_brands_finishing.BrandFinishingMethodsFilters, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):
    if current_user.permissions < 6:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={'detail': 'unauthorized'})

    try:
        query = db.query(mdl_brands.BrandFin).filter(
            mdl_brands.BrandFin.id == id)
        update = query.first()
        if not update:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'detail': f'Key (id)=({id}) is not present in table brand_finishing'})

        new_dict = brand.dict()
        new_dict['updated_by'] = current_user.id
        query.update(new_dict, synchronize_session=False)
        db.commit()

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return query.first()


# Update Method Releasing
@router.put('/method/releasing/{id}', status_code=status.HTTP_200_OK, response_model=val_brands_finishing.BrandFinishingMethodsReleasingOut)
@logger.catch()
def update_finishing_brand_method_releasing(id: int, brand: val_brands_finishing.BrandFinishingMethodsReleasing, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):
    if current_user.permissions < 6:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={'detail': 'unauthorized'})

    try:
        query = db.query(mdl_brands.BrandFin).filter(
            mdl_brands.BrandFin.id == id)
        update = query.first()
        if not update:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'detail': f'Key (id)=({id}) is not present in table brand_finishing'})

        new_dict = brand.dict()
        new_dict['updated_by'] = current_user.id
        query.update(new_dict, synchronize_session=False)
        db.commit()

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return query.first()


# Return Single Finishing Brand Method By ID
@router.get('/method/{id}', status_code=status.HTTP_200_OK, response_model=val_brands_finishing.BrandFinishingMethodsOut)
@logger.catch()
def get_finishing_brand_methods(id: int, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):
    if current_user.permissions < 1:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={'detail': 'unauthorized'})
    try:
        db_data = db.query(mdl_brands.BrandFin).filter(
            mdl_brands.BrandFin.id == id).first()
        if not db_data:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'detail': f'Key (id)=({id}) is not present in table brand_finishing'})

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return db_data
