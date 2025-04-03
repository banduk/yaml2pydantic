from datetime import datetime
from typing import ClassVar


class TypeRegistry:
    """Registry for custom types."""

    BUILTIN_TYPES: ClassVar[dict[str, type]] = {
        "str": str,
        "int": int,
        "float": float,
        "bool": bool,
        "datetime": datetime,
    }

    def __init__(self):
        """Initialize an empty type registry."""
        self.custom_types: dict[str, type] = {}

    def register(self, name: str, type_class: type) -> None:
        """Register a custom type."""
        self.custom_types[name] = type_class

    def resolve(self, type_str: str) -> type:
        """Resolve a type string to a Python type."""
        if type_str.startswith("Optional["):
            inner = type_str[9:-1]
            return self.resolve(inner) | None
        return self.BUILTIN_TYPES.get(type_str) or self.custom_types[type_str]


types = TypeRegistry()
