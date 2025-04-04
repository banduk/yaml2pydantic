from datetime import datetime

import pytest
from pydantic import TypeAdapter

from yaml2pydantic.components.types.monthyear import MonthYear


def test_monthyear_initialization() -> None:
    """Test basic MonthYear initialization."""
    date = datetime(2023, 4, 15)
    monthyear = MonthYear(date)
    assert monthyear.value.year == 2023
    assert monthyear.value.month == 4
    assert monthyear.value.day == 1  # Always set to 1


def test_monthyear_string_representation() -> None:
    """Test MonthYear string representation."""
    date = datetime(2023, 4, 15)
    monthyear = MonthYear(date)
    assert str(monthyear) == "04/2023"
    assert repr(monthyear) == "04/2023"


def test_monthyear_equality() -> None:
    """Test MonthYear equality comparison."""
    date1 = datetime(2023, 4, 15)
    date2 = datetime(2023, 4, 1)  # Different day, same month/year
    date3 = datetime(2023, 5, 1)  # Different month

    monthyear1 = MonthYear(date1)
    monthyear2 = MonthYear(date2)
    monthyear3 = MonthYear(date3)

    assert monthyear1 == monthyear2  # Same month/year, different days
    assert monthyear1 != monthyear3  # Different months


def test_monthyear_pydantic_schema() -> None:
    """Test MonthYear Pydantic schema generation."""
    json_schema = TypeAdapter(MonthYear).json_schema()
    assert json_schema["type"] == "string"
    assert json_schema["format"] == "month-year"
    assert json_schema["example"] == "03/2025"


def test_monthyear_invalid_input() -> None:
    """Test MonthYear with invalid input."""
    with pytest.raises(ValueError):
        MonthYear("invalid")
