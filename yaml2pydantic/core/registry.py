"""Central registry for all schema components.

This module provides access to the global registries for:
- Types (built-in and custom)
- Validators (field and model)
- Serializers (field)

These registries are populated automatically when schema components
are imported from the components directory.
"""

from yaml2pydantic.core.serializers import SerializerRegistry
from yaml2pydantic.core.type_registry import TypeRegistry
from yaml2pydantic.core.validators import ValidatorRegistry

__all__ = ["SerializerRegistry", "TypeRegistry", "ValidatorRegistry"]
