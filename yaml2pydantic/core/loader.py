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
from pydantic import BaseModel

from yaml2pydantic.core.factory import ModelFactory
from yaml2pydantic.core.serializers import serializer_registry
from yaml2pydantic.core.type_registry import types
from yaml2pydantic.core.validators import validator_registry


class SchemaLoader:
    """Loader for schema definitions from various file formats and data structures."""

    @staticmethod
    def load_all_dicts(source: str | dict[str, Any]) -> dict[str, Any]:
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
        source_dict: dict[str, Any] = {}
        if isinstance(source, dict):
            return source

        path = Path(source)
        if path.suffix in [".yaml", ".yml"]:
            with open(path) as f:
                source_dict = yaml.safe_load(f)
                return source_dict
        elif path.suffix == ".json":
            with open(path) as f:
                source_dict = json.load(f)
                return source_dict
        else:
            raise ValueError(f"Unsupported file format: {source}")

    @staticmethod
    def load_all(source: str | dict[str, Any]) -> dict[str, type[BaseModel]]:
        """Load a schema definition from a file or dictionary.

        Args:
        ----
            source: Either a file path (str) or a dictionary containing the schema
            name: The name of the schema to load

        Returns:
        -------
            A Pydantic model

        Raises:
        ------
            ValueError: If the file format is not supported

        """
        schemas: dict[str, Any] = SchemaLoader.load_all_dicts(source)
        factory = ModelFactory(types, validator_registry, serializer_registry)
        return factory.build_all(schemas)

    @staticmethod
    def load(source: str | dict[str, Any], name: str) -> type[BaseModel]:
        """Load all schema definitions from a file or dictionary.

        Args:
        ----
            source: Either a file path (str) or a dictionary containing the schema
            name: The name of the schema to load

        Returns:
        -------
            A Pydantic model

        Raises:
        ------
            ValueError: If the file format is not supported

        """
        models: dict[str, type[BaseModel]] = SchemaLoader.load_all(source)
        return models[name]
