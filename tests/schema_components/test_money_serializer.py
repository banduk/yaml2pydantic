from schema_components.serializers.money import money_as_string
from schema_components.types.money import Money


def test_money_as_string_default_currency() -> None:
    """Test money_as_string with default currency (R$)."""
    money = Money(amount=1000)  # 10.00 in R$
    assert money_as_string(money) == "R$ 10.00"

    money = Money(amount=1050)  # 10.50 in R$
    assert money_as_string(money) == "R$ 10.50"

    money = Money(amount=100)  # 1.00 in R$
    assert money_as_string(money) == "R$ 1.00"


def test_money_as_string_custom_currency() -> None:
    """Test money_as_string with custom currency."""
    money = Money(amount=1000, currency="USD")
    assert money_as_string(money) == "USD 10.00"

    money = Money(amount=1050, currency="EUR")
    assert money_as_string(money) == "EUR 10.50"


def test_money_as_string_edge_cases() -> None:
    """Test money_as_string with edge cases."""
    # Zero amount
    money = Money(amount=0)
    assert money_as_string(money) == "R$ 0.00"

    # Large amount
    money = Money(amount=1000000)  # 10,000.00
    assert money_as_string(money) == "R$ 10000.00"

    # Small amount
    money = Money(amount=1)  # 0.01
    assert money_as_string(money) == "R$ 0.01"


def test_money_as_string_rounding() -> None:
    """Test money_as_string with rounding cases."""
    money = Money(amount=1055)  # 10.55
    assert money_as_string(money) == "R$ 10.55"

    money = Money(amount=1056)  # 10.56
    assert money_as_string(money) == "R$ 10.56"
