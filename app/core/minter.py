from noid import mint
from core.config import settings


def mint_new_noid(n: int, naa: str = None):
    return mint(
        n=n,
        template=settings.NOID_TEMPLATE,
        scheme=settings.NOID_SCHEME if settings.NOID_SCHEME is not None else "",
        naa=naa if naa is not None else "",
    )
