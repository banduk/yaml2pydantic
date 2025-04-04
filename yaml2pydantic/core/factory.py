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

from yaml2pydantic.core.serializers import SerializerRegistry
from yaml2pydantic.core.type_registry import TypeRegistry
from yaml2pydantic.core.validators import ValidatorRegistry

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
        self.models: dict[str, Any] = {}
        self._load_components()

    def _load_components(self) -> None:
        """Load all schema components from the components directory.

        This includes types, validators, and serializers.
        """
        from yaml2pydantic.core import registry  # noqa: F401

        component_path = Path(__file__).parent.parent / "components"
        modules = ["types", "validators", "serializers"]

        for module in modules:
            module_path = component_path / module
            for file in module_path.glob("*.py"):
                if file.stem != "__init__":
                    importlib.import_module(
                        f"yaml2pydantic.components.{module}.{file.stem}"
                    )

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

    def build_model(self, name: str, definition: dict[str, Any]) -> Any:
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

            # If the field type is a model and has a default dict value,
            # we need to ensure the model is built before using it
            if "default" in field_args and isinstance(field_args["default"], dict):
                if field_type is not None and hasattr(field_type, "model_validate"):
                    # Ensure the model is built before using it
                    if field_type not in self.models.values():
                        self.build_model(props["type"], definition)
                    field_args["default"] = field_type.model_validate(
                        field_args["default"]
                    )

            if "default" in field_args:
                annotations[field_name] = (field_type, Field(**field_args))
            else:
                annotations[field_name] = (field_type, Field(..., **field_args))

        model = create_model(name, **annotations)  # type: ignore
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

    def build_all(self, definitions: dict[str, Any]) -> dict[str, Any]:
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

        # Step 2: Build models in dependency order
        built_models: set[str] = set()
        while len(built_models) < len(definitions):
            for name, definition in definitions.items():
                if name in built_models:
                    continue

                # Check if all dependencies are built
                dependencies = set()
                for field_def in definition.get("fields", {}).values():
                    field_type = field_def.get("type", "")
                    if field_type in definitions and field_type != name:
                        dependencies.add(field_type)

                if all(dep in built_models for dep in dependencies):
                    model = self.build_model(name, definition)
                    self.models[name] = model
                    self.types.register(
                        name, model
                    )  # Replace placeholder with real model
                    built_models.add(name)

        return self.models
