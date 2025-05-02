"""Type components for yaml2pydantic."""

from yaml2pydantic import types
from yaml2pydantic.components.types.money import Money

# Register all custom types
types.register("Money", Money)
