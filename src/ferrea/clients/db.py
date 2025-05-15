from __future__ import annotations

from dataclasses import dataclass
from types import TracebackType
from typing import Any, LiteralString, Protocol

from neo4j import GraphDatabase, ManagedTransaction

from ferrea.observability.logs import ferrea_logger


class DBClient(Protocol):
    """
    Protocol as all DB Interfaces should act.
    They need enter and exit dunder methods for being used as context manager.
    They also need read and write methods to interact with the db.
    """

    def __enter__(self) -> DBClient: ...

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None: ...

    def read(
        self, query: str, params: dict[str, int | str | float] | None = None, **kwargs
    ) -> list[Any]: ...

    def write(
        self, query: str, params: dict[str, int | str | float] | None = None, **kwargs
    ) -> list[Any]: ...


@dataclass
class Neo4jConnectionSettings:
    """Dataclass for connection settings like uri and credentials."""

    uri: str
    user: str
    password: str
    database: str = "neo4j"  # for Aura is set the default


class Neo4jClient:
    """Specific implementation for Neo4j DB."""

    def __enter__(self, connection_settings: Neo4jConnectionSettings) -> Neo4jClient:
        """
        Dunder method in order to use the 'with' statement.

        Returns:
            Neo4jClient: the self object.
        """
        uri = connection_settings.uri
        user = connection_settings.user
        pwd = connection_settings.password
        self.db = connection_settings.database
        self.driver = GraphDatabase.driver(uri, auth=(user, pwd))
        ferrea_logger.debug("Neo4j client: entered with.")

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
            ferrea_logger.exception(
                f"An exception has been raised. {exc_type=}, {exc_value=}, {exc_tb=}"
            )

        self.driver.close()

    def read(
        self,
        query: LiteralString,
        params: dict[str, int | str | float] | None = None,
    ) -> list[Any]:
        """
        This method performs a read operation towards the database.

        Args:
            query (LiteralString): the query to send.
            params (dict[str, int | str | float] | None, optional): parameters of the query. Defaults to None.

        Returns:
            list[Any]: the result records.
        """
        with self.driver.session(database=self.db) as session:
            res = session.execute_read(self._run_tx, query, params)
        return res

    def write(
        self,
        query: LiteralString,
        params: dict[str, int | str | float] | None = None,
    ) -> list[Any]:
        """
        This method performs a write operation towards the database.

        Args:
            query (LiteralString): the query to send.
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
        query: LiteralString,
        params: dict[str, int | str | float] | None = None,
    ) -> list[Any]:
        """
        This method runs a transaction against the database.

        Args:
            tx (ManagedTransaction): the transaction instance.
            query (LiteralString): the query to send.
            params (dict[str, int  |  str  |  float] | None, optional): parameters of the query. Defaults to None.

        Returns:
            list[Any]: the result records.
        """
        if params is None:
            params = {}
        return [result.values() for result in tx.run(query=query, parameters=params)]
