from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


def test_items_get():
    response = client.get("/items/")
    assert response.status_code == 200


def test_items_post(item):
    response = client.post("/items/", data=item.json())
    assert response.status_code == 201
    assert response.json() == item.dict()
