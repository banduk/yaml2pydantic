from typing import Callable, Dict


class SerializerRegistry:
    """Registry for managing field serializers.

    This class maintains a registry of custom serializers that can be
    used to customize field serialization in the generated models.
    """

    def __init__(self):
        """Initialize an empty serializer registry."""
        self.serializers: Dict[str, Callable] = {}

    def serializer(self, func: Callable):
        """Register a serializer function.

        Args:
        ----
            func: The serializer function to register

        Returns:
        -------
            The original function (for use as a decorator)

        """
        self.serializers[func.__name__] = func
        return func

    def get(self, name: str):
        """Get a serializer by name.

        Args:
        ----
            name: Name of the serializer to retrieve

        Returns:
        -------
            The serializer function

        Raises:
        ------
            KeyError: If the serializer is not found

        """
        return self.serializers[name]


serializer_registry = SerializerRegistry()
