import json
import logging

import pytest

from ferrea.observability import LogstashFormatterV1, init_logger


@pytest.fixture(autouse=True)
def redact_caplog_handlers(caplog) -> None:
    caplog.set_level(logging.INFO)
    caplog.handler.setFormatter(LogstashFormatterV1())


def _info_record(logger: logging.Logger) -> None:
    logger.info("Alice")


def _error_record(logger: logging.Logger) -> None:
    logger.error("Bob")


def test_message_logs_correct_message(caplog) -> None:
    logger = init_logger()
    _info_record(logger)
    data = json.loads(caplog.text)

    assert "Alice" == data["message"]


def test_level_logs_correct_message(caplog) -> None:
    logger = init_logger()
    _info_record(logger)
    data = json.loads(caplog.text)

    assert "INFO" == data["levelname"]


def test_name_logs_correct_message(caplog) -> None:
    logger = init_logger()
    _info_record(logger)
    data = json.loads(caplog.text)

    assert "ferrea" == data["name"]


def test_error_level_logs_correct_message(caplog) -> None:
    logger = init_logger()
    _error_record(logger)
    data = json.loads(caplog.text)

    assert "ERROR" == data["levelname"]
