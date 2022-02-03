from api.validators import val_brands_packaging


def test_get_all_brands(authorized_client, test_packaging_data):
    res = authorized_client.get('/brands/packaging')
    assert len(res.json()) == len(test_packaging_data)
    assert res.status_code == 200


def test_get_all_brands_empty(authorized_client):
    res = authorized_client.get('/brands/packaging')
    assert res.status_code == 404


def test_get_all_brands_unauthorized(authorized_client_permissions_0):
    res = authorized_client_permissions_0.get('/brands/packaging')
    assert res.status_code == 403


def test_create_brand(authorized_client, test_packaging_data):
    data = {
        "name": "PCK5",
        "is_organic": False,
        "note": "string",
        "is_active": True,
        "id_finishing": 1
    }
    res = authorized_client.post('/brands/packaging', json=data)
    brand = val_brands_packaging.BrandPackagingOut(**res.json())
    assert isinstance(brand.id, int)
    assert brand.name == "PCK5"
    assert brand.is_organic == False
    assert brand.note == "String"
    assert brand.is_active == True
    assert res.status_code == 201


def test_create_brand_unauthorized(authorized_client_permissions_0):
    data = {
        "name": "PCK5",
        "is_organic": False,
        "note": "string",
        "is_active": True,
        "id_finishing": 1
    }
    res = authorized_client_permissions_0.post('/brands/packaging', json=data)
    assert res.status_code == 403


def test_get_one_brand(authorized_client, test_packaging_data):
    res = authorized_client.get('/brands/packaging/1')
    brand = val_brands_packaging.BrandPackagingOut(**res.json())
    assert brand.id == 1
    assert res.status_code == 200


def test_get_one_brand_empty(authorized_client, test_packaging_data):
    res = authorized_client.get('/brands/packaging/50')
    assert res.status_code == 404


def test_get_one_brand_unauthorized(authorized_client_permissions_0):
    res = authorized_client_permissions_0.get('/brands/packaging/50')
    assert res.status_code == 403


def test_update_brand(authorized_client, test_packaging_data):
    data = {
        "name": "PCK5",
        "is_organic": False,
        "note": "string",
        "is_active": True,
        "id_finishing": 1
    }
    res = authorized_client.put('/brands/packaging/1', json=data)
    brand = val_brands_packaging.BrandPackagingOut(**res.json())
    assert brand.id == 1
    assert brand.name == "PCK5"
    assert brand.is_organic == False
    assert brand.note == "String"
    assert brand.is_active == True
    assert res.status_code == 200


def test_update_brand_unauthorized(authorized_client_permissions_0):
    data = {
        "name": "PCK5",
        "is_organic": False,
        "note": "string",
        "is_active": True,
        "id_finishing": 1
    }
    res = authorized_client_permissions_0.put('/brands/packaging/1', json=data)
    assert res.status_code == 403


def test_delete_brand(admin_authorized_client, test_packaging_data):
    res = admin_authorized_client.delete('/brands/packaging/1')
    assert res.status_code == 205


def test_delete_brand(authorized_client, test_packaging_data):
    res = authorized_client.delete('/brands/packaging/1')
    assert res.status_code == 403
