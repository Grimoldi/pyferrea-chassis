import locale
import uuid
from datetime import datetime
from enum import Enum
from platform import platform
from typing import Protocol

import geopy
from attrs import define, field
from graph_models.author_node import AuthorNode
from graph_models.book_node import (
    BookCopyNode,
    BookFormatNode,
    BookNode,
    PublisherNode,
    SagaNode,
)
from graph_models.library_node import LibraryNode
from graph_models.user import (
    ReadingNode,
    ReservationNode,
    UserNode,
    UserRoleNode,
)
from py2neo import ogm

import class_models._validators as custom_validators


@define
class BaseModel(Protocol):
    """
    This class describes how any instance should be structured using a Protocol.
    """

    def as_node(self) -> type[ogm.GraphObject]:
        """
        Converts the class to an ogm.GraphObject subclass.

        Returns:
            type[ogm.GraphObject]: the appropriate GraphObject subclass.
        """
        ...


@define
class Author:
    """
    This class describes how an Author instance should be structured.
    """

    author: str
    author_sort: str = field(default=None)
    portrait_url: str = field(default=None, validator=[custom_validators.validate_url])

    def as_node(self) -> AuthorNode:
        """
        Converts the class to an ogm.GraphObject subclass.

        Returns:
            AuthorNode: the representation of the class as a Neo4j node.
        """
        return AuthorNode(self)


@define
class Book:
    """
    This class describes how a Book instance should be structured.
    """

    isbn: str
    title: str
    language: str
    plot: str = field(default=None)
    title_sort: str = field(default=None)
    cover_url: str = field(default=None, validator=[custom_validators.validate_url])

    def as_node(self) -> BookNode:
        """
        Converts the class to an ogm.GraphObject subclass.

        Returns:
            BookNode: the representation of the class as a Neo4j node.
        """
        return BookNode(self)


@define
class BookCopy:
    """
    This class describes how a BookCopy instance should be structured.
    """

    copy_nr: int
    barcode: int

    @property
    def copy_id(self) -> int:
        """
        This calculated value is the copy id (mainly barcode and the copy number).

        Returns:
            int: the volume copy id.
        """
        return int(f"{self.barcode}{str(self.copy_nr).zfill(3)}")

    def as_node(self) -> BookCopyNode:
        """
        Converts the class to an ogm.GraphObject subclass.

        Returns:
            BookCopyNode: the representation of the class as a Neo4j node.
        """
        return BookCopyNode(self)


@define
class BookFormat:
    """
    This class describes how a BookFormat instance should be structured.
    """

    book_format: str

    def as_node(self) -> BookFormatNode:
        """
        Converts the class to an ogm.GraphObject subclass.

        Returns:
            BookFormatNode: the representation of the class as a Neo4j node.
        """
        return BookFormatNode(self)


@define
class Library:
    """
    This class describes how a Library instance should be structured.
    """

    name: str
    address: str
    location: geopy.Location
    email: str = field(default=None)
    phone: int = field(default=None)

    def as_node(self) -> LibraryNode:
        """
        Converts the class to an ogm.GraphObject subclass.

        Returns:
            LibraryNode: the representation of the class as a Neo4j node.
        """
        return LibraryNode(self)


@define
class Publisher:
    """
    This class describes how a Publisher instance should be structured.
    """

    publishing: str

    def as_node(self) -> PublisherNode:
        """
        Converts the class to an ogm.GraphObject subclass.

        Returns:
            PublisherNode: the representation of the class as a Neo4j node.
        """
        return PublisherNode(self)


@define
class Reading:
    """
    This class describes how a Reading instance should be structured.
    """

    def as_node(self) -> ReadingNode:
        """
        Converts the class to an ogm.GraphObject subclass.

        Returns:
            ReadingNode: the representation of the class as a Neo4j node.
        """
        return ReadingNode()


@define
class Reservation:
    """
    This class describes how a Reservation instance should be structured.
    """

    def as_node(self) -> ReservationNode:
        """
        Converts the class to an ogm.GraphObject subclass.

        Returns:
            ReservationNode: the representation of the class as a Neo4j node.
        """
        return ReservationNode()


@define
class Saga:
    """
    This class describes how a Saga instance should be structured.
    """

    series: str

    def as_node(self) -> SagaNode:
        """
        Converts the class to an ogm.GraphObject subclass.

        Returns:
            SagaNode: the representation of the class as a Neo4j node.
        """
        return SagaNode(self)


@define
class User:
    """
    This class describes how a User instance should be structured.
    """

    email: str = field(validator=custom_validators.validate_email)
    address: str
    location: geopy.Location
    name: str
    surname: str
    verified: bool
    userid: uuid.UUID = field(init=False)
    card_nr: int = field(init=False)
    phone: int = field(default=None)

    def set_userid(self) -> None:
        """
        Sets the value for userid.
        This should be checked against the db.
        """
        self.userid = uuid.uuid4()

    def set_card_nr(self, card_nr: int) -> None:
        """
        Sets the card number attribute.

        Args:
            card_nr (int): library card number.
        """
        self.card_nr = card_nr

    def as_node(self) -> UserNode:
        """
        Converts the class to an ogm.GraphObject subclass.

        Raises:
            ValueError: if either card_nr or userid are not set.

        Returns:
            UserNode: the representation of the class as a Neo4j node.
        """
        if self.userid is None or self.card_nr is None:
            raise ValueError(f"Both userid and card_nr must be not null.")
        return UserNode(self)


class UserRoles(Enum):
    """
    Enum class for the which roles are forseen.
    """

    ADMIN = "admin"
    LIBRARIAN = "librarian"
    USER = "user"


@define
class UserRole:
    """
    This class describes how a UserRole instance should be structured.
    """

    role: UserRoles

    def as_node(self) -> UserRoleNode:
        """
        Converts the class to an ogm.GraphObject subclass.

        Returns:
            UserRoleNode: the representation of the class as a Neo4j node.
        """
        return UserRoleNode(self)


@define
class Year:
    """
    This class describes how a Year instance should be structured.
    """

    date: datetime

    @property
    def year(self) -> int:
        return self.date.year


@define
class Month:
    """
    This class describes how a Month instance should be structured.
    """

    date: datetime

    def _set_locale(self) -> None:
        if platform.system() == "Windows":
            en_locale = "en_US"
        else:
            en_locale = "en_US.utf8"
        locale.setlocale(locale.LC_ALL, en_locale)

    @property
    def month(self) -> str:
        date_format = "%B"
        return datetime.strftime(self.date, date_format)


@define
class Day:
    """
    This class describes how a Day instance should be structured.
    """

    date: datetime

    @property
    def day(self) -> int:
        return self.date.day
