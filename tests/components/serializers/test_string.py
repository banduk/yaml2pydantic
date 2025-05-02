from yaml2pydantic.components.serializers.string import to_lower, to_upper


def test_string_to_lower() -> None:
    """Test to_lower serializer."""
    assert to_lower("Hello, World!") == "hello, world!"


def test_string_to_upper() -> None:
    """Test to_upper serializer."""
    assert to_upper("Hello, World!") == "HELLO, WORLD!"
