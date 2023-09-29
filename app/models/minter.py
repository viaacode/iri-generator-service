from sqlalchemy import UniqueConstraint
from core.config import settings
from models.base import IdMixin, TimestampMixin
from sqlmodel import SQLModel

# import traceback

# print('check')
# for line in traceback.format_stack():
#         print(line.strip())


class MinterBase(SQLModel):
    scheme: str = settings.NOID_SCHEME
    naa: str = settings.NOID_NAA
    template: str = settings.NOID_TEMPLATE
    last_n: int = 0


class MinterCreate(MinterBase):
    scheme: str = settings.NOID_SCHEME
    naa: str = settings.NOID_NAA
    template: str = settings.NOID_TEMPLATE
    last_n: int = None


class MinterUpdate(MinterBase):
    scheme: str = None
    naa: str = None
    template: str = None
    last_n: int = None


class Minter(IdMixin, TimestampMixin, MinterBase, table=True):
    __tablename__ = "minters"
    __table_args__ = (
        UniqueConstraint("scheme", "naa", "template", name="unique_minter_binding"),
    )


class MinterResponse(Minter, table=False):
    ...
