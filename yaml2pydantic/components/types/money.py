"""Money type for handling currency values with cents precision."""

from pydantic import BaseModel, field_validator


class Money(BaseModel):
    """A type for handling money values with cents precision.

    This class represents a monetary value with:
    - amount: The value in cents (int)
    - currency: The currency symbol (defaults to "R$")
    """

    amount: int | float
    currency: str = "R$"

    @field_validator("amount", mode="before")
    @classmethod
    def convert_float_to_cents(cls, v: int | float) -> int:
        """Convert float values to cents by multiplying by 100 and rounding.

        Args:
        ----
            v: The value to convert (int or float)

        Returns:
        -------
            The value in cents as an integer

        """
        if isinstance(v, float):
            return round(v * 100)
        return v
