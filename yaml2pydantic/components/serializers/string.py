"""String serializers for YAML2Pydantic models."""

from typing import Any

from yaml2pydantic.core.serializers import serializer_registry


@serializer_registry.serializer
def to_upper(value: str, _info: Any | None = None, **kwargs: Any) -> str:
    """Convert a string to uppercase.

    Args:
        value: The string to convert

    Returns:
        The uppercase version of the string
    """
    return value.upper()


@serializer_registry.serializer
def to_lower(value: str, _info: Any | None = None, **kwargs: Any) -> str:
    """Convert a string to lowercase.

    Args:
        value: The string to convert

    Returns:
        The lowercase version of the string
    """
    return value.lower()
