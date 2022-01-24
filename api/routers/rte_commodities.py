from fastapi import status, Response, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from .. database.database import get_db
from .. validators import val_user, val_commodities
from .. models import mdl_commodities
from .. oauth2.oauth2 import get_current_user

router = APIRouter(prefix='/commodities', tags=['Commodities'])


# Validaton: api/validators/val_commodities.py
# Model: api/models/mdl_commodities.py


# Create New Commodity
@router.post('', status_code=status.HTTP_201_CREATED, response_model=val_commodities.CommodityOut)
def create_commodity(commodity: val_commodities.CommodityCreate, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):

    does_exist_name = db.query(mdl_commodities.Commodities).filter(
        mdl_commodities.Commodities.name_local == commodity.name_local).first()
    if does_exist_name:
        raise HTTPException(status_code=status.HTTP_226_IM_USED,
                            detail=f'commodity local: {commodity.name_local} already exists')

    does_exist_name = db.query(mdl_commodities.Commodities).filter(
        mdl_commodities.Commodities.name_bit == commodity.name_bit).first()
    if does_exist_name:
        raise HTTPException(status_code=status.HTTP_226_IM_USED,
                            detail=f'commodity bit: {commodity.name_bit} already exists')

    db_data = mdl_commodities.Commodities(
        created_by=current_user.id, updated_by=current_user.id, **commodity.dict())
    db.add(db_data)
    db.commit()
    db.refresh(db_data)

    return db_data


# Return List Of All Commodities
@router.get('', status_code=status.HTTP_200_OK, response_model=List[val_commodities.CommodityOut])
def get_commodities(db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):

    db_data = db.query(mdl_commodities.Commodities).order_by(
        mdl_commodities.Commodities.name_local).all()
    if not db_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='commodities do not exist')

    return db_data


# Return Single Commodity By ID
@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=val_commodities.CommodityOut)
def get_commodity(id: int, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):

    db_data = db.query(mdl_commodities.Commodities).filter(
        mdl_commodities.Commodities.id == id).first()
    if not db_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'commodity with id: {id} does not exist')

    return db_data


# Update Commodity By ID
@router.put('/{id}', status_code=status.HTTP_200_OK, response_model=val_commodities.CommodityOut)
def update_job(id: int, commodity: val_commodities.CommodityUpdate, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):

    query = db.query(mdl_commodities.Commodities).filter(
        mdl_commodities.Commodities.id == id)
    does_exist = query.first()
    if not does_exist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'commodity with id: {id} does not exist')

    does_exist_name = db.query(mdl_commodities.Commodities).filter(
        mdl_commodities.Commodities.name_local == commodity.name_local).first()
    if does_exist_name and does_exist_name.id != id:
        raise HTTPException(status_code=status.HTTP_226_IM_USED,
                            detail=f'commodity local: {commodity.name_local} already exists')

    does_exist_name = db.query(mdl_commodities.Commodities).filter(
        mdl_commodities.Commodities.name_bit == commodity.name_bit).first()
    if does_exist_name and does_exist_name.id != id:
        raise HTTPException(status_code=status.HTTP_226_IM_USED,
                            detail=f'commodity bit: {commodity.name_bit} already exists')

    new_dict = commodity.dict()
    new_dict['updated_by'] = current_user.id
    query.update(new_dict, synchronize_session=False)
    db.commit()

    return query.first()


# Delete Commodity By ID
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_job(id: int, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):

    query = db.query(mdl_commodities.Commodities).filter(
        mdl_commodities.Commodities.id == id)
    if not query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'comodity with id: {id} does not exist')

    query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_205_RESET_CONTENT)
