from api.validators import val_manpower


def test_get_all_individual(authorized_client, test_manpower_individual_data):
    dt = {
        "start": "2021-02-03T13:12:25.332Z",
        "stop": "2100-02-03T13:12:25.332Z",
        "shift": 3
    }
    res = authorized_client.get('/manpower/individual', json=dt)
    assert len(res.json()) == len(test_manpower_individual_data)
    assert res.status_code == 200


def test_get_all_individual_unauthorized(authorized_client_permissions_0):
    dt = {
        "start": "2021-02-03T13:12:25.332Z",
        "stop": "2100-02-03T13:12:25.332Z",
        "shift": 3
    }
    res = authorized_client_permissions_0.get('/manpower/individual', json=dt)
    assert res.status_code == 403


def test_create_individual(authorized_client, test_manpower_individual_data):
    db_data = {
        "shift": 3,
        "id_users": 5,
        "id_jobs": 2,
        "note": "string"
    }
    res = authorized_client.post('/manpower/individual', json=db_data)
    data = val_manpower.ManPowerIndividualOut(**res.json())
    assert data.shift == 3
    assert data.brewer.name == 'Rachel Hinkel'
    assert data.job.name == 'Bh Panel'
    assert res.status_code == 201


def test_create_individual_unauthorized(authorized_client_permissions_0):
    db_data = {
        "shift": 3,
        "id_users": 5,
        "id_jobs": 2,
        "note": "string"
    }
    res = authorized_client_permissions_0.post(
        '/manpower/individual', json=db_data)
    assert res.status_code == 403


def test_delete_individual(authorized_client, test_manpower_individual_data):
    res = authorized_client.delete('/manpower/individual/1')
    assert res.status_code == 205


def test_delete_individual_unauthorized(authorized_client_permissions_0):
    res = authorized_client_permissions_0.delete('/manpower/individual/1')
    assert res.status_code == 403


def test_get_all_group(authorized_client, test_manpower_group_data):
    dt = {
        "start": "2021-02-03T13:12:25.332Z",
        "stop": "2100-02-03T13:12:25.332Z",
        "shift": 3
    }
    res = authorized_client.get('/manpower/group', json=dt)
    assert len(res.json()) == len(test_manpower_group_data)
    assert res.status_code == 200


def test_get_all_group(authorized_client_permissions_0):
    dt = {
        "start": "2021-02-03T13:12:25.332Z",
        "stop": "2100-02-03T13:12:25.332Z",
        "shift": 3
    }
    res = authorized_client_permissions_0.get('/manpower/group', json=dt)
    assert res.status_code == 403


def test_create_group(authorized_client):
    db_data = {
        "shift": 3,
        "note": "string"
    }
    res = authorized_client.post('/manpower/group', json=db_data)
    data = val_manpower.ManPowerGroupOut(**res.json())
    assert data.shift == 3
    assert data.note == 'String'
    assert res.status_code == 201


def test_create_group_unauthorized(authorized_client_permissions_0):
    db_data = {
        "shift": 3,
        "note": "string"
    }
    res = authorized_client_permissions_0.post('/manpower/group', json=db_data)
    assert res.status_code == 403


def test_delete_group(authorized_client, test_manpower_group_data):
    res = authorized_client.delete('/manpower/group/1')
    assert res.status_code == 205


def test_delete_group_unauthorized(authorized_client_permissions_0):
    res = authorized_client_permissions_0.delete('/manpower/group/1')
    assert res.status_code == 403
