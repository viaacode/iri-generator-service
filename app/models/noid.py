from models.base import IdMixin, TimestampMixin
from sqlmodel import SQLModel


class NoidBase(SQLModel):
    noid: str = None
    key: str = None


class NoidCreate(NoidBase):
    ...


class NoidUpdate(NoidBase):
    noid: str = None
    key: str = None


class Noid(IdMixin, TimestampMixin, NoidBase, table=True):
    __tablename__ = "noids"


class NoidResponse(Noid, table=False):
    ...
