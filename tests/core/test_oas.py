from pathlib import Path

import yaml
from fastapi import FastAPI
from fastapi.testclient import TestClient

from ferrea.core.oas import add_openapi_schema

OAS_URL = "/openapi.json"
OAS_PATH = Path(__file__).parent / "petstore.yaml"


def test_oas_loading() -> None:
    """Test the loading of the oas file into the FastAPI app."""
    app = FastAPI()
    app = add_openapi_schema(app, OAS_PATH)
    client = TestClient(app)

    response = client.get(OAS_URL)
    if response.is_success:
        actual_schema = response.json()
    else:
        raise Exception()

    expected_schema = yaml.load(OAS_PATH.read_text(), Loader=yaml.BaseLoader)

    assert actual_schema == expected_schema
