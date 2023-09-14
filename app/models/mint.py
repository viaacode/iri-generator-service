from pydantic import BaseModel
from models.noid import Noid

class MintRequest(BaseModel):
    naa: str | None = None
    bind: str | None = None
    count: int = 1

class MintResponse(BaseModel):
    noids: list[Noid] = []