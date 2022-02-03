from fastapi import status, Response, Depends, APIRouter
from ..database.database import cursor, conn, get_db
from .. validators import val_brands_packaging, val_user
from ..oauth2.oauth2 import get_current_user
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from .. models import mdl_brands
from loguru import logger
from typing import List


router = APIRouter(prefix='/brands/packaging', tags=['Packaging Brands'])


# Validaton: api/validators/val_brands.py
# Model: api/models/mdl_brands.py


# Create New Packaging Brand
@router.post('', status_code=status.HTTP_201_CREATED, response_model=val_brands_packaging.BrandPackagingOut)
@logger.catch()
def create_packaging_brand(brand: val_brands_packaging.BrandPackagingCreate, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):
    if current_user.permissions < 6:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={'detail': 'unauthorized'})

    try:
        does_exist = db.query(mdl_brands.BrandPck.name).filter(
            mdl_brands.BrandPck.name == brand.name).first()
        if does_exist:
            return JSONResponse(status_code=status.HTTP_226_IM_USED, content={'detail': f'Key (name)=({brand.name}) violates unique constraint on column brand_packaging.name'})

        does_exist = db.query(mdl_brands.BrandFin).filter(
            mdl_brands.BrandFin.id == brand.id_finishing).first()
        if not does_exist:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'detail': f'Key (id)=({brand.id_finishing}) is not present in table brand_finishing'})

        db_data = mdl_brands.BrandPck(
            created_by=current_user.id, updated_by=current_user.id, **brand.dict())
        db.add(db_data)
        db.commit()
        db.refresh(db_data)

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return db_data


# Return List Of All Packaging Brands
@router.get('', status_code=status.HTTP_200_OK, response_model=List[val_brands_packaging.BrandPackagingOut])
@logger.catch()
def get_packaging_brands(active: bool = True, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):
    if current_user.permissions < 1:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={'detail': 'unauthorized'})

    try:
        db_data = db.query(mdl_brands.BrandPck).filter(mdl_brands.BrandPck.is_active == active).order_by(
            mdl_brands.BrandPck.name).all()
        if not db_data:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'detail': 'Key (name)=(all) are not present in table brand_packaging'})

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return db_data


# Return Single Packaging Brand By ID
@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=val_brands_packaging.BrandPackagingOut)
@logger.catch()
def get_packaging_brand(id: int, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):
    if current_user.permissions < 1:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={'detail': 'unauthorized'})

    try:
        db_data = db.query(mdl_brands.BrandPck).filter(
            mdl_brands.BrandPck.id == id).first()
        if not db_data:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'detail': f'Key (id)=({id}) is not present in table brand_packaging'})

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return db_data


# Update Packaging Brand By ID
@router.put('/{id}', status_code=status.HTTP_200_OK, response_model=val_brands_packaging.BrandPackagingOut)
@logger.catch()
def update_finishing_brand(id: int, brand: val_brands_packaging.BrandPackagingUpdate, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):
    if current_user.permissions < 6:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={'detail': 'unauthorized'})

    try:
        query = db.query(mdl_brands.BrandPck).filter(
            mdl_brands.BrandPck.id == id)
        update = query.first()
        if not update:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'detail': f'Key (id)=({id}) is not present in table brand_packaging'})

        does_exist = db.query(mdl_brands.BrandPck).filter(
            mdl_brands.BrandPck.name == brand.name).first()
        if does_exist and does_exist.id != id:
            return JSONResponse(status_code=status.HTTP_226_IM_USED, content={'detail': f'Brand:{brand.name} is already used.'})

        does_exist = db.query(mdl_brands.BrandFin).filter(
            mdl_brands.BrandFin.id == brand.id_finishing).first()
        if not does_exist:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'detail': f'Key (id)=({id}) is not present in table brand_finishing'})

        new_dict = brand.dict()
        new_dict['updated_by'] = current_user.id
        query.update(new_dict, synchronize_session=False)
        db.commit()

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return query.first()


# Delete Packaging Brand By ID
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
@logger.catch()
def delete_finishing_brand(id: int, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):
    if current_user.permissions < 7:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={'detail': 'unauthorized'})

    try:
        query = db.query(mdl_brands.BrandPck).filter(
            mdl_brands.BrandPck.id == id)
        if not query.first():
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'detail': f'Key (id)=({id}) is not present in table brand_packaging'})

        query.delete(synchronize_session=False)
        db.commit()

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(status_code=status.HTTP_205_RESET_CONTENT)
