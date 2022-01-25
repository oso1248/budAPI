from os import name
from fastapi import status, Response, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from .. database.database import cursor, conn, get_db
from .. validators import val_user, val_inv_material
from .. models import mdl_inv_material
from .. oauth2.oauth2 import get_current_user
import uuid
import pendulum as ptime

router = APIRouter(prefix='/inventory/material', tags=['Material Inventory'])

tz = ptime.timezone('America/Denver')

# Validaton: api/validators/val_inv_material.py
# Model: api/models/mdl_inv_material.py


# Create New Material Inv Entry
@router.post('', status_code=status.HTTP_201_CREATED, response_model=val_inv_material.InvMaterialOut)
def create_entry(commodity: val_inv_material.InvMaterialCreate, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):

    try:
        date_start = ptime.now(tz).start_of('day')
        date_end = ptime.now(tz).end_of('day')
        uuid_exists = db.query(mdl_inv_material.InvMaterial).filter(
            mdl_inv_material.InvMaterial.created_at >= date_start, mdl_inv_material.InvMaterial.created_at <= date_end).first()
        if uuid_exists:
            unique_id = uuid_exists.inv_uuid
        else:
            unique_id = uuid.uuid4()
        db_data = mdl_inv_material.InvMaterial(
            created_by=current_user.id, inv_uuid=unique_id, **commodity.dict())
        db.add(db_data)
        db.commit()
        db.refresh(db_data)

    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return db_data


# Get Material Inventory By UUID Summed
@router.get('/read/sum/{inv_uuid}', status_code=status.HTTP_200_OK, response_model=List[val_inv_material.InvMaterialSumOut])
def get_inv_by_uuid_summed(inv_uuid: str, current_user: val_user.UserOut = Depends(get_current_user)):
    try:
        cursor.execute("""
            SELECT com.name_local, com.name_bit, com.sap, com.inventory, SUM(inv.total_pallets) AS total_pallets, SUM(inv.total_units) AS total_units, SUM(inv.total_end) AS total_end, DATE_TRUNC('day',inv.created_at)::timestamp::date AS inv_date  
            FROM inv_material AS inv
            JOIN commodities AS com ON inv.id_commodity = com.id
            JOIN users AS use ON inv.created_by = use.id
            WHERE inv_uuid = %s
            GROUP BY com.name_local, com.name_bit, com.sap, com.inventory, DATE_TRUNC('day',inv.created_at)::timestamp::date
            ORDER BY com.name_local
        """, (str(inv_uuid),))

        inv_material = cursor.fetchall()

        if not inv_material:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'inventory with uuid: {inv_uuid} does not exist')
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return inv_material


# Get Material Inventory By UUID Summed
@router.get('/read/complete/{inv_uuid}', status_code=status.HTTP_200_OK, response_model=List[val_inv_material.InvMaterialCompleteOut])
def get_inv_by_uuid_complete(inv_uuid: str, current_user: val_user.UserOut = Depends(get_current_user)):
    try:
        cursor.execute("""
            SELECT com.name_local, com.name_bit, com.sap, com.inventory, inv.total_pallets AS total_pallets, inv.total_units AS total_units, inv.total_end AS total_end, inv.note, use.name, inv.created_at::timestamp(0) AS inv_date  
            FROM inv_material AS inv
            JOIN commodities AS com ON inv.id_commodity = com.id
            JOIN users AS use ON inv.created_by = use.id
            WHERE inv_uuid = %s
            ORDER BY com.name_local
        """, (str(inv_uuid),))

        inv_material = cursor.fetchall()

        if not inv_material:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'inventory with uuid: {inv_uuid} does not exist')

    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return inv_material


# Get Dates of Material Inventories
@router.get('/read/dates', status_code=status.HTTP_200_OK, response_model=List[val_inv_material.InvDatesOut])
def get_inv_dates(current_user: val_user.UserOut = Depends(get_current_user)):
    try:
        cursor.execute("""
            SELECT DISTINCT DATE_TRUNC('day',created_at)::timestamp::date AS inv_date, inv_uuid
            FROM inv_material
            WHERE created_at > NOW() - INTERVAL '365 days'
            ORDER BY DATE_TRUNC('day',created_at)::timestamp::date DESC;
        """)

        inv_dates = cursor.fetchall()

        if not inv_dates:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='inventory dates do not exist')

    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return inv_dates
