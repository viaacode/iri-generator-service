import pytest
from api.routes.v1.mint import router as mint_router
from tests.routes.conftest import BaseTestRouter


@pytest.mark.asyncio
class TestMintRouter(BaseTestRouter):
    router = mint_router

    async def test_mint_noid(self, client):
        response = await client.post("/mint/")
        assert response.status_code == 201
        assert len(response.json()["noids"]) == 1
        assert response.json()["noids"][0]["noid"] == "00000000"
        assert response.json()["noids"][0]["key"] is None

        response2 = await client.post("/mint/")
        assert response2.status_code == 201
        assert len(response2.json()["noids"]) == 1
        assert response2.json()["noids"][0]["noid"] != response.json()["noids"][0]["noid"]
        assert response2.json()["noids"][0]["key"] is None

    async def test_mint_noid_with_count(self, session, client):
        response = await client.post("/mint/?count=10")
        assert response.status_code == 201
        assert len(response.json()["noids"]) == 10
        assert response.json()["noids"][0]["noid"] == "00000000"
        assert response.json()["noids"][0]["key"] is None

    async def test_mint_noid_with_bind(self, session, client):
        response = await client.post("/mint/?bind=test")
        assert response.status_code == 201
        assert len(response.json()["noids"]) == 1

        noid1 = response.json()["noids"][0]

        assert noid1["noid"] == "00000000"
        assert noid1["key"] == "test"

        response2 = await client.post("/mint/?bind=test")
        noid2 = response2.json()["noids"][0]
        assert noid1["noid"] == noid2["noid"]
        assert noid1["key"] == noid2["key"]

    async def test_mint_noid_with_bind_and_invalid_count(self, session, client):
        response = await client.post("/mint/?bind=test&count=2")
        assert response.status_code == 400
