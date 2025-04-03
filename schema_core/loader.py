import json
from pathlib import Path
from typing import Any, Dict, Union

import yaml


class SchemaLoader:
    @staticmethod
    def load(source: Union[str, Dict[str, Any]]) -> Dict[str, Any]:
        if isinstance(source, dict):
            return source

        path = Path(source)
        if path.suffix in [".yaml", ".yml"]:
            with open(path, "r") as f:
                return yaml.safe_load(f)
        elif path.suffix == ".json":
            with open(path, "r") as f:
                return json.load(f)
        else:
            raise ValueError(f"Unsupported file format: {source}")
