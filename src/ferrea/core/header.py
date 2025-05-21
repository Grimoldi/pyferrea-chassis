import uuid
from typing import Annotated

from fastapi import Header

FERRA_CORRELATION_HEADER = "ferrea-correlation-id"


async def get_correlation_id(
    ferrea_correlation_id: Annotated[str | None, Header()] = None,
) -> uuid.UUID:
    """Extract the correlation id from the `ferrea-correlation-id` id."""
    if ferrea_correlation_id is None:
        return uuid.uuid4()

    return uuid.UUID(ferrea_correlation_id)
