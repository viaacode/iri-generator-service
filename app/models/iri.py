from sqlmodel import SQLModel

from models.base import IdMixin, TimestampMixin


class IRIBase(SQLModel):
    noid: str = None
    namespace: str = None
    key: str = None


class IRICreate(IRIBase):
    ...


class IRIUpdate(IRIBase):
    noid: str = None
    namespace: str = None
    key: str = None


class IRI(IdMixin, TimestampMixin, IRIBase, table=True):
    __tablename__ = "iris"


class IRIResponse(IRI, table=False):
    ...