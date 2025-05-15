import json

import pytest
from loguru import logger

from ferrea.core.context import Context
from ferrea.observability.logs import patching

ALICE = "Alice"
ALICE_CONTEXT = Context("", "")
BOB = "Bob"
BOB_CONTEXT = Context("abcdefg", "")
CHARLIE = "Charlie"
CHARLIE_CONTEXT = Context("hijklmn", "Testing")


@pytest.fixture
def writer():
    """Fixture for fetching the logs."""

    def w(message):
        w.written.append(message)

    w.written = []
    w.read = lambda: "".join(w.written)
    w.clear = lambda: w.written.clear()

    return w


def setup_test_logger(writer):
    """Setup a test logger with the settings from the real one."""
    logger_patched = logger.patch(patching)
    logger.add(writer, format="{extra[serialized]}")

    logger_patched.configure(
        extra={
            "ferrea_uuid": "",
            "app": "",
        },
        patcher=patching,
    )
    return logger_patched


def test_basic_log(writer) -> None:
    """Test basic logging."""
    logger_patched = setup_test_logger(writer)
    logger_patched.info(ALICE, **ALICE_CONTEXT.log)

    data = json.loads(writer.read())
    assert data["message"] == ALICE
    assert data["ferrea_uuid"] == ""
    assert data["app"] == ""


def test_structured_log(writer) -> None:
    "Test logs with context data."
    logger_patched = setup_test_logger(writer)
    logger_patched.info(BOB, **BOB_CONTEXT.log)

    data = json.loads(writer.read())
    assert data["message"] == BOB
    assert data["ferrea_uuid"] == BOB_CONTEXT.uuid
    assert data["app"] == ""


def test_even_more_structured_log(writer) -> None:
    "Test logs with more context data."
    logger_patched = setup_test_logger(writer)
    logger_patched.info(CHARLIE, **CHARLIE_CONTEXT.log)

    data = json.loads(writer.read())
    assert data["message"] == CHARLIE
    assert data["ferrea_uuid"] == CHARLIE_CONTEXT.uuid
    assert data["app"] == CHARLIE_CONTEXT.app
