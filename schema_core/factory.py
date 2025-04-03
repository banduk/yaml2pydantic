import importlib
import logging
from pathlib import Path
from typing import Any, Dict

from pydantic import Field, create_model, field_serializer, field_validator, model_validator
from schema_core.serializers import SerializerRegistry
from schema_core.types import TypeRegistry
from schema_core.validators import ValidatorRegistry

logger = logging.getLogger(__name__)


class ModelFactory:
    def __init__(
        self, types: TypeRegistry, validators: ValidatorRegistry, serializers: SerializerRegistry
    ):
        self.types = types
        self.validators = validators
        self.serializers = serializers
        self.models = {}
        self._load_schema_components()

    def _load_schema_components(self):
        from schema_core import registry  # noqa: F401

        COMPONENT_PATH = Path(__file__).parent.parent / "schema_components"
        MODULES = ["types", "validators", "serializers"]

        for module in MODULES:
            module_path = COMPONENT_PATH / module
            for file in module_path.glob("*.py"):
                if file.stem != "__init__":
                    importlib.import_module(f"schema_components.{module}.{file.stem}")

    def _get_field_args(self, props: Dict[str, Any]) -> Dict[str, Any]:
        field_args = {}

        # Handle all possible field constraints
        for key, value in props.items():
            if key in ["type", "validators", "serializers"]:
                continue
            field_args[key] = value

        return field_args

    def build_model(self, name: str, definition: Dict[str, Any]):
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

    def build_all(self, definitions: Dict[str, Any]):
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
