"""MonthYear type for handling month and year values."""

from datetime import datetime
from typing import Any

from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic_core import core_schema

from schema_core.registry import types


class MonthYear:
    """A type for handling month and year values.

    This class represents a month and year combination, always setting
    the day to 1 to ensure consistent representation.
    """

    def __init__(self, value: datetime):
        """Initialize a MonthYear instance.

        Args:
        ----
            value: A datetime object representing the month and year

        """
        self.value = value.replace(day=1)

    def __str__(self) -> str:
        """Convert the MonthYear to a string in MM/YYYY format.

        Returns
        -------
            A string in the format "MM/YYYY"

        """
        return self.value.strftime("%m/%Y")

    def __repr__(self) -> str:
        """Get the string representation of the MonthYear.

        Returns
        -------
            The same as __str__ for consistency

        """
        return str(self)

    def __eq__(self, other: Any) -> bool:
        """Compare two MonthYear instances for equality.

        Args:
        ----
            other: The other value to compare with

        Returns:
        -------
            True if both are MonthYear instances with the same value

        """
        return isinstance(other, MonthYear) and self.value == other.value

    @classmethod
    def __get_pydantic_core_schema__(
        cls, _source_type: Any, _handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        """Get the Pydantic core schema for this type.

        Args:
        ----
            _source_type: The source type (unused)
            _handler: The schema handler

        Returns:
        -------
            A core schema for string validation

        """
        return core_schema.union_schema(
            [
                core_schema.is_instance_schema(cls),
                core_schema.str_schema(),
            ],
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda v: v.value.strftime("%m/%Y") if isinstance(v, MonthYear) else v
            ),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> dict[str, Any]:
        """Get the JSON schema for this type.

        Args:
        ----
            schema: The core schema
            handler: The schema handler

        Returns:
        -------
            A JSON schema with type and format information

        """
        json_schema = handler(schema)
        json_schema.update(type="string", format="month-year", example="03/2025")
        return json_schema


# Register globally once
types.register("MonthYear", MonthYear)
