import base64
from importlib.metadata import version
from typing import Any
from typing import Union
from warnings import warn

import compas
from compas.data import Data
from compas.data import DataDecoder
from google.protobuf.json_format import MessageToJson
from google.protobuf.json_format import Parse

from compas_pb.generated import geometry_pb2

from .registry import SerializerRegistry

_CURRENT_VERSION: str = version("compas_pb")


def _ensure_serializers():
    from .plugin import PLUGIN_MANAGER

    PLUGIN_MANAGER.discover_plugins()


def _decode_dict(data_dict: dict) -> Data:
    return DataDecoder().object_hook(data_dict)


def primitive_to_pb(obj: Union[int, float, bool, str, bytes]) -> geometry_pb2.AnyData:
    """
    Convert a python native type to a protobuf message.

    Parameters
    ----------
    obj : :class: `int`, `float`, `bool`, `str`, `bytes`
        The python native type to convert.

    Returns
    -------
    :class: `compas_pb.generated.geometry_pb2.AnyData`
        The protobuf message type of AnyData.
    """

    data_offset = geometry_pb2.AnyData()

    type_ = type(obj)
    if type_ is type(None):
        data_offset.value.null_value = 0  # this just needs to be set to any integer value to indicate null
    elif type_ is int:
        data_offset.value.number_value = float(obj)  # only float is supported in protobuf
    elif type_ is float:
        data_offset.value.number_value = obj
    elif type_ is bool:
        data_offset.value.bool_value = obj
    elif type_ is str:
        data_offset.value.string_value = obj
    elif type_ is bytes:
        data_offset.value.string_value = "base64:" + base64.b64encode(obj).decode("utf-8")  # Add base64: prefix
    else:
        raise TypeError(f"Unsupported type: {type_}")

    return data_offset


def primitive_from_pb(primitive: geometry_pb2.AnyData) -> Union[int, float, bool, str, bytes]:
    """Convert a protobuf message to a python native type.

    Parameters
    ----------
    proto_data : :class: `compas_pb.generated.geometry_pb2.AnyData`
        The protobuf message type of Anydata(contains struct_pb2.Value).

    Returns
    -------
    data_offset : Union[int, float, bool, str, bytes]
        The converted python native type.
    """
    type_ = primitive.value.WhichOneof("kind")
    if type_ == "null_value":
        data_offset = None
    elif type_ == "number_value":
        data_offset = primitive.value.number_value
        if data_offset.is_integer():
            data_offset = int(data_offset)
    elif type_ == "bool_value":
        data_offset = primitive.value.bool_value
    elif type_ == "string_value":
        data_offset = primitive.value.string_value
        if data_offset.startswith("base64:"):
            data_offset = base64.b64decode(data_offset[7:])
    else:
        raise ValueError(f"Unsupported primitive type: {type_}")

    return data_offset


def any_to_pb(obj: Union[compas.data.Data, int, float, bool, str, bytes]) -> geometry_pb2.AnyData:
    """Convert any object to a protobuf any message.

    Parameters
    ----------
    obj : Union[compas.data.Data, list, dict, int, float, bool, str]
        The object to convert. Can be a COMPAS Data object, list, dict, or primitive type.

    Returns
    -------
        :class: `compas_pb.generated.geometry_pb2.AnyData`
            The protobuf message type of AnyData.
    """
    _ensure_serializers()
    proto_data = geometry_pb2.AnyData()

    try:
        serializer = SerializerRegistry.get_serializer(obj)
        if serializer:
            pb_obj = serializer(obj)
            proto_data.message.Pack(pb_obj)
        elif isinstance(obj, Data):
            proto_data = _serialize_fallback(obj)
        else:
            proto_data = primitive_to_pb(obj)
        return proto_data
    except TypeError as e:
        raise TypeError(f"Unsupported type: {type(obj)}: {e}")


def any_from_pb(proto_data: geometry_pb2.AnyData) -> Union[compas.data.Data, int, float, bool, str, bytes]:
    """Convert a protobuf message to a supported object.

    Parameters
    ----------
    proto_data : :class: `compas_pb.generated.geometry_pb2.AnyData`
        The protobuf message type of AnyData.

    Returns
    -------
    Union[compas.data.Data, list, dict, int, float, bool, str]
        The converted object. Can be a COMPAS Data object, list, dict, or primitive type.
    """
    _ensure_serializers()

    union_field = proto_data.WhichOneof("data")
    if union_field == "value":
        return primitive_from_pb(proto_data)
    elif union_field == "fallback":
        return _deserialize_fallback(proto_data)
    elif union_field == "message":
        return _handle_known_type(proto_data)
    else:
        raise NameError(f"Unexpected AnyData field: {union_field}")


def _handle_known_type(proto_data: geometry_pb2.AnyData) -> Any:
    # type.googleapis.com/<fully.qualified.message.name>
    proto_type = proto_data.message.type_url.split("/")[-1]

    deserializer = SerializerRegistry.get_deserializer(proto_type)
    if not deserializer:
        raise TypeError(f"Unsupported proto type: {proto_type}")

    unpacked_instance = deserializer.__protobuf_cls__()
    _ = proto_data.message.Unpack(unpacked_instance)
    return deserializer(unpacked_instance)


def serialize_message(data) -> geometry_pb2.MessageData:
    """Serialize a top-level protobuf message.

    Parameters
    ----------
    data : object
        The data to be serialized. This can be a COMPAS object, a list of objects, or a dictionary.

    Returns
    -------
    message : geometry_pb2.MessageData

    """
    if not data:
        raise ValueError("No message data to convert.")

    message_data = _serializer_any(data)
    message = geometry_pb2.MessageData(data=message_data, version=_CURRENT_VERSION)
    return message


def serialize_message_bts(data) -> bytes:
    """Serialize a top-level protobuf message.

    Parameters
    ----------
    data : object
        The data to be serialized. This can be a COMPAS object, a list of objects, or a dictionary.

    Returns
    -------
    message : bytes
        The serialized protobuf message as bytes.

    """
    message = serialize_message(data)
    message_bts = message.SerializeToString()
    return message_bts


def serialize_message_to_json(data) -> dict:
    """Serialize a top-level protobuf message.

    Parameters
    ----------
    data : object
        The data to be serialized. This can be a COMPAS object, a list of objects, or a dictionary.

    Returns
    -------
    message : dict
        The serialized protobuf message as a dictionary.

    """
    message = serialize_message(data)
    message_json = MessageToJson(message)
    return message_json


def _serializer_any(obj) -> geometry_pb2.AnyData:
    """Serialize a COMPAS object to protobuf message."""
    any_data = geometry_pb2.AnyData()

    if isinstance(obj, (list, tuple)):
        data_offset = _serialize_list(obj)
        any_data.message.Pack(data_offset)
    elif isinstance(obj, dict):
        data_offset = _serialize_dict(obj)
        any_data.message.Pack(data_offset)
    else:
        # check if it is COMPAS object or Python native type or fallback to dictionary.
        any_data = any_to_pb(obj)
    return any_data


def _serialize_list(data_list) -> geometry_pb2.ListData:
    """Serialize a Python list containing mixed data type."""
    list_data = geometry_pb2.ListData()
    for item in data_list:
        data_offset = _serializer_any(item)
        list_data.items.append(data_offset)
    return list_data


def _serialize_dict(data_dict) -> geometry_pb2.DictData:
    """Serialize a Python dictionary containing mixed data types."""
    dict_data = geometry_pb2.DictData()
    for key, value in data_dict.items():
        data_offset = _serializer_any(value)
        dict_data.items[key].CopyFrom(data_offset)
    return dict_data


def _serialize_fallback(obj: Data) -> geometry_pb2.AnyData:
    """Fallback serializer to convert a dictionary to protobuf DictData."""
    result = geometry_pb2.AnyData()
    fallback_data = geometry_pb2.FallbackData()
    dict_data: geometry_pb2.DictData = _serialize_dict(obj.__jsondump__())
    fallback_data.data.CopyFrom(dict_data)
    result.fallback.CopyFrom(fallback_data)
    return result


def deserialize_message(binary_data) -> Union[list, dict]:
    """Deserialize a top-level protobuf message.

    Parameters
    ----------
    binary_data : bytes
        The binary data to be deserialized.

    Returns
    -------
    message : Union[list, dict]
        The deserialized protobuf message.

    """
    message_data = deserialize_message_bts(binary_data)
    return _deserialize_any(message_data)


def deserialize_message_bts(binary_data) -> geometry_pb2.MessageData:
    """Deserialize a binary data into bytes string.

    Parameters
    ----------
    binary_data : bytes
        The binary data to be deserialized.

    Returns
    -------
    message_data : geometry_pb2.MessageData
        The protobuf message data.

    """
    if not binary_data:
        raise ValueError("Binary data is empty.")

    any_data = geometry_pb2.MessageData()
    any_data.ParseFromString(binary_data)

    if not _check_version_compatibility(any_data):
        warn(f"Current version {_CURRENT_VERSION} is not compatible with: {any_data.version}", UserWarning)

    return any_data.data


def deserialize_message_from_json(json_data: str) -> dict:
    """Deserialize a top-level protobuf message into dictionary.

    Parameters
    ----------
    json_data : str
        A JSON string representation of the data.

    Returns
    -------
    message : dict
        The deserialized protobuf message as a dictionary.

    """
    if not json_data:
        raise ValueError("No message data to convert.")

    message = geometry_pb2.MessageData()
    json_message = Parse(json_data, message)

    any_data = geometry_pb2.MessageData()
    any_data.CopyFrom(json_message)

    if not _check_version_compatibility(any_data):
        warn(f"Current version {_CURRENT_VERSION} is not compatible with: {any_data.version}", UserWarning)

    return _deserialize_any(any_data.data)


def _deserialize_any(data: Union[geometry_pb2.AnyData, geometry_pb2.ListData, geometry_pb2.DictData]) -> Union[list, dict]:
    """Deserialize a protobuf message to COMPAS object."""
    if data.message.Is(geometry_pb2.ListData.DESCRIPTOR):
        list_data = geometry_pb2.ListData()
        data.message.Unpack(list_data)
        data_offset = _deserialize_list(list_data)
    elif data.message.Is(geometry_pb2.DictData.DESCRIPTOR):
        dict_data = geometry_pb2.DictData()
        data.message.Unpack(dict_data)
        data_offset = _deserialize_dict(dict_data)
    else:
        data_offset = any_from_pb(data)
    return data_offset


def _deserialize_list(data_list: geometry_pb2.ListData) -> list:
    """Deserialize a protobuf ListData message to Python list."""
    data_offset = []
    for item in data_list.items:
        data_offset.append(_deserialize_any(item))
    return data_offset


def _deserialize_dict(data_dict: geometry_pb2.DictData) -> dict:
    """Deserialize a protobuf DictData message to Python dictionary."""
    data_offset = {}
    for key, value in data_dict.items.items():
        data_offset[key] = _deserialize_any(value)
    return data_offset


def _deserialize_fallback(data_dict: geometry_pb2.AnyData) -> Data:
    """Fallback deserializer to convert a protobuf FallbackData message to Python dictionary."""
    obj_data = _deserialize_dict(data_dict.fallback.data)
    return _decode_dict(obj_data)


def _check_version_compatibility(any_data: geometry_pb2.MessageData) -> bool:
    """Check if the message version is compatible with the current version."""
    # for accept empty version string
    # Not sure if this is a good idea
    if any_data.version is None or any_data.version == "":
        warn("No version info found in the message, it may cause deserialization issues.", UserWarning)
        return True
    if any_data.version != _CURRENT_VERSION:
        return False
    return True
