# 🧬 yaml2pydantic

**A powerful, extensible schema compiler that turns YAML/JSON definitions into dynamic Pydantic models** — with full support for:

- ✅ Custom types  
- ✅ Field and model-level validators  
- ✅ Custom serializers (field- and model-level)  
- ✅ Default values  
- ✅ Nested models  
- ✅ Reusable shared components  
- ✅ Auto-importing of components
- ✅ Built-in type system

📚 [View the full documentation](https://yourusername.github.io/yaml2pydantic/)

Built for teams that want to define models declaratively in YAML but leverage all the power of Pydantic v2.

---

## ✨ Key Features

| Feature                       | Description                                                                 |
| ----------------------------- | --------------------------------------------------------------------------- |
| 📄 YAML/JSON to Pydantic       | Define your models in YAML or JSON, and compile them into Pydantic models.  |
| 🧱 Custom Types                | Extend your schema with types like `Money`, `MonthYear`, etc.               |
| 🧪 Validators                  | Use reusable or model-specific validators (`check_positive`, etc.)          |
| 🎨 Serializers                 | Serialize fields or models however you want (`Money` → `"R$ 10,00"`)        |
| 🔁 Field Defaults              | Fully supports defaults for primitive and complex types                     |
| ⚙️ Dynamic ModelFactory        | All logic for building Pydantic models is centralized and pluggable         |
| 📚 Registry-based architecture | Types, validators, serializers all managed through shared registries        |
| 🔄 Auto-importing              | Components are automatically imported from schema_components directory      |
| 🏗️ Built-in Types              | Support for common types like Money, MonthYear, and all Pydantic primitives |

---

## 🧭 Project Structure

```
yaml2pydantic/
├── main.py                        # Entry point to load + test models
├── models/                        # YAML/JSON model definitions
│   └── user.yaml
├── schema_components/            # Shared reusable logic
│   ├── serializers/              # Custom serialization functions
│   │   └── money.py             # Money-specific serializers
│   ├── types/                    # Custom types (Money, MonthYear)
│   │   ├── money.py             # Money type implementation
│   │   └── monthyear.py         # MonthYear type implementation
│   └── validators/               # Custom validation logic
│       ├── email.py             # Email-related validators
│       └── numeric.py           # Numeric validators
└── schema_core/                  # Core schema engine
    ├── factory.py                # ModelFactory that builds Pydantic models
    ├── loader.py                 # Loads YAML, JSON, or dict input
    ├── registry.py               # Shared registries for types, validators, serializers
    ├── types.py                  # TypeRegistry
    ├── validators.py             # ValidatorRegistry
    └── serializers.py            # SerializerRegistry
```

---

## 🛠️ How It Works

### 1. 📝 Define Your Model in YAML

```yaml
User:
  fields:
    name:
      type: str
      max_length: 10  # Built-in Pydantic field constraints
    age:
      type: int
      ge: 0          # Built-in Pydantic field constraints
      validators:
        - check_positive  # Custom validator
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
      serializers:
        - money_as_string  # Custom serializer
    start_date:
      type: MonthYear
      default: "03/2025"
  validators:
    - email_contains_name  # Model-level validator

Address:
  fields:
    street:
      type: str
    city:
      type: str
    zip:
      type: str
```

---

### 2. 🏗 Build Models Dynamically

```python
from schema_core.loader import SchemaLoader
from schema_core.factory import ModelFactory
from schema_core.registry import types, validators, serializers

# Load from file
schema = SchemaLoader.load("models/user.yaml")

# Or load from dict
schema = SchemaLoader.load({
    "User": {
        "fields": {
            "name": {"type": "str"},
            # ... other fields
        }
    }
})

factory = ModelFactory(types, validators, serializers)
models = factory.build_all(schema)

User = models["User"]
```

---

### 3. ✅ Built-in Types

#### Money Type
```python
# In YAML
balance:
  type: Money
  default: 0
  serializers:
    - money_as_string

# Usage
user = User(balance={"amount": 100})  # 100 cents = R$ 1,00
print(user.balance)  # R$ 1,00
```

#### MonthYear Type
```python
# In YAML
start_date:
  type: MonthYear
  default: "03/2025"

# Usage
user = User(start_date="04/2025")  # Accepts "YYYY-MM" or "MM/YYYY" format
print(user.start_date)  # 04/2025
```

---

### 4. ✅ Field and Model Validators

#### Field Validators
```python
# In YAML
age:
  type: int
  validators:
    - check_positive

# Implementation
@validators.validator
def check_positive(cls, v):
    if v <= 0:
        raise ValueError("Must be positive")
    return v
```

#### Model Validators
```python
# In YAML
User:
  fields:
    name: { type: str }
    email: { type: Optional[str] }
  validators:
    - email_contains_name

# Implementation
@validators.validator
def email_contains_name(cls, values):
    name, email = values.get("name"), values.get("email")
    if email and name.lower() not in email.lower():
        raise ValueError("Email must contain user's name")
    return values
```

---

### 5. ✅ Custom Serializers

```python
# In YAML
balance:
  type: Money
  serializers:
    - money_as_string

# Implementation
@serializers.serializer
def money_as_string(value: Money) -> str:
    return f"{value.currency} {value.amount / 100:.2f}"
```

---

### 6. ✅ Field Constraints

All Pydantic field constraints are supported:

```yaml
User:
  fields:
    name:
      type: str
      max_length: 10
      min_length: 3
    age:
      type: int
      ge: 0
      le: 120
    email:
      type: str
      pattern: "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
```

---

### 7. 🔧 Extending Components

The library is designed to be easily extensible. You can add new types, validators, and serializers by creating new files in the `schema_components` directory.

#### Creating a New Type

1. Create a new file in `schema_components/types/` (e.g., `phone.py`):

```python
from pydantic import GetCoreSchemaHandler
from pydantic_core import core_schema
from schema_core.registry import types

class Phone:
    def __init__(self, value: str):
        self.value = value

    def __str__(self):
        return self.value

    @staticmethod
    def _validate(v):
        if isinstance(v, Phone):
            return v
        if isinstance(v, str):
            # Add your validation logic here
            if not v.replace("+", "").replace("-", "").replace(" ", "").isdigit():
                raise ValueError("Invalid phone number format")
            return Phone(v)
        raise ValueError("Phone must be a string")

    @staticmethod
    def _serialize(instance: "Phone") -> str:
        return instance.value

    @classmethod
    def __get_pydantic_core_schema__(
        cls, _source_type, _handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        return core_schema.no_info_plain_validator_function(
            cls._validate,
            serialization=core_schema.plain_serializer_function_ser_schema(
                cls._serialize,
                return_schema=core_schema.str_schema(),
            ),
        )

# Register globally
types.register("Phone", Phone)
```

2. Use it in your YAML:

```yaml
User:
  fields:
    phone:
      type: Phone
      default: "+55 11 99999-9999"
```

#### Creating a New Validator

1. Create a new file in `schema_components/validators/` (e.g., `phone.py`):

```python
from schema_core.registry import validators

@validators.validator
def validate_brazilian_phone(cls, v):
    if not v.value.startswith("+55"):
        raise ValueError("Phone number must be Brazilian (+55)")
    return v
```

2. Use it in your YAML:

```yaml
User:
  fields:
    phone:
      type: Phone
      validators:
        - validate_brazilian_phone
```

#### Creating a New Serializer

1. Create a new file in `schema_components/serializers/` (e.g., `phone.py`):

```python
from schema_components.types.phone import Phone
from schema_core.registry import serializers

@serializers.serializer
def format_phone(value: Phone) -> str:
    # Format phone number as (XX) XXXXX-XXXX
    cleaned = value.value.replace("+", "").replace("-", "").replace(" ", "")
    return f"({cleaned[:2]}) {cleaned[2:7]}-{cleaned[7:]}"
```

2. Use it in your YAML:

```yaml
User:
  fields:
    phone:
      type: Phone
      serializers:
        - format_phone
```

#### Component Auto-importing

All components are automatically imported when the application starts. The system looks for Python files in:

- `schema_components/types/`
- `schema_components/validators/`
- `schema_components/serializers/`

Each file should:
1. Define your component (type, validator, or serializer)
2. Register it with the appropriate registry
3. Export any necessary types or functions

Example of a complete component file:

```python
# schema_components/types/cpf.py
from pydantic import GetCoreSchemaHandler
from pydantic_core import core_schema
from schema_core.registry import types

class CPF:
    def __init__(self, value: str):
        self.value = value

    def __str__(self):
        return self.value

    @staticmethod
    def _validate(v):
        if isinstance(v, CPF):
            return v
        if isinstance(v, str):
            # Add CPF validation logic
            if not v.replace(".", "").replace("-", "").isdigit():
                raise ValueError("Invalid CPF format")
            return CPF(v)
        raise ValueError("CPF must be a string")

    @staticmethod
    def _serialize(instance: "CPF") -> str:
        return instance.value

    @classmethod
    def __get_pydantic_core_schema__(
        cls, _source_type, _handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        return core_schema.no_info_plain_validator_function(
            cls._validate,
            serialization=core_schema.plain_serializer_function_ser_schema(
                cls._serialize,
                return_schema=core_schema.str_schema(),
            ),
        )

# Register the type
types.register("CPF", CPF)
```

---

## 🧪 Example Usage

```python
# Create a user
user = User(
    name="Alice",
    age=30,
    email="alice@example.com",
    birthday="1993-04-01T00:00:00",
    balance={"amount": 100},
    start_date="04/2025",
)

# Access fields
print(user.name)  # Alice
print(user.balance)  # R$ 1,00
print(user.start_date)  # 04/2025

# Serialize to dict/JSON
print(user.model_dump())  # Python dict
print(user.model_dump_json())  # JSON string (with custom serializers)

# Validation
try:
    User(name="Alice", age=-1)  # Raises ValueError: Must be positive
except ValueError as e:
    print(e)

try:
    User(name="Alice", email="bob@example.com")  # Raises ValueError: Email must contain user's name
except ValueError as e:
    print(e)
```

---

## ✅ Supported YAML Field Options

Each field can include:

| Key                                         | Description                                                       |
| ------------------------------------------- | ----------------------------------------------------------------- |
| `type`                                      | Type name (built-in or custom)                                    |
| `default`                                   | Optional default value                                            |
| `validators`                                | List of validator function names                                  |
| `serializers`                               | List of serializer function names (for JSON output customization) |
| `max_length`                                | Maximum length for strings                                        |
| `min_length`                                | Minimum length for strings                                        |
| `ge`                                        | Greater than or equal to (for numbers)                            |
| `le`                                        | Less than or equal to (for numbers)                               |
| `pattern`                                   | Regular expression pattern for strings                            |
| ...and all other Pydantic field constraints |

---

## 🧪 Testing

Run the test app:

```bash
python main.py
```

You'll see pretty-printed model outputs.

---

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/yaml2pydantic.git
cd yaml2pydantic
```

2. Create and activate a virtual environment:
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
uv pip install -e .[dev]
```

## 📦 Adding New Dependencies

To add new dependencies:

1. Add them to `pyproject.toml` under the appropriate section:
   - For runtime dependencies: Add to `[project].dependencies`
   - For development dependencies: Add to `[project.optional-dependencies].dev`

2. Install the updated dependencies:
```bash
source .venv/bin/activate && uv pip install -e .[dev]
```

---

## 🧱 Future Improvements

- CLI to validate YAML schemas
- Auto-generate OpenAPI / JSON Schema
- Format coercion (e.g., `"R$ 12,34"` → `Money`)
- Schema linter
- More built-in types (Phone, CPF, etc.)
- Schema versioning
- Schema inheritance

---

## 👥 Contributing

Your devs can contribute:

- New types in `schema_components/types/`
- New reusable validators in `schema_components/validators/`
- Custom serializers in `schema_components/serializers/`

No need to modify `schema_core/` directly.

---

## 🔐 License

MIT

---

## 🙌 Special Thanks

Inspired by the declarative power of OpenAPI and the performance of Pydantic.

## 🧪 Development Setup

This project uses modern Python development tools from the Astral.sh ecosystem for a fast and efficient development experience.

### Prerequisites

- Python 3.8 or higher
- Git
- Make (for using Makefile commands)

### Development Tools

We use the following tools from Astral.sh:
- [Uv](https://github.com/astral-sh/uv) - Fast Python package installer
- [Ruff](https://github.com/astral-sh/ruff) - Fast Python linter and formatter
- [Hatch](https://hatch.pypa.io/) - Modern Python project management

### Quick Start

The project includes a Makefile to simplify common development tasks. Here's how to use it:

1. Show available commands:
```bash
make help
```

2. Set up the development environment:
```bash
make setup
```

3. Activate the virtual environment:
```bash
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### Common Development Tasks

The Makefile provides several useful commands:

| Command       | Description                                                                           |
| ------------- | ------------------------------------------------------------------------------------- |
| `make setup`  | Set up the development environment (installs Uv, creates venv, installs dependencies) |
| `make lint`   | Run the linter (Ruff)                                                                 |
| `make format` | Format the code (Ruff)                                                                |
| `make build`  | Build the project (Hatch)                                                             |
| `make test`   | Run tests                                                                             |
| `make clean`  | Clean up build artifacts                                                              |
| `make dev`    | Start the development server                                                          |
| `make all`    | Run all checks and build (setup, lint, format, build, test)                           |

### VS Code Integration

The project includes VS Code settings for a seamless development experience. Make sure you have the following VS Code extensions installed:
- Python
- Ruff

The configuration enables:
- Format on save
- Auto-fix on save
- Ruff-based linting and formatting

### Project Structure

The project follows a clean, modular structure:
```
yaml2pydantic/
├── main.py                        # Entry point to load + test models
├── models/                        # YAML/JSON model definitions
├── schema_components/            # Shared reusable logic
└── schema_core/                  # Core schema engine
```

### Adding Dependencies

To add new dependencies:

1. Add them to `pyproject.toml` under the appropriate section:
   - For runtime dependencies: Add to `[project].dependencies`
   - For development dependencies: Add to `[project.optional-dependencies].dev`

2. Install the updated dependencies:
```bash
source .venv/bin/activate && uv pip install -e .[dev]
```

### Git Workflow

The project uses Git for version control. Make sure to:
- Create feature branches for new work
- Keep commits focused and descriptive
- Run linting and formatting before committing (`make lint format`)
- Update documentation as needed