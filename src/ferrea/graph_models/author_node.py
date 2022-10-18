import py2neo.ogm as ogm
from class_models import models


class AuthorNode(ogm.GraphObject):
    """
    This class defines the Author node, with it's properties and relationships.
    """

    __primarykey__ = "author"

    author = ogm.Property()
    author_sort = ogm.Property()
    portrait_url = ogm.Property()

    wrote = ogm.RelatedTo("BookNode", "WROTE")
    serialized = ogm.RelatedTo("SagaNode", "SERIALIZED")

    def __init__(self, author: models.Author) -> None:
        """
        Getting the attributes from the model object, then calling the super to init the node object.

        Args:
            author (Author): the author object to be stored as a node entity.
        """
        self.author = author.author
        self.author_sort = author.author_sort
        self.portrait_url = author.portrait_url
        super().__init__()
