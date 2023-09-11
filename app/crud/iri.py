from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, delete
from uuid import UUID

from models.iri import IRI, IRICreate, IRIUpdate


async def create_iri(session: AsyncSession, iri: IRICreate) -> IRI:
    db_iri = IRI(**iri.dict())
    try:
        session.add(db_iri)
        await session.commit()
        await session.refresh(db_iri)
        return db_iri
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=409,
            detail="iri already exists",
        )


async def get_iri(session: AsyncSession, id: UUID) -> IRI:
    query = select(IRI).where(IRI.id == id)
    response = await session.execute(query)
    return response.scalar_one_or_none()


async def get_iri_by_key(session: AsyncSession, key: str) -> IRI:
    query = select(IRI).where(IRI.key == key)
    response = await session.execute(query)
    return response.scalar_one_or_none()


async def update_iri(session: AsyncSession, id: UUID, iri: IRIUpdate) -> IRI:
    db_iri = await get_iri(session, id)
    if not db_iri:
        raise HTTPException(status_code=404, detail="iri not found")

    for k, v in iri.dict(exclude_unset=True).items():
        setattr(db_iri, k, v)

    try:
        await session.commit()
        await session.refresh(db_iri)
        return db_iri
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=409,
            detail="Updated iri collides with other iris",
        )


async def delete_iri(session: AsyncSession, id: UUID) -> int:
    query = delete(IRI).where(IRI.id == id)
    response = await session.execute(query)
    await session.commit()
    return response.rowcount