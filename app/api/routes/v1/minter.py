from crud.minter import create_minter, get_minters, get_minter
from db.session import get_session
from fastapi import APIRouter, HTTPException, status, Depends
from models.minter import MinterCreate, Minter
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from api.routes.v1.mint import router as mint_router
from api.routes.v1.noid import router as noid_router
from typing import List

router = APIRouter(
    prefix="/minters",
    tags=["minters"],
)

# POST /minters
@router.post(
    "/",
    summary="Create a new minter.",
    status_code=status.HTTP_201_CREATED,
    response_model=Minter,
)
async def post_minter_route(minter: MinterCreate, db: AsyncSession = Depends(get_session)):
    return await create_minter(db, minter)

# GET /minters
@router.get(
    "/",
    summary="Get all minters",
    status_code=status.HTTP_200_OK,
    response_model=List[Minter],
)
async def get_minters_route(db: AsyncSession = Depends(get_session)):
    return await get_minters(db)

# GET /minters/{id}
@router.get(
    "/{id}",
    summary="Get minter",
    status_code=status.HTTP_200_OK,
    response_model=Minter,
)
async def get_minter_route(id: UUID, db: AsyncSession = Depends(get_session)):
    minter = await get_minter(db, id=id)
    if minter is None:
        raise HTTPException(
            status_code=404,
            detail="Minter not found",
        )
    return minter

router.include_router(mint_router, prefix="/{id}/mint")
router.include_router(noid_router, prefix="/{id}/noids")