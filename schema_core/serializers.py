from typing import Callable, Dict


class SerializerRegistry:
    def __init__(self):
        self.serializers: Dict[str, Callable] = {}

    def serializer(self, func: Callable):
        self.serializers[func.__name__] = func
        return func

    def get(self, name: str):
        return self.serializers[name]


serializer_registry = SerializerRegistry()
