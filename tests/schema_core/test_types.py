from datetime import datetime

import pytest

from schema_core.types import TypeRegistry


def test_type_registry_initialization():
    """Test that the type registry initializes correctly."""
    registry = TypeRegistry()
    assert isinstance(registry.custom_types, dict)
    assert len(registry.custom_types) == 0


def test_builtin_types():
    """Test that all built-in types are properly defined."""
    registry = TypeRegistry()
    assert registry.BUILTIN_TYPES["str"] is str
    assert registry.BUILTIN_TYPES["int"] is int
    assert registry.BUILTIN_TYPES["float"] is float
    assert registry.BUILTIN_TYPES["bool"] is bool
    assert registry.BUILTIN_TYPES["datetime"] is datetime


def test_custom_type_registration():
    """Test registration of custom types."""
    registry = TypeRegistry()

    class CustomType:
        pass

    registry.register("CustomType", CustomType)
    assert registry.custom_types["CustomType"] == CustomType


def test_type_resolution():
    """Test resolution of both built-in and custom types."""
    registry = TypeRegistry()

    class CustomType:
        pass

    registry.register("CustomType", CustomType)

    assert registry.resolve("str") is str
    assert registry.resolve("int") is int
    assert registry.resolve("CustomType") is CustomType


def test_optional_type_resolution():
    """Test resolution of Optional types."""
    registry = TypeRegistry()
    assert registry.resolve("Optional[str]") == str | None
    assert registry.resolve("Optional[int]") == int | None
    assert registry.resolve("Optional[float]") == float | None


def test_type_resolution_error_handling():
    """Test error handling when resolving non-existent types."""
    registry = TypeRegistry()
    with pytest.raises(KeyError, match="nonexistent_type"):
        registry.resolve("nonexistent_type")


def test_optional_type_error_handling():
    """Test error handling for Optional types with non-existent inner types."""
    registry = TypeRegistry()
    with pytest.raises(KeyError, match="nonexistent_type"):
        registry.resolve("Optional[nonexistent_type]")
