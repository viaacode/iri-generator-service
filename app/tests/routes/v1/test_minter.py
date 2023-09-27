import pytest
from api.routes.v1.minter import router as minter_router
from crud.minter import create_minter, get_minter
from models.minter import MinterCreate
from tests.routes.conftest import BaseTestRouter
from core.config import settings


@pytest.mark.asyncio
class TestMintRouter(BaseTestRouter):
    router = minter_router

    async def test_create_minter(self, client):
        response = await client.post("/minters/")
        assert response.status_code == 201

        assert response.json()["naa"] == settings.NOID_NAA
        assert response.json()["scheme"] == settings.NOID_SCHEME
        assert response.json()["template"] == settings.NOID_TEMPLATE

    async def test_get_minter(self, session, client):
        minter = await create_minter(
            session, MinterCreate(naa="naa", template="template", scheme="scheme")
        )
        response = await client.get(f"/minters/{minter.id}")
        assert response.status_code == 200
        assert response.json()["naa"] == minter.naa
        assert response.json()["scheme"] == minter.scheme
        assert response.json()["template"] == minter.template

    async def test_get_minters(self, session, client):
        minter = await create_minter(
            session, MinterCreate(naa="naa", template="template", scheme="scheme")
        )
        response = await client.get("/minters/")
        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]["naa"] == minter.naa
        assert response.json()[0]["scheme"] == minter.scheme
        assert response.json()[0]["template"] == minter.template

    
    async def test_delete_user(self, session, client):
        minter = await create_minter(session, MinterCreate(naa="naa", template="template", scheme="scheme"))
        response = await client.delete(f"/minters/{minter.id}")
        assert response.status_code == 405
        # assert response.json() == dict(deleted=1)

        # user_deleted = await get_minter(session, id=minter.id)
        # assert user_deleted is None