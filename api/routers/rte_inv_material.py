from fastapi import status, Response, Depends, APIRouter
from .. models import mdl_inv_material, mdl_commodities
from .. database.database import cursor, conn, get_db
from .. validators import val_user, val_inv_material
from .. oauth2.oauth2 import get_current_user
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from loguru import logger
import pendulum as ptime
from typing import List
import uuid


tz = ptime.timezone('America/Denver')

router = APIRouter(prefix='/inventory/material', tags=['Material Inventory'])


# Validaton: api/validators/val_inv_material.py
# Model: api/models/mdl_inv_material.py


# Create New Material Inv Entry
@router.post('', status_code=status.HTTP_201_CREATED, response_model=val_inv_material.InvMaterialOut)
@logger.catch()
def create_entry(commodity: val_inv_material.InvMaterialCreate, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):
    if current_user.permissions < 3:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={'detail': 'unauthorized'})

    try:
        does_exist = db.query(mdl_commodities.Commodities).filter(
            mdl_commodities.Commodities.id == commodity.id_commodity).first()
        if not does_exist:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'detail': f'Key (id_commodity)=({commodity.id_commodity}) is not present in table commodities'})

        date_start = ptime.now(tz).start_of('day')
        date_end = ptime.now(tz).end_of('day')

        does_exist = db.query(mdl_inv_material.InvMaterial).filter(
            mdl_inv_material.InvMaterial.created_at >= date_start, mdl_inv_material.InvMaterial.created_at <= date_end).first()
        if does_exist:
            unique_id = does_exist.inv_uuid
        else:
            unique_id = uuid.uuid4()

        db_data = mdl_inv_material.InvMaterial(
            created_by=current_user.id, inv_uuid=unique_id, **commodity.dict())
        db.add(db_data)
        db.commit()
        db.refresh(db_data)

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return db_data


# Delete Entry From Inventory
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
@logger.catch()
def delete_entry(id: int, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):
    if current_user.permissions < 3:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={'detail': 'unauthorized'})

    try:
        query = db.query(mdl_inv_material.InvMaterial).filter(
            mdl_inv_material.InvMaterial.id == id)

        does_exist = query.first()
        if not does_exist:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'detail': f'Key (id)=({id}) is not present in table inv_material'})

        query.delete(synchronize_session=False)
        db.commit()

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(status_code=status.HTTP_205_RESET_CONTENT)


# Get Material Inventory By UUID Summed
@router.get('/read/sum/{inv_uuid}', status_code=status.HTTP_200_OK, response_model=List[val_inv_material.InvMaterialSumOut])
@logger.catch()
def get_inv_by_uuid_summed(inv_uuid: str, current_user: val_user.UserOut = Depends(get_current_user)):
    if current_user.permissions < 1:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={'detail': 'unauthorized'})

    try:
        cursor.execute("""
            SELECT com.name_local, com.name_bit, com.sap, com.inventory, SUM(inv.total_pallets) AS total_pallets, SUM(inv.total_units) AS total_units, SUM(inv.total_end) AS total_end, DATE_TRUNC('day',inv.created_at)::timestamp::date AS inv_date, inv.inv_uuid  
            FROM inv_material AS inv
            JOIN commodities AS com ON inv.id_commodity = com.id
            JOIN users AS use ON inv.created_by = use.id
            WHERE inv_uuid = %s
            GROUP BY com.name_local, com.name_bit, com.sap, com.inventory, DATE_TRUNC('day',inv.created_at)::timestamp::date, inv.inv_uuid
            ORDER BY com.name_local
            """, (str(inv_uuid),))

        inv_material = cursor.fetchall()

        if not inv_material:
            return Response(status_code=status.HTTP_404_NOT_FOUND)

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return inv_material


# Get Material Inventory By UUID Complete
@router.get('/read/complete/{inv_uuid}', status_code=status.HTTP_200_OK, response_model=List[val_inv_material.InvMaterialCompleteOut])
@logger.catch()
def get_inv_by_uuid_complete(inv_uuid: uuid.UUID, current_user: val_user.UserOut = Depends(get_current_user)):
    if current_user.permissions < 1:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={'detail': 'unauthorized'})

    try:

        cursor.execute("""
            SELECT com.name_local, com.name_bit, com.sap, com.inventory, inv.total_pallets AS total_pallets, inv.total_units AS total_units, inv.total_end AS total_end, inv.note, use.name, inv.created_at::timestamp(0) AS inv_date, inv_uuid  
            FROM inv_material AS inv
            JOIN commodities AS com ON inv.id_commodity = com.id
            JOIN users AS use ON inv.created_by = use.id
            WHERE inv_uuid = %s
            ORDER BY com.name_local
            """, (str(inv_uuid),))

        inv_material = cursor.fetchall()

        if not inv_material:
            return Response(status_code=status.HTTP_404_NOT_FOUND)

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return inv_material


# Get Dates of Material Inventories
@router.get('/read/dates', status_code=status.HTTP_200_OK, response_model=List[val_inv_material.InvMaterialDatesOut])
@logger.catch()
def get_inv_dates(current_user: val_user.UserOut = Depends(get_current_user)):
    if current_user.permissions < 1:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={'detail': 'unauthorized'})

    try:
        cursor.execute("""
            SELECT DISTINCT DATE_TRUNC('day',created_at)::timestamp::date AS inv_date, inv_uuid
            FROM inv_material
            WHERE created_at > NOW() - INTERVAL '365 days'
            ORDER BY DATE_TRUNC('day',created_at)::timestamp::date DESC;
            """)

        inv_dates = cursor.fetchall()

        if not inv_dates:
            return Response(status_code=status.HTTP_404_NOT_FOUND)

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return inv_dates
