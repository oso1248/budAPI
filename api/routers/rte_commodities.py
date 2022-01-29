from fastapi import status, Response, Depends, APIRouter
from .. models import mdl_commodities, mdl_suppliers
from .. validators import val_user, val_commodities
from .. oauth2.oauth2 import get_current_user
from fastapi.responses import JSONResponse
from .. database.database import get_db
from sqlalchemy.orm import Session
from loguru import logger
from typing import List
from sqlalchemy import func

router = APIRouter(prefix='/commodities', tags=['Commodities'])


# Validaton: api/validators/val_commodities.py
# Model: api/models/mdl_commodities.py


# Create New Commodity
@router.post('', status_code=status.HTTP_201_CREATED, response_model=val_commodities.CommodityOut)
@logger.catch
def create_commodity(commodity: val_commodities.CommodityCreate, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):
    if current_user.permissions < 4:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={'detail': 'unauthorized'})
    try:
        does_exist = db.query(mdl_commodities.Commodities).filter(
            mdl_commodities.Commodities.name_local == commodity.name_local).first()
        if does_exist:
            return JSONResponse(status_code=status.HTTP_226_IM_USED, content={'detail': f'Key (name)=({commodity.name_local}) violates unique contraint on column commodities.name_local'})

        does_exist = db.query(mdl_commodities.Commodities).filter(
            mdl_commodities.Commodities.name_bit == commodity.name_bit).first()
        if does_exist:
            return JSONResponse(status_code=status.HTTP_226_IM_USED, content={'detail': f'Key (name)=({commodity.name_bit}) violates unique contraint on column commodities.name_bit'})

        does_exist = db.query(mdl_suppliers.Suppliers).filter(
            mdl_suppliers.Suppliers.id == commodity.id_supplier).first()
        if not does_exist:
            return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content={'detail': f'Key (id_supplier)=({commodity.id_supplier}) is not present id table suppliers'})

        db_data = mdl_commodities.Commodities(
            created_by=current_user.id, updated_by=current_user.id, **commodity.dict())
        db.add(db_data)
        db.commit()
        db.refresh(db_data)

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return db_data


# Return List Of All Commodities
@router.get('', status_code=status.HTTP_200_OK, response_model=List[val_commodities.CommodityOut])
@logger.catch()
def get_commodities(active: bool = True, type: str = '', sap: str = '', db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):
    try:
        db_data = db.query(mdl_commodities.Commodities).filter(mdl_commodities.Commodities.is_active == active, func.lower(
            mdl_commodities.Commodities.type).contains(func.lower(type)), mdl_commodities.Commodities.sap.contains(sap)).order_by(mdl_commodities.Commodities.name_local).all()
        if not db_data:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'detail': f'Key (name)=(all) are not present in table commodities'})

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return db_data


# Return Single Commodity By ID
@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=val_commodities.CommodityOut)
@logger.catch()
def get_commodity(id: int, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):
    try:
        db_data = db.query(mdl_commodities.Commodities).filter(
            mdl_commodities.Commodities.id == id).first()
        if not db_data:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'detail': f'Key (id)=({id}) is not present in table commodities'})

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return db_data


# Update Commodity By ID
@router.put('/{id}', status_code=status.HTTP_200_OK, response_model=val_commodities.CommodityOut)
@logger.catch()
def update_job(id: int, commodity: val_commodities.CommodityUpdate, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):
    if current_user.permissions < 4:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={'detail': 'unauthorized'})
    try:
        query = db.query(mdl_commodities.Commodities).filter(
            mdl_commodities.Commodities.id == id)
        does_exist = query.first()
        if not does_exist:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'detail': f'Key (id)=({id}) is not present in table commodities'})

        does_exist_name = db.query(mdl_commodities.Commodities).filter(
            mdl_commodities.Commodities.name_local == commodity.name_local).first()
        if does_exist_name and does_exist_name.id != id:
            return JSONResponse(status_code=status.HTTP_226_IM_USED, content={'detail': f'Key (name)=({commodity.name_local}) violates unique contraint on column commodities.name_local'})

        does_exist_name = db.query(mdl_commodities.Commodities).filter(
            mdl_commodities.Commodities.name_bit == commodity.name_bit).first()
        if does_exist_name and does_exist_name.id != id:
            return JSONResponse(status_code=status.HTTP_226_IM_USED, content={'detail': f'Key (name)=({commodity.name_bit}) violates unique contraint on column commodities.name_bit'})

        does_exist = db.query(mdl_suppliers.Suppliers).filter(
            mdl_suppliers.Suppliers.id == commodity.id_supplier).first()
        if not does_exist:
            return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content={'detail': f'Key (id_supplier)=({commodity.id_supplier}) is not present id table suppliers'})

        new_dict = commodity.dict()
        new_dict['updated_by'] = current_user.id
        query.update(new_dict, synchronize_session=False)
        db.commit()
        db_data = query.first()

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return db_data


# Delete Commodity By ID
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
@logger.catch()
def delete_job(id: int, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):
    if current_user.permissions < 7:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={'detail': 'unauthorized'})

    try:
        query = db.query(mdl_commodities.Commodities).filter(
            mdl_commodities.Commodities.id == id)
        if not query.first():
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'detail': f'Key (id)=({id}) is not present in table commodities'})

        query.delete(synchronize_session=False)
        db.commit()

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(status_code=status.HTTP_205_RESET_CONTENT)
