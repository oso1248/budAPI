import pytest


@pytest.fixture
def test_job_data(admin_authorized_client):
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
def test_user_job_data(admin_authorized_client):
    db_data = [
        {
            "id_users": 2,
            "id_jobs": 1,
            "skap": 2
        },
        {
            "id_users": 1,
            "id_jobs": 2,
            "skap": 6
        },
        {
            "id_users": 2,
            "id_jobs": 2,
            "skap": 2
        },
        {
            "id_users": 1,
            "id_jobs": 1,
            "skap": 6
        }
    ]
    for job in db_data:
        res = admin_authorized_client.post('/jobs/userjobs', json=job)
        assert res.status_code == 201

    return db_data
