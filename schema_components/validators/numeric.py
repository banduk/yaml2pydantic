"""Numeric validation functions."""

from schema_core.registry import validators


@validators.validator
def check_positive(cls, v):
    """Validate that a number is positive.

    Args:
    ----
        cls: The model class (unused)
        v: The value to validate

    Returns:
    -------
        The validated value

    Raises:
    ------
        ValueError: If the value is not positive

    """
    if v <= 0:
        raise ValueError("Must be positive")
    return v
