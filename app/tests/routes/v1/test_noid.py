from urllib.parse import quote
import pytest
from api.routes.v1.minter import router as minter_router
from crud.noid import create_noids, update_noid_binding
from models.noid import NoidCreate
from tests.routes.conftest import BaseTestRouter
from noid import mint as mint_noid

@pytest.mark.asyncio
class TestNoidRouter(BaseTestRouter):
    router = minter_router

    async def test_create_noid(self, minter, client):
        noid = NoidCreate(
            noid=mint_noid(
                n=minter.last_n,
                template=minter.template,
                scheme=minter.scheme,
                naa=minter.naa,
            ),
            minter=minter,
            minter_id=minter.id,
            n=minter.last_n
        )
        response = await client.post(f"/minters/{minter.id}/noids/")
        assert response.status_code == 201
        assert len(response.json()) == 1
        assert response.json()[0]["noid"] == noid.noid
        assert response.json()[0]["binding"] == noid.binding
        assert response.json()[0]["n"] == noid.n
        assert response.json()[0]["minter_id"] == str(minter.id)

    async def test_get_noid(self, session, minter, client):
        noid, = await create_noids(session, minter)
        response = await client.get(f"/minters/{minter.id}/noids/{noid.noid}")
        assert response.status_code == 200
        assert response.json()["noid"] == noid.noid
        assert response.json()["binding"] == noid.binding
        assert response.json()["n"] == noid.n
        assert response.json()["minter_id"] == str(minter.id)

    async def test_get_noid_with_uri(self, session, uri_minter, client):
        noid, = await create_noids(session, uri_minter)
        quoted= quote(noid.noid,safe="")
        response = await client.get(f"/minters/{uri_minter.id}/noids/{quoted}")
        assert response.status_code == 200
        assert response.json()["noid"] == noid.noid
        assert response.json()["binding"] == noid.binding
        assert response.json()["n"] == noid.n
        assert response.json()["minter_id"] == str(uri_minter.id)

    async def test_get_noids(self, session, minter, client):
        noid, = await create_noids(session, minter)
        response = await client.get(f"/minters/{minter.id}/noids/")
        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]["noid"] == noid.noid
        assert response.json()[0]["binding"] == noid.binding
        assert response.json()[0]["n"] == noid.n
        assert response.json()[0]["minter_id"] == str(minter.id)

    async def test_get_noids_by_binding(self, session, minter, client):
        noid, = await create_noids(session, minter)
        updated_noid = await update_noid_binding(session, minter, noid.noid, 'test')
        response = await client.get(f"/minters/{minter.id}/noids/?binding=test")
        assert response.status_code == 200
        assert response.json()[0]["noid"] == noid.noid
        assert response.json()[0]["binding"] =='test'
        assert response.json()[0]["n"] == noid.n
        assert response.json()[0]["minter_id"] == str(minter.id)

    async def test_bind_noid(self, session, minter, client):
        noid, = await create_noids(session, minter)
        quoted= quote(noid.noid,safe="")
        response = await client.put(f"/minters/{minter.id}/noids/{quoted}?binding=test")
        assert response.status_code == 200
        assert response.json()["noid"] == noid.noid
        assert response.json()["binding"] == 'test'

        response2 = await client.put(f"/minters/{minter.id}/noids/{quoted}")
        assert response2.status_code == 405

    async def test_bind_noid_with_uri(self, session, uri_minter, client):
        noid, = await create_noids(session, uri_minter)
        quoted= quote(noid.noid,safe="")
        response = await client.put(f"/minters/{uri_minter.id}/noids/{quoted}?binding=test")
        assert response.status_code == 200
        assert response.json()["noid"] == noid.noid
        assert response.json()["binding"] == 'test'

        response2 = await client.put(f"/minters/{uri_minter.id}/noids/{quoted}")
        assert response2.status_code == 405

    async def test_delete_noid_binding(self, session, minter, client):
        noid, = await create_noids(session, minter)
        quoted= quote(noid.noid,safe="")
        response = await client.delete(f"/minters/{minter.id}/noids/{quoted}?binding")
        assert response.status_code == 200
        assert response.json()["noid"] == noid.noid
        assert response.json()["binding"] is None

        response2 = await client.delete(f"/minters/{minter.id}/noids/{quoted}")
        assert response2.status_code == 405