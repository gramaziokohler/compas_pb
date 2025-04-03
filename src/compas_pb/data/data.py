from compas.data import Data
from compas.geometry import Frame, Line, Point, Vector

from compas_pb.data import element_pb2 as ElementData
from compas_pb.data import frame_pb2 as FrameData
from compas_pb.data import line_pb2 as LineData
from compas_pb.data import message_pb2 as AnyData
from compas_pb.data import point_pb2 as PointData
from compas_pb.data import vector_pb2 as VectorData


class PBData:
    pass
#     """This class is used to convert COMPAS objects to protobuf messages."""
#
#     def __init__(self):
#         self.data_offset = None
#         self.data_type_enum = None
#
#     def
#
#     def point_to_pb(self, obj):
#         """Convert a Point object to a protobuf message."""
#
#         if not isinstance(obj, Point):
#             raise TypeError("Expected a Compas Point object")
#
#         point_data = PointData.PointData()
#         point_data.guid = str(obj.guid)
#         point_data.name = obj.name
#         point_data.x = obj.x
#         point_data.y = obj.y
#         point_data.z = obj.z
#
#         self.data_offset = point_data
#         self.data_type_enum = AnyData.DataType.POINT
#
#         return point_data, AnyData.DataType.POINT
#
#     def vector_to_pb(self, obj):
#         """Convert a Vector object to a protobuf message."""
#
#         if not isinstance(obj, Vector):
#             raise TypeError("Expected a Vector object")
#
#         vector_data = VectorData.VectorData()
#         vector_data.guid = str(obj.guid)
#         vector_data.name = obj.name
#         vector_data.x = obj.x
#         vector_data.y = obj.y
#         vector_data.z = obj.z
#
#         self.data_offset = vector_data
#         self.data_type_enum = AnyData.DataType.VECTOR
#
#         return vector_data, AnyData.DataType.VECTOR
#
#     def line_to_pb(self, obj):
#         """Convert a Line object to a protobuf message."""
#
#         if not isinstance(obj, Line):
#             raise TypeError("Expected a Line object")
#
#         line_data = LineData.LineData()
#         start, _ = self.point_to_pb(obj.start)
#         end, _ = self.point_to_pb(obj.end)
#
#         line_data.guid = str(obj.guid)
#         line_data.name = obj.name
#         line_data.start.CopyFrom(start)
#         line_data.end.CopyFrom(end)
#
#         self.data_offset = line_data
#         self.data_type_enum = AnyData.DataType.LINE
#
#         return line_data, AnyData.DataType.LINE
#
#     def frame_to_pb(self, obj):
#         if not isinstance(obj, Frame):
#             raise TypeError("Expected a Frame object")
#
#         frame_data = FrameData.FrameData()
#         point, _ = self.point_to_pb(obj.point)
#         xaxis, _ = self.vector_to_pb(obj.xaxis)
#         yaxis, _ = self.vector_to_pb(obj.yaxis)
#
#         frame_data.guid = str(obj.guid)
#         frame_data.name = obj.name
#         frame_data.point.CopyFrom(point)
#         frame_data.xaxis.CopyFrom(xaxis)
#         frame_data.yaxis.CopyFrom(yaxis)
#
#         self.data_offset = frame_data
#         self.data_type_enum = AnyData.DataType.FRAME
#
#         return frame_data, AnyData.DataType.FRAME
#
#     def element_to_pb(self, obj):
#         element_data = ElementData.ElementData()
#         frame, _ = self.frame_to_pb(obj.frame)
#
#         if not isinstance(obj, Element):
#             raise TypeError("Expected a Element object")
#
#         element_data.guid = str(obj.guid)
#         element_data.name = obj.name
#         element_data.frame.CopyFrom(frame)
#         element_data.xsize = obj.xsize
#         element_data.ysize = obj.ysize
#         element_data.zsize = obj.zsize
#
#         self.data_offset = element_data
#         self.data_type_enum = AnyData.DataType.ELEMENT
#
#         return element_data, AnyData.DataType.ELEMENT
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
