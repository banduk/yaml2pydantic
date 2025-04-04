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

📚 [View the full documentation](https://banduk.github.io/yaml2pydantic/)

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
| 🔄 Auto-importing              | Components are automatically imported from components directory             |
| 🏗️ Built-in Types              | Support for common types like Money, MonthYear, and all Pydantic primitives |

---

## 🛠️ Installation

```bash
# Clone the repository
git clone https://github.com/banduk/yaml2pydantic.git
cd yaml2pydantic

# Set up the development environment
make setup

# Activate the virtual environment
source .venv/bin/activate
```

---

## 🧭 Project Structure

```
yaml2pydantic/
├── main.py                       # Entry point to load + test models
├── models/                       # YAML/JSON model definitions
│   └── user.yaml
├── components/                   # Shared reusable logic
│   ├── serializers/              # Custom serialization functions
│   │   └── money.py              # Money-specific serializers
│   ├── types/                    # Custom types (Money, MonthYear)
│   │   ├── money.py              # Money type implementation
│   │   └── monthyear.py          # MonthYear type implementation
│   └── validators/               # Custom validation logic
│       ├── email.py              # Email-related validators
│       └── numeric.py            # Numeric validators
└── core/                         # Core schema engine
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

Address:
  fields:
    street:
      type: str
    city:
      type: str
    zip:
      type: str
      pattern: "^[0-9]{5}(-[0-9]{4})?$"
```

### 2. 🏗️ Compile to Pydantic

```python
from yaml2pydantic import ModelFactory

# Load and compile the model
factory = ModelFactory()
User = factory.create_model("User", "models/user.yaml")

# Use it like any Pydantic model
user = User(
    name="John Doe",
    age=30,
    email="john@example.com",
    birthday="1990-01-01",
    address={
        "street": "123 Main St",
        "city": "Anytown",
        "zip": "12345"
    },
    balance=1000,
    start_date="03/2025"
)
```

---

## 🧪 Testing

```bash
# Run all tests
make test

# Run tests with coverage
python -m pytest --cov=yaml2pydantic
```

---

## 📚 Documentation

```bash
# Build the documentation
make docs

# View the documentation
make docs-serve
```

---

## 🧹 Code Quality

```bash
# Run the linter
make lint

# Format the code
make format

# Run type checking
python -m mypy .
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run the tests and checks:
   ```bash
   make all
   ```
5. Submit a pull request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🧪 Development Setup

This project uses modern Python development tools for a fast and efficient development experience.

### Project Structure

```
yaml2pydantic/
├── main.py                        # Entry point to load + test models
├── models/                        # YAML/JSON model definitions
│   └── user.yaml
├── components/            # Shared reusable logic
│   ├── serializers/              # Custom serialization functions
│   │   └── money.py             # Money-specific serializers
│   ├── types/                    # Custom types (Money, MonthYear)
│   │   ├── money.py             # Money type implementation
│   │   └── monthyear.py         # MonthYear type implementation
│   └── validators/               # Custom validation logic
│       ├── email.py             # Email-related validators
│       └── numeric.py           # Numeric validators
└── score/                  # Core schema engine
    ├── factory.py                # ModelFactory that builds Pydantic models
    ├── loader.py                 # Loads YAML, JSON, or dict input
    ├── registry.py               # Shared registries for types, validators, serializers
    ├── types.py                  # TypeRegistry
    ├── validators.py             # ValidatorRegistry
    └── serializers.py            # SerializerRegistry
```

### Common Commands

```bash
# Set up the environment
make setup

# Run tests
make test

# Run linters
make lint

# Format code
make format

# Type check
python -m mypy .
```