import pytest


@pytest.mark.asyncio
async def test_items_get(get_client):
    response = await get_client.get("/items/")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_items_post(item, get_client):
    response = await get_client.post("/items/", content=item.json())
    assert response.status_code == 201
    assert response.json() == item.dict()
