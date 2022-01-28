from fastapi import status, Response, Depends, APIRouter
from .. database.database import cursor, conn, get_db
from .. validators import val_user, val_brands
from .. oauth2.oauth2 import get_current_user
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from .. models import mdl_brands
from loguru import logger
from typing import List


router = APIRouter(prefix='/brands', tags=['Brands'])


# Validaton: api/validators/val_brands.py
# Model: api/models/mdl_brands.py


# Brewing Brands
# Create New Brewing Brand
@router.post('/brewing', status_code=status.HTTP_201_CREATED, response_model=val_brands.BrandBrewingOut)
@logger.catch()
def create_brewing_brand(brand: val_brands.BrandBrewingCreate, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):
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
@router.get('/brewing', status_code=status.HTTP_200_OK, response_model=List[val_brands.BrandBrewingOut])
@logger.catch()
def get_brewing_brands(active: str = True, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):
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
@router.get('/brewing/{id}', status_code=status.HTTP_200_OK, response_model=val_brands.BrandBrewingOut)
@logger.catch()
def get_brewing_brand(id: int, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):
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
@router.put('/brewing/{id}', status_code=status.HTTP_200_OK, response_model=val_brands.BrandBrewingOut)
@logger.catch()
def update_brewing_brand(id: int, brand: val_brands.BrandBrewingUpdate, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):
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
@router.delete('/brewing/{id}', status_code=status.HTTP_204_NO_CONTENT)
@logger.catch()
def delete_brewing_brand(id: int, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):
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
@router.put('/brewing/method/acx/{id}', status_code=status.HTTP_200_OK, response_model=val_brands.BrandBrewingMethodsAcxOut)
@logger.catch()
def update_brewing_brand_method_acx(id: int, brand: val_brands.BrandBrewingMethodsAcx, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):
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
@router.put('/brewing/method/csx/{id}', status_code=status.HTTP_200_OK, response_model=val_brands.BrandBrewingMethodsCsxOut)
@logger.catch()
def update_brewing_brand_method_csx(id: int, brand: val_brands.BrandBrewingMethodsCsx, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):
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
@router.get('/brewing/method/{id}', status_code=status.HTTP_200_OK, response_model=val_brands.BrandBrewingMethodsOut)
@logger.catch()
def get_brewing_brand_methods(id: int, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):
    try:
        db_data = db.query(mdl_brands.BrandBrw).filter(
            mdl_brands.BrandBrw.id == id).first()
        if not db_data:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'detail': f'Key (id)=({id}) are not present in table brand_brewing'})

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return db_data


# Finishing Brands
# Create New Finishing Brand
@router.post('/finishing', status_code=status.HTTP_201_CREATED, response_model=val_brands.BrandFinishingOut)
@logger.catch()
def create_finishing_brand(brand: val_brands.BrandFinishingCreate, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):
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
@router.get('/finishing', status_code=status.HTTP_200_OK, response_model=List[val_brands.BrandFinishingOut])
@logger.catch()
def get_finishing_brands(active: str = True, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):
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
@router.get('/finishing/{id}', status_code=status.HTTP_200_OK, response_model=val_brands.BrandFinishingOut)
@logger.catch()
def get_finishing_brand(id: int, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):
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
@router.put('/finishing/{id}', status_code=status.HTTP_200_OK, response_model=val_brands.BrandFinishingOut)
@logger.catch()
def update_finishing_brand(id: int, brand: val_brands.BrandFinishingUpdate, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):
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
@router.delete('/finishing/{id}', status_code=status.HTTP_205_RESET_CONTENT)
@logger.catch()
def delete_finishing_brand(id: int, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):
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
@router.put('/finishing/method/filters/{id}', status_code=status.HTTP_200_OK, response_model=val_brands.BrandFinishingMethodsFiltersOut)
@logger.catch()
def update_finishing_brand_method_filters(id: int, brand: val_brands.BrandFinishingMethodsFilters, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):
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
@router.put('/finishing/method/releasing/{id}', status_code=status.HTTP_200_OK, response_model=val_brands.BrandFinishingMethodsReleasingOut)
@logger.catch()
def update_finishing_brand_method_releasing(id: int, brand: val_brands.BrandFinishingMethodsReleasing, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):
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
@router.get('/finishing/method/{id}', status_code=status.HTTP_200_OK, response_model=val_brands.BrandFinishingMethodsOut)
@logger.catch()
def get_finishing_brand_methods(id: int, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):
    try:
        db_data = db.query(mdl_brands.BrandFin).filter(
            mdl_brands.BrandFin.id == id).first()
        if not db_data:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'detail': f'Key (id)=({id}) is not present in table brand_finishing'})

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return db_data


# Packaging Brands
# Create New Packaging Brand
@router.post('/packaging', status_code=status.HTTP_201_CREATED, response_model=val_brands.BrandPackagingOut)
@logger.catch()
def create_packaging_brand(brand: val_brands.BrandPackagingCreate, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):
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
@router.get('/packaging', status_code=status.HTTP_200_OK, response_model=List[val_brands.BrandPackagingOut])
@logger.catch()
def get_packaging_brands(active: str = True, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):
    try:
        db_data = db.query(mdl_brands.BrandPck).filter(mdl_brands.BrandPck == active).order_by(
            mdl_brands.BrandPck.name).all()
        if not db_data:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'detail': 'Key (name)=(all) are not present in table brand_packaging'})

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return db_data


# Return Single Packaging Brand By ID
@router.get('/packaging/{id}', status_code=status.HTTP_200_OK, response_model=val_brands.BrandPackagingOut)
@logger.catch()
def get_packaging_brand(id: int, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):
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
@router.put('/packaging/{id}', status_code=status.HTTP_200_OK, response_model=val_brands.BrandPackagingOut)
@logger.catch()
def update_finishing_brand(id: int, brand: val_brands.BrandPackagingUpdate, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):
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
@router.delete('/packaging/{id}', status_code=status.HTTP_204_NO_CONTENT)
@logger.catch()
def delete_finishing_brand(id: int, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):
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
