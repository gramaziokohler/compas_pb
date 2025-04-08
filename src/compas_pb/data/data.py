from compas.data import Data
from compas.geometry import Frame, Line, Point

# from compas_model.elements import Element
from compas_pb.data.proto import element_pb2 as ElementData
from compas_pb.data.proto import frame_pb2 as FrameData
from compas_pb.data.proto import line_pb2 as LineData
from compas_pb.data.proto import message_pb2 as AnyData
from compas_pb.data.proto import point_pb2 as PointData
from compas_pb.data.proto import vector_pb2 as VectorData

from abc import ABC, abstractmethod



class _ProtoBufferData():
    """ProtoBufferData is a base class for all data types that can be converted to protobuf data."""

    @abstractmethod
    def to_pb(self, obj):
        """ Convert a data object to a protobuf message.

        Args:
            obj: The data object to convert.
        """
        raise NotImplementedError("Subclasses implement this method")
    @abstractmethod
    def from_pb(self, proto_data):
        """" Convert a protobuf message to a data object.

        Args:
            proto_data: The protobuf message to convert.
        """
        raise NotImplementedError("Subclasses implement this method")

class _ProtoBufferPoint(_ProtoBufferData):
    """ """

    PB_TYPE = AnyData.DataType.POINT

    def __init__(self, obj):
        super().__init__()
        self._obj = obj
        self._proto_data = PointData.PointData()

    def to_pb(self):
        """Convert a Point object to a protobuf message."""

        self._proto_data.guid = str(self._obj.guid)
        self._proto_data.name = self._obj.name
        self._proto_data.x = self._obj.x
        self._proto_data.y = self._obj.y
        self._proto_data.z = self._obj.z
        return self._proto_data

    @staticmethod
    def from_pb(proto_data):
        """Convert a protobuf message to a Point object."""
        point_data = None
        if hasattr(proto_data, "point"):
            point_data = Point(
                proto_data.point.x,
                proto_data.point.y,
                proto_data.point.z,
            )
        else:
            point_data = Point(
                proto_data.x,
                proto_data.y,
                proto_data.z,
            )
        return point_data


# class ProtoBufferLine(ProtoBufferData):
#     """ """

#     def __init__(self, obj=None, name=None):
#         super(ProtoBufferLine, self).__init__(name=name)
#         self._proto_data = LineData.LineData()
#         self._type_enum = AnyData.DataType.LINE

#     def to_pb(self, obj):
#         self._proto_data.guid = str(obj.guid)
#         self._proto_data.name = obj.name
#         start, _ = ProtoBufferPoint().to_pb(obj.start)
#         end, _ = ProtoBufferPoint().to_pb(obj.end)

#         self._proto_data.start.CopyFrom(start)
#         self._proto_data.end.CopyFrom(end)

#         return self._proto_data, self._type_enum

#     @staticmethod
#     def from_pb(proto_data):
#         """Convert a protobuf message to a Line object."""
#         start = ProtoBufferPoint.from_pb(proto_data.line.start)
#         end = ProtoBufferPoint.from_pb(proto_data.line.end)
#         line_data = Line(start, end)
#         return line_data


# class ProtoBufferVector(ProtoBufferData):
#     """ """

#     def __init__(self, obj=None, name=None):
#         super(ProtoBufferVector, self).__init__(name=name)
#         self._proto_data = VectorData.VectorData()
#         self._type_enum = AnyData.DataType.VECTOR

#         if obj is not None:
#             proto_data, type_enum = self.to_pb(obj)
#             self.proto_data = proto_data
#             self.type_enum = type_enum

#     def to_pb(self, obj):
#         self._proto_data.guid = str(obj.guid)
#         self._proto_data.name = obj.name
#         self._proto_data.x = obj.x
#         self._proto_data.y = obj.y
#         self._proto_data.z = obj.z

#         return self._proto_data, self._type_enum

#     @staticmethod
#     def from_pb(proto_data):
#         """Convert a protobuf message to a Vector object."""
#         # field_name = AnyData.DataType.Name(proto_data.type).lower()
#         # from google.protobuf.json_format import MessageToDict
#         vector_data = None
#         if hasattr(proto_data, "vector"):
#             vector_data = Point(
#                 proto_data.vector.x,
#                 proto_data.vector.y,
#                 proto_data.vector.z,
#             )
#         else:
#             vector_data = Point(
#                 proto_data.x,
#                 proto_data.y,
#                 proto_data.z,
#             )
#         return vector_data


# class ProtoBufferFrame(ProtoBufferData):
#     """ """

#     def __init__(self, obj=None, name=None):
#         super(ProtoBufferFrame, self).__init__(name=name)
#         self._proto_data = FrameData.FrameData()
#         self._type_enum = AnyData.DataType.FRAME

#         if obj is not None:
#             proto_data, type_enum = self.to_pb(obj)
#             self.proto_data = proto_data
#             self.type_enum = type_enum

#     def to_pb(self, obj):
#         """Convert a Frame object to a protobuf message."""
#         self._proto_data.guid = str(obj.guid)
#         self._proto_data.name = obj.name
#         point, _ = ProtoBufferPoint().to_pb(obj.point)
#         xaxis, _ = ProtoBufferVector().to_pb(obj.xaxis)
#         yaxis, _ = ProtoBufferVector().to_pb(obj.yaxis)

#         self._proto_data.point.CopyFrom(point)
#         self._proto_data.xaxis.CopyFrom(xaxis)
#         self._proto_data.yaxis.CopyFrom(yaxis)

#         return self._proto_data, self._type_enum

#     @staticmethod
#     def from_pb(proto_data):
#         """Convert a protobuf message to a Vector object."""
#         point = ProtoBufferPoint.from_pb(proto_data.frame.point)
#         xaxis = ProtoBufferVector.from_pb(proto_data.frame.xaxis)
#         yaxis = ProtoBufferVector.from_pb(proto_data.frame.yaxis)
#         frame = Frame(
#             point=point,
#             xaxis=xaxis,
#             yaxis=yaxis,
#         )
#         return frame


# class ProtoBufferElement(ProtoBufferData):
#     """ """

#     def __init__(self, obj=None, name=None):
#         super(ProtoBufferElement, self).__init__(name=name)
#         self._proto_data = ElementData.ElementData()
#         self._type_enum = AnyData.DataType.ELEMENT

#         if obj is not None:
#             proto_data, type_enum = self.to_pb(obj)
#             self.proto_data = proto_data
#             self.type_enum = type_enum

#     def to_pb(self, obj):
#         """Convert a Element object to a protobuf message."""
#         self._proto_data.guid = str(obj.guid)
#         self._proto_data.name = obj.name
#         frame, _ = ProtoBufferFrame().to_pb(obj.frame)

#         self._proto_data.frame.CopyFrom(frame)
#         self._proto_data.xsize = obj.xsize
#         self._proto_data.ysize = obj.ysize
#         self._proto_data.zsize = obj.zsize

#         return self._proto_data, self._type_enum

#     # TODO:
#     # @staticmethod
#     # def from_pb(proto_data):
#     #     """Convert a protobuf message to a Vector object."""
#     #     element = Element()
#     #     return frame


# class ProtoBufferAny(ProtoBufferData):
#     def __init__(self, name=None):
#         super(ProtoBufferAny, self).__init__(name=name)
#         self._proto_data = AnyData.AnyData()
#         self._type_enum = AnyData.DataType.UNKNOWN


# class ProtoBufferList(ProtoBufferData):
#     """ """

#     def __init__(self, obj=None, name=None):
#         super(ProtoBufferList, self).__init__(name=name)
#         self._proto_data = AnyData.ListData()
#         self._type_enum = AnyData.DataType.LIST


# class ProtoBufferDict(ProtoBufferData):
#     """ """

#     def __init__(self, obj=None, name=None):
#         super(ProtoBufferDict, self).__init__(name=name)
#         self._proto_data = AnyData.DictData()
#         self._type_enum = AnyData.DataType.DICT


if __name__ == "__main__":
    point = Point(1, 2, 3)
    point_data = _ProtoBufferPoint(point).to_pb()
    print(point_data)

