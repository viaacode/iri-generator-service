import pytest
from api.routes.v1.minter import router as minter_router
from tests.routes.conftest import BaseTestRouter


@pytest.mark.asyncio
class TestMintRouter(BaseTestRouter):
    router = minter_router

    async def test_create_minter(self, client):
        response = await client.post("/minter/")
        assert response.status_code == 201
        assert len(response.json()["noids"]) == 1
        assert response.json()["noids"][0]["noid"] == "00000000"
        assert response.json()["noids"][0]["key"] is None
