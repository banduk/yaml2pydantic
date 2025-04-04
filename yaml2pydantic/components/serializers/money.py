from yaml2pydantic.components.types.money import Money
from yaml2pydantic.core.registry import serializers


@serializers.serializer
def money_as_string(value: Money) -> str:
    """Format a Money instance as a human-readable string.

    This serializer converts a Money instance into a formatted string
    representation, showing the currency symbol and the amount with
    two decimal places.

    Args:
    ----
        value: The Money instance to format

    Returns:
    -------
        A string in the format "R$ XX.XX"

    """
    return f"{value.currency} {value.amount / 100:.2f}"
