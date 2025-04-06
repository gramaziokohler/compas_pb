from compas.geometry import Frame, Line, Point, Vector
from compas_model.elements import Element

from compas_pb.data.data import ProtoBufferElement, ProtoBufferFrame, ProtoBufferLine, ProtoBufferPoint, ProtoBufferVector

# ProtoBufferList,
# ProtoBufferDict,
# ProtoBufferAny,
from compas_pb.data.proto import message_pb2 as AnyData

SERIALIZERS = {
    Point: ProtoBufferPoint,
    Vector: ProtoBufferVector,
    Line: ProtoBufferLine,
    Frame: ProtoBufferFrame,
    Element: ProtoBufferElement,
}


class DataSerializer:
    """Data Encoder for COMPAS objects to protobuf messages."""

    def __init__(self, *args, **kwargs):
        super(DataSerializer, self).__init__(*args, **kwargs)

    def serialize_message(self, data):
        """Serialize a top-level protobuf message."""
        message_data = self._serializer_any(data)
        message = AnyData.MessageData(data=message_data)
        # print(message)
        return message.SerializeToString()

    def _serializer_any(self, obj):
        """ "Serialize a COMPAS object to protobuf message."""

        any_data = AnyData.AnyData()

        if isinstance(obj, list):
            data_offset = self._serialize_list(obj)
            any_data.type = AnyData.DataType.LIST
            any_data.list.CopyFrom(data_offset)

        elif isinstance(obj, dict):
            data_offset = self._serialize_dict(obj)
            any_data.type = AnyData.DataType.DICT
            any_data.dict.CopyFrom(data_offset)

        else:
            serializer = SERIALIZERS.get(type(obj))

            if not serializer:
                raise TypeError(f"Unsupported type: {type(obj)}")

            buffer_obj = serializer().to_pb(obj)
            data_offset, type_enum = buffer_obj

            any_data.type = type_enum
            field_name = AnyData.DataType.Name(type_enum).lower()
            getattr(any_data, field_name).CopyFrom(data_offset)

        return any_data

    def _serialize_list(self, data_list):
        """Serialize a Python list containing mixed data type."""
        list_data = AnyData.ListData()
        for item in data_list:
            data_offset = self._serializer_any(item)
            list_data.data.append(data_offset)
        return list_data

    def _serialize_dict(self, data_dict):
        """Serialize a Python dictionary containing mixed data types."""
        dict_data = AnyData.DictData()
        for key, value in data_dict.items():
            data_offset = self._serializer_any(value)
            dict_data.data[key].CopyFrom(data_offset)
        return dict_data


DESERIALIZERS = {
    AnyData.DataType.POINT: ProtoBufferPoint,
    AnyData.DataType.VECTOR: ProtoBufferVector,
    AnyData.DataType.LINE: ProtoBufferLine,
    AnyData.DataType.FRAME: ProtoBufferFrame,
    AnyData.DataType.ELEMENT: ProtoBufferElement,
}


class DataDeserializer:
    """Data Decoder for protobuf messages to COMPAS objects.

    The decoder hooks into the Protocol Buffer deserialization process
    to reconstruct COMPAS data objects from serialized protobuf data.

    Examples
    --------
    >>> from compas_pb.data import pb_load
    >>> point = pb_load("point.pb")  # doctest: +SKIP

    """

    def __init__(self, *args, **kwargs):
        super(DataDeserializer, self).__init__(*args, **kwargs)
        self.message_data = AnyData.MessageData()

    def deserialize_message(self, binary_data):
        """Deserialize a top-level protobuf message."""
        if not binary_data:
            raise ValueError("Binary data is empty.")
        self.message_data.ParseFromString(binary_data)
        return self._deserialize_any(self.message_data.data)

    def _deserialize_any(self, data):
        """Deserialize a protobuf message to COMPAS object."""
        if data.type == AnyData.DataType.LIST:
            return self._deserialize_list(data.list)

        elif data.type == AnyData.DataType.DICT:
            return self._deserialize_dict(data.dict)

        else:
            deserializer = DESERIALIZERS.get(data.type)

            if not deserializer:
                raise TypeError(f"Unsupported type: {data.type}")

            buffer_obj = deserializer()
            data_offset = buffer_obj.from_pb(data)

            return data_offset

    def _deserialize_list(self, data_list):
        """Deserialize a protobuf ListData message to Python list."""
        data_offset = []
        for item in data_list.data:
            data_offset.append(self._deserialize_any(item))
        return data_offset

    def _deserialize_dict(self, data_dict):
        """Deserialize a protobuf DictData message to Python dictionary."""
        data_offset = {}
        for key, value in data_dict.data.items():
            data_offset[key] = self._deserialize_any(value)
        return data_offset

    def to_dict(self):
        """Convert protobuf message to dictionary."""
        from google.protobuf.json_format import MessageToDict

        if not self.message_data:
            raise ValueError("No message data to convert.")
        proto_dict = MessageToDict(self.message_data, preserving_proto_field_name=True)
        return proto_dict


if __name__ == "__main__":
    # Example usage
    nested_data = {
        "point": Point(1.0, 2.0, 3.0),
        "line": Line(Point(1.0, 2.0, 3.0), Point(4.0, 5.0, 6.0)),
        "list": [Point(4.0, 5.0, 6.0), [Vector(7.0, 8.0, 9.0)]],  # Nested list
        "frame": Frame(Point(1.0, 2.0, 3.0), Vector(4.0, 5.0, 6.0)),
        # "element": element,
    }

    # Dump the binary data to a file
    encoder = DataSerializer()
    binary_data = encoder.serialize_message(nested_data)
    print("Successfully serialized")
    with open("./nested_data.bin", "wb") as f:
        f.write(binary_data)

    # Deserialize
    # load the binary data from the file
    with open("./nested_data.bin", "rb") as f:
        binary_data = f.read()

    decoder = DataDeserializer()
    message_data = decoder.deserialize_message(binary_data)
    # message_data_dict = decoder.to_dict()

    print("Successfully deserialized")
    print(message_data)

    line = message_data["line"]
    print(message_data["line"])
    print(type(line))
