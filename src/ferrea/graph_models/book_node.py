"""
This module encapsule all the nodes related to a copy of a book, such as:
- the book
- the single copy
- the format of the copy
- the publisher
- the saga
"""

import models.models as models
import py2neo.ogm as ogm


class BookNode(ogm.GraphObject):
    """
    This class defines the Book node, with it's properties and relationships.
    """

    __primarykey__ = "isbn"

    isbn = ogm.Property()
    title = ogm.Property()
    language = ogm.Property()
    plot = ogm.Property()
    title_sort = ogm.Property()
    cover_url = ogm.Property()

    book_copy = ogm.RelatedTo("BookCopyNode", "AVAILABLE_AS")
    date_published = ogm.RelatedTo("YearNode", "PUBLISHED_ON")
    belongs_to = ogm.RelatedTo("SagaNode", "BELONGS_TO")

    def __init__(self, book: models.Book) -> None:
        """
        Getting the attributes from the model object, then calling the super to init the node object.

        Args:
            book (Book): the book object to be stored as a node entity.
        """
        self.isbn = book.isbn
        self.title = book.title
        self.language = book.language
        self.plot = book.plot
        self.title_sort = book.title_sort
        self.cover_url = book.cover_url
        super().__init__()


class BookCopyNode(ogm.GraphObject):
    """
    This class defines the BookCopy node, with it's properties and relationships.
    """

    __primarykey__ = "copy_id"

    copy_id = ogm.Property()
    copy_nr = ogm.Property()

    book_format = ogm.RelatedTo("BookFormatNode", "PUBLISHED_AS")

    def __init__(self, book_copy: models.BookCopy) -> None:
        """
        Getting the attributes from the model object, then calling the super to init the node object.

        Args:
            book_copy (BookCopy): the book copy object to be stored as a node entity.
        """
        self.copy_id = book_copy.copy_id
        self.copy_nr = book_copy.copy_nr
        super().__init__()


class BookFormatNode(ogm.GraphObject):
    """
    This class defines the BookFormat node, with it's properties and relationships.
    """

    __primarykey__ = "book_format"

    book_format = ogm.Property()

    def __init__(self, book_format: models.BookFormat) -> None:
        """
        Getting the attributes from the model object, then calling the super to init the node object.

        Args:
            book_format (BookFormat): the book format object to be stored as a node entity.
        """
        self.book_format = book_format.book_format
        super().__init__()


class PublisherNode(ogm.GraphObject):
    """
    This class defines the Publisher node, with it's properties and relationships.
    """

    __primarykey__ = "publishing"

    publishing = ogm.Property()

    published = ogm.RelatedTo("BookNode", "PUBLISHED")

    def __init__(self, publisher: models.Publisher) -> None:
        """
        Getting the attributes from the model object, then calling the super to init the node object.

        Args:
            publisher (Publisher): the book format object to be stored as a node entity.
        """
        self.publishing = publisher.publishing
        super().__init__()


class SagaNode(ogm.GraphObject):
    """
    This class defines the Saga node, with it's properties and relationships.
    """

    __primarykey__ = "series"

    series = ogm.Property()

    def __init__(self, saga: models.Saga) -> None:
        """
        Getting the attributes from the model object, then calling the super to init the node object.

        Args:
            saga (Saga): the saga object to be stored as a node entity.
        """
        self.series = saga.series
        super().__init__()
