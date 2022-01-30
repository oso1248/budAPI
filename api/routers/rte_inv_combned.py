from fastapi import status, Response, Depends, APIRouter
from .. validators import val_user, val_inv_combined
from .. database.database import cursor, conn
from .. oauth2.oauth2 import get_current_user
from pydantic.types import UUID4
from loguru import logger
from typing import List


router = APIRouter(prefix='/inventory/combined', tags=['Combined Inventory'])


# Validaton: api/validators/val_inv_combined.py


# Get Combined Inventories By UUID Summed
@router.get('', status_code=status.HTTP_200_OK, response_model=List[val_inv_combined.InvCombinedOut])
@logger.catch()
def get_inv_by_uuid_summed(uuids: val_inv_combined.InvCombinedIn, current_user: val_user.UserOut = Depends(get_current_user)):
    try:
        cursor.execute("""
            SELECT name_local, name_bit, sap, inventory, SUM(total_pallets) AS total_pallets, SUM(total_units) AS total_units, SUM(total_end) AS total_end, inv_date
            FROM (
              SELECT com.name_local, com.name_bit, com.sap, com.inventory, inv.total_pallets, inv.total_units, inv.total_end, DATE_TRUNC('day',inv.created_at)::timestamp::date AS inv_date
              FROM inv_hop AS inv
              JOIN commodities AS com ON inv.id_commodity = com.id
              JOIN users AS use ON inv.created_by = use.id
              WHERE inv_uuid = %s
              UNION ALL
              SELECT com.name_local, com.name_bit, com.sap, com.inventory, inv.total_pallets, inv.total_units, inv.total_end, DATE_TRUNC('day',inv.created_at)::timestamp::date AS inv_date  
              FROM inv_material AS inv
              JOIN commodities AS com ON inv.id_commodity = com.id
              JOIN users AS use ON inv.created_by = use.id
              WHERE inv_uuid = %s) AS z
            GROUP BY name_local, name_bit, sap, inventory,  inv_date
            ORDER BY name_local
            """, (str(uuids.uuid_hop), str(uuids.uuid_material)))

        inv_combined = cursor.fetchall()

        if not inv_combined:
            return Response(status_code=status.HTTP_404_NOT_FOUND)

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return inv_combined
