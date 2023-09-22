from uuid_extensions import uuid7
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from models.minter import MinterCreate
from crud.minter import create_minter, get_minter, get_minters, delete_minter


async def test_create_minter(session: AsyncSession):
    minter = MinterCreate(naa="naa", template="template", scheme="scheme")
    created_minter = await create_minter(session, minter)
    assert created_minter.id is not None
    assert created_minter.naa == minter.naa
    assert created_minter.scheme == minter.scheme
    assert created_minter.template == minter.template
    assert created_minter.created_at is not None
    assert created_minter.updated_at is not None


async def test_get_minter(session: AsyncSession):
    minter = MinterCreate(naa="naa", template="template", scheme="scheme")
    created_minter = await create_minter(session, minter)
    retrieved_minter = await get_minter(session, created_minter.id)
    assert retrieved_minter == created_minter


async def test_get_nonexistent_minter(session: AsyncSession):
    retrieved_minter = await get_minter(session, uuid7())
    assert retrieved_minter is None

async def test_get_minters(session: AsyncSession):
    retrieved_minters = await get_minters(session)
    assert retrieved_minters.minters is not None
    assert len(retrieved_minters.minters) == 0

    minter = MinterCreate(naa="naa", template="template", scheme="scheme")
    created_minter = await create_minter(session, minter)
    assert len(retrieved_minters.minters) == 1
    assert retrieved_minters.minters[0] == created_minter

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


async def test_delete_minter(session: AsyncSession):
    minter = MinterCreate(naa="naa", template="template", scheme="scheme")
    created_minter = await create_minter(session, minter)
    deleted_count = await delete_minter(session, created_minter.id)
    assert deleted_count == 1
    retrieved_minter = await get_minter(session, created_minter.id)
    assert retrieved_minter is None


async def test_delete_nonexistent_iri(session: AsyncSession):
    deleted_count = await delete_minter(session, uuid7())
    assert deleted_count == 0