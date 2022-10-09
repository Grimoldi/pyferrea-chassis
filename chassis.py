"""
This module is aimed to provide a standard configuration for all the python Ferrea's libraries.
It sets up the logger, the metrics and the tracer.
"""

import logging

from logstash_formatter import LogstashFormatterV1
from statsd import StatsClient


__version__ = "prd"

def init_metrics( host: str, prefix: str|None =None, port: int =8125) -> StatsClient: 
    """
    This function initialize the metrics.
    It uses statsd for performance monitoring.

    Args:
        host (str): the host to which send the metrics.
        prefix (str | None, optional): the prefix for the metrics. Defaults to None.
        port (int, optional): the port of the host for the metrics. Defaults to 8125.

    Returns:
        StatsClient: the statsd client to be used.
    """
    return StatsClient(host, port, prefix=prefix)


def init_logger(level: int = logging.DEBUG) -> logging.Logger:
    """
    This function initialize the logger.
    It uses logstash on top of the python logging module.

    Args:
        level (int, optional): the logging level for the logger. Defaults to logging.DEBUG.

    Returns:
        logging.Logger: the logger.
    """    
    logger = logging.getLogger()
    logger.setLevel(level)
    formatter = LogstashFormatterV1()

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger


def init_tracer() -> None:
    """
    This function initialize the tracer.
    It is currently under development.

    Raises:
        NotImplementedError: currently not implemented yet.
    """    
    # raise NotImplementedError("Currently under development")  # TODO Jaeger has been moved to opentelemetry
    ...
