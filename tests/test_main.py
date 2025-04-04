from datetime import datetime

import pytest
import yaml

from yaml2pydantic import serializers, types, validators
from yaml2pydantic.components.types.money import Money
from yaml2pydantic.core.factory import ModelFactory
from yaml2pydantic.core.loader import SchemaLoader

# Test data
user_schema = yaml.safe_load("""
User:
  fields:
    name:
      type: str
      max_length: 10
    age:
      type: int
      ge: 0
    email:
      type: Optional[str]
      default: null
    birthday:
      type: datetime
    address:
      type: Address
      default:
        street: "Unknown"
        city: "Unknown"
        zip: "00000"
    balance:
      type: Money
      default: 0
    start_date:
      type: MonthYear
      default: "03/2025"

Address:
  fields:
    street:
      type: str
    city:
      type: str
    zip:
      type: str
""")


def test_model_creation() -> None:
    # Load schema and create models
    schema = SchemaLoader.load(user_schema)
    factory = ModelFactory(types, validators, serializers)
    models = factory.build_all(schema)
    User = models["User"]

    # Test creating user with direct parameters
    user1 = User(
        name="Alice",
        age=30,
        email="alice@example.com",
        birthday="1993-04-01T00:00:00",
        balance=Money(amount=100),
        start_date="04/2025",
    )

    assert user1.name == "Alice"
    assert user1.age == 30
    assert user1.email == "alice@example.com"
    assert user1.birthday == datetime(1993, 4, 1, 0, 0, 0)
    assert user1.balance.amount == 100
    assert user1.start_date == "04/2025"
    assert user1.address.street == "Unknown"
    assert user1.address.city == "Unknown"
    assert user1.address.zip == "00000"


def test_model_creation_with_dict() -> None:
    # Load schema and create models
    schema = SchemaLoader.load(user_schema)
    factory = ModelFactory(types, validators, serializers)
    models = factory.build_all(schema)
    User = models["User"]

    # Test creating user with dictionary unpacking
    user2 = User(
        **{
            "name": "Alice",
            "age": 30,
            "email": "alice@example.com",
            "birthday": "1993-04-01T00:00:00",
            "balance": {"amount": 100},
            "start_date": "04/2025",
        }
    )

    assert user2.name == "Alice"
    assert user2.age == 30
    assert user2.email == "alice@example.com"
    assert user2.birthday == datetime(1993, 4, 1, 0, 0, 0)
    assert user2.balance.amount == 100
    assert user2.start_date == "04/2025"


def test_model_validation() -> None:
    # Load schema and create models
    schema = SchemaLoader.load(user_schema)
    factory = ModelFactory(types, validators, serializers)
    models = factory.build_all(schema)
    User = models["User"]

    # Test validation of name length
    with pytest.raises(ValueError):
        User(
            name="Alice with a big Name",  # Exceeds max_length: 10
            age=30,
            email="alice@example.com",
            birthday="1993-04-01T00:00:00",
            balance=Money(amount=100),
            start_date="04/2025",
        )

    # Test validation of age
    with pytest.raises(ValueError):
        User(
            name="Alice",
            age=-1,  # Violates ge: 0
            email="alice@example.com",
            birthday="1993-04-01T00:00:00",
            balance=Money(amount=100),
            start_date="04/2025",
        )


def test_model_serialization() -> None:
    # Load schema and create models
    schema = SchemaLoader.load(user_schema)
    factory = ModelFactory(types, validators, serializers)
    models = factory.build_all(schema)
    User = models["User"]

    user = User(
        name="Alice",
        age=30,
        email="alice@example.com",
        birthday="1993-04-01T00:00:00",
        balance=Money(amount=100),
        start_date="04/2025",
    )

    # Test model_dump
    dump_data = user.model_dump()
    assert dump_data["name"] == "Alice"
    assert dump_data["age"] == 30
    assert dump_data["email"] == "alice@example.com"
    assert isinstance(dump_data["birthday"], datetime)
    assert dump_data["balance"]["amount"] == 100
    assert dump_data["start_date"] == "04/2025"

    # Test model_dump_json
    json_data = user.model_dump_json()
    assert isinstance(json_data, str)
    assert "Alice" in json_data
    assert "30" in json_data
