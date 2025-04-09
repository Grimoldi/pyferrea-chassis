"""
This module is a util to read the pyproject.toml (from poetry) as load it as a PyProject object.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import tomllib


@dataclass
class PyProject:
    """Abstraction for the important fields of a pyproject.toml file"""

    name: str
    description: str
    version: str
    authors: list[str] = field(default_factory=list)


def get_pyproject(root_folder: Path) -> PyProject:
    """Loads the pyproject.toml file as a PyProject object."""
    return _create_pyproject(_load_pyproject(root_folder))


def _load_pyproject(root_folder: Path) -> dict[str, Any]:
    """Loads a pyproject.toml file."""
    file_path = root_folder / "pyproject.toml"
    with open(file_path, mode="rb") as file:
        raw_toml = tomllib.load(file)

    return raw_toml


def _create_pyproject(raw_toml: dict[str, Any]) -> PyProject:
    """Converts a dictionary to a PyProject object."""
    raw_project = raw_toml["tool"]["poetry"]
    temp = {
        "name": raw_project["name"],
        "description": raw_project["description"],
        "version": raw_project["version"],
        "authors": raw_project["authors"],
    }

    return PyProject(**temp)
