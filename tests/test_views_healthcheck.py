import pytest
from starlette import status


@pytest.mark.asyncio
async def test_view_health_check_200_ok(get_client, get_app):
    res = await get_client.get(get_app.url_path_for('health-check'))
    assert res.status_code == status.HTTP_200_OK
