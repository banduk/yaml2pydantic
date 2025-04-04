import pytest

from schema_components.validators.numeric import check_positive


def test_check_positive_valid() -> None:
    """Test check_positive with valid positive numbers."""
    assert check_positive(None, 1) == 1
    assert check_positive(None, 0.1) == 0.1
    assert check_positive(None, 1000) == 1000


def test_check_positive_invalid() -> None:
    """Test check_positive with invalid (non-positive) numbers."""
    with pytest.raises(ValueError, match="Must be positive"):
        check_positive(None, 0)

    with pytest.raises(ValueError, match="Must be positive"):
        check_positive(None, -1)

    with pytest.raises(ValueError, match="Must be positive"):
        check_positive(None, -0.1)


def test_check_positive_edge_cases() -> None:
    """Test check_positive with edge cases."""
    # Test with very small positive number
    assert check_positive(None, 0.0000001) == 0.0000001

    # Test with very large positive number
    assert check_positive(None, 1e100) == 1e100


def test_check_positive_invalid_types() -> None:
    """Test check_positive with invalid input types."""
    with pytest.raises(TypeError):
        check_positive(None, "not a number")

    with pytest.raises(TypeError):
        check_positive(None, None)
