from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, delete
from uuid import UUID

from models.minter import Minter


async def create_minter(session: AsyncSession, naa: str) -> Minter:
    db_minter = Minter(naa=naa)
    try:
        session.add(db_minter)
        await session.commit()
        await session.refresh(db_minter)
        return db_minter
    except IntegrityError:
        session.rollback()


async def get_minter(session: AsyncSession, id: UUID) -> Minter:
    query = select(Minter).where(Minter.id == id)
    response = await session.execute(query)
    return response.scalar_one_or_none()


async def get_minter_by_naa(session: AsyncSession, naa: str) -> Minter:
    query = select(Minter).where(Minter.naa == naa)
    response = await session.execute(query)
    return response.scalar_one_or_none()


async def update_minter_n(session: AsyncSession, id: UUID, n: int) -> Minter:
    db_minter = await get_minter(session, id)
    db_minter.last_n = n

    try:
        await session.commit()
        await session.refresh(db_minter)
        return db_minter
    except IntegrityError:
        session.rollback()


async def delete_minter(session: AsyncSession, id: UUID) -> int:
    query = delete(Minter).where(Minter.id == id)
    response = await session.execute(query)
    await session.commit()
    return response.rowcount