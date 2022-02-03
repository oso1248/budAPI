from api.validators import val_user, val_auth
from api.config import settings
from jose import jwt
import pytest


def test_login_user(client, test_user):
    res = client.post(
        '/login', data={'username': test_user['username'], 'password': test_user['password']})

    login_res = val_auth.Token(**res.json())
    payload = jwt.decode(login_res.access_token,
                         settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    id = payload['id']
    assert id == test_user['id']
    assert login_res.token_type == 'bearer'
    assert res.status_code == 200


@pytest.mark.parametrize('username, password, status_code', [
    ('wrongname', 'password123', 403),
    ('username', 'wrongpassword', 403),
    ('wrongname', 'wrongemail', 403),
    (None, 'wrongpassword', 422),
    ('wrongname', None, 422),
])
def test_incorrect_login(client, test_user, username, password, status_code):
    res = client.post(
        '/login', data={'username': username, 'password': password})
    res_data = res.json()
    assert res.status_code == status_code
