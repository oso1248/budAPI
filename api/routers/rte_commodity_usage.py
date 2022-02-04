from fastapi import status, Response, Depends, APIRouter
from sqlalchemy.sql.expression import desc
from .. models import mdl_commodities, mdl_brands
from .. validators import val_user, val_commodity_usage
from .. oauth2.oauth2 import get_current_user
from fastapi.responses import JSONResponse
from .. database.database import get_db
from sqlalchemy.orm import Session
from loguru import logger
from typing import List
from sqlalchemy import func, desc


router = APIRouter(prefix='/commodity/usage', tags=['Commodity Usage'])


# Validaton: api/validators/val_commodity_usage.py
# Model: api/models/mdl_commodities.py


# Create New Commodity Usage
@router.post('', status_code=status.HTTP_201_CREATED, response_model=val_commodity_usage.CommodityUsageOut)
@logger.catch
def create_commodity_usage(commodity: val_commodity_usage.CommodityUsageIn, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):
    if current_user.permissions < 6:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={'detail': 'unauthorized'})

    try:
        does_exist = db.query(mdl_commodities.Commodities).filter(
            mdl_commodities.Commodities.id == commodity.id_commodity).first()
        if not does_exist:
            return JSONResponse(status_code=status.HTTP_226_IM_USED, content={'detail': f'Key (id_commodity)=({commodity.id_commodity}) does not exist in table commodities'})

        does_exist = db.query(mdl_brands.BrandBrw).filter(
            mdl_brands.BrandBrw.id == commodity.id_brand_brewing).first()
        if not does_exist:
            return JSONResponse(status_code=status.HTTP_226_IM_USED, content={'detail': f'Key (id_brand_brewing)=({commodity.id_brand_brewing}) does not exist in table brand_brewing'})

        does_exist = db.query(mdl_commodities.CommoditiesBridge).filter(
            mdl_commodities.CommoditiesBridge.id_brand_brewing == commodity.id_brand_brewing,
            mdl_commodities.CommoditiesBridge.id_commodity == commodity.id_commodity,
            mdl_commodities.CommoditiesBridge.id_brewhouse == commodity.id_brewhouse).first()
        if does_exist:
            return JSONResponse(status_code=status.HTTP_226_IM_USED, content={'detail': f'Key (id_commodity, id_brand_brewing, id_brewhouse)=({commodity.id_commodity}, {commodity.id_brand_brewing}, {commodity.id_brewhouse}) violates composite key constraint on table bridge_commodities'})

        db_data = mdl_commodities.CommoditiesBridge(
            created_by=current_user.id, updated_by=current_user.id, **commodity.dict())
        db.add(db_data)
        db.commit()
        db.refresh(db_data)

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return db_data


# Update Commodity Usage
@router.put('', status_code=status.HTTP_200_OK, response_model=val_commodity_usage.CommodityUsageOut)
@logger.catch
def update_commodity_usage(commodity: val_commodity_usage.CommodityUsageIn, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):
    if current_user.permissions < 6:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={'detail': 'unauthorized'})

    try:
        query = db.query(mdl_commodities.CommoditiesBridge).filter(
            mdl_commodities.CommoditiesBridge.id_brand_brewing == commodity.id_brand_brewing,
            mdl_commodities.CommoditiesBridge.id_commodity == commodity.id_commodity,
            mdl_commodities.CommoditiesBridge.id_brewhouse == commodity.id_brewhouse)
        does_exist = query.first()
        if not does_exist:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'detail': f'Key (id_commodity, id_brand_brewing)=({commodity.id_commodity}, {commodity.id_brand_brewing}) does not exist in table bridge_commodities'})

        new_dict = commodity.dict()
        new_dict['updated_by'] = current_user.id
        query.update(new_dict, synchronize_session=False)
        db.commit()
        db_data = query.first()

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return db_data


# Delete Commodity Usage
@router.delete('', status_code=status.HTTP_201_CREATED)
@logger.catch
def delete_commodity_usage(commodity: val_commodity_usage.CommodityUsageDelete, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):
    if current_user.permissions < 6:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={'detail': 'unauthorized'})

    try:
        query = db.query(mdl_commodities.CommoditiesBridge).filter(
            mdl_commodities.CommoditiesBridge.id_brand_brewing == commodity.id_brand_brewing,
            mdl_commodities.CommoditiesBridge.id_commodity == commodity.id_commodity,
            mdl_commodities.CommoditiesBridge.id_brewhouse == commodity.id_brewhouse)
        does_exist = query.first()
        if not does_exist:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'detail': f'Key (id_commodity, id_brand_brewing)=({commodity.id_commodity}, {commodity.id_brand_brewing}) does not exist in table bridge_commodities'})

        query.delete(synchronize_session=False)
        db.commit()

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(status_code=status.HTTP_205_RESET_CONTENT)


# Return List of Commodity Brand Usage
@router.get('/commodity/{id}', status_code=status.HTTP_200_OK, response_model=List[val_commodity_usage.CommodityUsageOut])
@logger.catch()
def get_commodity_usage_by_commodity_id(id: int, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):
    if current_user.permissions < 1:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={'detail': 'unauthorized'})
    try:
        db_data = db.query(mdl_commodities.CommoditiesBridge).join(
            mdl_commodities.Commodities, mdl_commodities.CommoditiesBridge.id_commodity == mdl_commodities.Commodities.id).join(
            mdl_brands.BrandBrw, mdl_commodities.CommoditiesBridge.id_brand_brewing == mdl_brands.BrandBrw.id).order_by(mdl_commodities.CommoditiesBridge.id_brewhouse,
                                                                                                                        mdl_brands.BrandBrw.name).filter(mdl_commodities.CommoditiesBridge.id_commodity == id).all()
        if not db_data:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'detail': f'Key (id_commodity)=({id}) is not present in table bridge_users_jobs'})

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return db_data


# Return List of Brand Commodity Usage
@router.get('/brand/{id}', status_code=status.HTTP_200_OK, response_model=List[val_commodity_usage.CommodityUsageOut])
@logger.catch()
def get_commodity_usage_by_brand_id(id: int, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):
    if current_user.permissions < 1:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={'detail': 'unauthorized'})
    try:
        db_data = db.query(mdl_commodities.CommoditiesBridge).join(
            mdl_commodities.Commodities, mdl_commodities.CommoditiesBridge.id_commodity == mdl_commodities.Commodities.id).join(
            mdl_brands.BrandBrw, mdl_commodities.CommoditiesBridge.id_brand_brewing == mdl_brands.BrandBrw.id).order_by(
                mdl_commodities.Commodities.name_local).filter(mdl_commodities.CommoditiesBridge.id_brand_brewing == id).all()
        if not db_data:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'detail': f'Key (id_brand_brewing)=({id}) is not present in table bridge_users_jobs'})

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return db_data
