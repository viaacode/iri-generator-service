from db.session import get_session
from fastapi import APIRouter, status, Depends
from models.base import DeleteResponse
from models.noid import NoidResponse
from crud.noid import get_noid
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

router = APIRouter(
    prefix="/noid",
    tags=["noids"],
)

# GET /noid/{noid}
@router.get(
    "/{noid}",
    summary="Get a noid by .",
    status_code=status.HTTP_200_OK,
    response_model=NoidResponse,
)
async def get_noid_route(n: int, db: AsyncSession = Depends(get_session)):
    return await get_noid(session=db, )


@router.put(
    "/{noid}/bindings/{bind}",
    summary="Put a binding a noid by number.",
    status_code=status.HTTP_200_OK,
    response_model=NoidResponse,
)
async def put_binding_route(n: int, db: AsyncSession = Depends(get_session)):
    return await get_bindings_by_noid(session=db, n=n)

# GET /noid/1?scheme=xx&&naa