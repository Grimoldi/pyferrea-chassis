"""
This module aims as a Factory Strategy Pattern for the creation of FastAPI app.
"""
from pathlib import Path

import yaml
from fastapi import FastAPI
from yamlinclude import YamlIncludeConstructor


def init_api(ferrea_app: str, models_path: Path) -> FastAPI:
    """
    This function creates the FastAPI app based on the microservice name.
    It loads also the OpenApi Schema (oas) from the models path.

    Args:
        ferrea_app (str): the name of the app.
        models_path (Path): path under which the oas file can be found.

    Returns:
        FastAPI: the initialized app.
    """
    app = FastAPI(
        debug=True,
        openapi_url=f"/openapi/{ferrea_app}.json",
        docs_url=f"/docs/{ferrea_app}",
        title=f"Ferrea - {ferrea_app.title()}",
    )

    models_path = Path(__file__).parent / "definitions"
    YamlIncludeConstructor.add_to_loader_class(
        loader_class=yaml.FullLoader, base_dir=models_path
    )
    oas_path = models_path / "oas.yaml"
    oas_doc = yaml.load(oas_path.read_text(), Loader=yaml.FullLoader)

    app.openapi = lambda: oas_doc

    return app
