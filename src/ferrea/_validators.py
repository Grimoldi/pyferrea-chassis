import re
from typing import Any

from attrs import Attribute


def validate_url(instance: Any, attribute: Attribute, value: str) -> None:
    """
    Validator for any url.
    If a value is passed, it should be an url like pattern.

    Args:
        instance (Any): the object instance.
        attribute (Attribute): the attribute to be checked.
        value (str): the value against which run the validation.

    Raises:
        ValueError: error describing the bad attribute value.
    """
    if value is not None:
        pattern = r"http(s?)://[\w|-|\.]+"
        match = re.search(pattern=pattern, string=value)
        if not match:
            raise ValueError(
                f"{attribute.name} should be a valid url, received {value}."
            )


def validate_email(instance: Any, attribute: Attribute, value: str) -> None:
    """
    Validator for any email.
    If a value is passed, it should be an email like pattern.

    Args:
        instance (Any): the object instance.
        attribute (Attribute): the attribute to be checked.
        value (str): the value against which run the validation.

    Raises:
        ValueError: error describing the bad attribute value.
    """
    if value is not None:
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        match = re.search(pattern=pattern, string=value)
        if not match:
            raise ValueError(
                f"{attribute.name} should be a valid email, received {value}."
            )


def validate_publishing_year(instance: Any, attribute: Attribute, value: int) -> None:
    """
    Validator for publishing year.
    If a value is passed, it should be a year greater than zero.

    Args:
        instance (Any): the object instance.
        attribute (Attribute): the attribute to be checked.
        value (str): the value against which run the validation.

    Raises:
        ValueError: error describing the bad attribute value.
    """
    is_valid_value = value is not None and isinstance(value, int) and value > 0
    if not is_valid_value:
        raise ValueError(
            f"{attribute.name} should be a valid year (int > 0), received {type(value)} with value {value}."
        )
