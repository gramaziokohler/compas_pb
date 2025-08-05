from typing import Any

import compas
from compas.plugins import pluggable
from google.protobuf.json_format import MessageToJson
from google.protobuf.json_format import Parse

from compas_pb.generated import message_pb2

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
    int: message_pb2.DataType.INT,
    float: message_pb2.DataType.FLOAT,
    bool: message_pb2.DataType.BOOL,
    str: message_pb2.DataType.STR,
    bytes: message_pb2.DataType.BYTES
}

PY_TYPES_DESERIALIZER = {key.__name__.lower(): value for key, value in PY_TYPES_SERIALIZER.items()}


def primitive_to_pb(obj: int | float | bool | str | bytes) -> message_pb2.PrimitiveData:
    """
    Convert a python native type to a protobuf message.

    Parameters
    ----------
    obj : :class: `int`, `float`, `bool`, `str`, `bytes`
        The python native type to convert.

    Returns
    -------
    :class: `compas_pb.generated.message_pb2.AnyData`
        The protobuf message type of AnyData.
    """
    if obj is None:
        obj = "None"  # HACK: find proper way to handle None

    data_offset = message_pb2.PrimitiveData()

    type_ = type(obj)
    if type_ is int:
        data_offset.int = obj
    elif type_ is float:
        data_offset.float = obj
    elif type_ is bool:
        data_offset.bool = obj
    elif type_ is str:
        data_offset.str = obj
    elif type_ is bytes:
        data_offset.bytes = obj
    else:
        raise TypeError(f"Unsupported type: {type_}")

    return data_offset


def primitive_from_pb(primitive: message_pb2.PrimitiveData) -> int | float | bool | str | bytes:
    """Convert a protobuf message to a python native type.

    Parameters
    ----------
    proto_data : :class: `compas_pb.generated.message_pb2.PrimitiveData`
        The protobuf message type of PrimitiveData.

    Returns
    -------
    data_offset : int | float | bool | str | bytes
        The converted python native type.
    """
    type_ = primitive.WhichOneof("data")
    if type_ == "int":
        data_offset = primitive.int
    elif type_ == "float":
        data_offset = primitive.float
    elif type_ == "bool":
        data_offset = primitive.bool
    elif type_ == "str":
        data_offset = primitive.str
    elif type_ == "bytes":
        data_offset = primitive.bytes
    else:
        raise ValueError(f"Unsupported primitive type: {type_}")

    return data_offset


def any_to_pb(obj: compas.data.Data | int | float | bool | str | bytes, fallback_serializer=None) -> message_pb2.AnyData:
    """Convert any object to a protobuf any message.

    Parameters
    ----------
    obj : compas.data.Data | list | dict | int | float | bool | str
        The object to convert. Can be a COMPAS Data object, list, dict, or primitive type.

    Returns
    -------
        :class: `compas_pb.generated.message_pb2.AnyData`
            The protobuf message type of AnyData.
    """
    _discover_serializers()
    proto_data = message_pb2.AnyData()

    if obj is None:
        obj = "None"  # HACK: find proper way to handle None

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
            primitive = primitive_to_pb(obj)
            proto_data.data.Pack(primitive)
        return proto_data
    except TypeError as e:
        raise TypeError(f"Unsupported type: {type(obj)}: {e}")


def any_from_pb(proto_data: message_pb2.AnyData) -> compas.data.Data | int | float | bool | str | bytes:
    """Convert a protobuf message to a supported object.

    Parameters
    ----------
    proto_data : :class: `compas_pb.generated.message_pb2.AnyData`
        The protobuf message type of AnyData.

    Returns
    -------
    compas.data.Data | list | dict | int | float | bool | str
        The converted object. Can be a COMPAS Data object, list, dict, or primitive type.
    """
    _discover_serializers()

    # type.googleapis.com/<fully.qualified.message.name>
    proto_type = proto_data.data.type_url.split("/")[-1]

    if proto_type == message_pb2.PrimitiveData.DESCRIPTOR.full_name:
        primitive_data = message_pb2.PrimitiveData()
        is_unpacked = proto_data.data.Unpack(primitive_data)
        if not is_unpacked:
            raise TypeError(f"Unsupported proto type: {proto_type}")

        return primitive_from_pb(primitive_data)

    deserializer = SerialzerRegistry.get_deserializer(proto_type)
    if not deserializer:
        raise TypeError(f"Unsupported proto type: {proto_type}")

    unpacked_instance = deserializer.__deserializer_type__()
    _ = proto_data.data.Unpack(unpacked_instance)
    return  deserializer(unpacked_instance)


def serialize_message(data) -> message_pb2.MessageData:
    """Serialize a top-level protobuf message.

    Parameters:
    ----------
    data : object
        The data to be serialized. This can be a COMPAS object, a list of objects, or a dictionary.

    Returns:
    -------
    message : message_pb2.MessageData

    """
    if not data:
        raise ValueError("No message data to convert.")

    message_data = _serializer_any(data)
    message = message_pb2.MessageData(data=message_data)
    return message


def serialize_message_bts(data) -> bytes:
    """Serialize a top-level protobuf message.

    Parameters:
    ----------
    data : object
        The data to be serialized. This can be a COMPAS object, a list of objects, or a dictionary.

    Returns:
    -------
    message : bytes
        The serialized protobuf message as bytes.

    """
    message = serialize_message(data)
    message_bts = message.SerializeToString()
    return message_bts


def serialize_message_to_json(data) -> dict:
    """Serialize a top-level protobuf message.

    Parameters:
    ----------
    data : object
        The data to be serialized. This can be a COMPAS object, a list of objects, or a dictionary.

    Returns:
    -------
    message : dict
        The serialized protobuf message as a dictionary.

    """
    message = serialize_message(data)
    message_json = MessageToJson(message)
    return message_json


def _serializer_any(obj) -> message_pb2.AnyData:
    """Serialize a COMPAS object to protobuf message."""
    any_data = message_pb2.AnyData()

    if isinstance(obj, (list, tuple)):
        data_offset = _serialize_list(obj)
        any_data.data.Pack(data_offset)
    elif isinstance(obj, dict):
        data_offset = _serialize_dict(obj)
        any_data.data.Pack(data_offset)
    else:
        # check if it is COMPAS object or Python native type or fallback to dictionary.
        any_data = any_to_pb(obj, fallback_serializer=_serialize_dict)
    return any_data


def _serialize_list(data_list) -> message_pb2.ListData:
    """Serialize a Python list containing mixed data type."""
    list_data = message_pb2.ListData()
    for item in data_list:
        data_offset = _serializer_any(item)
        list_data.data.append(data_offset)
    return list_data


def _serialize_dict(data_dict) -> message_pb2.DictData:
    """Serialize a Python dictionary containing mixed data types."""
    dict_data = message_pb2.DictData()
    for key, value in data_dict.items():
        data_offset = _serializer_any(value)
        dict_data.data[key].CopyFrom(data_offset)
    return dict_data


def deserialize_message(binary_data) -> list | dict:
    """Deserialize a top-level protobuf message.

    Parameters:
    ----------
    binary_data : bytes
        The binary data to be deserialized.

    Returns:
    -------
    message : list | dict
        The deserialized protobuf message.

    """
    message_data = deserialize_message_bts(binary_data)
    return _deserialize_any(message_data)


def deserialize_message_bts(binary_data) -> message_pb2.MessageData:
    """Deserialize a binary data into bytes string.

    Parameters:
    ----------
    binary_data : bytes
        The binary data to be deserialized.

    Returns:
    -------
    message_data : message_pb2.MessageData
        The protobuf message data.

    """
    if not binary_data:
        raise ValueError("Binary data is empty.")

    any_data = message_pb2.MessageData()
    any_data.ParseFromString(binary_data)
    return any_data.data


def deserialize_message_from_json(json_data: str) -> dict:
    """Deserialize a top-level protobuf message into dictionary.

    Parameters:
    ----------
    json_data : str
        A JSON string representation of the data.

    Returns:
    -------
    message : dict
        The deserialized protobuf message as a dictionary.

    """
    if not json_data:
        raise ValueError("No message data to convert.")

    message = message_pb2.MessageData()
    json_message = Parse(json_data, message)

    any_data = message_pb2.MessageData()
    any_data.CopyFrom(json_message)

    return _deserialize_any(any_data.data)


def _deserialize_any(data: message_pb2.AnyData | message_pb2.ListData | message_pb2.DictData) -> list | dict:
    """Deserialize a protobuf message to COMPAS object."""
    if data.data.Is(message_pb2.ListData.DESCRIPTOR):
        data_offset = _deserialize_list(data)
    elif data.data.Is(message_pb2.DictData.DESCRIPTOR):
        data_offset = _deserialize_dict(data)
    else:
        data_offset = any_from_pb(data)
    return data_offset


def _deserialize_list(data_list: message_pb2.ListData) -> list:
    """Deserialize a protobuf ListData message to Python list."""
    data_offset = []
    list_data = message_pb2.ListData()
    data_list.data.Unpack(list_data)
    for item in list_data.data:
        data_offset.append(_deserialize_any(item))
    return data_offset


def _deserialize_dict(data_dict: message_pb2.AnyData) -> dict:
    """Deserialize a protobuf DictData message to Python dictionary."""
    data_offset = {}
    dict_data = message_pb2.DictData()
    data_dict.data.Unpack(dict_data)
    for key, value in dict_data.data.items():
        data_offset[key] = _deserialize_any(value)
    return data_offset
