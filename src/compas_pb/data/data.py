from compas.data import Data
from compas.geometry import Point, Vector

from compas_pb.data import point_pb2 as PointData
from compas_pb.data import vector_pb2 as VectorData
# from compas_pb.data import line_pb2 as LineData
# from compas_pb.data import frame_pb2 as FrameData
# from compas_pb.data import element_pb2 as ElementData
from compas_pb.data import message_pb2 as AnyData


class ProtoBufferData(Data):
    """ProtoBufferData is a base class for all data types that can be converted to protobuf data.
    inherits from the Data class in COMPAS.
    """

    def __init__(self, name=None):
        super(ProtoBufferData, self).__init__(name=name)
        self._proto_data = None
        self._type_enum = 0

    # ==========================================================================
    # Properties
    # ==========================================================================

    @property
    def data_offset(self):
        return self._proto_data

    @data_offset.setter
    def data_offset(self, data):
        self._proto_data = data

    @property
    def type_enum(self):
        return self._type_enum

    @type_enum.setter
    def type_enum(self, data):
        self._type_enum = data

    def get_proto_fields(self):
        if self._proto_data is None:
            raise ValueError("Proto data not set")
        return self._proto_data.DESCRIPTOR.fields_by_name.keys()

    # ==========================================================================
    # Methods
    # ==========================================================================

    def _to_pb(self, obj):
        raise NotImplementedError("Subclasses implement this method")

class ProtoBufferPoint(ProtoBufferData):
    """

    """
    def __init__(self, name=None):
        super(ProtoBufferPoint, self).__init__(name=name)
        self._proto_data = PointData.PointData()
        self._type_enum = AnyData.DataType.POINT

    def _to_pb(self, obj):

        self._proto_data.guid = str(obj.guid)
        self._proto_data.name = obj.name
        self._proto_data.x = obj.x
        self._proto_data.y = obj.y
        self._proto_data.z = obj.z

        return self._proto_data, self._type_enum

class ProtoBufferVector(ProtoBufferData):
    """

    """
    def __init__(self, name=None):
        super(ProtoBufferVector, self).__init__(name=name)
        self._proto_data = VectorData.VectorData()
        self._type_enum = AnyData.DataType.VECTOR

    def _to_pb(self, obj):

        self._proto_data.guid = str(obj.guid)
        self._proto_data.name = obj.name
        self._proto_data.x = obj.x
        self._proto_data.y = obj.y
        self._proto_data.z = obj.z

        return self._proto_data, self._type_enum


# def line_to_pb(self, obj):
#     """Convert a Line object to a protobuf message."""
#
#     if not isinstance(obj, Line):
#         raise TypeError("Expected a Line object")
#
#     line_data = LineData.LineData()
#     start, _ = self.point_to_pb(obj.start)
#     end, _ = self.point_to_pb(obj.end)
#
#     line_data.guid = str(obj.guid)
#     line_data.name = obj.name
#     line_data.start.CopyFrom(start)
#     line_data.end.CopyFrom(end)
#
#     return line_data, AnyData.DataType.LINE


# def frame_to_pb(self, obj):
#     if not isinstance(obj, Frame):
#         raise TypeError("Expected a Frame object")
#
#     frame_data = FrameData.FrameData()
#     point, _ = self.point_to_pb(obj.point)
#     xaxis, _ = self.vector_to_pb(obj.xaxis)
#     yaxis, _ = self.vector_to_pb(obj.yaxis)
#
#     frame_data.guid = str(obj.guid)
#     frame_data.name = obj.name
#     frame_data.point.CopyFrom(point)
#     frame_data.xaxis.CopyFrom(xaxis)
#     frame_data.yaxis.CopyFrom(yaxis)
#
#     return frame_data, AnyData.DataType.FRAME


# def element_to_pb(self, obj):
#     element_data = ElementData.ElementData()
#     frame, _ = self.frame_to_pb(obj.frame)
#
#     if not isinstance(obj, Element):
#         raise TypeError("Expected a Element object")
#
#     element_data.guid = str(obj.guid)
#     element_data.name = obj.name
#     element_data.frame.CopyFrom(frame)
#     element_data.xsize = obj.xsize
#     element_data.ysize = obj.ysize
#     element_data.zsize = obj.zsize
#
#     return element_data, AnyData.DataType.ELEMENT


if __name__ == "__main__":

    point = Point(1, 2, 3)
    point_data = ProtoBufferData().point_to_pb(point)
    print(point_data)

    vector = Vector(1, 2, 3)
    vector_data = ProtoBufferData().vector_to_pb(vector)
    print(vector_data)
