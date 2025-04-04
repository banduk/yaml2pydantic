from datetime import datetime

from schema_core.types import TypeRegistry


def test_type_registry_initialization():
    """Test that the type registry initializes correctly."""
    registry = TypeRegistry()
    assert isinstance(registry.custom_types, dict)
    assert len(registry.custom_types) == 0


def test_builtin_types():
    """Test that all built-in types are properly defined."""
    registry = TypeRegistry()
    assert registry.BUILTIN_TYPES["str"] == str
    assert registry.BUILTIN_TYPES["int"] == int
    assert registry.BUILTIN_TYPES["float"] == float
    assert registry.BUILTIN_TYPES["bool"] == bool
    assert registry.BUILTIN_TYPES["datetime"] == datetime


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

    assert registry.resolve("str") == str
    assert registry.resolve("int") == int
    assert registry.resolve("CustomType") == CustomType


def test_optional_type_resolution():
    """Test resolution of Optional types."""
    registry = TypeRegistry()
    assert registry.resolve("Optional[str]") == str | None
    assert registry.resolve("Optional[int]") == int | None
    assert registry.resolve("Optional[float]") == float | None


def test_type_resolution_error_handling():
    """Test error handling when resolving non-existent types."""
    registry = TypeRegistry()
    try:
        registry.resolve("nonexistent_type")
        assert False, "Expected KeyError"
    except KeyError:
        pass


def test_optional_type_error_handling():
    """Test error handling for Optional types with non-existent inner types."""
    registry = TypeRegistry()
    try:
        registry.resolve("Optional[nonexistent_type]")
        assert False, "Expected KeyError"
    except KeyError:
        pass
