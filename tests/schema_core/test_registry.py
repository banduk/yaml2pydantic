import pytest

from schema_core.registry import serializers, types, validators


def test_registry_initialization():
    """Test that all registries are properly initialized."""
    assert types is not None
    assert serializers is not None
    assert validators is not None


def test_type_registry_builtin_types():
    """Test that built-in types are properly registered."""
    assert types.BUILTIN_TYPES["str"] is str
    assert types.BUILTIN_TYPES["int"] is int
    assert types.BUILTIN_TYPES["float"] is float
    assert types.BUILTIN_TYPES["bool"] is bool
    assert types.BUILTIN_TYPES["datetime"] is not None


def test_type_registry_custom_types():
    """Test custom type registration and resolution."""

    class CustomType:
        pass

    types.register("CustomType", CustomType)
    assert types.resolve("CustomType") == CustomType


def test_type_registry_optional_types():
    """Test resolution of Optional types."""
    assert types.resolve("Optional[str]") == str | None
    assert types.resolve("Optional[int]") == int | None


def test_serializer_registry():
    """Test serializer registration and retrieval."""

    @serializers.serializer
    def test_serializer(value):
        return str(value).upper()

    assert "test_serializer" in serializers.serializers
    assert serializers.get("test_serializer")("test") == "TEST"


def test_validator_registry():
    """Test validator registration and retrieval."""

    @validators.validator
    def test_validator(value):
        return value > 0

    assert "test_validator" in validators.validators
    assert validators.get("test_validator")(5) is True
    assert validators.get("test_validator")(-1) is False


def test_registry_error_handling():
    """Test error handling in registries."""
    with pytest.raises(KeyError):
        serializers.get("nonexistent_serializer")

    with pytest.raises(KeyError):
        validators.get("nonexistent_validator")

    with pytest.raises(KeyError):
        types.resolve("nonexistent_type")
