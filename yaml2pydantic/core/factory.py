import importlib
import logging
from collections.abc import Callable
from pathlib import Path
from typing import Any

from pydantic import (
    BaseModel,
    Field,
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

    types: TypeRegistry
    validators: ValidatorRegistry
    serializers: SerializerRegistry
    models: dict[str, type[BaseModel]]

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
        self.models: dict[str, type[BaseModel]] = {}
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

    def _process_field_default(
        self,
        field_type: Any,
        field_args: dict[str, Any],
        props: dict[str, Any],
        definition: dict[str, Any],
    ) -> dict[str, Any]:
        """Process default value for a field, especially for model types.

        Args:
        ----
            field_type: The resolved type of the field
            field_args: The field arguments dictionary
            props: The field properties from the schema
            definition: The complete model definition

        Returns:
        -------
            Updated field_args dictionary
        """
        if "default" in field_args and isinstance(field_args["default"], dict):
            if field_type is not None and hasattr(field_type, "model_validate"):
                # Ensure the model is built before using it
                if field_type not in self.models.values():
                    # This branch should never execute in practice because we check
                    # first
                    self.build_model(props["type"], definition)  # pragma: no cover
                field_args["default"] = field_type.model_validate(field_args["default"])

        return field_args

    def _add_field_to_model(
        self,
        field_name: str,
        field_type: Any,
        field_args: dict[str, Any],
        namespace: dict[str, Any],
        annotations: dict[str, Any],
    ) -> None:
        """Add a field to the model namespace and annotations.

        Args:
        ----
            field_name: The name of the field
            field_type: The resolved type of the field
            field_args: The field arguments dictionary
            namespace: The namespace dictionary for the model
            annotations: The annotations dictionary for the model
        """
        annotations[field_name] = field_type
        if "default" in field_args:
            namespace[field_name] = Field(**field_args)
        else:
            namespace[field_name] = Field(..., **field_args)

    def _add_serializers(
        self, field_name: str, props: dict[str, Any], namespace: dict[str, Any]
    ) -> None:
        """Add serializers for a field to the model namespace.

        Args:
        ----
            field_name: The name of the field
            props: The field properties from the schema
            namespace: The namespace dictionary for the model
        """
        serializer_names = props.get("serializers", [])
        for serializer_name in serializer_names:
            serializer_fn = self.serializers.get(serializer_name)

            # Create a serializer method
            def create_serializer(
                fn: Callable[[Any], Any],
            ) -> Callable[[Any], Any]:
                @field_serializer(field_name)
                def serializer(v: Any) -> Any:
                    return fn(v)

                return serializer

            namespace[f"serialize_{field_name}_{serializer_name}"] = create_serializer(
                serializer_fn
            )

    def _add_field_validators(
        self, field_name: str, props: dict[str, Any], namespace: dict[str, Any]
    ) -> None:
        """Add field validators to the model namespace.

        Args:
        ----
            field_name: The name of the field
            props: The field properties from the schema
            namespace: The namespace dictionary for the model
        """
        for validator_name in props.get("validators", []):
            validator_fn = self.validators.get(validator_name)
            namespace[f"validate_{field_name}_{validator_name}"] = field_validator(
                field_name
            )(validator_fn)

    def _add_model_validators(
        self, definition: dict[str, Any], namespace: dict[str, Any]
    ) -> None:
        """Add model validators to the model namespace.

        Args:
        ----
            definition: The model definition from the schema
            namespace: The namespace dictionary for the model
        """
        for validator_name in definition.get("validators", []):
            validator_fn = self.validators.get(validator_name)
            namespace[f"model_validate_{validator_name}"] = model_validator(
                mode="after"
            )(validator_fn)

    def build_model(self, name: str, definition: dict[str, Any]) -> type[BaseModel]:
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
        namespace: dict[str, Any] = {}
        annotations: dict[str, Any] = {}

        # Process all field definitions
        for field_name, props in fields_def.items():
            field_type = self.types.resolve(props["type"])
            field_args = self._get_field_args(props)

            # Process default values
            field_args = self._process_field_default(
                field_type, field_args, props, definition
            )

            # Add field to namespace and annotations
            self._add_field_to_model(
                field_name, field_type, field_args, namespace, annotations
            )

            # Add serializers for this field
            self._add_serializers(field_name, props, namespace)

        # Add validators
        for field_name, props in fields_def.items():
            self._add_field_validators(field_name, props, namespace)

        # Add model validators
        self._add_model_validators(definition, namespace)

        # Create the model class
        namespace["__annotations__"] = annotations
        ModelClass = type(name, (BaseModel,), namespace)
        self.models[name] = ModelClass
        return ModelClass

    def build_all(self, definitions: dict[str, Any]) -> dict[str, type[BaseModel]]:
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
