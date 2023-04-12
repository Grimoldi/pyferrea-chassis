from __future__ import annotations

import os
from types import TracebackType
from typing import Any, Protocol

from ferrea import observability
from neo4j import GraphDatabase, ManagedTransaction


class DBInterface(Protocol):
    """
    Protocol as all DB Interfaces should act.
    They need enter and exit dunder methods for being used as context manager.
    They also need read and write methods to interact with the db.
    """

    def __enter__(self) -> DBInterface:
        ...

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        ...

    def read(
        self, query: str, params: dict[str, int | str | float] | None = None, **kwargs
    ) -> list[Any]:
        ...

    def write(
        self, query: str, params: dict[str, int | str | float] | None = None, **kwargs
    ) -> list[Any]:
        ...


class Neo4jInterface:
    """Specific implementation for Neo4J DB."""

    def __init__(self) -> None:
        """
        Initializer of the class.
        """
        self.logger = observability.init_logger()

    def __enter__(self) -> Neo4jInterface:
        """
        Dunder method in order to use the 'with' statement.

        Returns:
            DBInterface: the self object.
        """
        uri = os.environ["DB_URL"]
        user = os.environ["DB_USR"]
        pwd = os.environ["DB_PWD"]
        self.db = "neo4j"  # for Aura is set to neo4j
        self.driver = GraphDatabase.driver(uri, auth=(user, pwd))
        self.logger.info("Entered with")

        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        Dunder method called upon exiting from the with statement.

        Args:
            exc_type (type[BaseException] | None): the exception type (if raised).
            exc_value (BaseException | None): the exception value (if raised).
            exc_tb (TracebackType | None): the traceback (if an exception is raised).
        """
        if exc_type is not None:
            self.logger.exception(
                f"An exception has been raised. {exc_type=}, {exc_value=}, {exc_tb=}"
            )

        self.driver.close()

    def read(
        self, query: str, params: dict[str, int | str | float] | None = None, **kwargs
    ) -> list[Any]:
        """
        This method performs a read operation towards the database.

        Args:
            query (str): the query to send.
            params (dict[str, int | str | float] | None, optional): parameters of the query. Defaults to None.

        Returns:
            list[Any]: the result records.
        """
        with self.driver.session(database=self.db) as session:
            res = session.execute_read(self._run_tx, query, params)
        return res

    def write(
        self, query: str, params: dict[str, int | str | float] | None = None, **kwargs
    ) -> list[Any]:
        """
        This method performs a write operation towards the database.

        Args:
            query (str): the query to send.
            params (dict[str, int | str | float] | None, optional): parameters of the query. Defaults to None.

        Returns:
            list[Any]: the result records.
        """
        with self.driver.session(database=self.db) as session:
            res = session.execute_write(self._run_tx, query, params)
        return res

    def _run_tx(
        self,
        tx: ManagedTransaction,
        query: str,
        params: dict[str, int | str | float] | None = None,
    ) -> list[Any]:
        """
        This method runs a transaction against the database.

        Args:
            tx (ManagedTransaction): the transaction instance.
            query (str): the query to send.
            params (dict[str, int  |  str  |  float] | None, optional): parameters of the query. Defaults to None.

        Returns:
            list[Any]: the result records.
        """
        if params is None:
            params = {}
        return [result.values() for result in tx.run(query=query, parameters=params)]  # type: ignore
