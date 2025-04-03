"""Loader for schema definitions from various sources.

This module provides functionality to load schema definitions from:
- YAML files
- JSON files
- Python dictionaries
"""

import json
from pathlib import Path
from typing import Any

import yaml


class SchemaLoader:
    """Loader for schema definitions from various file formats and data structures."""

    @staticmethod
    def load(source: str | dict[str, Any]) -> dict[str, Any]:
        """Load a schema definition from a file or dictionary.

        Args:
        ----
            source: Either a file path (str) or a dictionary containing the schema

        Returns:
        -------
            Dictionary containing the schema definition

        Raises:
        ------
            ValueError: If the file format is not supported

        """
        if isinstance(source, dict):
            return source

        path = Path(source)
        if path.suffix in [".yaml", ".yml"]:
            with open(path) as f:
                return yaml.safe_load(f)
        elif path.suffix == ".json":
            with open(path) as f:
                return json.load(f)
        else:
            raise ValueError(f"Unsupported file format: {source}")
