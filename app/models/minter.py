from sqlmodel import SQLModel, Field

from models.base import IdMixin, TimestampMixin
from core.config import settings


class MinterBase(SQLModel):
    scheme: str = settings.NOID_SCHEME
    naa: str = Field(None, unique=True)
    template: str = settings.NOID_TEMPLATE
    last_n:int = 0


class MinterCreate(MinterBase):
    ...

class MinterUpdate(MinterBase):
    scheme: str = None
    naa: str = None
    template: str = None
    last_n:int = 0


class Minter(IdMixin, TimestampMixin, MinterBase, table=True):
    __tablename__ = "minters"


class MinterResponse(Minter, table=False):
    ...