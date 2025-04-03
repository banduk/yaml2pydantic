"""Central registry for all schema components.

This module provides access to the global registries for:
- Types (built-in and custom)
- Validators (field and model)
- Serializers (field)

These registries are populated automatically when schema components
are imported from the schema_components directory.
"""

import schema_components  # noqa: F401 -- triggers auto-import
from schema_core.serializers import SerializerRegistry
from schema_core.types import TypeRegistry
from schema_core.validators import ValidatorRegistry

# These will be populated by schema_components auto-import side effect
types = TypeRegistry()
serializers = SerializerRegistry()
validators = ValidatorRegistry()
