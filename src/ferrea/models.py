import locale
import uuid
from datetime import datetime
from enum import Enum
from platform import platform
from typing import Any

import geopy
from attrs import define, field, validators

import ferrea._validators as custom_validators


@define
class Author:
    """
    This class describes how an Author instance should be structured.
    """

    author: str
    author_sort: str = field(default=None)
    portrait_url: str = field(default=None, validator=[custom_validators.validate_url])

    def serialize(self) -> dict[str, Any]:
        """
        This method returns the object serialized.

        Returns:
            dict[str, Any]: the serialized object.
        """
        return {
            "author": self.author,
            "author_sort": self.author_sort,
            "portrait_url": self.portrait_url,
        }


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

    def serialize(self) -> dict[str, Any]:
        """
        This method returns the object serialized.

        Returns:
            dict[str, Any]: the serialized object.
        """
        return {
            "isbn": self.isbn,
            "title": self.title,
            "title_sort": self.title_sort,
            "language": self.language,
            "plot": self.plot,
            "cover_url": self.cover_url,
        }


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

    def serialize(self) -> dict[str, Any]:
        """
        This method returns the object serialized.

        Returns:
            dict[str, Any]: the serialized object.
        """
        return {
            "copy_nr": self.copy_nr,
            "barcode": self.barcode,
        }


@define
class BookFormat:
    """
    This class describes how a BookFormat instance should be structured.
    """

    book_format: str

    def serialize(self) -> dict[str, Any]:
        """
        This method returns the object serialized.

        Returns:
            dict[str, Any]: the serialized object.
        """
        return {
            "book_format": self.book_format,
        }


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

    def serialize(self) -> dict[str, Any]:
        """
        This method returns the object serialized.

        Returns:
            dict[str, Any]: the serialized object.
        """
        return {
            "email": self.email,
            "address": self.address,
            "name": self.name,
            "phone": self.phone,
            "latitude": self.location.latitude,
            "longitude": self.location.longitude,
        }


@define
class Publisher:
    """
    This class describes how a Publisher instance should be structured.
    """

    publishing: str

    def serialize(self) -> dict[str, Any]:
        """
        This method returns the object serialized.

        Returns:
            dict[str, Any]: the serialized object.
        """
        return {
            "publishing": self.publishing,
        }


@define
class Rating:
    """
    This class describes how a Rating instance should be structured.
    Note that this is a meant to be a relationship object (the only one).
    """

    stars: int = field(validator=[validators.gt(0), validators.le(5)])

    def serialize(self) -> dict[str, Any]:
        """
        This method returns the object serialized.

        Returns:
            dict[str, Any]: the serialized object.
        """
        return {
            "stars": self.stars,
        }


@define
class Reading:
    """
    This class describes how a Reading instance should be structured.
    """

    def serialize(self) -> dict[str, Any]:
        """
        This method returns the object serialized.

        Returns:
            dict[str, Any]: the serialized object.
        """
        return {}


@define
class Reservation:
    """
    This class describes how a Reservation instance should be structured.
    """

    def serialize(self) -> dict[str, Any]:
        """
        This method returns the object serialized.

        Returns:
            dict[str, Any]: the serialized object.
        """
        return {}


@define
class Saga:
    """
    This class describes how a Saga instance should be structured.
    """

    series: str

    def serialize(self) -> dict[str, Any]:
        """
        This method returns the object serialized.

        Returns:
            dict[str, Any]: the serialized object.
        """
        return {
            "series": self.series,
        }


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

    def serialize(self) -> dict[str, Any]:
        """
        This method returns the object serialized.

        Returns:
            dict[str, Any]: the serialized object.
        """
        return {
            "email": self.email,
            "address": self.address,
            "location": self.location,
            "name": self.name,
            "surname": self.surname,
            "verified": self.verified,
            "userid": self.userid,
            "card_nr": self.card_nr,
            "phone": self.phone,
        }


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

    def serialize(self) -> dict[str, Any]:
        """
        This method returns the object serialized.

        Returns:
            dict[str, Any]: the serialized object.
        """
        return {"role": self.role.value}


@define
class Year:
    """
    This class describes how a Year instance should be structured.
    """

    date: datetime

    @property
    def year(self) -> int:
        return self.date.year

    def serialize(self) -> dict[str, Any]:
        """
        This method returns the object serialized.

        Returns:
            dict[str, Any]: the serialized object.
        """
        return {"year": self.year}


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

    def serialize(self) -> dict[str, Any]:
        """
        This method returns the object serialized.

        Returns:
            dict[str, Any]: the serialized object.
        """
        return {"month": self.month}


@define
class Day:
    """
    This class describes how a Day instance should be structured.
    """

    date: datetime

    @property
    def day(self) -> int:
        return self.date.day

    def serialize(self) -> dict[str, Any]:
        """
        This method returns the object serialized.

        Returns:
            dict[str, Any]: the serialized object.
        """
        return {"day": self.day}


@define
class Datasource:
    """
    This class describes how a Datasource instance should be structured.
    """

    title: str
    author: list[str]
    publishing: str = field(default=None)
    published_on: int = field(
        default=None, validator=custom_validators.validate_publishing_year
    )
    cover: str = field(default=None)
    plot: str = field(default=None)
    language: list[str] = field(default=None)
    book_format: str = field(default=None)
    author_portrait: str = field(default=None)

    def serialize(self) -> dict[str, Any]:
        """
        This method returns the object serialized.

        Returns:
            dict[str, Any]: the serialized object.
        """
        return {
            "title": self.title,
            "author": self.author,
            "publishing": self.publishing,
            "published_on": self.published_on,
            "cover": self.cover,
            "plot": self.plot,
            "language": self.language,
            "book_format": self.book_format,
            "author_portrait": self.author_portrait,
        }
