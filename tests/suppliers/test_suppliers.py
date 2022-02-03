from api.validators import val_suppliers


def test_get_all_suppliers(authorized_client, test_supplier_data):
    res = authorized_client.get('/suppliers')
    assert len(res.json()) == len(test_supplier_data)
    assert res.status_code == 200


def test_get_all_suppliers_empty(authorized_client):
    res = authorized_client.get('/suppliers')
    assert res.status_code == 404


def test_get_all_suppliers_unauthorized(authorized_client_permissions_0):
    res = authorized_client_permissions_0.get('/suppliers')
    assert res.status_code == 403


def test_create_supplier(authorized_client):
    res = authorized_client.post('/suppliers', json={
        "name": "Supplier 1",
        "contact": "Contact 1",
        "email": "user@example.com",
        "phone": "1234567890",
        "note": "test note",
        "is_active": True
    })
    data = val_suppliers.SupplierOut(**res.json())
    assert data.name == 'Supplier 1'
    assert data.contact == 'Contact 1'
    assert data.email == 'user@example.com'
    assert data.phone == '(123) 456-7890'
    assert data.note == 'Test Note'
    assert data.is_active == True
    assert res.status_code == 201


def test_create_supplier_unauthorized(authorized_client_permissions_0):
    res = authorized_client_permissions_0.post('/suppliers', json={
        "name": "Supplier 1",
        "contact": "Contact 1",
        "email": "user@example.com",
        "phone": "1234567890",
        "note": "test note",
        "is_active": True
    })
    assert res.status_code == 403


def test_get_one_suppliers(authorized_client, test_supplier_data):
    res = authorized_client.get('/suppliers/1')
    supplier = val_suppliers.SupplierOut(**res.json())
    assert supplier.id == 1
    assert res.status_code == 200


def test_get_one_suppliers_empty(authorized_client):
    res = authorized_client.get('/suppliers/1')
    assert res.status_code == 404


def test_get_one_suppliers_empty_unauthorized(authorized_client_permissions_0):
    res = authorized_client_permissions_0.get('/suppliers/1')
    assert res.status_code == 403


def test_update_supplier(authorized_client, test_supplier_data):
    data = {
        "name": "New Name",
        "contact": "New Contact",
        "email": "9user@example.com",
        "phone": "1234567890",
        "note": "string",
        "is_active": False
    }
    res = authorized_client.put('/suppliers/1',  json=data)

    update = val_suppliers.SupplierOut(**res.json())

    assert update.id == 1
    assert update.name == 'New Name'
    assert update.contact == 'New Contact'
    assert update.email == '9user@example.com'
    assert update.phone == '(123) 456-7890'
    assert update.note == 'String'
    assert update.is_active == False
    assert res.status_code == 200


def test_update_supplier_empty(authorized_client, test_supplier_data):
    data = {
        "name": "New Name",
        "contact": "New Contact",
        "email": "9user@example.com",
        "phone": "1234567890",
        "note": "string",
        "is_active": False
    }
    res = authorized_client.put('/suppliers/50',  json=data)

    assert res.status_code == 404


def test_update_supplier_unauthorized(authorized_client_permissions_0):
    data = {
        "name": "New Name",
        "contact": "New Contact",
        "email": "9user@example.com",
        "phone": "1234567890",
        "note": "string",
        "is_active": False
    }
    res = authorized_client_permissions_0.put('/suppliers/1',  json=data)

    assert res.status_code == 403


def test_delete_supplier(admin_authorized_client, test_supplier_data):
    res = admin_authorized_client.delete('/suppliers/1')
    assert res.status_code == 205


def test_delete_supplier_unauthorized(authorized_client):
    res = authorized_client.delete('/suppliers/1')
    assert res.status_code == 403
