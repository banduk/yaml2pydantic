"""Example usage of the yaml2pydantic library.

This module demonstrates how to:
1. Define models in YAML
2. Load and compile them into Pydantic models
3. Create instances with different input formats
4. Serialize models to different formats
"""

import yaml
from rich import print as pprint

from schema_components.types.money import Money
from schema_core.factory import ModelFactory
from schema_core.loader import SchemaLoader
from schema_core.registry import serializers, types, validators

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


schema = SchemaLoader.load(user_schema)
factory = ModelFactory(types, validators, serializers)
models = factory.build_all(schema)
User = models["User"]
user1 = User(
    name="Alice",
    age=30,
    email="alice@example.com",
    birthday="1993-04-01T00:00:00",
    balance=Money(amount=100),
    start_date="04/2025",
)
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
pprint(user1)
pprint(user2)
pprint(user1.model_dump())
pprint(user1.model_dump_json())
pprint(user2.model_dump())
pprint(user2.model_dump_json())


user3 = User(
    **{
        "name": "Alice with a big Name",
        "age": 30,
        "email": "alice@example.com",
        "birthday": "1993-04-01T00:00:00",
        "balance": {"amount": 100},
        "start_date": "04/2025",
    }
)
