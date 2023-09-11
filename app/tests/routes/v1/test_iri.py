import pytest
from api.routes.v1.iri import router as iri_router
from crud.iri import create_iri, get_iri
from models.iri import IRICreate
from tests.routes.conftest import BaseTestRouter


@pytest.mark.asyncio
class TestUserRouter(BaseTestRouter):
    router = iri_router

    async def test_create_iri(self, client):
        data = {"key": "123456"}
        response = await client.post("/iris/", json=data)
        assert response.status_code == 201
        assert response.json()["key"] == data["key"]

    async def test_get_iri(self, session, client):
        iri = await create_iri(session, IRICreate(key="123456"))
        response = await client.get(f"/iris/{iri.id}")
        assert response.status_code == 200
        assert response.json()["key"] == iri.key

    async def test_update_iri(self, session, client):
        iri = await create_iri(session, IRICreate(key="123456"))
        response = await client.patch(
            f"/iris/{iri.id}", json=dict(key="abcdefg")
        )
        assert response.status_code == 200
        assert response.json()["key"] == iri.key

        iri_updated = await get_iri(session, id=iri.id)
        assert iri_updated.key == "abcdefg"

    async def test_delete_iri(self, session, client):
        iri = await create_iri(session, IRICreate(key="123456"))
        response = await client.delete(f"/iris/{iri.id}")
        assert response.status_code == 200
        assert response.json() == dict(deleted=1)

        iri_deleted = await get_iri(session, id=iri.id)
        assert iri_deleted is None