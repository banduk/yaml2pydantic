from schema_core.serializers import SerializerRegistry
from schema_core.types import TypeRegistry
from schema_core.validators import ValidatorRegistry

# These will be populated by schema_components auto-import side effect
types = TypeRegistry()
serializers = SerializerRegistry()
validators = ValidatorRegistry()

import schema_components  # noqa: F401 -- triggers auto-import
