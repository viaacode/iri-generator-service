from crud.noid import create_noids, get_noids, get_noid
from crud.minter import get_minter
from db.session import get_session
from fastapi import APIRouter, HTTPException, status, Depends
from models.noid import Noid
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List

router = APIRouter(
    tags=["noids"],
)


# POST /noids
@router.post(
    "/",
    summary="Create a new noid.",
    status_code=status.HTTP_201_CREATED,
    response_model=List[Noid],
)
async def post_noid_route(id: UUID, count: int  = 1, db: AsyncSession = Depends(get_session)):
    print('here!')
    db_minter = await get_minter(db, id=id)
    return await create_noids(session=db, db_minter=db_minter, count=count)


# GET /noids
@router.get(
    "/",
    summary="Get all noids",
    status_code=status.HTTP_200_OK,
    response_model=List[Noid],
)
async def get_noids_route(id: UUID, db: AsyncSession = Depends(get_session)):
    db_minter = await get_minter(db, id=id)
    return await get_noids(db, db_minter=db_minter)


# GET /noids/{noid}
@router.get(
    "/{noid}",
    summary="Get a noid",
    status_code=status.HTTP_200_OK,
    response_model=Noid,
)
async def get_noid_route(id: UUID, db: AsyncSession = Depends(get_session)):
    db_minter = await get_minter(db, id=id)
    noid = await get_noid(db, db_minter=db_minter, id=id)
    if noid is None:
        raise HTTPException(
            status_code=404,
            detail="Noid not found",
        )
    return noid
