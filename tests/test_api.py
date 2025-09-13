import json
import pytest
from app import create_app

@pytest.fixture()
def client():
    app = create_app({"TESTING": True})
    with app.test_client() as c:
        yield c


def test_list_inventory(client):
    resp = client.get("/inventory")
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data, list)
    assert len(data) >= 2


def test_create_get_update_delete(client):
    # Create
    payload = {
        "name": "Sparkling Water",
        "brand": "Bubbly",
        "price": 0.99,
        "stock": 100,
        "barcode": "1234567",
    }
    r = client.post("/inventory", data=json.dumps(payload), content_type="application/json")
    assert r.status_code == 201
    created = r.get_json()

    # Get
    r = client.get(f"/inventory/{created['id']}")
    assert r.status_code == 200
    assert r.get_json()["name"] == "Sparkling Water"

    # Patch
    r = client.patch(
        f"/inventory/{created['id']}",
        data=json.dumps({"price": 1.49, "stock": 80}),
        content_type="application/json",
    )
    assert r.status_code == 200
    patched = r.get_json()
    assert patched["price"] == 1.49
    assert patched["stock"] == 80

    # Delete
    r = client.delete(f"/inventory/{created['id']}")
    assert r.status_code == 204

    # Ensure gone
    r = client.get(f"/inventory/{created['id']}")
    assert r.status_code == 404