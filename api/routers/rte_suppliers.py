from fastapi import status, Response, Depends, APIRouter
from .. validators import val_user, val_suppliers
from .. oauth2.oauth2 import get_current_user
from fastapi.responses import JSONResponse
from .. database.database import get_db
from .. models import mdl_suppliers
from sqlalchemy.orm import Session
from loguru import logger
from typing import List


router = APIRouter(prefix='/suppliers', tags=['Suppliers'])


# Validaton: api/validators/val_suppliers.py
# Model: api/models/mdl_suppliers.py


# Create New Supplier
@router.post('', status_code=status.HTTP_201_CREATED, response_model=val_suppliers.SupplierOut)
@logger.catch()
def create_supplier(supplier: val_suppliers.SupplierCreate, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):
    try:
        does_exist = db.query(mdl_suppliers.Suppliers).filter(
            mdl_suppliers.Suppliers.name == supplier.name).first()
        if does_exist:
            return JSONResponse(status_code=status.HTTP_226_IM_USED, content={'detail': f'Key (name)=({supplier.name}) violates unique contraint on column suppliers.name'})

        db_data = mdl_suppliers.Suppliers(
            created_by=current_user.id, updated_by=current_user.id, **supplier.dict())
        db.add(db_data)
        db.commit()
        db.refresh(db_data)

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return db_data


# Return List Of All Suppliers
@router.get('', status_code=status.HTTP_200_OK, response_model=List[val_suppliers.SupplierOut])
@logger.catch()
def get_suppliers(active: bool = True, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):
    try:
        db_data = db.query(mdl_suppliers.Suppliers).filter(mdl_suppliers.Suppliers.is_active == active).order_by(
            mdl_suppliers.Suppliers.name).all()
        if not db_data:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'detail': f'Key (name)=(all) are not present in table suppliers'})

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return db_data


# Return Single Supplier By ID
@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=val_suppliers.SupplierOut)
@logger.catch()
def get_job(id: int, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):
    try:
        db_data = db.query(mdl_suppliers.Suppliers).filter(
            mdl_suppliers.Suppliers.id == id).first()
        if not db_data:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'detail': f'Key (id)=({id}) is not present in table suppliers'})

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return db_data


# Update Supplier By ID
@router.put('/{id}', status_code=status.HTTP_200_OK, response_model=val_suppliers.SupplierOut)
@logger.catch()
def update_job(id: int, supplier: val_suppliers.SupplierUpdate, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):
    try:
        query = db.query(mdl_suppliers.Suppliers).filter(
            mdl_suppliers.Suppliers.id == id)
        does_exist = query.first()
        if not does_exist:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'detail': f'Key (id)=({id}) is not present in table suppliers'})

        does_exist = db.query(mdl_suppliers.Suppliers).filter(
            mdl_suppliers.Suppliers.name == supplier.name).first()
        if does_exist and does_exist.id != id:
            return JSONResponse(status_code=status.HTTP_226_IM_USED, content={'detail': f'Key (name)=({supplier.name}) violates unique constraint on column suppliers.name'})

        new_dict = supplier.dict()
        new_dict['updated_by'] = current_user.id
        query.update(new_dict, synchronize_session=False)
        db.commit()

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return query.first()


# Delete Supplier By ID
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
@logger.catch()
def delete_job(id: int, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):
    try:
        query = db.query(mdl_suppliers.Suppliers).filter(
            mdl_suppliers.Suppliers.id == id)
        if not query.first():
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'detail': f'Key (id)=({id}) is not present in table suppliers'})

        query.delete(synchronize_session=False)
        db.commit()

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(status_code=status.HTTP_205_RESET_CONTENT)
