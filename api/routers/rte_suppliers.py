from fastapi import status, Response, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from .. database.database import get_db
from .. validators import val_user, val_suppliers
from .. models import mdl_suppliers
from .. oauth2.oauth2 import get_current_user

router = APIRouter(prefix='/suppliers', tags=['Suppliers'])


# Validaton: api/validators/val_suppliers.py
# Model: api/models/mdl_suppliers.py


# Create New Supplier
@router.post('', status_code=status.HTTP_201_CREATED, response_model=val_suppliers.SupplierOut)
def create_supplier(supplier: val_suppliers.SupplierCreate, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):

    does_exist_name = db.query(mdl_suppliers.Suppliers).filter(
        mdl_suppliers.Suppliers.name == supplier.name).first()
    if does_exist_name:
        raise HTTPException(status_code=status.HTTP_226_IM_USED,
                            detail=f'supplier: {supplier.name} already exists')

    db_data = mdl_suppliers.Suppliers(
        created_by=current_user.id, updated_by=current_user.id, **supplier.dict())
    db.add(db_data)
    db.commit()
    db.refresh(db_data)

    return db_data


# Return List Of All Suppliers
@router.get('', status_code=status.HTTP_200_OK, response_model=List[val_suppliers.SupplierOut])
def get_suppliers(db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):

    db_data = db.query(mdl_suppliers.Suppliers).order_by(
        mdl_suppliers.Suppliers.name).all()
    if not db_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='suppliers do not exist')

    return db_data


# Return Single Supplier By ID
@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=val_suppliers.SupplierOut)
def get_job(id: int, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):

    db_data = db.query(mdl_suppliers.Suppliers).filter(
        mdl_suppliers.Suppliers.id == id).first()
    if not db_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'supplier with id: {id} does not exist')

    return db_data


# Update Supplier By ID
@router.put('/{id}', status_code=status.HTTP_200_OK, response_model=val_suppliers.SupplierOut)
def update_job(id: int, supplier: val_suppliers.SupplierUpdate, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):

    query = db.query(mdl_suppliers.Suppliers).filter(
        mdl_suppliers.Suppliers.id == id)
    does_exist = query.first()
    if not does_exist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'supplier with id: {id} does not exist')

    does_exist_name = db.query(mdl_suppliers.Suppliers).filter(
        mdl_suppliers.Suppliers.name == supplier.name).first()
    if does_exist_name and does_exist_name.id != id:
        raise HTTPException(status_code=status.HTTP_226_IM_USED,
                            detail=f'supplier name: {supplier.name} already exists')

    new_dict = supplier.dict()
    new_dict['updated_by'] = current_user.id
    query.update(new_dict, synchronize_session=False)
    db.commit()

    return query.first()


# Delete Supplier By ID
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_job(id: int, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):

    query = db.query(mdl_suppliers.Suppliers).filter(
        mdl_suppliers.Suppliers.id == id)
    if not query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'supplier with id: {id} does not exist')

    query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_205_RESET_CONTENT)
