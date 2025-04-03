"""Money type for handling currency values with cents precision."""

from typing import Union

from pydantic import BaseModel, field_validator

from schema_core.registry import types


class Money(BaseModel):
    """A type for handling money values with cents precision.

    This class represents a monetary value with:
    - amount: The value in cents (int)
    - currency: The currency symbol (defaults to "R$")
    """

    amount: int
    currency: str = "R$"

    @field_validator("amount", mode="before")
    @classmethod
    def convert_float_to_cents(cls, v: Union[int, float]) -> int:
        """Convert float values to cents by multiplying by 100 and rounding.

        Args:
        ----
            v: The value to convert (int or float)

        Returns:
        -------
            The value in cents as an integer

        """
        if isinstance(v, float):
            return int(round(v * 100))
        return v


# Register globally once
types.register("Money", Money)
