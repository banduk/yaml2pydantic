"""String validators for YAML2Pydantic models."""

from typing import Any

from yaml2pydantic.core.validators import validator_registry


@validator_registry.validator
def non_empty(value: Any) -> Any:
    """Validate that a value is not empty.

    For strings, checks if the string is not empty after stripping whitespace.
    For lists, dictionaries, and other collections, checks if they are not empty.
    For other types, checks if the value is not None.

    Args:
        value: The value to validate

    Returns:
        The original value if it is not empty

    Raises:
        ValueError: If the value is empty
    """
    if value is None:
        raise ValueError("Value cannot be None")

    if isinstance(value, str):
        if not value.strip():
            raise ValueError("String cannot be empty")
    elif hasattr(value, "__len__"):
        if len(value) == 0:
            raise ValueError("Collection cannot be empty")

    return value
