
from typing import Callable
from typing import Dict
from typing import Type
from types import ModuleType


class PbSerializerRegistrationError(Exception):
    """Custom exception for errors in Protocol Buffer serializer registration."""
    pass


__SERIALIZERS: Dict[Type, Callable] = {}
__DESERIALIZERS: Dict[str, Callable] = {}


def pb_serializer(obj_type: Type):
    """Decorator which registers a serializer for ``obj_type`` to its protobuf."""
    def wrapper(func):
        print(f"Registering serializer for {obj_type.__name__}")
        __SERIALIZERS[obj_type] = func
        return func
    return wrapper


def pb_deserializer(pb_module: ModuleType):
    """Decorator which registers a deserializer for the protobuf module."""
    def wrapper(func):
        print(f"Registering deserializer for {pb_module}")
        try:
            __DESERIALIZERS[pb_module.DESCRIPTOR.name] = func
        except AttributeError:
            raise PbSerializerRegistrationError(f"Unable to register deserializer for {pb_module}. Sure it's a protobuf module?")
        return func
    return wrapper
