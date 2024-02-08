import logging
from urllib.parse import unquote
from crud.noid import (get_noids_by_binding, update_noid_binding, create_noids, delete_noid_binding, get_noid_binding, get_noids, get_noid)
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
async def get_noids_route(id: UUID, binding = None, db: AsyncSession = Depends(get_session)):
    db_minter = await get_minter(db, id=id)
    if binding is not None:
        return await get_noids_by_binding(db, db_minter=db_minter, binding=binding)
    return await get_noids(db, db_minter=db_minter)


# GET /noids/{noid}
@router.get(
    "/{noid:path}",
    summary="Get a noid",
    status_code=status.HTTP_200_OK,
    response_model=Noid,
)
async def get_noid_route(id: UUID, noid: str, db: AsyncSession = Depends(get_session)):
    db_minter = await get_minter(db, id=id)
    db_noid = await get_noid(db, db_minter=db_minter, noid=noid)
    if db_noid is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Noid {noid} not found",
        )
    return db_noid

# PUT /noids/{noid}
@router.put(
    "/{noid:path}",
    summary="Set a noid",
    status_code=status.HTTP_200_OK,
    response_model=Noid,
)
async def put_noid_route(id: UUID, noid: str, binding: str = None, db: AsyncSession = Depends(get_session)):
    if binding is None:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail=f"Parameter 'binding' not supplied.",
        )

    db_minter = await get_minter(db, id=id)
    db_noid = await update_noid_binding(session=db, db_minter=db_minter,noid=noid, binding=binding)
    if db_noid is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Noid {noid} not found",
        )
    
    return db_noid

@router.delete(
    "/{noid:path}",
    summary="Unbind a noid",
    status_code=status.HTTP_200_OK,
    response_model=Noid,
)
async def delete_binding_route(id: UUID, noid: str, binding: str = None, db: AsyncSession = Depends(get_session)):
    if binding is None:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail=f"Parameter 'binding' not supplied.",
        )

    db_minter = await get_minter(db, id=id)
    db_noid = await delete_noid_binding(session=db, db_minter=db_minter,noid=noid)
    if db_noid is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Noid {noid} not found",
        )
    return db_noid
