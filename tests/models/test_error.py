import uuid
from typing import Annotated

from fastapi import Depends, FastAPI, Response
from fastapi.testclient import TestClient

from ferrea.core.context import Context
from ferrea.core.header import FERRA_CORRELATION_HEADER, get_correlation_id
from ferrea.models.error import FerreaError

FOO_ENDPOINT = "/foo"
FERREA_CORRELATION_VALUE = str(uuid.uuid4())
ERROR_CODE = "test.app"
ERROR_TITLE = "Test Error"
ERROR_MESSAGE = "Testing error from webserver"


def make_fake_app() -> FastAPI:
    """Create a fake app just for the sake of the tests."""
    app = FastAPI()

    @app.get(FOO_ENDPOINT)
    async def get_foo(
        response: Response,
        _id: Annotated[uuid.UUID, Depends(get_correlation_id)],
    ):
        """Foo endpoint."""
        context = Context(str(_id), "TST")
        error = FerreaError(
            uuid=context.uuid,
            code=ERROR_CODE,
            title=ERROR_TITLE,
            message=ERROR_MESSAGE,
        )
        response.headers[FERRA_CORRELATION_HEADER] = str(_id)
        return error

    return app


def test_error_response() -> None:
    """Test an error response."""
    app = make_fake_app()
    client = TestClient(app)

    headers = {FERRA_CORRELATION_HEADER: FERREA_CORRELATION_VALUE}
    response = client.get(FOO_ENDPOINT, headers=headers)
    data = response.json()

    assert data["uuid"] == FERREA_CORRELATION_VALUE
    assert data["code"] == ERROR_CODE
    assert data["title"] == ERROR_TITLE
    assert data["message"] == ERROR_MESSAGE

    # testing also the uuid since it is important to keep it (although some dedicated tests already exists)
    assert response.headers[FERRA_CORRELATION_HEADER] == FERREA_CORRELATION_VALUE
