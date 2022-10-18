import py2neo.ogm as ogm
from class_models import models


class LibraryNode(ogm.GraphObject):
    """
    This class defines the Library node, with it's properties and relationships.
    """

    __primarykey__ = "name"

    name = ogm.Property()
    address = ogm.Property()
    location = ogm.Property()
    email = ogm.Property()
    phone = ogm.Property()

    holds = ogm.RelatedTo("BookCopy", "HOLDS")

    def __init__(self, library: models.Library) -> None:
        """
        Getting the attributes from the model object, then calling the super to init the node object.

        Args:
            library (Library): the library object to be stored as a node entity.
        """
        self.name = library.name
        self.address = library.address
        self.location = library.location
        self.mail = library.email
        self.phone = library.phone
        super().__init__()
