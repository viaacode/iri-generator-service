import pytest
from api.routes.v1.noid import router as noid_router
from crud.noid import create_noids
from models.minter import MinterCreate
from crud.minter import create_minter, get_minter
from models.noid import NoidCreate
from tests.routes.conftest import BaseTestRouter
from core.config import settings

@pytest.mark.asyncio
class TestNoidRouter(BaseTestRouter):
    router = noid_router

    async def test_create_noid(self, session, client):
        minter = await create_minter(
            session, MinterCreate(naa="naa", template="template", scheme="scheme")
        )
        response = await client.post(f"/minters/{minter.id}/noids/")
        assert response.status_code == 201

        assert response.json()["naa"] == settings.NOID_NAA
        assert response.json()["scheme"] == settings.NOID_SCHEME
        assert response.json()["template"] == settings.NOID_TEMPLATE

    async def test_get_noid(self, session, client):
        minter = await create_minter(
            session, MinterCreate(naa="naa", template="template", scheme="scheme")
        )
        noid = await create_noids(session, minter)
        response = await client.get(f"/minters/{minter.id}/noids/{noid[0].noid}")
        assert response.status_code == 200
        assert response.json()["naa"] == minter.naa
        assert response.json()["scheme"] == minter.scheme
        assert response.json()["template"] == minter.template