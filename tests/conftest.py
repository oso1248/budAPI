from api.oauth2.oauth2 import create_access_token
from fastapi.testclient import TestClient
from api.database.database import get_db
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from api.config import settings
from api.models import mdl_user
from api.main import server
from sqlalchemy import text
import pytest


SQLALCHEMY_DATABASE_URL = f"""postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOST}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}_test"""

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope='function')
def session():
    mdl_user.Base.metadata.drop_all(bind=engine)
    mdl_user.Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope='function')
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    server.dependency_overrides[get_db] = override_get_db
    yield TestClient(server)


@pytest.fixture
def admin_user(session):
    session.execute("""INSERT INTO users (name, username, role, password, created_by, updated_by, brewery, permissions) VALUES ('Admin', 'admin', 'Admin', '$2b$12$uxpquslSDnH4qR/zKdWSEe6Tk5NNAqxZby14HYzDOn86wX2/Z75k2', 1, 1, 'FTC', 7);""")
    admin = session.execute(
        text("""SELECT id, name, permissions FROM users""")).all()
    return admin[0]


@pytest.fixture
def admin_token(admin_user):
    return create_access_token({'id': admin_user[0], 'name': admin_user[1], 'permissions': admin_user[2]})


@pytest.fixture
def admin_authorized_client(client, admin_token):
    client.headers = {**client.headers,
                      'Authorization': f'bearer {admin_token}'}
    return client


@pytest.fixture
def test_user(admin_authorized_client):
    user_data = {'name': 'Meika woollard', 'username': 'meiks', 'password': 'BudAdmin1!',
                 'is_active': True, 'role': 'BPM', 'brewery': 'FTC', 'permissions': 6}
    res = admin_authorized_client.post('/users', json=user_data)
    new_user = res.json()
    new_user['password'] = user_data['password']
    new_user['username'] = user_data['username']
    assert res.status_code == 201
    return new_user


@pytest.fixture
def test_user_permissions_0(admin_authorized_client):
    user_data = {'name': 'Meika woollard', 'username': 'meiks', 'password': 'BudAdmin1!',
                 'is_active': True, 'role': 'BPM', 'brewery': 'FTC', 'permissions': 0}
    res = admin_authorized_client.post('/users', json=user_data)
    new_user = res.json()
    new_user['password'] = user_data['password']
    new_user['username'] = user_data['username']
    assert res.status_code == 201
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({'id': test_user['id'], 'name': test_user['name'], 'permissions': test_user['permissions']})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {**client.headers, 'Authorization': f'bearer {token}'}
    return client


@pytest.fixture
def token_1(test_user_permissions_0):
    return create_access_token({'id': test_user_permissions_0['id'], 'name': test_user_permissions_0['name'], 'permissions': test_user_permissions_0['permissions']})


@pytest.fixture
def authorized_client_permissions_0(client, token_1):
    client.headers = {**client.headers, 'Authorization': f'bearer {token_1}'}
    return client
