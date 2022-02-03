from fastapi import status, Response, Depends, APIRouter
from ratelimit.decorators import sleep_and_retry
from ..database.database import cursor, conn, get_db
from .. validators import val_brands_brewing, val_user
from ..oauth2.oauth2 import get_current_user
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from .. models import mdl_brands
from loguru import logger
from typing import List


router = APIRouter(prefix='/brands/brewing', tags=['Brewing Brands'])


# Validaton: api/validators/val_brands.py
# Model: api/models/mdl_brands.py


# Create New Brewing Brand
@router.post('', status_code=status.HTTP_201_CREATED, response_model=val_brands_brewing.BrandBrewingOut)
@logger.catch()
def create_brewing_brand(brand: val_brands_brewing.BrandBrewingCreate, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):
    if current_user.permissions < 6:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={'detail': 'unauthorized'})

    try:
        does_exist = db.query(mdl_brands.BrandBrw.name).filter(
            mdl_brands.BrandBrw.name == brand.name).first()
        if does_exist:
            return JSONResponse(status_code=status.HTTP_226_IM_USED, content={'detail': f'Key (name)=({brand.name}) violates unique contraint on column brand_brewing.name'})

        db_data = mdl_brands.BrandBrw(
            created_by=current_user.id, updated_by=current_user.id, **brand.dict())
        db.add(db_data)
        db.commit()
        db.refresh(db_data)

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return db_data


# Return List Of All Brewing Brands
@router.get('', status_code=status.HTTP_200_OK, response_model=List[val_brands_brewing.BrandBrewingOut])
@logger.catch()
def get_brewing_brands(active: bool = True, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):
    if current_user.permissions < 1:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={'detail': 'unauthorized'})

    try:
        db_data = db.query(mdl_brands.BrandBrw).filter(mdl_brands.BrandBrw.is_active == active).order_by(
            mdl_brands.BrandBrw.name).all()

        if not db_data:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'detail': f'Key (name)=(all) are not present in table brand_brewing'})

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return db_data


# Return Single Brewing Brand By ID
@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=val_brands_brewing.BrandBrewingOut)
@logger.catch()
def get_brewing_brand(id: int, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):
    if current_user.permissions < 1:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={'detail': 'unauthorized'})

    try:
        db_data = db.query(mdl_brands.BrandBrw).filter(
            mdl_brands.BrandBrw.id == id).first()
        if not db_data:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'detail': f'Key (id)=({id}) id not present in table brand_brewing'})

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return db_data


# Update Brewing Brand By ID
@router.put('/{id}', status_code=status.HTTP_200_OK, response_model=val_brands_brewing.BrandBrewingOut)
@logger.catch()
def update_brewing_brand(id: int, brand: val_brands_brewing.BrandBrewingUpdate, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):
    if current_user.permissions < 6:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={'detail': 'unauthorized'})

    try:
        query = db.query(mdl_brands.BrandBrw).filter(
            mdl_brands.BrandBrw.id == id)

        does_exist = query.first()
        if not does_exist:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'detail': f'Key (id)=({id}) is not present in table brand_brewing'})

        does_exist = db.query(mdl_brands.BrandBrw).filter(
            mdl_brands.BrandBrw.name == brand.name).first()
        if does_exist and does_exist.id != id:
            return JSONResponse(status_code=status.HTTP_226_IM_USED, content={'detail': f'Key (name)=({brand.name}) violates unique contraint on column brand_brewing.name'})

        new_dict = brand.dict()
        new_dict['updated_by'] = current_user.id
        query.update(new_dict, synchronize_session=False)
        db.commit()
        db_data = query.first()

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return db_data


# Delete Brewing Brand By ID
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
@logger.catch()
def delete_brewing_brand(id: int, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):
    if current_user.permissions < 7:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={'detail': 'unauthorized'})

    try:
        query = db.query(mdl_brands.BrandBrw).filter(
            mdl_brands.BrandBrw.id == id)
        if not query.first():
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'detail': f'Key (id)=({id}) is not present in table brand_brewing'})

        query.delete(synchronize_session=False)
        db.commit()

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(status_code=status.HTTP_205_RESET_CONTENT)


# Update Method Acx
@router.put('/method/acx/{id}', status_code=status.HTTP_200_OK, response_model=val_brands_brewing.BrandBrewingMethodsAcxOut)
@logger.catch()
def update_brewing_brand_method_acx(id: int, brand: val_brands_brewing.BrandBrewingMethodsAcx, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):
    if current_user.permissions < 6:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={'detail': 'unauthorized'})

    try:
        query = db.query(mdl_brands.BrandBrw).filter(
            mdl_brands.BrandBrw.id == id)
        does_exist = query.first()
        if not does_exist:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'detail': f'Key (id)=({id}) is not present in table brand_brewing'})

        new_dict = brand.dict()
        new_dict['updated_by'] = current_user.id
        query.update(new_dict, synchronize_session=False)
        db.commit()

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return query.first()


# Update Method Csx
@router.put('/method/csx/{id}', status_code=status.HTTP_200_OK, response_model=val_brands_brewing.BrandBrewingMethodsCsxOut)
@logger.catch()
def update_brewing_brand_method_csx(id: int, brand: val_brands_brewing.BrandBrewingMethodsCsx, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):
    if current_user.permissions < 6:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={'detail': 'unauthorized'})

    try:
        query = db.query(mdl_brands.BrandBrw).filter(
            mdl_brands.BrandBrw.id == id)
        does_exist = query.first()
        if not does_exist:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'detail': f'Key (id)=({id}) id not present in table brand_brewing'})

        new_dict = brand.dict()
        new_dict['updated_by'] = current_user.id
        query.update(new_dict, synchronize_session=False)
        db.commit()

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return query.first()


# Return Single Brewing Brand Methods By ID
@router.get('/method/{id}', status_code=status.HTTP_200_OK, response_model=val_brands_brewing.BrandBrewingMethodsOut)
@logger.catch()
def get_brewing_brand_methods(id: int, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):
    if current_user.permissions < 1:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={'detail': 'unauthorized'})

    try:
        db_data = db.query(mdl_brands.BrandBrw).filter(
            mdl_brands.BrandBrw.id == id).first()
        if not db_data:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'detail': f'Key (id)=({id}) are not present in table brand_brewing'})

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return db_data
