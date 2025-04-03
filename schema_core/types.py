from datetime import datetime
from typing import Any, Dict, Optional, Type


class TypeRegistry:
    BUILTIN_TYPES = {
        "str": str,
        "int": int,
        "float": float,
        "bool": bool,
        "datetime": datetime,
    }

    def __init__(self):
        self.custom_types: Dict[str, Type[Any]] = {}

    def register(self, name: str, type_: Type[Any]):
        self.custom_types[name] = type_

    def resolve(self, type_str: str):
        if type_str.startswith("Optional["):
            inner = type_str[9:-1]
            return Optional[self.resolve(inner)]
        return self.BUILTIN_TYPES.get(type_str) or self.custom_types[type_str]


types = TypeRegistry()
