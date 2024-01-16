from crud.noid import (update_noid_binding, create_noids, delete_noid_binding, get_noid_binding, get_noids, get_noid)
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
async def get_noid_route(id: UUID, noid: str, db: AsyncSession = Depends(get_session)):
    db_minter = await get_minter(db, id=id)
    db_noid = await get_noid(db, db_minter=db_minter, noid=noid)
    if db_noid is None:
        raise HTTPException(
            status_code=404,
            detail="Noid not found",
        )
    return db_noid

@router.put(
    "/{noid}/binding",
    summary="Bind a noid",
    status_code=status.HTTP_200_OK,
    response_model=Noid,
)
async def put_binding_route(id: UUID, noid: str, binding:str, db: AsyncSession = Depends(get_session)):
    db_minter = await get_minter(db, id=id)
    db_noid = await update_noid_binding(session=db, db_minter=db_minter,noid=noid, binding=binding)
    if db_noid is None:
        raise HTTPException(
            status_code=404,
            detail="Noid not found",
        )
    return db_noid

@router.delete(
    "/{noid}/binding",
    summary="Unbind a noid",
    status_code=status.HTTP_200_OK,
    response_model=Noid,
)
async def delete_binding_route(id: UUID, noid: str, db: AsyncSession = Depends(get_session)):
    db_minter = await get_minter(db, id=id)
    db_noid = await delete_noid_binding(session=db, db_minter=db_minter,noid=noid)
    if db_noid is None:
        raise HTTPException(
            status_code=404,
            detail="Noid not found",
        )
    return db_noid

@router.get(
    "/{noid}/binding",
    summary="Get the binding of this noid.",
    status_code=status.HTTP_200_OK,
    response_model=Noid,
)
async def get_binding_route(id: UUID, noid: str, db: AsyncSession = Depends(get_session)):
    db_minter = await get_minter(db, id=id)
    db_noid = await get_noid_binding(session=db, db_minter=db_minter,noid=noid)
    if db_noid is None:
        raise HTTPException(
            status_code=404,
            detail="Noid not found",
        )
    return db_noid