import pytest
from api.routes.v1.minter import router as minter_router
from tests.routes.conftest import BaseTestRouter


@pytest.mark.asyncio
class TestBindRouter(BaseTestRouter):
    router = minter_router

    async def test_bind_noid(self, minter, client):
        response = await client.post(f"/minters/{minter.id}/bind/", json={'bindings': 'test'})
        assert response.status_code == 201
        assert len(response.json()) == 1
        assert response.json()[0]["noid"] == "00"
        assert response.json()[0]["binding"] == 'test'

    async def test_bind_noids(self, minter, client):
        response = await client.post(f"/minters/{minter.id}/bind/", json={'bindings': ['test', 'test2']})
        assert response.status_code == 201
        assert len(response.json()) == 2
        assert response.json()[0]["noid"] == "00"
        assert response.json()[0]["binding"] == 'test'
        assert response.json()[1]["noid"] == "11"
        assert response.json()[1]["binding"] == 'test2'
        
    async def test_get_binding(self, minter, client):
        response = await client.get(f"/minters/{minter.id}/bind/test")
        assert response.status_code == 200
        assert response.json()["noid"] == "00"
        assert response.json()["binding"] == 'test'

        response2 = await client.get(f"/minters/{minter.id}/bind/test")
        assert response2.status_code == 200
        assert response2.json() == response.json()

        response3 = await client.get(f"/minters/{minter.id}/bind/test2")
        assert response3.status_code == 200
        assert response3.json() != response.json()