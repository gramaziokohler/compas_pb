from typing import Any

from compas.plugins import pluggable

from compas_pb.generated import message_pb2 as MessageData

from .registry import SerialzerRegistry


@pluggable(category="factories", selector="collect_all")
def register_serializers() -> None:
    """Collects all the plugins which register custom serializers with _ProtoBufferAny."""
    pass


_DISCOVERY_DONE = False


def _discover_serializers() -> None:
    global _DISCOVERY_DONE
    if _DISCOVERY_DONE:
        return

    register_serializers()
    _DISCOVERY_DONE = True


PY_TYPES_SERIALIZER = {
    int: MessageData.DataType.INT,
    float: MessageData.DataType.FLOAT,
    bool: MessageData.DataType.BOOL,
    str: MessageData.DataType.STR,
}

PY_TYPES_DESERIALIZER = {key.__name__.lower(): value for key, value in PY_TYPES_SERIALIZER.items()}


def primitive_to_pb(obj: Any) -> MessageData.AnyData:
    """
    Convert a python native type to a protobuf message.

    Parameters:
    ----------
        obj : :class: `int`, `float`, `bool`, `str`
            The python native type to convert.

    Returns:
        :class: `compas_pb.data.proto.message_pb2.AnyData`
            The protobuf message type of AnyData.
    """
    if obj is None:
        obj = "None"  # HACK: find proper way to handle None
        # raise ValueError("No object provided for conversion.")

    proto_data = MessageData.AnyData()

    try:
        type_obj = PY_TYPES_SERIALIZER.get(type(obj))
        field_name = MessageData.DataType.Name(type_obj).lower()
        data_offset = MessageData.PrimitiveData()
        setattr(data_offset, field_name, obj)
        proto_data.data.Pack(data_offset)
        return proto_data

    except TypeError as e:
        raise TypeError(f"Unsupported type: {type(obj)}: {e}")


def primitive_from_pb(proto_data: MessageData.PrimitiveData) -> int | float | bool | str | bytes:
    """Convert a protobuf message to a python native type.

    Parameters
    -----------
        proto_data : :class: `compas_pb.data.proto.message_pb2.PrimitiveData`
            The protobuf message type of PrimitiveData.

    Returns
    -------
        data_offset : python object
            The converted python native type.
    """
    primitive_data = MessageData.PrimitiveData()
    is_unpacked = proto_data.data.Unpack(primitive_data)
    if not is_unpacked:
        # TODO: this really shouldn't be reached. if we're here it means it's some type which is not a primitive and hasn't been registered
        raise ValueError(f"Unknown data type: {proto_data.data.type_url}")
    type_ = primitive_data.WhichOneof("data")
    if type_ == "int":
        data_offset = primitive_data.int
    elif type_ == "float":
        data_offset = primitive_data.float
    elif type_ == "bool":
        data_offset = primitive_data.bool
    elif type_ == "str":
        data_offset = primitive_data.str
    else:
        raise ValueError(f"Unsupported primitive type: {type_}")

    return data_offset


def any_to_pb(obj: Any, fallback_serializer=None) -> MessageData.AnyData:
    """Convert any object to a protobuf any message.

    Parameters
    ----------
        obj : :class:   `compas.geometry.Point`,
                        `compas.geometry.Vector`,
                        `compas.geometry.Line`,
                        `compas.geometry.Frame`
            If the object is not one of the above, and it has the attribute from the listed above,
            it will be converted to the corresponding object type and as `data`.

    Returns
    -------
        :class: `compas_pb.data.proto.message_pb2.AnyData`
            The protobuf message type of AnyData.
    """
    _discover_serializers()
    proto_data = MessageData.AnyData()

    if obj is None:
        obj = "None"  # HACK: find proper way to handle None
        # raise ValueError("No object provided for conversion.")

    try:
        serializer = SerialzerRegistry.get_serializer(obj)
        if serializer:
            pb_obj = serializer(obj)
            proto_data.data.Pack(pb_obj)
        elif hasattr(obj, "__jsondump__"):
            obj_dict = {obj.__class__.__name__: obj.__jsondump__()}
            data_offset = fallback_serializer(obj_dict)
            proto_data.data.Pack(data_offset)
        else:
            proto_data = primitive_to_pb(obj)
        return proto_data
    except TypeError as e:
        raise TypeError(f"Unsupported type: {type(obj)}: {e}")


def any_from_pb(proto_data: MessageData.AnyData) -> list | dict | object:
    """Convert a protobuf message to a supported COMPAS object.

    Parameters
    -----------
        proto_data : :class: `compas_pb.data.proto.message_pb2.AnyData`
            The protobuf message type of AnyData.

    Returns
    ----------
        data_offset : python object
    """
    _discover_serializers()

    # type.googleapis.com/<fully.qualified.message.name>
    proto_type = proto_data.data.type_url.split("/")[-1]
    try:
        deserializer = SerialzerRegistry.get_deserializer(proto_type)
        if deserializer:
            unpacked_instance = deserializer.__deserializer_type__()
            _ = proto_data.data.Unpack(unpacked_instance)
            data_offset = deserializer(unpacked_instance)
        else:
            data_offset = primitive_from_pb(proto_data)
        return data_offset
    except TypeError as e:
        raise TypeError(f"Unsupported type: {proto_type}: {e}")
