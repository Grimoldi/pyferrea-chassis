import py2neo.ogm as ogm
from class_models import models


class YearNode(ogm.GraphObject):
    """
    This class defines the Year node, with it's properties and relationships.
    """

    __primarykey__ = "year"

    year = ogm.Property()

    has_month = ogm.RelatedTo("MonthNode", "HAS_MONTH")

    def __init__(self, year: models.Year) -> None:
        """
        Getting the attributes from the model object, then calling the super to init the node object.

        Args:
            year (Year): the year object to be stored as a node entity.
        """
        self.year = year.year
        super().__init__()


class MonthNode(ogm.GraphObject):
    """
    This class defines the Month node, with it's properties and relationships.
    """

    __primarykey__ = "month"

    month = ogm.Property()

    has_day = ogm.RelatedTo("DayNode", "HAS_DAY")

    def __init__(self, month: models.Month) -> None:
        """
        Getting the attributes from the model object, then calling the super to init the node object.

        Args:
            month (Month): the month object to be stored as a node entity.
        """
        self.month = month.month
        super().__init__()


class DayNode(ogm.GraphObject):
    """
    This class defines the Day node, with it's properties and relationships.
    """

    __primarykey__ = "day"

    day = ogm.Property()

    def __init__(self, day: models.Day) -> None:
        """
        Getting the attributes from the model object, then calling the super to init the node object.

        Args:
            day (Day): the day object to be stored as a node entity.
        """
        self.day = day.day
        super().__init__()
