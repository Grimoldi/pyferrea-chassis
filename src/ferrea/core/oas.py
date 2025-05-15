from pathlib import Path

import yaml
from fastapi import FastAPI


def add_openapi_schema(app: FastAPI, oas_path: Path) -> FastAPI:
    """
    Since I prefer to create the oas, this function adds it to the FastAPI app.

    Args:
        app (FastAPI): the app.
        models_path (Path): path under which the oas file can be found.

    Returns:
        FastAPI: the app with the added oas documentation.
    """

    oas_doc = yaml.load(oas_path.read_text(), Loader=yaml.BaseLoader)
    app.openapi = lambda: oas_doc

    return app
