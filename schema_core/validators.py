from typing import Callable, Dict


class ValidatorRegistry:
    def __init__(self):
        self.validators: Dict[str, Callable] = {}

    def validator(self, func: Callable):
        self.validators[func.__name__] = func
        return func

    def get(self, name: str):
        return self.validators[name]


validator_registry = ValidatorRegistry()
