import sys
from typing import Any
from typing import Callable
from typing import Dict
from typing import Type


class PbSerializerRegistrationError(Exception):
    """Custom exception for errors in Protocol Buffer serializer registration."""

    pass


_SERIALIZERS: Dict[Type, Callable] = {}
_DESERIALIZERS: Dict[str, Callable] = {}


def pb_serializer(obj_type: Type):
    """Decorator which registers a serializer for ``obj_type`` to its protobuf."""

    def wrapper(func):
        print(f"Registering serializer for {obj_type.__name__}")
        _SERIALIZERS[obj_type] = func
        return func

    return wrapper


def pb_deserializer(pb_type: Type):
    """Decorator which registers a deserializer for the protobuf module."""

    def wrapper(func):
        module = sys.modules[pb_type.__module__]
        type_url = f"{module.DESCRIPTOR.package}.{pb_type.DESCRIPTOR.name}"
        try:
            _DESERIALIZERS[type_url] = func
        except AttributeError:
            raise PbSerializerRegistrationError(f"Unable to register deserializer for {pb_type}. Sure it's a protobuf type?")
        else:
            # used for unpacking Any
            func.__deserializer_type__ = pb_type
        return func

    return wrapper


class SerialzerRegistry:
    @staticmethod
    def get_serializer(data: Any) -> Callable:
        result = None
        for cls in type(data).mro():
            result = _SERIALIZERS.get(cls)
            if result:
                break
        return result

    @staticmethod
    def get_deserializer(pb_typename) -> Callable:
        return _DESERIALIZERS.get(pb_typename)
