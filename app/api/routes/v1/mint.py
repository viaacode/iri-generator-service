from crud.noid import mint_noid_and_bind
from db.session import get_session
from fastapi import APIRouter, status, Depends, HTTPException
from models.mint import MintRequest, MintResponse
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

router = APIRouter(
    prefix="/mint",
    tags=["mint"],
)

# /mint
# /mint?count=10
# /mint?bind="string"
# /mint?naa=""
@router.post(
    "/",
    summary="Get a new IRI.",
    status_code=status.HTTP_201_CREATED,
    response_model=MintResponse,
)
async def post_mint_route(count: int = 1, bind:str = None, naa:str = None, db: AsyncSession = Depends(get_session)):
    if count < 1:
        raise HTTPException(
            status_code=400,
            detail="The count parameter cannot be 0 or less.",
        )

    if bind is not None and count != 1:
        raise HTTPException(
            status_code=400,
            detail="Cannot bind more than one noid.",
        )

    return await mint_noid_and_bind(session=db, mint=MintRequest(count=count, naa=naa, bind=bind))
