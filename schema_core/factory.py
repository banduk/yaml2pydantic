import importlib
import logging
from pathlib import Path
from typing import Any

from pydantic import (
    Field,
    create_model,
    field_serializer,
    field_validator,
    model_validator,
)

from schema_core.serializers import SerializerRegistry
from schema_core.types import TypeRegistry
from schema_core.validators import ValidatorRegistry

logger = logging.getLogger(__name__)


class ModelFactory:
    """Factory for building Pydantic models from schema definitions.

    This class handles the conversion of YAML/JSON schema definitions into
    Pydantic models, including:
    - Custom type resolution
    - Field validation
    - Model validation
    - Custom serialization
    """

    def __init__(
        self,
        types: TypeRegistry,
        validators: ValidatorRegistry,
        serializers: SerializerRegistry,
    ):
        """Initialize the ModelFactory.

        Args:
        ----
            types: Registry of available types (built-in and custom)
            validators: Registry of field and model validators
            serializers: Registry of field serializers

        """
        self.types = types
        self.validators = validators
        self.serializers = serializers
        self.models = {}
        self._load_schema_components()

    def _load_schema_components(self):
        """Load all schema components from the schema_components directory.

        This includes types, validators, and serializers.
        """
        from schema_core import registry  # noqa: F401

        component_path = Path(__file__).parent.parent / "schema_components"
        modules = ["types", "validators", "serializers"]

        for module in modules:
            module_path = component_path / module
            for file in module_path.glob("*.py"):
                if file.stem != "__init__":
                    importlib.import_module(f"schema_components.{module}.{file.stem}")

    def _get_field_args(self, props: dict[str, Any]) -> dict[str, Any]:
        """Extract field arguments from field properties.

        Args:
        ----
            props: Field properties from the schema definition

        Returns:
        -------
            Dictionary of field arguments for Pydantic Field

        """
        field_args = {}

        # Handle all possible field constraints
        for key, value in props.items():
            if key in ["type", "validators", "serializers"]:
                continue
            field_args[key] = value

        return field_args

    def build_model(self, name: str, definition: dict[str, Any]):
        """Build a Pydantic model from a schema definition.

        Args:
        ----
            name: Name of the model to create
            definition: Schema definition for the model

        Returns:
        -------
            A Pydantic model class

        """
        if name in self.models:
            return self.models[name]

        fields_def = definition.get("fields", {})
        annotations = {}

        for field_name, props in fields_def.items():
            field_type = self.types.resolve(props["type"])
            field_args = self._get_field_args(props)

            if "default" in field_args:
                annotations[field_name] = (field_type, Field(**field_args))
            else:
                annotations[field_name] = (field_type, Field(..., **field_args))

        model = create_model(name, **annotations)
        self.models[name] = model

        for field_name, props in fields_def.items():
            for validator_name in props.get("validators", []):
                validator_fn = self.validators.get(validator_name)
                setattr(
                    model,
                    f"validate_{field_name}_{validator_name}",
                    field_validator(field_name)(validator_fn),
                )

        for validator_name in definition.get("validators", []):
            validator_fn = self.validators.get(validator_name)
            setattr(
                model,
                f"model_validate_{validator_name}",
                model_validator(mode="after")(validator_fn),
            )

        # After create_model(...) and before return
        for field_name, props in fields_def.items():
            serializer_names = props.get("serializers", [])
            for serializer_name in serializer_names:
                serializer_fn = self.serializers.get(serializer_name)

                # Attach a field serializer dynamically
                setattr(
                    model,
                    f"serialize_{field_name}_{serializer_name}",
                    field_serializer(field_name)(serializer_fn),
                )

        return model

    def build_all(self, definitions: dict[str, Any]):
        """Build all models from a schema definition dictionary.

        This method handles forward references by:
        1. Pre-registering dummy models
        2. Building and replacing them with real models

        Args:
        ----
            definitions: Dictionary of model definitions

        Returns:
        -------
            Dictionary mapping model names to their Pydantic model classes

        """
        # Step 1: Pre-register dummy models in the registry for forward references
        for name in definitions:
            # Register dummy model so types.resolve() can find it
            self.types.register(name, object)  # Use `object` or a placeholder type

        # Step 2: Build and replace dummy models
        for name, definition in definitions.items():
            model = self.build_model(name, definition)
            self.models[name] = model
            self.types.register(name, model)  # Replace placeholder with real model

        return self.models
