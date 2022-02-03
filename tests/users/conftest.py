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
