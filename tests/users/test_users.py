from api.validators import val_user


def test_get_all_users(authorized_client, test_user_data):
    res = authorized_client.get('/users')
    assert len(res.json()) == len(test_user_data) + 1
    assert res.status_code == 200


def test_get_all_users_empty(admin_authorized_client):
    res = admin_authorized_client.get('/users')
    assert res.status_code == 404


def test_get_all_users_unauthorized(authorized_client_permissions_0):
    res = authorized_client_permissions_0.get('/users')
    assert res.status_code == 403


def test_create_user(authorized_client):
    res = authorized_client.post('/users', json={'name': 'maria kowalchuk', 'username': 'mariac',
                                                 'password': 'BudAdmin1!', 'is_active': True, 'role': 'BPM', 'brewery': 'FTC', 'permissions': 6})
    new_user = val_user.UserOut(**res.json())
    assert new_user.id == 3
    assert new_user.name == 'Maria Kowalchuk'
    assert new_user.is_active == True
    assert new_user.role == 'BPM'
    assert new_user.permissions == 6
    assert new_user.creator == {'id': 1, 'name': 'Admin'}
    assert res.status_code == 201


def test_create_user_unauthorized(authorized_client_permissions_0):
    res = authorized_client_permissions_0.post('/users', json={
        'name': 'maria kowalchuk',
        'username': 'mariac',
        'password': 'BudAdmin1!',
        'is_active': True,
        'role': 'BPM',
        'brewery': 'FTC',
        'permissions': 6
    })
    assert res.status_code == 403


def test_update_user(authorized_client, test_user_data):
    res = authorized_client.put('/users/2', json={
        "name": "Meika Woollard",
        "is_active": True,
        "role": "Brewer",
        "brewery": "FTC",
        "permissions": 1
    })
    data = val_user.UserOut(**res.json())
    assert data.name == "Meika Woollard"
    assert data.permissions == 1
    assert res.status_code == 200


def test_update_user_empty(authorized_client, test_user_data):
    res = authorized_client.put('/users/50', json={
        "name": "Meika Woollard",
        "is_active": True,
        "role": "Brewer",
        "brewery": "FTC",
        "permissions": 1
    })
    assert res.status_code == 404


def test_update_user_unauthorized(authorized_client_permissions_0):
    res = authorized_client_permissions_0.put('/users/2', json={
        "name": "Meika Woollard",
        "is_active": True,
        "role": "Brewer",
        "brewery": "FTC",
        "permissions": 1
    })
    assert res.status_code == 403


def test_get_one_user(authorized_client, test_user_data):
    res = authorized_client.get('/users/4')
    user = val_user.UserOut(**res.json())
    assert user.id == 4
    assert res.status_code == 200


def test_get_one_user_empty(authorized_client, test_user_data):
    res = authorized_client.get('/users/50')
    assert res.status_code == 404


def test_get_one_user_unauthorized(authorized_client_permissions_0):
    res = authorized_client_permissions_0.get('/users/2')
    assert res.status_code == 403


def test_delete_user(admin_authorized_client, test_user_data):
    res = admin_authorized_client.delete('/users/4')
    assert res.status_code == 205


def test_delete_user_empty(admin_authorized_client, test_user_data):
    res = admin_authorized_client.delete('/users/50')
    assert res.status_code == 404


def test_delete_user_unauthorized(authorized_client, test_user_data):
    res = authorized_client.delete('/users/4')
    assert res.status_code == 403
