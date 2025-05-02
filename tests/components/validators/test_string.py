import pytest

from yaml2pydantic.components.validators.string import non_empty


def test_non_empty_validator() -> None:
    """Test non_empty validator."""
    assert non_empty("Hello, World!") == "Hello, World!"

    with pytest.raises(ValueError):
        non_empty("")

    with pytest.raises(ValueError):
        non_empty(None)

    with pytest.raises(ValueError):
        non_empty([])
