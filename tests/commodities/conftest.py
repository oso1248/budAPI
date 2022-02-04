import pytest


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
            "type": "MC_Addition",
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
def test_brewing_data(admin_authorized_client):
    data = [
        {
            "name": "brw1",
            "is_organic": False,
            "is_hop_kettle": True,
            "is_hop_dry": False,
            "is_addition": False,
            "note": "string",
            "is_active": True
        },
        {
            "name": "brw2",
            "is_organic": False,
            "is_hop_kettle": True,
            "is_hop_dry": False,
            "is_addition": False,
            "note": "string",
            "is_active": True
        }
    ]
    for brand in data:
        res = admin_authorized_client.post('/brands/brewing', json=brand)
        assert res.status_code == 201

    return data


@pytest.fixture
def test_commodity_usage_data(admin_authorized_client, test_brewing_data, test_commodity_data):
    db_data = [
        {
            "id_commodity": 1,
            "id_brand_brewing": 1,
            "id_brewhouse": 0,
            "amount_per_brew": 10
        },
        {
            "id_commodity": 2,
            "id_brand_brewing": 1,
            "id_brewhouse": 0,
            "amount_per_brew": 20
        },
        {
            "id_commodity": 3,
            "id_brand_brewing": 1,
            "id_brewhouse": 0,
            "amount_per_brew": 30
        },
        {
            "id_commodity": 4,
            "id_brand_brewing": 2,
            "id_brewhouse": 0,
            "amount_per_brew": 40
        },
        {
            "id_commodity": 1,
            "id_brand_brewing": 2,
            "id_brewhouse": 0,
            "amount_per_brew": 50
        },
        {
            "id_commodity": 2,
            "id_brand_brewing": 2,
            "id_brewhouse": 0,
            "amount_per_brew": 60
        }
    ]

    for commodity in db_data:
        res = admin_authorized_client.post('/commodity/usage', json=commodity)
        assert res.status_code == 201

    return db_data
