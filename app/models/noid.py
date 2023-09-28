from typing import List, Optional
from uuid import UUID

from sqlalchemy import UniqueConstraint

from models.base import IdMixin, TimestampMixin
from models.minter import Minter
from pydantic import BaseModel
from sqlmodel import Field, Relationship, SQLModel


class NoidBase(SQLModel):
    noid: str = Field(
        index=True,
        nullable=False,
    )
    binding: Optional[str] = Field(
        index=True,
        nullable=True,
    )
    n: int
    minter_id: UUID = Field(nullable=False, foreign_key="minters.id")
    minter: Minter = Relationship(back_populates="minters")


class NoidCreate(NoidBase):
    ...


class NoidUpdate(NoidBase):
    noid: str = None
    binding: str = None


class Noid(IdMixin, TimestampMixin, NoidBase, table=True):
    __tablename__ = "noids"
    __table_args__ = (
        UniqueConstraint("noid", "binding", "minter_id", name="unique_noid_binding"),
    )


class NoidResponse(Minter, table=False):
    ...


class MintRequest(BaseModel):
    bindings: str | List[str] = []
