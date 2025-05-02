"""Tests for the schema loader module."""

import json
import tempfile
from pathlib import Path

import pytest
import yaml

from yaml2pydantic.core.loader import SchemaLoader


@pytest.fixture
def yaml_file():
    """Create a temporary YAML file with test data."""
    data = {
        "schema1": {"fields": {"value": {"type": "str"}}},
        "schema2": {"fields": {"value": {"type": "int"}}},
    }
    with tempfile.NamedTemporaryFile(suffix=".yaml", mode="w", delete=False) as f:
        yaml.dump(data, f)
        return Path(f.name)


@pytest.fixture
def json_file():
    """Create a temporary JSON file with test data."""
    data = {
        "schema1": {"fields": {"value": {"type": "str"}}},
        "schema2": {"fields": {"value": {"type": "int"}}},
    }
    with tempfile.NamedTemporaryFile(suffix=".json", mode="w", delete=False) as f:
        json.dump(data, f)
        return Path(f.name)


@pytest.fixture
def cleanup_files(yaml_file, json_file):
    """Clean up temporary files after tests."""
    yield
    yaml_file.unlink()
    json_file.unlink()


class TestSchemaLoader:
    """Tests for the SchemaLoader class."""

    def test_load_all_from_dict(self):
        """Test loading schema from a dictionary."""
        data = {"schema1": {"fields": {"value": {"type": "str"}}}}
        result = SchemaLoader.load_all(data)
        assert isinstance(result, dict)
        assert "schema1" in result
        assert hasattr(result["schema1"], "__annotations__")
        assert result["schema1"].__annotations__["value"] is str

    def test_load_all_from_yaml(self, yaml_file):
        """Test loading schema from a YAML file."""
        result = SchemaLoader.load_all(str(yaml_file))
        assert isinstance(result, dict)
        assert "schema1" in result
        assert "schema2" in result
        assert hasattr(result["schema1"], "__annotations__")
        assert hasattr(result["schema2"], "__annotations__")
        assert result["schema1"].__annotations__["value"] is str
        assert result["schema2"].__annotations__["value"] is int

    def test_load_all_from_json(self, json_file):
        """Test loading schema from a JSON file."""
        result = SchemaLoader.load_all(str(json_file))
        assert isinstance(result, dict)
        assert "schema1" in result
        assert "schema2" in result
        assert hasattr(result["schema1"], "__annotations__")
        assert hasattr(result["schema2"], "__annotations__")
        assert result["schema1"].__annotations__["value"] is str
        assert result["schema2"].__annotations__["value"] is int

    def test_load_all_invalid_file_format(self):
        """Test loading schema from an unsupported file format."""
        with pytest.raises(ValueError, match="Unsupported file format"):
            SchemaLoader.load_all("test.txt")

    def test_load_existing_schema(self, yaml_file):
        """Test loading a specific schema that exists."""
        result = SchemaLoader.load(str(yaml_file), "schema1")
        assert hasattr(result, "__annotations__")
        assert result.__annotations__["value"] is str

    def test_load_nonexistent_schema(self, yaml_file):
        """Test loading a specific schema that doesn't exist."""
        with pytest.raises(KeyError, match="'nonexistent'"):
            SchemaLoader.load(str(yaml_file), "nonexistent")

    def test_load_from_dict(self):
        """Test loading a specific schema from a dictionary."""
        data = {"schema1": {"fields": {"value": {"type": "str"}}}}
        result = SchemaLoader.load(data, "schema1")
        assert hasattr(result, "__annotations__")
        assert result.__annotations__["value"] is str
