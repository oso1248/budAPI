from api.validators import val_jobs


def test_get_all_jobs(authorized_client, test_job_data):
    res = authorized_client.get('/jobs')
    assert len(res.json()) == len(test_job_data)
    assert res.status_code == 200


def test_get_all_jobs_empty(authorized_client):
    res = authorized_client.get('/jobs')
    assert res.status_code == 404


def test_get_all_jobs_unauthorized(authorized_client_permissions_0):
    res = authorized_client_permissions_0.get('/jobs')
    assert res.status_code == 403


def test_get_one_jobs(authorized_client, test_job_data):
    res = authorized_client.get('/jobs/1')
    job = val_jobs.JobOut(**res.json())
    assert job.id == 1
    assert res.status_code == 200


def test_get_one_jobs_empty(authorized_client, test_job_data):
    res = authorized_client.get('/jobs/5')
    assert res.status_code == 404


def test_get_one_jobs_unauthorized(authorized_client_permissions_0):
    res = authorized_client_permissions_0.get('/jobs/1')
    assert res.status_code == 403


def test_create_job(authorized_client):
    res = authorized_client.post('/jobs', json={
        "name": "Releasing",
        "area": "Finishing",
        "is_active": True,
        "is_work_restriction": False
    })

    new_user = val_jobs.JobOut(**res.json())
    assert new_user.name == 'Releasing'
    assert res.status_code == 201


def test_create_job_unauthorized(authorized_client_permissions_0):
    res = authorized_client_permissions_0.post('/jobs', json={
        "name": "Releasing",
        "area": "Finishing",
        "is_active": True,
        "is_work_restriction": False
    })
    assert res.status_code == 403


def test_update_job(authorized_client, test_job_data):
    res = authorized_client.put('/jobs/1', json={
        "name": "Support 1",
        "area": "Finishing",
        "is_active": False,
        "is_work_restriction": False
    })
    data = val_jobs.JobOut(**res.json())
    assert data.name == 'Support 1'
    assert data.is_active == False
    assert res.status_code == 200


def test_update_job_empty(authorized_client, test_job_data):
    res = authorized_client.put('/jobs/50', json={
        "name": "Support 1",
        "area": "Finishing",
        "is_active": False,
        "is_work_restriction": False
    })
    assert res.status_code == 404


def test_update_job_unauthorized(authorized_client_permissions_0):
    res = authorized_client_permissions_0.put('/jobs/1', json={
        "name": "Support 1",
        "area": "Finishing",
        "is_active": False,
        "is_work_restriction": False
    })
    assert res.status_code == 403


def test_delete_job(admin_authorized_client, test_job_data):
    res = admin_authorized_client.delete('/jobs/1')
    assert res.status_code == 205


def test_delete_job_unauthorized(authorized_client, test_job_data):
    res = authorized_client.delete('/jobs/1')
    assert res.status_code == 403


def test_update_skap(authorized_client, test_job_data, test_user_job_data):
    res = authorized_client.put('/jobs/userjobs', json={
        "id_users": 1,
        "id_jobs": 2,
        "skap": 1
    })

    data = val_jobs.UserJobOut(**res.json())
    assert data.brewer.id == 1
    assert data.job.id == 2
    assert data.skap == 1
    assert res.status_code == 200


def test_update_skap_empty_user(authorized_client, test_job_data, test_user_job_data):
    res = authorized_client.put('/jobs/userjobs', json={
        "id_users": 50,
        "id_jobs": 2,
        "skap": 1
    })
    assert res.status_code == 404


def test_update_skap_empty_job(authorized_client, test_job_data, test_user_job_data):
    res = authorized_client.put('/jobs/userjobs', json={
        "id_users": 1,
        "id_jobs": 50,
        "skap": 1
    })
    assert res.status_code == 404


def test_update_skap_unauthorized(authorized_client_permissions_0):
    res = authorized_client_permissions_0.put('/jobs/userjobs', json={
        "id_users": 1,
        "id_jobs": 50,
        "skap": 1
    })
    assert res.status_code == 403


def test_add_job_to_user(authorized_client, test_job_data):
    res = authorized_client.post('/jobs/userjobs', json={
        "id_users": 1,
        "id_jobs": 2,
        "skap": 6
    })

    data = val_jobs.UserJobOut(**res.json())
    assert data.brewer.id == 1
    assert data.job.id == 2
    assert data.skap == 6
    assert res.status_code == 201


def test_add_job_to_user_empty_user(authorized_client, test_job_data):
    res = authorized_client.post('/jobs/userjobs', json={
        "id_users": 100,
        "id_jobs": 2,
        "skap": 6
    })
    assert res.status_code == 404


def test_add_job_to_user_empty_job(authorized_client, test_job_data):
    res = authorized_client.post('/jobs/userjobs', json={
        "id_users": 1,
        "id_jobs": 200,
        "skap": 6
    })
    assert res.status_code == 404


def test_add_job_to_user_unauthorized(authorized_client_permissions_0):
    res = authorized_client_permissions_0.post('/jobs/userjobs', json={
        "id_users": 1,
        "id_jobs": 200,
        "skap": 6
    })
    assert res.status_code == 403


def test_delete_job_from_user(authorized_client, test_job_data, test_user_job_data):
    res = authorized_client.delete('/jobs/userjobs', json={
        "id_users": 1,
        "id_jobs": 2,
    })
    assert res.status_code == 205


def test_delete_job_from_user_empty_user(authorized_client, test_job_data, test_user_job_data):
    res = authorized_client.delete('/jobs/userjobs', json={
        "id_users": 50,
        "id_jobs": 2,
    })
    assert res.status_code == 404


def test_delete_job_from_user_empty_job(authorized_client, test_job_data, test_user_job_data):
    res = authorized_client.delete('/jobs/userjobs', json={
        "id_users": 1,
        "id_jobs": 50,
    })
    assert res.status_code == 404


def test_delete_job_from_user_unauthorized(authorized_client_permissions_0):
    res = authorized_client_permissions_0.delete('/jobs/userjobs', json={
        "id_users": 1,
        "id_jobs": 2,
    })
    assert res.status_code == 403


def test_get_job_with_users(authorized_client, test_job_data, test_user_job_data):
    res = authorized_client.get('/jobs/userjobs/jobs/1')
    data = res.json()
    data[0]['job']['id'] == data[1]['job']['id']
    assert res.status_code == 200


def test_get_job_with_users_empty_job(authorized_client, test_job_data, test_user_job_data):
    res = authorized_client.get('/jobs/userjobs/jobs/50')
    assert res.status_code == 404


def test_get_job_with_users_unauthorized(authorized_client_permissions_0):
    res = authorized_client_permissions_0.get('/jobs/userjobs/jobs/50')
    assert res.status_code == 403


def test_get_user_with_jobs(authorized_client, test_job_data, test_user_job_data):
    res = authorized_client.get('/jobs/userjobs/users/1')
    data = res.json()
    data[0]['brewer']['id'] == data[1]['brewer']['id']
    assert res.status_code == 200


def test_get_user_with_jobs_empty_user(authorized_client, test_job_data, test_user_job_data):
    res = authorized_client.get('/jobs/userjobs/users/50')
    assert res.status_code == 404


def test_get_user_with_jobs_unauthorized(authorized_client_permissions_0):
    res = authorized_client_permissions_0.get('/jobs/userjobs/users/1')
    assert res.status_code == 403
