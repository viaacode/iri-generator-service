from typing import List

from fastapi import HTTPException
from models.minter import Minter
from models.noid import MintRequest, Noid
from noid import mint as mint_noid
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import delete, select


async def create_noids(
    session: AsyncSession, db_minter: Minter, count: int = 1
) -> List[Noid]:
    # 2. mint next noid
    try:
        db_noids = []
        for n in range(db_minter.last_n, db_minter.last_n + count):
            # Create new noid and store
            db_noid = Noid(
                noid=mint_noid(
                    n=n,
                    template=db_minter.template,
                    scheme=db_minter.scheme,
                    naa=db_minter.naa,
                ),
                n=n,
                minter_id=db_minter.id,
            )
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


async def mint_noids(
    session: AsyncSession, db_minter: Minter, mint: MintRequest
) -> List[Noid]:
    # 2. mint next noid
    try:
        bindings = mint.bindings if isinstance(mint.bindings, list) else [mint.bindings]
        n = db_minter.last_n
        db_noids = []
        for binding in bindings:
            db_noid = await get_noid_by_binding(
                session=session, db_minter=db_minter, binding=binding
            )

            if db_noid is None:
                # Create new noid and store
                db_noid = Noid(
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
                session.add(db_noid)
                n = n + 1
            db_noids.append(db_noid)

        # 3. update minter
        db_minter.last_n = n
        session.add(db_minter)
        await session.commit()
        print(db_noids)
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
