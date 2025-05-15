import json
import sys

from loguru import logger

ferrea_logger = logger


def serialize(record) -> str:
    """Record's subset fields that will be logged."""
    subset = {
        "timestamp": record["time"].timestamp(),
        "message": record["message"],
        "level": record["level"].name,
        "ferrea_uuid": record["extra"]["ferrea_uuid"],
        "app": record["extra"]["app"],
        "module": record["module"],
        "name": record["name"],
        "line": record["line"],
    }

    return json.dumps(subset)


def patching(record) -> None:
    """Add a field under extra that will hold the actual record."""
    record["extra"]["serialized"] = serialize(record)


def setup_logger() -> None:
    """Setup the logger stuff."""
    logger.remove(0)
    _logger = logger.patch(patching)
    logger_format = "{extra[serialized]}"

    """
    Default values, refer to:
    https://github.com/Delgan/loguru/issues/586#issuecomment-1030819250
    https://github.com/Delgan/loguru/issues/882#issuecomment-1570874100
    """
    _logger.configure(
        extra={
            "ferrea_uuid": "",
            "app": "",
        },
        patcher=patching,
    )
    _logger.add(sys.stderr, format=logger_format)
