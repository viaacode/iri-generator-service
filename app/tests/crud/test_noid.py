from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from models.minter import Minter
from models.noid import NoidCreate
from crud.noid import (create_and_bind_noids, get_noid, get_noid_binding, get_noid_by_binding, create_noids, delete_noid_binding, update_noid_binding, mint_new_noid)
from noid import mint as mint_noid


async def test_create_noids(session: AsyncSession, minter: Minter):
    # Expected object
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
    # actual
    created_noid, = await create_noids(session, db_minter=minter)

    # compare
    assert created_noid is not None
    assert created_noid.binding == noid.binding
    assert created_noid.noid == noid.noid
    assert created_noid.created_at is not None
    assert created_noid.updated_at is not None


    next_noid, = await create_noids(session, db_minter=minter)
    assert created_noid.noid != next_noid.noid

async def test_create_multiple_noids(session: AsyncSession, minter: Minter):
    noid1 = NoidCreate(
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
    noid2 = NoidCreate(
        noid=mint_noid(
            n=minter.last_n + 1,
            template=minter.template,
            scheme=minter.scheme,
            naa=minter.naa,
        ),
        minter=minter,
        minter_id=minter.id,
        n=minter.last_n + 1
    )
    created_noids = await create_noids(session, db_minter=minter, count=2)
    assert len(created_noids) == 2

    assert created_noids[0].binding == noid1.binding
    assert created_noids[0].noid == noid1.noid
    assert created_noids[1].binding == noid2.binding
    assert created_noids[1].noid == noid2.noid

    assert created_noids[0].created_at != created_noids[1].created_at
    assert created_noids[0].updated_at != created_noids[1].updated_at
    assert created_noids[0].noid != created_noids[1].noid

    next_noid, = await create_noids(session, db_minter=minter)
    assert created_noids[0].noid != next_noid.noid
    assert created_noids[1].noid != next_noid.noid

async def test_get_noid(session: AsyncSession, minter: Minter):
    # Expected
    noid = mint_noid(
            n=minter.last_n,
            template=minter.template,
            scheme=minter.scheme,
            naa=minter.naa,
        )
    # store
    created_noid, = await create_noids(session, db_minter=minter)
    # actual
    retrieved_noid = await get_noid(session, minter, created_noid.noid)
    assert retrieved_noid == created_noid
    assert retrieved_noid.noid == noid

# TODO: for milan
# async def test_get_noid_with_uri(session: AsyncSession, minter: Minter):
#     # Expected
#     noid = mint_noid(
#             n=minter.last_n,
#             template=minter.template,
#             scheme=minter.scheme,
#             naa=minter.naa,
#         )
#     # store
#     created_noid, = await create_noids(session, db_minter=minter)
#     # actual
#     retrieved_noid = await get_noid(session, minter, created_noid.noid)
#     assert retrieved_noid == created_noid
#     assert retrieved_noid.noid == noid

async def test_mint_new_noid(session: AsyncSession, minter: Minter):
    noid = mint_new_noid(minter, 0)
    assert noid is not None
    assert noid.binding is None
    assert noid.noid == '00'
    assert noid.created_at is not None
    assert noid.updated_at is not None

async def test_mint_new_noid_with_binding(session: AsyncSession, minter: Minter):
    noid = mint_new_noid(minter, 1, 'test')
    assert noid is not None
    assert noid.binding == 'test'
    assert noid.noid == '11'
    assert noid.created_at is not None
    assert noid.updated_at is not None

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

async def test_create_duplicate_noid(session: AsyncSession, minter: Minter):
    n = minter.last_n
    await create_noids(session, db_minter=minter)
    try:
        minter.last_n = n
        await create_noids(session, db_minter=minter)
    except HTTPException as e:
        assert e.status_code == 409
        assert e.detail == "noid already exists"


async def test_get_noid_by_binding(session: AsyncSession, minter: Minter):
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
    created_noid, = await create_and_bind_noids(session, db_minter=minter, bindings='test')
    retrieved_noid = await get_noid_by_binding(session, db_minter=minter, binding='test')
    assert retrieved_noid == created_noid


async def test_get_nonexistent_noid_by_binding(session: AsyncSession, minter: Minter):
    retrieved_noid = await get_noid_by_binding(session, db_minter=minter, binding='test')
    assert retrieved_noid is None


async def test_update_noid_binding(session: AsyncSession, minter: Minter):
    created_noid, = await create_noids(session, db_minter=minter)
    binding = await update_noid_binding(session, db_minter=minter, noid=created_noid.noid, binding='test')
    assert binding == 'test'
    assert binding == created_noid.binding


async def test_update_binding_of_nonexistent_noid(session: AsyncSession, minter: Minter):
    binding = await update_noid_binding(session, db_minter=minter, noid='test', binding='test')
    assert binding is None


async def test_delete_noid_binding(session: AsyncSession, minter: Minter):
    created_noid, = await create_and_bind_noids(session, db_minter=minter, bindings="test")
    success = await delete_noid_binding(session, db_minter=minter, noid=created_noid.noid)
    assert success
    retrieved_noid = await get_noid_by_binding(session, db_minter=minter, binding="test")
    assert retrieved_noid is None
    retrieved_binding = await get_noid_binding(session, db_minter=minter, noid=created_noid.noid)
    assert retrieved_binding is None


async def test_delete_nonexistent_noid_binding(session: AsyncSession, minter: Minter):
    success = await delete_noid_binding(session, db_minter=minter, noid='test')
    assert not success
