from models.noid import Noid
from pydantic import BaseModel


class MintRequest(BaseModel):
    naa: str | None = None
    bind: str | None = None
    count: int = 1


class MintResponse(BaseModel):
    noids: list[Noid] = []
