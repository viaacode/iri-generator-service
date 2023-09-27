from uuid_extensions import uuid7
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from crud.minter import create_minter
from models.minter import Minter, MinterCreate
from models.noid import MintRequest, NoidCreate
from crud.noid import get_noid, get_noid_by_binding, create_noids
from noid import mint as mint_noid


async def test_create_noids(session: AsyncSession, minter: Minter):
    # minter = MinterCreate(naa="naa", template="template", scheme="scheme")
    # created_minter = await create_minter(session, minter)

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
    created_noid, = await create_noids(session, db_minter=minter)
    assert created_noid is not None
    assert created_noid.binding == noid.binding
    assert created_noid.noid == noid.noid
    assert created_noid.created_at is not None
    assert created_noid.updated_at is not None


    next_noid, = await create_noids(session, db_minter=minter)
    assert created_noid.noid != next_noid.noid

async def test_get_noid(session: AsyncSession, minter: Minter):
    noid = mint_noid(
            n=minter.last_n,
            template=minter.template,
            scheme=minter.scheme,
            naa=minter.naa,
        )
    created_noid, = await create_noids(session, db_minter=minter)
    retrieved_noid = await get_noid(session, minter, created_noid.noid)
    assert retrieved_noid == created_noid
    assert retrieved_noid.noid == noid
    

def test_mint_noid():
    n = 0
    assert mint_noid(n=n) == '00'
    n = n+1
    assert mint_noid(n=n) == '11'

def test_mint_noid_with_naa():
    n = 0
    assert mint_noid(n=n, naa='id') == 'id/00'
    n = n+1
    assert mint_noid(n=n, naa='id') == 'id/11'

# async def test_create_duplicate_iri(session: AsyncSession):
#     iri = IRICreate(key="123456")
#     await create_iri(session, iri)
#     try:
#         await create_iri(session, iri)
#     except HTTPException as e:
#         assert e.status_code == 409
#         assert e.detail == "iri already exists"


# async def test_get_iri(session: AsyncSession):
#     iri = IRICreate(key="123456")
#     created_iri = await create_iri(session, iri)
#     retrieved_iri = await get_iri(session, created_iri.id)
#     assert retrieved_iri == created_iri


# async def test_get_nonexistent_iri(session: AsyncSession):
#     retrieved_iri = await get_iri(session, uuid7())
#     assert retrieved_iri is None


# async def test_get_iri_by_key(session: AsyncSession):
#     iri = IRICreate(key="123456")
#     created_iri = await create_iri(session, iri)
#     retrieved_iri = await get_iri_by_key(session, iri.key)
#     assert retrieved_iri == created_iri


# async def test_get_nonexistent_iri_by_key(session: AsyncSession):
#     retrieved_iri = await get_iri_by_key(session, "123456")
#     assert retrieved_iri is None


# async def test_update_iri(session: AsyncSession):
#     created_iri = await create_iri(
#         session, IRICreate(namespace="http://example.org/", key="123456")
#     )
#     updated_iri = await update_iri(
#         session, created_iri.id, IRIUpdate(namespace="http://example.org/")
#     )
#     assert updated_iri.id == created_iri.id
#     assert updated_iri.key == "123456"
#     assert updated_iri.namespace == "http://example.org/"


# async def test_update_nonexistent_iri(session: AsyncSession):
#     try:
#         await update_iri(session, uuid7(), IRIUpdate(namespace="http://example.org/"))
#     except HTTPException as e:
#         assert e.status_code == 404
#         assert e.detail == "iri not found"


# async def test_delete_iri(session: AsyncSession):
#     created_iri = await create_iri(session, IRICreate(key="123456"))
#     deleted_count = await delete_iri(session, created_iri.id)
#     assert deleted_count == 1
#     retrieved_iri = await get_iri(session, created_iri.id)
#     assert retrieved_iri is None


# async def test_delete_nonexistent_iri(session: AsyncSession):
#     deleted_count = await delete_iri(session, uuid7())
#     assert deleted_count == 0
