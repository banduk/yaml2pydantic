from typing import Callable, Dict


class ValidatorRegistry:
    """Registry for managing field and model validators.

    This class maintains a registry of custom validators that can be
    used to validate fields and models in the generated models.
    """

    def __init__(self):
        """Initialize an empty validator registry."""
        self.validators: Dict[str, Callable] = {}

    def validator(self, func: Callable):
        """Register a validator function.

        Args:
        ----
            func: The validator function to register

        Returns:
        -------
            The original function (for use as a decorator)

        """
        self.validators[func.__name__] = func
        return func

    def get(self, name: str):
        """Get a validator by name.

        Args:
        ----
            name: Name of the validator to retrieve

        Returns:
        -------
            The validator function

        Raises:
        ------
            KeyError: If the validator is not found

        """
        return self.validators[name]


validator_registry = ValidatorRegistry()
