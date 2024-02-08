from typing import List

from fastapi import HTTPException
from models.minter import Minter
from models.noid import Noid
from noid import mint as mint_noid
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select


def mint_new_noid(db_minter: Minter, n: int, binding: str | None = None) -> Noid:
    return Noid(
        noid=mint_noid(
            n=n,
            template=db_minter.template,
            scheme=db_minter.scheme,
            naa=db_minter.naa,
        ),
        n=n,
        binding=binding,
        minter_id=db_minter.id,
    )


async def create_noids(
    session: AsyncSession, db_minter: Minter, count: int = 1
) -> List[Noid]:
    # 2. mint next noid
    try:
        db_noids = []
        for n in range(db_minter.last_n, db_minter.last_n + count):
            # Create new noid and store
            db_noid = mint_new_noid(db_minter, n)
            session.add(db_noid)
            db_noids.append(db_noid)
            # 3. update minter
            db_minter.last_n = n + 1
        session.add(db_minter)
        await session.commit()
        return db_noids
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=409,
            detail="noid already exists",
        )


async def update_noid_binding(
    session: AsyncSession, db_minter: Minter, noid: str, binding: str
) -> str:
    db_noid: Noid = await get_noid(session=session, db_minter=db_minter, noid=noid)
    if db_noid is None:
        return None

    db_noid.binding = binding
    session.add(db_noid)
    await session.commit()
    await session.refresh(db_noid)
    return db_noid


async def delete_noid_binding(
    session: AsyncSession, db_minter: Minter, noid: str
) -> bool:
    db_noid: Noid = await get_noid(session=session, db_minter=db_minter, noid=noid)
    if db_noid is None:
        return None

    db_noid.binding = None
    session.add(db_noid)
    await session.commit()
    await session.refresh(db_noid)
    return db_noid


async def get_noid_binding(session: AsyncSession, db_minter: Minter, noid: str) -> str:
    db_noid: Noid = await get_noid(session=session, db_minter=db_minter, noid=noid)
    return db_noid.binding


async def create_and_bind_noids(
    session: AsyncSession, db_minter: Minter, bindings: str | List[str] = []
) -> List[Noid]:
    # 2. mint next noid
    try:
        # Ensure bindings is an array
        bindings = bindings if isinstance(bindings, list) else [bindings]
        n = db_minter.last_n
        db_noids = []
        for binding in bindings:
            db_noid = await get_noid_by_binding(
                session=session, db_minter=db_minter, binding=binding
            )

            if db_noid is None:
                # Create new noid and store
                db_noid = mint_new_noid(db_minter, n, binding=binding)
                session.add(db_noid)
                n = n + 1
            db_noids.append(db_noid)

        # 3. update minter
        db_minter.last_n = n
        session.add(db_minter)
        await session.commit()
        return db_noids
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=409,
            detail="noid already exists",
        )


async def get_noid_by_binding(
    session: AsyncSession, db_minter: Minter, binding: str
) -> Noid:
    query = (
        select(Noid)
        .where(Noid.minter_id == db_minter.id)
        .where(Noid.binding == binding)
    )
    response = await session.execute(query)
    return response.scalar_one_or_none()


async def get_noid(session: AsyncSession, db_minter: Minter, noid: str) -> Noid:
    query = select(Noid).where(Noid.minter_id == db_minter.id).where(Noid.noid == noid)
    response = await session.execute(query)
    return response.scalar_one_or_none()


async def get_noids(session: AsyncSession, db_minter: Minter) -> List[Noid]:
    query = select(Noid).where(Noid.minter_id == db_minter.id)
    response = await session.execute(query)
    return response.scalars().all()


async def get_noids_by_binding(
    session: AsyncSession, db_minter: Minter, binding: str
) -> Noid:
    query = (
        select(Noid)
        .where(Noid.minter_id == db_minter.id)
        .where(Noid.binding == binding)
    )
    response = await session.execute(query)
    return response.scalars().all()