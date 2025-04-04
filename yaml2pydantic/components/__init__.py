import importlib
from pathlib import Path

MODULES = ["validators", "types", "serializers"]

for module in MODULES:
    module_path = Path(__file__).parent / module
    for file in module_path.glob("*.py"):
        if file.stem != "__init__":
            importlib.import_module(f"yaml2pydantic.components.{module}.{file.stem}")
