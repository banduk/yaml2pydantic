from typing import Union

from pydantic import BaseModel, field_validator
from schema_core.registry import types


class Money(BaseModel):
    amount: int
    currency: str = "R$"

    @field_validator("amount", mode="before")
    @classmethod
    def convert_float_to_cents(cls, v: Union[int, float]) -> int:
        if isinstance(v, float):
            return int(round(v * 100))
        return v


# Register globally once
types.register("Money", Money)
