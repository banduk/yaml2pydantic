"""Tests for the schema loader module."""

import pytest
from pydantic import BaseModel

from yaml2pydantic.core.factory import ModelFactory
from yaml2pydantic.core.serializers import SerializerRegistry
from yaml2pydantic.core.type_registry import TypeRegistry
from yaml2pydantic.core.validators import ValidatorRegistry


class User(BaseModel):
    username: str


class Address(BaseModel):
    street: str
    city: str
    zip: str


@pytest.fixture
def type_registry():
    """Create a type registry with basic types."""
    registry = TypeRegistry()
    registry.register("str", str)
    registry.register("int", int)
    registry.register("float", float)
    registry.register("bool", bool)
    return registry


@pytest.fixture
def validator_registry():
    """Create a validator registry with basic validators."""
    registry = ValidatorRegistry()

    @registry.validator
    def positive(value):
        if value <= 0:
            raise ValueError("Value must be positive")
        return value

    @registry.validator
    def non_empty(value):
        if not value:
            raise ValueError("Value cannot be empty")
        return value

    return registry


@pytest.fixture
def serializer_registry():
    """Create a serializer registry with basic serializers."""
    registry = SerializerRegistry()

    @registry.serializer
    def to_upper(value):
        return value.upper()

    @registry.serializer
    def to_lower(value):
        return value.lower()

    return registry


@pytest.fixture
def model_factory(type_registry, validator_registry, serializer_registry):
    """Create a ModelFactory instance with the provided registries."""
    return ModelFactory(type_registry, validator_registry, serializer_registry)


def test_model_factory_initialization(model_factory):
    """Test that ModelFactory initializes correctly."""
    assert isinstance(model_factory.types, TypeRegistry)
    assert isinstance(model_factory.validators, ValidatorRegistry)
    assert isinstance(model_factory.serializers, SerializerRegistry)
    assert isinstance(model_factory.models, dict)
    assert len(model_factory.models) == 0


def test_build_simple_model(model_factory):
    """Test building a simple model with basic types."""
    schema = {
        "Person": {
            "fields": {
                "name": {"type": "str"},
                "age": {"type": "int"},
                "is_active": {"type": "bool", "default": True},
            }
        }
    }

    models = model_factory.build_all(schema)
    assert "Person" in models

    Person = models["Person"]
    person = Person(name="John", age=30)

    assert person.name == "John"
    assert person.age == 30
    assert person.is_active is True


def test_build_model_with_validators(model_factory):
    """Test building a model with field validators."""
    schema = {
        "Product": {
            "fields": {
                "name": {
                    "type": "str",
                    "validators": ["non_empty"],
                },
                "price": {
                    "type": "float",
                    "validators": ["positive"],
                },
            }
        }
    }

    models = model_factory.build_all(schema)
    Product = models["Product"]

    # Test valid data
    product = Product(name="Laptop", price=999.99)
    assert product.name == "Laptop"
    assert product.price == 999.99

    with pytest.raises(ValueError, match="Value cannot be empty"):
        Product(name="", price=999.99)

    with pytest.raises(ValueError, match="Value must be positive"):
        Product(name="Laptop", price=-1.0)


def test_build_model_with_serializers(model_factory):
    """Test building a model with field serializers."""
    schema = {
        "User": {
            "fields": {
                "username": {
                    "type": "str",
                    "serializers": ["to_upper"],
                },
                "email": {
                    "type": "str",
                    "serializers": ["to_lower"],
                },
            }
        }
    }

    models = model_factory.build_all(schema)
    User = models["User"]
    user = User(username="john", email="John@Example.com")

    # Test serialization
    dump_data = user.model_dump(mode="json")
    assert dump_data["username"] == "JOHN"
    assert dump_data["email"] == "john@example.com"


def test_build_nested_models(model_factory):
    """Test building models with nested model references."""
    schema = {
        "Address": {
            "fields": {
                "street": {"type": "str"},
                "city": {"type": "str"},
                "zip": {"type": "str"},
            }
        },
        "Person": {
            "fields": {
                "name": {"type": "str"},
                "address": {"type": "Address"},
            }
        },
    }

    models = model_factory.build_all(schema)
    assert "Address" in models
    assert "Person" in models

    Person = models["Person"]
    Address = models["Address"]

    address = Address(street="123 Main St", city="Springfield", zip="12345")
    person = Person(name="John", address=address)

    assert person.name == "John"
    assert person.address.street == "123 Main St"
    assert person.address.city == "Springfield"
    assert person.address.zip == "12345"


def test_build_model_with_default_values(model_factory):
    """Test building a model with default values."""
    schema = {
        "Settings": {
            "fields": {
                "theme": {"type": "str", "default": "light"},
                "notifications": {"type": "bool", "default": True},
                "refresh_rate": {"type": "int", "default": 60},
            }
        }
    }

    models = model_factory.build_all(schema)
    Settings = models["Settings"]

    # Test with no values provided
    settings = Settings()
    assert settings.theme == "light"
    assert settings.notifications is True
    assert settings.refresh_rate == 60

    # Test with some values provided
    settings = Settings(theme="dark", refresh_rate=30)
    assert settings.theme == "dark"
    assert settings.notifications is True
    assert settings.refresh_rate == 30


def test_build_model_when_model_already_exists(model_factory):
    """Test building a model when the model already exists."""
    model_factory.models["User"] = User
    schema = {
        "User": {
            "fields": {
                "username": {
                    "type": "str",
                    "serializers": ["to_upper"],
                    "validators": ["non_empty"],
                },
            }
        }
    }

    model = model_factory.build_model("User", schema)
    assert model == User


def test_build_model_with_nested_default_values(model_factory):
    """Test building a model with nested default values."""
    # First, build and register the User model
    user_schema = {"fields": {"username": {"type": "str"}}}
    UserModel = model_factory.build_model("User", user_schema)
    model_factory.types.register("User", UserModel)

    # Define a schema with a nested model field that has a default value
    schema = {
        "fields": {"user": {"type": "User", "default": {"username": "default_user"}}}
    }

    # Build the model
    model = model_factory.build_model("Profile", schema)

    # Create an instance without providing the user field
    instance = model()

    # Verify the default value was properly set
    assert isinstance(instance.user, UserModel)
    assert instance.user.username == "default_user"

    # Create an instance with a custom user value
    custom_instance = model(user={"username": "custom_user"})
    assert isinstance(custom_instance.user, UserModel)
    assert custom_instance.user.username == "custom_user"


def test_build_model_with_invalid_field_type(model_factory):
    """Test building a model with an invalid field type."""
    # Use a type that is not None but doesn't have model_validate
    model_factory.types.register("custom_type", object)

    # Create a schema with a field that has a dictionary default value
    schema = {
        "fields": {
            "custom_field": {
                "type": "custom_type",
                "default": {"some": "value"},  # This is a dictionary
            }
        }
    }

    # Build the model - this should not raise an error
    model = model_factory.build_model("InvalidModel", schema)

    # Create an instance - the default value should be preserved
    instance = model()
    assert instance.custom_field == {"some": "value"}

    # Create an instance with a custom value
    custom_instance = model(custom_field={"other": "value"})
    assert custom_instance.custom_field == {"other": "value"}


def test_build_model_with_model_validators(model_factory):
    """Test building a model with model-level validators."""

    # Add a model validator
    @model_factory.validators.validator
    def validate_model(model):
        if hasattr(model, "name") and model.name == "invalid":
            raise ValueError("Invalid name")
        return model

    schema = {"fields": {"name": {"type": "str"}}, "validators": ["validate_model"]}

    model = model_factory.build_model("ValidatedModel", schema)

    # Test valid case
    instance = model(name="valid")
    assert instance.name == "valid"

    # Test invalid case
    with pytest.raises(ValueError, match="Invalid name"):
        model(name="invalid")
