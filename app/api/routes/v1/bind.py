from typing import Annotated, List
from crud.noid import create_and_bind_noids, get_noid_by_binding
from crud.minter import get_minter
from db.session import get_session
from fastapi import APIRouter, Query, status, Depends, HTTPException
from models.noid import MintRequest, Noid
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

router = APIRouter(
    tags=["mint"],
)

# /bind
@router.post(
    "/",
    summary="Get a new NOID.",
    status_code=status.HTTP_201_CREATED,
    response_model=List[Noid],
)
async def post_bind_route(id: UUID, mint: MintRequest, db: AsyncSession = Depends(get_session)):
    db_minter = await get_minter(db, id=id)
    return await create_and_bind_noids(session=db, db_minter=db_minter, bindings=mint.bindings)

@router.get(
    "/{binding}",
    summary="Get a NOID by its binding.",
    status_code=status.HTTP_200_OK,
    response_model=Noid,
)
async def get_bind_route(id: UUID, binding: str, db: AsyncSession = Depends(get_session)):
    db_minter = await get_minter(db, id=id)
    db_noids = await create_and_bind_noids(session=db, db_minter=db_minter, bindings=binding)
    return db_noids[0]