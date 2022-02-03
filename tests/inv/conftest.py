import pytest


@pytest.fixture(scope='function')
def inv_material_uuid(session):
    res = session.execute(
        "SELECT inv_uuid FROM inv_material WHERE id = 1").first()
    return res[0]


@pytest.fixture
def test_supplier_data(admin_authorized_client):
    db_data = [
        {
            "name": "Supplier 1",
            "contact": "Contact 1",
            "email": "1user@example.com",
            "phone": "1234567890",
            "note": "Test Note",
            "is_active": True
        },
        {
            "name": "Supplier 2",
            "contact": "Contact 2",
            "email": "2user@example.com",
            "phone": "0987654321",
            "note": "Test Note",
            "is_active": True
        }
    ]
    for supplier in db_data:
        res = admin_authorized_client.post('/suppliers', json=supplier)
        assert res.status_code == 201

    return db_data


@pytest.fixture
def test_commodity_data(admin_authorized_client, test_supplier_data):
    db_data = [
        {
            "name_bit": "Name Bit 1",
            "name_local": "Name Local 1",
            "location": "Grains",
            "sap": "12345678",
            "inventory": "Brw",
            "threshold": 0,
            "per_pallet": 0,
            "per_unit": 0,
            "unit_of_measurement": "string",
            "type": "Hop",
            "note": "Note 1",
            "is_active": True,
            "id_supplier": 1
        },
        {
            "name_bit": "Name Bit 2",
            "name_local": "Name Local 2",
            "location": "Brewhouse",
            "sap": "87654321",
            "inventory": "Fin",
            "threshold": 0,
            "per_pallet": 0,
            "per_unit": 0,
            "unit_of_measurement": "string",
            "type": "Addition",
            "note": "Note 2",
            "is_active": True,
            "id_supplier": 1
        },
        {
            "name_bit": "Name Bit 3",
            "name_local": "Name Local 3",
            "location": "Fermenting",
            "sap": "09876543",
            "inventory": "Log",
            "threshold": 0,
            "per_pallet": 0,
            "per_unit": 2,
            "unit_of_measurement": "string",
            "type": "Chemical",
            "note": "Note 3",
            "is_active": True,
            "id_supplier": 2
        },
        {
            "name_bit": "Name Bit 4",
            "name_local": "Name Local 4",
            "location": "Chips",
            "sap": "34567890",
            "inventory": "Brw",
            "threshold": 0,
            "per_pallet": 0,
            "per_unit": 0,
            "unit_of_measurement": "string",
            "type": "Hop",
            "note": "Note 4",
            "is_active": True,
            "id_supplier": 2
        }
    ]
    for commodity in db_data:
        res = admin_authorized_client.post('/commodities', json=commodity)
        assert res.status_code == 201

    return db_data


@pytest.fixture
def test_inv_material_data(admin_authorized_client, test_commodity_data):
    db_data = [
        {
            "total_pallets": 1,
            "total_units": 10,
            "total_per_unit": 10,
            "total_end": 100,
            "note": "string",
            "id_commodity": 1,
        },
        {
            "total_pallets": 1,
            "total_units": 10,
            "total_per_unit": 10,
            "total_end": 100,
            "note": "string",
            "id_commodity": 1,
        },
        {
            "total_pallets": 2,
            "total_units": 10,
            "total_per_unit": 10,
            "total_end": 200,
            "note": "string",
            "id_commodity": 2,
        },
        {
            "total_pallets": 2,
            "total_units": 10,
            "total_per_unit": 10,
            "total_end": 200,
            "note": "string",
            "id_commodity": 2,
        },
        {
            "total_pallets": 3,
            "total_units": 10,
            "total_per_unit": 10,
            "total_end": 300,
            "note": "string",
            "id_commodity": 3,
        },
        {
            "total_pallets": 3,
            "total_units": 10,
            "total_per_unit": 10,
            "total_end": 300,
            "note": "string",
            "id_commodity": 3,
        },
        {
            "total_pallets": 4,
            "total_units": 10,
            "total_per_unit": 10,
            "total_end": 400,
            "note": "string",
            "id_commodity": 4,
        },
        {
            "total_pallets": 4,
            "total_units": 10,
            "total_per_unit": 10,
            "total_end": 400,
            "note": "string",
            "id_commodity": 4,
        }
    ]
    for commodity in db_data:
        res = admin_authorized_client.post(
            '/inventory/material', json=commodity)
        assert res.status_code == 201

    return db_data
