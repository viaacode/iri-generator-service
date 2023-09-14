from core.minter import mint_new_noid
from crud.minter import create_minter, get_minter_by_naa, update_minter_n
from fastapi import HTTPException
from models.mint import MintRequest, MintResponse
from models.minter import Minter
from models.noid import Noid, NoidCreate
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import delete, select


async def mint_noid_and_bind(session: AsyncSession, mint: MintRequest) -> MintResponse:
    if mint.bind is None:
        noids = []
        for i in range(0, mint.count):
            noids.append(await mint_noid(session, mint=mint))
        return MintResponse(noids=noids)

    # 1. get noid by key
    db_noid = await get_noid_by_key(session, key=mint.bind)
    # 2. If noid does not exist, create and store new one
    if db_noid is None:
        noid: Noid = await mint_noid(session, mint=mint)
        db_noid = await create_noid(session, noid)

    return MintResponse(noids=[db_noid])


async def mint_noid(session: AsyncSession, mint: MintRequest) -> Noid:
    # 1. get minter config from DB
    db_minter: Minter = await get_minter_by_naa(session, naa=mint.naa)

    if db_minter is None:
        db_minter = await create_minter(session, naa=mint.naa)

    # 2. mint next noid
    noid = Noid(noid=mint_new_noid(n=db_minter.last_n, naa=mint.naa), key=mint.bind)

    # 3. update minter
    await update_minter_n(session, id=db_minter.id, n=db_minter.last_n + 1)

    return noid


async def get_noid_by_key(session: AsyncSession, key: str) -> Noid:
    query = select(Noid).where(Noid.key == key)
    response = await session.execute(query)
    return response.scalar_one_or_none()


async def get_noid(session: AsyncSession, noid: str) -> Noid:
    query = select(Noid).where(Noid.noid == noid)
    response = await session.execute(query)
    return response.scalar_one_or_none()


async def create_noid(session: AsyncSession, noid: NoidCreate) -> Noid:
    db_noid = Noid(**noid.dict())
    try:
        session.add(db_noid)
        await session.commit()
        await session.refresh(db_noid)
        return db_noid
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=409,
            detail="noid already exists",
        )
