from fastapi import status, Response, Depends, APIRouter
from pydantic.types import UUID4
from .. models import mdl_inv_hop, mdl_commodities
from .. database.database import cursor, conn, get_db
from .. validators import val_user, val_inv_hop
from .. oauth2.oauth2 import get_current_user
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from loguru import logger
import pendulum as ptime
from typing import List


tz = ptime.timezone('America/Denver')

router = APIRouter(prefix='/inventory/hop', tags=['Hop Inventory'])


# Validaton: api/validators/val_inv_hop.py
# Model: api/models/mdl_inv_hop.py


# Create New Last Brews Inv Entry
@router.post('/lastbrews', status_code=status.HTTP_201_CREATED, response_model=val_inv_hop.InvHopLastBrewsOut)
@logger.catch()
def create_entry(brews: val_inv_hop.InvHopLastBrewsIn, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):
    if current_user.permissions < 1:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={'detail': 'unauthorized'})

    try:
        date_start = ptime.now(tz).start_of('day')
        date_end = ptime.now(tz).end_of('day')

        does_exist = db.query(mdl_inv_hop.InvLastBrews).filter(
            mdl_inv_hop.InvLastBrews.created_at >= date_start, mdl_inv_hop.InvLastBrews.created_at <= date_end).first()
        if does_exist:
            return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={'detail': f' Daily Key (inv_uuid)=(inv_uuid) already present in table inv_last_brews'})

        db_data = mdl_inv_hop.InvLastBrews(
            created_by=current_user.id, **brews.dict())
        db.add(db_data)
        db.commit()
        db.refresh(db_data)

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return db_data


# Delete Entry From Last Brews
@router.delete('/lastbrews/{inv_uuid}', status_code=status.HTTP_204_NO_CONTENT)
@logger.catch()
def delete_entry(inv_uuid: UUID4, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):
    if current_user.permissions < 1:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={'detail': 'unauthorized'})

    try:
        query = db.query(mdl_inv_hop.InvLastBrews).filter(
            mdl_inv_hop.InvLastBrews.inv_uuid == inv_uuid)
        does_exist = query.first()
        if not does_exist:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'detail': f'Key (inv_uuid)=({inv_uuid}) is not present in table inv_material'})

        query.delete(synchronize_session=False)
        db.commit()

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(status_code=status.HTTP_205_RESET_CONTENT)


# Create New Material Inv Entry
@router.post('', status_code=status.HTTP_201_CREATED, response_model=val_inv_hop.InvHopOut)
@logger.catch()
def create_entry(commodity: val_inv_hop.InvHopCreate, db: Session = Depends(get_db), current_user: val_user.UserOut = Depends(get_current_user)):
    if current_user.permissions < 1:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={'detail': 'unauthorized'})

    try:
        does_exist = db.query(mdl_commodities.Commodities).filter(
            mdl_commodities.Commodities.id == commodity.id_commodity).first()
        if not does_exist:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'detail': f'Key (id_commodity)=({commodity.id_commodity}) is not present in table commodities'})

        date_start = ptime.now(tz).start_of('day')
        date_end = ptime.now(tz).end_of('day')

        does_exist = db.query(mdl_inv_hop.InvLastBrews).filter(
            mdl_inv_hop.InvLastBrews.created_at >= date_start, mdl_inv_hop.InvLastBrews.created_at <= date_end).first()
        if does_exist:
            unique_id = does_exist.inv_uuid
        else:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'detail': f'Key (inv_uuid)=(inv_uuid) is not present in table inv_last_brews'})

        db_data = mdl_inv_hop.InvHop(
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
    if current_user.permissions < 1:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={'detail': 'unauthorized'})

    try:
        query = db.query(mdl_inv_hop.InvHop).filter(
            mdl_inv_hop.InvHop.id == id)

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
@router.get('/read/sum/{inv_uuid}', status_code=status.HTTP_200_OK, response_model=List[val_inv_hop.InvHopSumOut])
@logger.catch()
def get_inv_by_uuid_summed(inv_uuid: UUID4, current_user: val_user.UserOut = Depends(get_current_user)):
    try:
        cursor.execute("""
            SELECT com.name_local, com.name_bit, com.sap, com.inventory, SUM(inv.total_pallets) AS total_pallets, SUM(inv.total_units) AS total_units, SUM(inv.total_end) AS total_end, DATE_TRUNC('day',inv.created_at)::timestamp::date AS inv_date, inv.inv_uuid
            FROM inv_hop AS inv
            JOIN commodities AS com ON inv.id_commodity = com.id
            JOIN users AS use ON inv.created_by = use.id
            WHERE inv_uuid = %s
            GROUP BY com.name_local, com.name_bit, com.sap, com.inventory, DATE_TRUNC('day',inv.created_at)::timestamp::date, inv.inv_uuid
            ORDER BY com.name_local
            """, (str(inv_uuid),))

        inv_hop = cursor.fetchall()

        if not inv_hop:
            return Response(status_code=status.HTTP_404_NOT_FOUND)

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return inv_hop


# Get Material Inventory By UUID Complete
@router.get('/read/complete/{inv_uuid}', status_code=status.HTTP_200_OK, response_model=List[val_inv_hop.InvHopCompleteOut])
@logger.catch()
def get_inv_by_uuid_complete(inv_uuid: str, current_user: val_user.UserOut = Depends(get_current_user)):
    try:
        cursor.execute("""
            SELECT inv.id, com.name_local, com.name_bit, com.sap, com.inventory, inv.total_pallets AS total_pallets, inv.total_units AS total_units, inv.total_end AS total_end, inv.note, use.name, inv.created_at::timestamp(0) AS inv_date, inv.inv_uuid
            FROM inv_hop AS inv
            JOIN commodities AS com ON inv.id_commodity = com.id
            JOIN users AS use ON inv.created_by = use.id
            WHERE inv_uuid = %s
            ORDER BY com.name_local
            """, (str(inv_uuid),))

        inv_hop = cursor.fetchall()

        if not inv_hop:
            return Response(status_code=status.HTTP_404_NOT_FOUND)

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return inv_hop


# Get Dates of Material Inventories
@router.get('/read/dates', status_code=status.HTTP_200_OK, response_model=List[val_inv_hop.InvHopDatesOut])
@logger.catch()
def get_inv_dates(current_user: val_user.UserOut = Depends(get_current_user)):
    try:
        cursor.execute("""
            SELECT DISTINCT DATE_TRUNC('day',created_at)::timestamp::date AS inv_date, inv_uuid
            FROM inv_last_brews
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
