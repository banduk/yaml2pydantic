import pytest

from schema_core.serializers import SerializerRegistry


def test_serializer_registry_initialization():
    """Test that the serializer registry initializes correctly."""
    registry = SerializerRegistry()
    assert isinstance(registry.serializers, dict)
    assert len(registry.serializers) == 0


def test_serializer_registration():
    """Test that serializers can be registered and retrieved."""
    registry = SerializerRegistry()

    @registry.serializer
    def test_serializer(value):
        return str(value).upper()

    assert "test_serializer" in registry.serializers
    assert registry.serializers["test_serializer"] == test_serializer


def test_serializer_retrieval():
    """Test that registered serializers can be retrieved and used."""
    registry = SerializerRegistry()

    @registry.serializer
    def test_serializer(value):
        return str(value).upper()

    serializer = registry.get("test_serializer")
    assert serializer("hello") == "HELLO"
    assert serializer(123) == "123"


def test_serializer_decorator_returns_original_function():
    """Test that the serializer decorator returns the original function."""
    registry = SerializerRegistry()

    def test_serializer(value):
        return str(value).upper()

    decorated = registry.serializer(test_serializer)
    assert decorated == test_serializer


def test_serializer_error_handling():
    """Test error handling when retrieving non-existent serializers."""
    registry = SerializerRegistry()
    with pytest.raises(KeyError, match="nonexistent_serializer"):
        registry.get("nonexistent_serializer")
