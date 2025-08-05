from google.protobuf.json_format import MessageToJson
from google.protobuf.json_format import Parse

from compas_pb.core import any_from_pb
from compas_pb.core import any_to_pb
from compas_pb.generated import message_pb2


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
