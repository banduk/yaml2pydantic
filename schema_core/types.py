from datetime import datetime
from typing import Any, Dict, Optional, Type


class TypeRegistry:
    """Registry for managing types used in schema definitions.

    This class maintains a registry of both built-in Python types
    and custom types defined by the user.
    """

    BUILTIN_TYPES = {
        "str": str,
        "int": int,
        "float": float,
        "bool": bool,
        "datetime": datetime,
    }

    def __init__(self):
        """Initialize an empty type registry."""
        self.custom_types: Dict[str, Type[Any]] = {}

    def register(self, name: str, type_: Type[Any]):
        """Register a custom type.

        Args:
        ----
            name: Name of the type as used in schema definitions
            type_: The actual Python type to register

        """
        self.custom_types[name] = type_

    def resolve(self, type_str: str):
        """Resolve a type string to its actual Python type.

        Args:
        ----
            type_str: String representation of the type (e.g., "str", "Optional[str]")

        Returns:
        -------
            The resolved Python type

        Raises:
        ------
            KeyError: If the type is not found in either built-in or custom types

        """
        if type_str.startswith("Optional["):
            inner = type_str[9:-1]
            return Optional[self.resolve(inner)]
        return self.BUILTIN_TYPES.get(type_str) or self.custom_types[type_str]


types = TypeRegistry()
