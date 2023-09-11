from crud.iri import create_iri, get_iri, update_iri, delete_iri
from db.session import get_session
from fastapi import APIRouter, status, Depends
from models.base import DeleteResponse
from models.iri import IRICreate, IRIUpdate, IRIResponse
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

router = APIRouter(
    prefix="/iris",
    tags=["iris"],
)


@router.post(
    "/",
    summary="Create a new iri.",
    status_code=status.HTTP_201_CREATED,
    response_model=IRIResponse,
)
async def create_iri_route(
    data: IRICreate,
    db: AsyncSession = Depends(get_session),
):
    return await create_iri(session=db, iri=data)


@router.get(
    "/{id}",
    summary="Get a iri.",
    status_code=status.HTTP_200_OK,
    response_model=IRIResponse,
)
async def get_iri_route(id: UUID, db: AsyncSession = Depends(get_session)):
    return await get_iri(session=db, id=id)


@router.patch(
    "/{id}",
    summary="Update a iri.",
    status_code=status.HTTP_200_OK,
    response_model=IRIResponse,
)
async def update_iri_route(
    id: UUID,
    data: IRIUpdate,
    db: AsyncSession = Depends(get_session),
):
    return await update_iri(session=db, id=id, iri=data)


@router.delete(
    "/{id}",
    summary="Delete a iri.",
    status_code=status.HTTP_200_OK,
    response_model=DeleteResponse,
)
async def delete_iri_route(id: UUID, db: AsyncSession = Depends(get_session)):
    deleted = await delete_iri(session=db, id=id)
    return DeleteResponse(deleted=deleted)