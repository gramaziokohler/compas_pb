from google.protobuf.json_format import MessageToJson
from google.protobuf.json_format import Parse

from compas_pb.data.data import _ProtoBufferAny
from compas_pb.generated import message_pb2 as MessageData


class DataSerializer:
    """Data Encoder for COMPAS objects to protobuf messages.

    Parameters:
    ----------
    data : object
        The data to be serialized. This can be a COMPAS object, a list of objects, or a dictionary.

    """

    def __init__(self, data=None):
        super().__init__()
        self._data = data

    def serialize_message(self) -> MessageData.MessageData:
        """Serialize a top-level protobuf message.

        Parameters:
        ----------
        data : object

        Returns:
        -------
        message : MessageData.MessageData

        """
        if not self._data:
            raise ValueError("No message data to convert.")

        message_data = self._serializer_any(self._data)
        message = MessageData.MessageData(data=message_data)
        return message

    def serialize_message_bts(self) -> bytes:
        """Serialize a top-level protobuf message.

        Returns:
        -------
        message : bytes
            The serialized protobuf message as bytes.

        """
        message = self.serialize_message()
        message_bts = message.SerializeToString()
        return message_bts

    def serialize_message_to_json(self) -> dict:
        """Serialize a top-level protobuf message.

        Returns:
        -------
        message : dict
            The serialized protobuf message as a dictionary.

        """
        message = self.serialize_message()
        message_json = MessageToJson(message)
        return message_json

    def _serializer_any(self, obj) -> MessageData.AnyData:
        """ "Serialize a COMPAS object to protobuf message."""
        any_data = MessageData.AnyData()

        if isinstance(obj, list):
            data_offset = self._serialize_list(obj)
            any_data.data.Pack(data_offset)
        elif isinstance(obj, dict):
            data_offset = self._serialize_dict(obj)
            any_data.data.Pack(data_offset)
        else:
            # check if it is COMPAS object or Python native type or fallback to dictionary.
            any_data = _ProtoBufferAny(obj, fallback_serializer=self._serialize_dict).to_pb()
        return any_data

    def _serialize_list(self, data_list) -> MessageData.ListData:
        """Serialize a Python list containing mixed data type."""
        list_data = MessageData.ListData()
        for item in data_list:
            data_offset = self._serializer_any(item)
            list_data.data.append(data_offset)
        return list_data

    def _serialize_dict(self, data_dict) -> MessageData.DictData:
        """Serialize a Python dictionary containing mixed data types."""
        dict_data = MessageData.DictData()
        for key, value in data_dict.items():
            data_offset = self._serializer_any(value)
            dict_data.data[key].CopyFrom(data_offset)
        return dict_data


class DataDeserializer:
    """Data Decoder for protobuf messages to objects."""

    def __init__(self, data=None):
        super().__init__()
        self._data = data

    def deserialize_message(self) -> list | dict:
        """Deserialize a top-level protobuf message.

        Returns:
        -------
        message : MessageData.MessageData
            The deserialized protobuf message.

        """
        message_data = self.deserialize_message_bts()
        return self._deserialize_any(message_data)

    def deserialize_message_bts(self) -> MessageData.MessageData:
        """Deserialize a binary data into bytes string.

        Parameters:
        ----------
        message_data : MessageData.MessageData
            The protobuf message data to be deserialized.
        Returns:
        -------

        """
        if not self._data:
            raise ValueError("Binary data is empty.")
        binary_data = self._data

        any_data = MessageData.MessageData()
        any_data.ParseFromString(binary_data)
        return any_data.data

    def deserialize_message_from_json(self) -> dict:
        """Deserialize a top-level protobuf message into dictionary.

        Returns:
        -------
        message :
            The serialized protobuf message as a json like string.

        """
        if not self._data:
            raise ValueError("No message data to convert.")

        json_format_data = self._data
        message = MessageData.MessageData()
        json_message = Parse(json_format_data, message)

        any_data = MessageData.MessageData()
        any_data.CopyFrom(json_message)

        return self._deserialize_any(any_data.data)

    def _deserialize_any(self, data: MessageData.AnyData | MessageData.ListData | MessageData.DictData) -> list | dict:
        """Deserialize a protobuf message to COMPAS object."""

        if data.data.Is(MessageData.ListData.DESCRIPTOR):
            data_offset = self._deserialize_list(data)
        elif data.data.Is(MessageData.DictData.DESCRIPTOR):
            data_offset = self._deserialize_dict(data)
        else:
            data_offset = _ProtoBufferAny.from_pb(data)
        return data_offset

    def _deserialize_list(self, data_list: MessageData.ListData) -> list:
        """Deserialize a protobuf ListData message to Python list."""
        data_offset = []
        list_data = MessageData.ListData()
        data_list.data.Unpack(list_data)
        for item in list_data.data:
            data_offset.append(self._deserialize_any(item))
        return data_offset

    def _deserialize_dict(self, data_dict: MessageData.AnyData) -> dict:
        """Deserialize a protobuf DictData message to Python dictionary."""
        data_offset = {}
        dict_data = MessageData.DictData()
        data_dict.data.Unpack(dict_data)
        for key, value in dict_data.data.items():
            data_offset[key] = self._deserialize_any(value)
        return data_offset
