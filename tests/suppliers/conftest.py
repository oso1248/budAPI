import pytest


@pytest.fixture
def test_supplier_data(admin_authorized_client):
    db_data = [
        {
            "name": "Supplier 1",
            "contact": "Contact 1",
            "email": "1user@example.com",
            "phone": "1234567890",
            "note": "Test Note",
            "is_active": True
        },
        {
            "name": "Supplier 2",
            "contact": "Contact 2",
            "email": "2user@example.com",
            "phone": "0987654321",
            "note": "Test Note",
            "is_active": True
        }
    ]
    for supplier in db_data:
        res = admin_authorized_client.post('/suppliers', json=supplier)
        assert res.status_code == 201

    return db_data
