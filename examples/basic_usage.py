"""Basic usage example of yaml2pydantic."""

import yaml
from rich import print as pprint

from yaml2pydantic import create_models

# Define schema in YAML
schema = yaml.safe_load("""
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

# Create models from schema
models = create_models(schema)
User = models["User"]

# Create instances using different input formats
user1 = User(
    name="Alice",
    age=30,
    email="alice@example.com",
    birthday="1993-04-01T00:00:00",
    balance={"amount": 100},
    start_date="04/2025",
)

# Print the model instance
pprint(user1)

# Serialize to different formats
pprint(user1.model_dump())
pprint(user1.model_dump_json())
