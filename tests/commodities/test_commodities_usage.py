from api.validators import val_commodity_usage


def test_update_commodity_usage(authorized_client, test_commodity_usage_data):
    db_data = {
        "id_commodity": 1,
        "id_brand_brewing": 1,
        "id_brewhouse": 0,
        "amount_per_brew": 100
    }
    res = authorized_client.put('/commodity/usage', json=db_data)
    data = val_commodity_usage.CommodityUsageOut(**res.json())
    assert data.amount_per_brew == 100
    assert data.brand.id == 1
    assert data.commodity.id == 1
    assert data.id_brewhouse == 0
    assert res.status_code == 200


def test_update_commodity_usage_empty(authorized_client, test_commodity_usage_data):
    db_data = {
        "id_commodity": 1,
        "id_brand_brewing": 1,
        "id_brewhouse": 2,
        "amount_per_brew": 100
    }
    res = authorized_client.put('/commodity/usage', json=db_data)
    assert res.status_code == 404


def test_update_commodity_usage_unauthorized(authorized_client_permissions_0):
    db_data = {
        "id_commodity": 1,
        "id_brand_brewing": 1,
        "id_brewhouse": 2,
        "amount_per_brew": 100
    }
    res = authorized_client_permissions_0.put('/commodity/usage', json=db_data)
    assert res.status_code == 403


def test_create_commodity_usage(authorized_client, test_commodity_usage_data):
    db_data = {
        "id_commodity": 1,
        "id_brand_brewing": 1,
        "id_brewhouse": 1,
        "amount_per_brew": 100
    }
    res = authorized_client.post('/commodity/usage', json=db_data)
    data = val_commodity_usage.CommodityUsageOut(**res.json())
    assert data.amount_per_brew == 100
    assert data.brand.id == 1
    assert data.commodity.id == 1
    assert data.id_brewhouse == 1
    assert res.status_code == 201


def test_create_commodity_usage_unauthorized(authorized_client_permissions_0):
    db_data = {
        "id_commodity": 1,
        "id_brand_brewing": 1,
        "id_brewhouse": 1,
        "amount_per_brew": 100
    }
    res = authorized_client_permissions_0.post(
        '/commodity/usage', json=db_data)
    assert res.status_code == 403


def test_delete_commodity_usage(authorized_client, test_commodity_usage_data):
    db_data = {
        "id_commodity": 1,
        "id_brand_brewing": 1,
        "id_brewhouse": 0
    }
    res = authorized_client.delete('/commodity/usage', json=db_data)
    assert res.status_code == 205


def test_delete_commodity_usage_empty(authorized_client, test_commodity_usage_data):
    db_data = {
        "id_commodity": 1,
        "id_brand_brewing": 1,
        "id_brewhouse": 2
    }
    res = authorized_client.delete('/commodity/usage', json=db_data)
    assert res.status_code == 404


def test_delete_commodity_usage_unauthorized(authorized_client_permissions_0):
    db_data = {
        "id_commodity": 1,
        "id_brand_brewing": 1,
        "id_brewhouse": 2
    }
    res = authorized_client_permissions_0.delete(
        '/commodity/usage', json=db_data)
    assert res.status_code == 403


def test_get_usage_by_commodity_id(authorized_client, test_commodity_usage_data):
    res = authorized_client.get('/commodity/usage/commodity/1')
    assert len(res.json()) == 2
    assert res.status_code == 200


def test_get_usage_by_commodity_id_empty(authorized_client, test_commodity_usage_data):
    res = authorized_client.get('/commodity/usage/commodity/10')
    assert res.status_code == 404


def test_get_usage_by_commodity_id_unauthorized(authorized_client_permissions_0):
    res = authorized_client_permissions_0.get('/commodity/usage/commodity/1')
    assert res.status_code == 403


def test_get_usage_by_brand_id(authorized_client, test_commodity_usage_data):
    res = authorized_client.get('/commodity/usage/brand/1')
    assert len(res.json()) == 3
    assert res.status_code == 200


def test_get_usage_by_brand_id_empty(authorized_client, test_commodity_usage_data):
    res = authorized_client.get('/commodity/usage/brand/10')
    assert res.status_code == 404


def test_get_usage_by_brand_id_unauthorized(authorized_client_permissions_0):
    res = authorized_client_permissions_0.get('/commodity/usage/brand/1')
    assert res.status_code == 403
