import pytest


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
def test_finishing_data(admin_authorized_client, test_brewing_data):
    data = [
        {
            "name": "fin1",
            "is_pre_injection": False,
            "is_post_injection": False,
            "is_bypass": False,
            "is_organic": False,
            "note": "string",
            "is_active": True,
            "id_brewing": 1
        },
        {
            "name": "fin2",
            "is_pre_injection": False,
            "is_post_injection": False,
            "is_bypass": False,
            "is_organic": False,
            "note": "string",
            "is_active": True,
            "id_brewing": 1
        },
        {
            "name": "fin3",
            "is_pre_injection": False,
            "is_post_injection": False,
            "is_bypass": False,
            "is_organic": False,
            "note": "string",
            "is_active": True,
            "id_brewing": 2
        },
        {
            "name": "fin4",
            "is_pre_injection": False,
            "is_post_injection": False,
            "is_bypass": False,
            "is_organic": False,
            "note": "string",
            "is_active": True,
            "id_brewing": 2
        }
    ]
    for brand in data:
        res = admin_authorized_client.post('/brands/finishing', json=brand)
        assert res.status_code == 201

    return data


@pytest.fixture
def test_packaging_data(admin_authorized_client, test_finishing_data):
    data = [
        {
            "name": "pck1",
            "is_organic": False,
            "note": "string",
            "is_active": True,
            "id_finishing": 1
        },
        {
            "name": "pck2",
            "is_organic": False,
            "note": "string",
            "is_active": True,
            "id_finishing": 2
        },
        {
            "name": "pck3",
            "is_organic": False,
            "note": "string",
            "is_active": True,
            "id_finishing": 3
        },
        {
            "name": "pck4",
            "is_organic": False,
            "note": "string",
            "is_active": True,
            "id_finishing": 4
        }
    ]
    for brand in data:
        res = admin_authorized_client.post('/brands/packaging', json=brand)
        assert res.status_code == 201

    return data
