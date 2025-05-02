__version__ = "0.1.0"

from .core.factory import ModelFactory as ModelFactory
from .core.loader import SchemaLoader as SchemaLoader
from .core.registry import SerializerRegistry as SerializerRegistry
from .core.registry import TypeRegistry as TypeRegistry
from .core.registry import ValidatorRegistry as ValidatorRegistry

# Create registry instances
types = TypeRegistry()
serializers = SerializerRegistry()
validators = ValidatorRegistry()
