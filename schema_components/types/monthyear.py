from datetime import datetime

from pydantic import GetCoreSchemaHandler
from pydantic_core import core_schema
from schema_core.registry import types


class MonthYear:
    def __init__(self, value: datetime):
        self.value = value.replace(day=1)

    def __str__(self):
        return self.value.strftime("%m/%Y")

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return isinstance(other, MonthYear) and self.value == other.value

    @staticmethod
    def _validate(v):
        if isinstance(v, MonthYear):
            return v
        if isinstance(v, datetime):
            return MonthYear(v)
        if isinstance(v, str):
            for fmt in ("%Y-%m", "%m/%Y"):
                try:
                    return MonthYear(datetime.strptime(v, fmt))
                except ValueError:
                    continue
        raise ValueError(
            "MonthYear must be a datetime or a string in 'YYYY-MM' or 'MM/YYYY' format."
        )

    @staticmethod
    def _serialize(instance: "MonthYear") -> str:
        return instance.value.strftime("%m/%Y")

    @classmethod
    def __get_pydantic_core_schema__(
        cls, _source_type, _handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        return core_schema.no_info_plain_validator_function(
            cls._validate,
            serialization=core_schema.plain_serializer_function_ser_schema(
                cls._serialize,
                return_schema=core_schema.str_schema(),
            ),
        )

    @classmethod
    def __get_pydantic_json_schema__(cls, schema: core_schema.CoreSchema, handler):
        json_schema = handler(schema)
        json_schema.update(type="string", format="month-year", example="03/2025")
        return json_schema


# Register globally once
types.register("MonthYear", MonthYear)
