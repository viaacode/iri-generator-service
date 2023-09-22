from typing import List
from crud.noid import mint_noids
from crud.minter import get_minter
from db.session import get_session
from fastapi import APIRouter, status, Depends, HTTPException
from models.noid import MintRequest, Noid
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

router = APIRouter(
    tags=["mint"],
)

# /mint
# /mint?count=10
# /mint?bind="string"
# /mint?naa=""
@router.post(
    "/",
    summary="Get a new NOID.",
    status_code=status.HTTP_201_CREATED,
    response_model=List[Noid],
)
async def post_mint_route(id: UUID, mint: MintRequest, db: AsyncSession = Depends(get_session)):
    db_minter = await get_minter(db, id=id)
    return await mint_noids(session=db, db_minter=db_minter, mint=mint)

