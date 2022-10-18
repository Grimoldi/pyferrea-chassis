"""
This module encapsule all the nodes related to a user, such as:
- the user
- the user role
- his reservation(s)
- his reading(s)
"""

import py2neo.ogm as ogm
from class_models import models


class UserNode(ogm.GraphObject):
    """
    This class defines the User node, with it's properties and relationships.
    """

    __primarykey__ = "userid"

    email = ogm.Property()
    address = ogm.Property()
    location = ogm.Property()
    name = ogm.Property()
    surname = ogm.Property()
    verified = ogm.Property()
    userid = ogm.Property()
    card_nr = ogm.Property()
    phone = ogm.Property()

    reads = ogm.RelatedTo("ReadingNode", "DOES_READ")
    holds = ogm.RelatedTo("ReservationNode", "HOLDS")
    role = ogm.RelatedTo("RoleNode", "HAS_ROLE")

    def __init__(self, user: models.User) -> None:
        """
        Getting the attributes from the model object, then calling the super to init the node object.

        Args:
            user (User): the user object to be stored as a node entity.
        """
        self.email = user.email
        self.address = user.address
        self.location = user.location
        self.name = user.name
        self.surname = user.surname
        self.verified = user.verified
        self.userid = user.userid
        self.card_nr = user.card_nr
        self.phone = user.phone
        super().__init__()


class UserRoleNode(ogm.GraphObject):
    """
    This class defines the UserRole node, with it's properties and relationships.
    """

    __primarykey__ = "role"

    role = ogm.Property()

    def __init__(self, user_role: models.UserRole) -> None:
        """
        Getting the attributes from the model object, then calling the super to init the node object.

        Args:
            user_role (UserRole): the user role object to be stored as a node entity.
        """
        self.role = user_role.role
        super().__init__()


class ReservationNode(ogm.GraphObject):
    """
    This class defines the Reservation node, with it's properties and relationships.
    """

    reserverd_on = ogm.RelatedTo("DayNode", "RESERVED_ON")
    reserved_copy = ogm.RelatedTo("BookCopyNode", "RESERVED_COPY")

    def __init__(self) -> None:
        """
        Getting the attributes from the model object, then calling the super to init the node object.
        """
        super().__init__()


class ReadingNode(ogm.GraphObject):
    """
    This class defines the Reading node, with it's properties and relationships.
    """

    read_from = ogm.RelatedTo("DayNode", "READ_FROM")
    read_to = ogm.RelatedTo("DayNode", "READ_TO")

    def __init__(self) -> None:
        """
        Getting the attributes from the model object, then calling the super to init the node object.
        """
        super().__init__()
