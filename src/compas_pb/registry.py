from typing import Any
from typing import Callable
from typing import Dict
from typing import Type


class PbSerializerRegistrationError(Exception):
    """Custom exception for errors in Protocol Buffer serializer registration."""

    pass


class SerializerRegistry:
    """Registry for managing protobuf serializers and deserializers."""

    _SERIALIZERS: Dict[Type, Callable] = {}
    _DESERIALIZERS: Dict[str, Callable] = {}

    @classmethod
    def get_serializer(cls, data: Any) -> Callable:
        result = None
        for obj_cls in type(data).mro():
            result = cls._SERIALIZERS.get(obj_cls)
            if result:
                break
        return result

    @classmethod
    def get_deserializer(cls, pb_typename: str) -> Callable:
        return cls._DESERIALIZERS.get(pb_typename)

    @classmethod
    def register_serializer(cls, obj_type: Type, func: Callable) -> None:
        """Register a serializer function for a given type."""
        cls._SERIALIZERS[obj_type] = func

    @classmethod
    def register_deserializer(cls, type_url: str, func: Callable) -> None:
        """Register a deserializer function for a given protobuf type URL."""
        cls._DESERIALIZERS[type_url] = func


def pb_serializer(obj_type: Type):
    """Decorator which registers a serializer for ``obj_type`` to its protobuf."""

    def wrapper(func):
        SerializerRegistry.register_serializer(obj_type, func)
        return func

    return wrapper


def pb_deserializer(pb_type: Type):
    """Decorator which registers a deserializer for the protobuf module."""

    def wrapper(func):
        type_url = pb_type.DESCRIPTOR.full_name
        try:
            SerializerRegistry.register_deserializer(type_url, func)
        except AttributeError:
            raise PbSerializerRegistrationError(f"Unable to register deserializer for {pb_type}. Sure it's a protobuf type?")
        else:
            # used for unpacking Any
            func.__deserializer_type__ = pb_type
        return func

    return wrapper
