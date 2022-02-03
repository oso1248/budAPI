import pytest


@pytest.fixture
def test_user_data(admin_authorized_client, session):
    user_data = [{'name': 'maria kowalchuk', 'username': 'mariac', 'password': 'BudAdmin1!',
                  'is_active': True, 'role': 'BPM', 'brewery': 'FTC', 'permissions': 6},
                 {'name': 'abby sarnoski', 'username': 'abbys', 'password': 'BudAdmin1!',
                 'is_active': True, 'role': 'BPM', 'brewery': 'FTC', 'permissions': 6},
                 {'name': 'rachel hinkel', 'username': 'rachh', 'password': 'BudAdmin1!',
                 'is_active': True, 'role': 'BPM', 'brewery': 'FTC', 'permissions': 6},
                 {'name': 'alexis ren', 'username': 'lexir', 'password': 'BudAdmin1!',
                 'is_active': True, 'role': 'BPM', 'brewery': 'FTC', 'permissions': 6},
                 ]
    for user in user_data:
        res = admin_authorized_client.post('/users', json=user)
        assert res.status_code == 201
    return user_data


@pytest.fixture
def test_job_data(admin_authorized_client, test_user_data):
    db_data = [
        {
            "name": "Filters",
            "area": "Finishing",
            "is_active": True,
            "is_work_restriction": False
        },
        {
            "name": "BH Panel",
            "area": "Brewhouse",
            "is_active": True,
            "is_work_restriction": False
        },
    ]
    for job in db_data:
        res = admin_authorized_client.post('/jobs', json=job)
        assert res.status_code == 201

    return db_data


@pytest.fixture
def test_user_job_data(admin_authorized_client, test_job_data):
    db_data = [
        {
            "id_users": 1,
            "id_jobs": 1,
            "skap": 2
        },
        {
            "id_users": 2,
            "id_jobs": 2,
            "skap": 6
        },
        {
            "id_users": 3,
            "id_jobs": 2,
            "skap": 2
        },
        {
            "id_users": 4,
            "id_jobs": 1,
            "skap": 6
        }
    ]
    for job in db_data:
        res = admin_authorized_client.post('/jobs/userjobs', json=job)
        assert res.status_code == 201

    return db_data


@pytest.fixture
def test_manpower_individual_data(admin_authorized_client, test_user_job_data):
    db_data = [
        {
            "shift": 3,
            "id_users": 3,
            "id_jobs": 1,
            "note": "string"
        },
        {
            "shift": 3,
            "id_users": 4,
            "id_jobs": 2,
            "note": "string"
        }
    ]

    for job in db_data:
        res = admin_authorized_client.post('/manpower/individual', json=job)
        assert res.status_code == 201

    return db_data


@pytest.fixture
def test_manpower_group_data(admin_authorized_client):
    db_data = [
        {
            "shift": 3,
            "note": "string"
        },
        {
            "shift": 3,
            "note": "string"
        }
    ]

    for job in db_data:
        res = admin_authorized_client.post('/manpower/group', json=job)
        assert res.status_code == 201

    return db_data
