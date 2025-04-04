# yaml2pydantic

A Python library for converting YAML files to Pydantic models.

```{include} ../README.md
```

```{toctree}
:maxdepth: 2
:caption: Contents

api/index
contributing
```

## Features

- Convert YAML files to Pydantic models
- Support for nested structures
- Type validation
- Easy to use API

## Quick Start

```python
from yaml2pydantic import Yaml2Pydantic

# Create a converter
converter = Yaml2Pydantic()

# Convert YAML to Pydantic model
model = converter.convert("config.yaml")
```

## Installation

```bash
pip install yaml2pydantic
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## API Documentation

The following sections contain the detailed API documentation:

```{toctree}
:maxdepth: 2
:caption: API Reference

api/core
api/components
``` 