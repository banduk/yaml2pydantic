# yaml2pydantic

A Python library for converting YAML files to Pydantic models.

```{toctree}
:maxdepth: 2
:caption: Contents

installation
usage
api
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