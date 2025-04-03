from schema_components.types.money import Money
from schema_core.registry import serializers


@serializers.serializer
def money_as_string(value: Money) -> str:
    return f"{value.currency} {value.amount / 100:.2f}"
