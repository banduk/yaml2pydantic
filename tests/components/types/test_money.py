import pytest

from yaml2pydantic.components.types.money import Money


def test_money_initialization() -> None:
    """Test basic Money initialization."""
    money = Money(amount=1000)
    assert money.amount == 1000
    assert money.currency == "R$"


def test_money_float_conversion() -> None:
    """Test conversion of float values to cents."""
    money = Money(amount=10.50)
    assert money.amount == 1050  # 10.50 * 100 = 1050 cents


def test_money_float_rounding() -> None:
    """Test rounding of float values to nearest cent."""
    money = Money(amount=10.555)
    assert money.amount == 1056  # 10.555 * 100 = 1055.5, rounded to 1056


def test_money_custom_currency() -> None:
    """Test Money with custom currency."""
    money = Money(amount=1000, currency="USD")
    assert money.amount == 1000
    assert money.currency == "USD"


def test_money_validation() -> None:
    """Test Money validation."""
    with pytest.raises(ValueError):
        Money(amount="invalid")  # type: ignore

    with pytest.raises(ValueError):
        Money(amount=None)  # type: ignore


def test_money_equality() -> None:
    """Test Money equality comparison."""
    money1 = Money(amount=1000)
    money2 = Money(amount=1000)
    money3 = Money(amount=2000)

    assert money1 == money2
    assert money1 != money3
