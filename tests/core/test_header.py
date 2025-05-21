import json
import uuid
from typing import Annotated

from fastapi import Depends, FastAPI, Response
from fastapi.testclient import TestClient

from ferrea.core.header import get_correlation_id

FOO_ENDPOINT = "/foo"
FERRA_CORRELATION_HEADER = "ferrea-correlation-id"
FERREA_CORRELATION_VALUE = str(uuid.uuid4())


def make_fake_app() -> FastAPI:
    """Create a fake app just for the sake of the tests."""
    app = FastAPI()

    @app.get(FOO_ENDPOINT)
    async def get_foo(
        response: Response,
        _id: Annotated[uuid.UUID, Depends(get_correlation_id)],
    ):
        """Foo endpoint."""
        content = {"foo": "bar"}
        response.headers[FERRA_CORRELATION_HEADER] = str(_id)
        return content

    return app


def test_correlation_header_added() -> None:
    """Test the automatically insert of the correlation header in a response, given the absence in the request."""
    app = make_fake_app()
    client = TestClient(app)

    response = client.get(FOO_ENDPOINT)
    assert FERRA_CORRELATION_HEADER in response.headers


def test_correlation_header_unmodified() -> None:
    """Test tha given a correlation header in the request, it is kept in the response."""
    app = make_fake_app()
    client = TestClient(app)

    headers = {FERRA_CORRELATION_HEADER: FERREA_CORRELATION_VALUE}
    response = client.get(FOO_ENDPOINT, headers=headers)
    assert FERREA_CORRELATION_VALUE == response.headers[FERRA_CORRELATION_HEADER]
