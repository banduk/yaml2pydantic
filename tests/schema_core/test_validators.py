import pytest

from schema_core.validators import ValidatorRegistry


def test_validator_registry_initialization():
    """Test that the validator registry initializes correctly."""
    registry = ValidatorRegistry()
    assert isinstance(registry.validators, dict)
    assert len(registry.validators) == 0


def test_validator_registration():
    """Test that validators can be registered and retrieved."""
    registry = ValidatorRegistry()

    @registry.validator
    def test_validator(value):
        return value > 0

    assert "test_validator" in registry.validators
    assert registry.validators["test_validator"] == test_validator


def test_validator_retrieval():
    """Test that registered validators can be retrieved and used."""
    registry = ValidatorRegistry()

    @registry.validator
    def test_validator(value):
        return value > 0

    validator = registry.get("test_validator")
    assert validator(5) is True
    assert validator(-1) is False


def test_validator_decorator_returns_original_function():
    """Test that the validator decorator returns the original function."""
    registry = ValidatorRegistry()

    def test_validator(value):
        return value > 0

    decorated = registry.validator(test_validator)
    assert decorated == test_validator


def test_validator_error_handling():
    """Test error handling when retrieving non-existent validators."""
    registry = ValidatorRegistry()
    with pytest.raises(KeyError, match="nonexistent_validator"):
        registry.get("nonexistent_validator")


def test_multiple_validators():
    """Test registration and usage of multiple validators."""
    registry = ValidatorRegistry()

    @registry.validator
    def is_positive(value):
        return value > 0

    @registry.validator
    def is_even(value):
        return value % 2 == 0

    assert registry.get("is_positive")(5) is True
    assert registry.get("is_positive")(-5) is False
    assert registry.get("is_even")(4) is True
    assert registry.get("is_even")(5) is False
