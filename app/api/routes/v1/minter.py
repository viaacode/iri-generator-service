from crud.minter import create_minter, get_minters, get_minter
from db.session import get_session
from fastapi import APIRouter, HTTPException, status, Depends
from models.minter import MinterCreate, MinterResponse
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from api.routes.v1.bind import router as bind_router
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
    response_model=MinterResponse,
)
async def post_minter_route(minter: MinterCreate = MinterCreate(), db: AsyncSession = Depends(get_session)):
    return await create_minter(session=db, minter=minter)

# GET /minters
@router.get(
    "/",
    summary="Get all minters",
    status_code=status.HTTP_200_OK,
    response_model=List[MinterResponse],
)
async def get_minters_route(db: AsyncSession = Depends(get_session)):
    return await get_minters(session=db)

# GET /minters/{id}
@router.get(
    "/{id}",
    summary="Get minter",
    status_code=status.HTTP_200_OK,
    response_model=MinterResponse,
)
async def get_minter_route(id: UUID, db: AsyncSession = Depends(get_session)):
    minter = await get_minter(session=db, id=id)
    if minter is None:
        raise HTTPException(
            status_code=404,
            detail="Minter not found",
        )
    return minter

router.include_router(bind_router, prefix="/{id}/bind")
router.include_router(noid_router, prefix="/{id}/noids")