from typing import List, Optional
from uuid import UUID

from models.base import TimestampMixin
from models.minter import Minter
from pydantic import BaseModel
from sqlmodel import Field, Relationship, SQLModel


class NoidBase(SQLModel):
    noid: str = Field(
        primary_key=True,
        index=True,
        nullable=False,
    )
    binding: Optional[str] = None
    n: int
    minter_id: UUID = Field(nullable=False, foreign_key="minters.id")
    minter: Minter = Relationship(back_populates="minters")


class NoidCreate(NoidBase):
    ...


class NoidUpdate(NoidBase):
    noid: str = None
    binding: str = None


class Noid(TimestampMixin, NoidBase, table=True):
    __tablename__ = "noids"


class MintRequest(BaseModel):
    bindings: str | List[str] = []
