from api.validators import val_commodities


def test_get_all_commodities(authorized_client, test_commodity_data):
    res = authorized_client.get('/commodities')
    assert len(res.json()) == len(test_commodity_data)
    assert res.status_code == 200


def test_get_all_commodities_empty(authorized_client):
    res = authorized_client.get('/commodities')
    assert res.status_code == 404


def test_get_all_commodities_unauthorized(authorized_client_permissions_0):
    res = authorized_client_permissions_0.get('/commodities')
    assert res.status_code == 403


def test_create_commodity(authorized_client, test_commodity_data):
    data = {
        "name_bit": "Name Bit 8",
        "name_local": "Name Local 8",
        "location": "Finishing",
        "sap": "98765432",
        "inventory": "Log",
        "threshold": 0,
        "per_pallet": 0,
        "per_unit": 0,
        "unit_of_measurement": "inch",
        "type": "Hop",
        "note": "Note 8",
        "is_active": True,
        "id_supplier": 1
    }
    res = authorized_client.post('/commodities', json=data)
    commodity = val_commodities.CommodityOut(**res.json())

    assert commodity.name_bit == "Name Bit 8"
    assert commodity.name_local == "Name Local 8"
    assert commodity.location == "Finishing"
    assert commodity.sap == "98765432"
    assert commodity.inventory == "Log"
    assert commodity.threshold == 0
    assert commodity.per_pallet == 0
    assert commodity.per_unit == 0
    assert commodity.unit_of_measurement == "inch"
    assert commodity.type == "Hop"
    assert commodity.note == "Note 8"
    assert commodity.is_active == True
    assert commodity.supplier.id == 1
    assert res.status_code == 201


def test_create_commodity_unauthorized(authorized_client_permissions_0):
    data = {
        "name_bit": "Name Bit 8",
        "name_local": "Name Local 8",
        "location": "Finishing",
        "sap": "98765432",
        "inventory": "Log",
        "threshold": 0,
        "per_pallet": 0,
        "per_unit": 0,
        "unit_of_measurement": "inch",
        "type": "Hop",
        "note": "Note 8",
        "is_active": True,
        "id_supplier": 1
    }
    res = authorized_client_permissions_0.post('/commodities', json=data)
    assert res.status_code == 403


def test_get_one_commodity(authorized_client, test_commodity_data):
    res = authorized_client.get('/commodities/1')
    commodity = val_commodities.CommodityOut(**res.json())
    assert commodity.id == 1
    assert res.status_code == 200


def test_get_one_commodity_empty(authorized_client, test_commodity_data):
    res = authorized_client.get('/commodities/50')
    assert res.status_code == 404


def test_get_one_commodity_unauthorized(authorized_client_permissions_0):
    res = authorized_client_permissions_0.get('/commodities')
    assert res.status_code == 403


def test_update_commodity(authorized_client, test_commodity_data):
    data = {
        "name_bit": "New Name Bit",
        "name_local": "New Name Local",
        "location": "Finishing",
        "sap": "12345678",
        "inventory": "Log",
        "threshold": 0,
        "per_pallet": 0,
        "per_unit": 0,
        "unit_of_measurement": "gallon",
        "type": "Addition",
        "note": "New Note",
        "balance_inactive": 0,
        "is_active": False,
        "id_supplier": 2
    }
    res = authorized_client.put('/commodities/1', json=data)
    commodity = val_commodities.CommodityOut(**res.json())

    assert commodity.name_bit == "New Name Bit"
    assert commodity.name_local == "New Name Local"
    assert commodity.location == "Finishing"
    assert commodity.sap == "12345678"
    assert commodity.inventory == "Log"
    assert commodity.threshold == 0
    assert commodity.per_pallet == 0
    assert commodity.per_unit == 0
    assert commodity.unit_of_measurement == "gallon"
    assert commodity.type == "Addition"
    assert commodity.note == "New Note"
    assert commodity.is_active == False
    assert commodity.supplier.id == 2
    assert res.status_code == 200


def test_update_commodity(authorized_client_permissions_0):
    data = {
        "name_bit": "New Name Bit",
        "name_local": "New Name Local",
        "location": "Finishing",
        "sap": "12345678",
        "inventory": "Log",
        "threshold": 0,
        "per_pallet": 0,
        "per_unit": 0,
        "unit_of_measurement": "gallon",
        "type": "Addition",
        "note": "New Note",
        "balance_inactive": 0,
        "is_active": False,
        "id_supplier": 2
    }
    res = authorized_client_permissions_0.put('/commodities/1', json=data)
    assert res.status_code == 403


def test_delete_commodity(admin_authorized_client, test_commodity_data):
    res = admin_authorized_client.delete('/commodities/1')
    assert res.status_code == 205


def test_delete_commodity_unauthorized(authorized_client):
    res = authorized_client.delete('/commodities/1')
    assert res.status_code == 403
