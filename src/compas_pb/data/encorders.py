from compas.data import Data
from compas.geometry import Frame, Line, Point, Vector
from compas_model.elements import Element

from compas_pb.data.data import ProtoBufferPoint, ProtoBufferVector


SERIALIZERS = {
    Point: ProtoBufferPoint,
    Vector: ProtoBufferVector,
    # Line: line_to_pb,
    # Frame: frame_to_pb,
    # Element: element_to_pb,
}

class DataSerializer:
    """Data Encoder for COMPAS objects to protobuf messages."""

    @staticmethod
    def serializer_any(obj):

        serializer = SERIALIZERS.get(type(obj))

        print(serializer)
        if not serializer:
            raise TypeError(f"Unsupported type: {type(obj)}")

        # return serializer(obj)

        # return getattr(cls, serializer)(obj)

if __name__ == "__main__":

    # Example usage
    point = Point(0, 0, 0)
    encoder = DataSerializer()
    encoded_point = encoder.serializer_any(point)
    print(encoded_point)

# def serialize_any(obj):
#     """Serialize any object to a protobuf message"""
#     if isinstance(obj, list):
#         type_enum = AnyData.DataType.LIST
#         offset = serialize_list(obj)
#     elif isinstance(obj, dict):
#         type_enum = AnyData.DataType.DICT
#         offset = serialize_dict(obj)
#     else:
#         serializer = SERIALIZERS.get(type(obj))
#         if not serializer:
#             raise ValueError(f"Unsupported type: {type(obj)}")
#         offset, type_enum = serializer(obj)
#     return type_enum, offset
#
#
# # SERIALIZERS = {
# #     Point: point_to_pb,
# #     Vector: vector_to_pb,
# #     Line: line_to_pb,
# #     Frame: frame_to_pb,
# #     Element: element_to_pb,
# # }
#
#
# def serialize_any(obj):
#     """Serialize any object to a protobuf message"""
#     if isinstance(obj, list):
#         type_enum = AnyData.DataType.LIST
#         offset = serialize_list(obj)
#     elif isinstance(obj, dict):
#         type_enum = AnyData.DataType.DICT
#         offset = serialize_dict(obj)
#     else:
#         serializer = SERIALIZERS.get(type(obj))
#         if not serializer:
#             raise ValueError(f"Unsupported type: {type(obj)}")
#         offset, type_enum = serializer(obj)
#     return type_enum, offset
#
#
# def serialize_any_wrapper(obj):
#     """Wraps Any protobuf data in a protobuf AnyData."""
#     type_enum, offset = serialize_any(obj)
#     any_data = AnyData.AnyData()
#     any_data.type = type_enum
#
#     dtype = AnyData.DataType.Name(type_enum).lower()
#     getattr(any_data, dtype).CopyFrom(offset)
#
#     return any_data
#
#
# def serialize_list(data_list):
#     """Serialize a Python list containing mixed data types."""
#     list_data = AnyData.ListData()
#     for item in data_list:
#         list_data.data.append(serialize_any_wrapper(item))
#     return list_data
#
#
# def serialize_dict(data_dict):
#     """Serialize a Python dictionary containing mixed data types."""
#     dict_data = AnyData.DictData()
#     for key, value in data_dict.items():
#         dict_data.data[key].CopyFrom(serialize_any_wrapper(value))
#     return dict_data
#
#
# def serialize_message(data):
#     """Serialize a top-level protobuf message."""
#     message_data = serialize_any_wrapper(data)
#     message = AnyData.MessageData(data=message_data)
#     return message.SerializeToString()
#
#
# class Element(Data):
#     """Mock class to simulate a data structure"""
#
#     def __init__(self, frame, xsize, ysize, zsize, name=None):
#         super(Element, self).__init__(name)
#         self.name = name
#         self.frame = frame
#         self.xsize = xsize
#         self.ysize = ysize
#         self.zsize = zsize


# def main():
#     # Example nested data structure
#     frame = Frame.worldXY()
#     element = Element(frame, 1.0, 2.0, 3.0, name="Element")
#     nested_data = {
#         "point": Point(1.0, 2.0, 3.0),
#         "line": Line(Point(1.0, 2.0, 3.0), Point(4.0, 5.0, 6.0)),
#         "list": [Point(4.0, 5.0, 6.0), [Vector(7.0, 8.0, 9.0)]],  # Nested list
#         "frame": frame,
#         "element": element,
#     }
#
#     point = Point(1.0, 2.0, 3.0)
#     pbdata = PBData(point)
#     pbdata.to_pb(point)
#     print(pbdata.data_offset, pbdata.data_type_enum)
#
#     # Serialize and save
#     # binary_data = serialize_message(nested_data)
#     # binary_data = serialize_message(point)
#     # print("Successfully serialized")
#     # with open("./temp/nested_data.bin", "wb") as f:
#     #     f.write(binary_data)
#
#     # Deserialize
#     # with open("./temp/nested_data.bin", "rb") as f:
#     #     binary_data = f.read()
#     #     proto_data = AnyData.MessageData()
#     #     proto_data.ParseFromString(binary_data)
#     #
#     #     # for debug
#     #     print(f"Successfully deserialized\n{proto_data}")
#
#
# if __name__ == "__main__":
#     main()

