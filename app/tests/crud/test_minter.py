from uuid_extensions import uuid7
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from models.minter import MinterCreate
from crud.minter import create_minter, get_minter, get_minters, delete_minter, get_minter_by_naa


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
    assert retrieved_minters is not None
    assert len(retrieved_minters) == 0

    minter = MinterCreate(naa="naa", template="template", scheme="scheme")
    created_minter = await create_minter(session, minter)
    retrieved_minters = await get_minters(session)
    assert len(retrieved_minters) == 1
    assert retrieved_minters[0] == created_minter

async def test_get_minter_by_naa(session: AsyncSession):
    minter = MinterCreate(naa="naa")
    created_minter = await create_minter(session, minter)
    retrieved_minter = await get_minter_by_naa(session, minter.naa)
    assert retrieved_minter == created_minter


async def test_get_nonexistent_minter_by_naa(session: AsyncSession):
    retrieved_minter = await get_minter_by_naa(session, "test")
    assert retrieved_minter is None


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