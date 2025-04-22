from abc import ABC
from abc import abstractmethod

from compas.geometry import Frame
from compas.geometry import Line
from compas.geometry import Point
from compas.geometry import Vector

# from compas_model.elements import Element
from compas_pb.data.proto import element_pb2 as ElementData
from compas_pb.data.proto import frame_pb2 as FrameData
from compas_pb.data.proto import line_pb2 as LineData
from compas_pb.data.proto import message_pb2 as AnyData
from compas_pb.data.proto import point_pb2 as PointData
from compas_pb.data.proto import vector_pb2 as VectorData


class _ProtoBufferData(ABC):
    """A abstract class for protobuf data."""

    @abstractmethod
    def to_pb(self):
        """Convert a data object to a protobuf message.

        Parameters:
        -----------
            obj: The data object to convert.
        """
        raise NotImplementedError("Subclasses implement this method")

    @staticmethod
    @abstractmethod
    def from_pb(proto_data):
        """ " Convert a protobuf message to a data object.

        Parameters:
            proto_data: The protobuf message to convert.
        """
        raise NotImplementedError("Subclasses implement this method")


class _ProtoBufferPoint(_ProtoBufferData):
    """A class to hold the protobuf data for a Point object.

    Parameters:
    ----------
    obj : :class: `compas.geometry.Point`

    Methods:
    -------

    """

    PB_TYPE = AnyData.DataType.POINT

    def __init__(self, obj=None):
        super().__init__()
        self._obj = obj
        self._proto_data = PointData.PointData()

    def to_pb(self):
        """Convert a Point object to a protobuf message.

        Returns:
        :class: `compas_pb.data.proto.point_pb2.PointData`
            The protobuf message type of PointData.

        """

        point_obj = self._obj

        if point_obj is None:
            raise ValueError("No Point object provided for conversion.")

        self._proto_data.guid = str(point_obj.guid)
        self._proto_data.name = point_obj.name
        self._proto_data.x = point_obj.x
        self._proto_data.y = point_obj.y
        self._proto_data.z = point_obj.z

        return self._proto_data

    @staticmethod
    def from_pb(proto_data):
        """Convert a protobuf message to a Point object.

        Parameters:
        proto_data : :class: `compas_pb.data.proto.point_pb2.PointData`
            The protobuf message type of PointData.

        Returns:
        :class: `compas.geometry.Point`

        """

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


class _ProtoBufferLine(_ProtoBufferData):
    """A class to hold the protobuf data for a Line object.

    Parameters:
    ----------
    obj : :class: `compas.geometry.Line`

    Methods:
    -------

    """

    PB_TYPE = AnyData.DataType.LINE

    def __init__(self, obj=None):
        super().__init__()
        self._obj = obj
        self._proto_data = LineData.LineData()

    def to_pb(self):
        """Convert a Line object to a protobuf message.

        Returns:
        :class: `compas_pb.data.proto.line_pb2.LineData`
            The protobuf message type of LineData.

        """
        line_obj = self._obj

        if line_obj is None:
            raise ValueError("No Line object provided for conversion.")

        self._proto_data.guid = str(line_obj.guid)
        self._proto_data.name = line_obj.name
        start = _ProtoBufferPoint(line_obj.start).to_pb()
        end = _ProtoBufferPoint(line_obj.end).to_pb()

        self._proto_data.start.CopyFrom(start)
        self._proto_data.end.CopyFrom(end)

        return self._proto_data

    @staticmethod
    def from_pb(proto_data):
        """Convert a protobuf message to a Line object.

        Parameters:
            proto_data : :class: `compas_pb.data.proto.line_pb2.LineData`
                The protobuf message type of LineData.

        Returns:
            :class: `compas.geometry.Line`
                The converted Line object.
        """
        if hasattr(proto_data, "line"):
            start = _ProtoBufferPoint.from_pb(proto_data.line.start)
            end = _ProtoBufferPoint.from_pb(proto_data.line.end)
        else:
            start = _ProtoBufferPoint.from_pb(proto_data.start)
            end = _ProtoBufferPoint.from_pb(proto_data.end)
        line_data = Line(start, end)
        return line_data


class _ProtoBufferVector(_ProtoBufferData):
    """A class to hold the protobuf data for a Vector object.

    Parameters:
    ----------
    obj : :class: `compas.geometry.Vector`

    Methods:
    -------

    """

    PB_TYPE = AnyData.DataType.VECTOR

    def __init__(self, obj=None):
        super().__init__()
        self._obj = obj
        self._proto_data = VectorData.VectorData()

    def to_pb(self):
        """Convert a Vector object to a protobuf message.

        Returns:
        :class: `compas_pb.data.proto.vector_pb2.VectorData`
            The protobuf message type of VectorData.

        """
        vector_obj = self._obj

        if vector_obj is None:
            raise ValueError("No Vector object provided for conversion.")

        self._proto_data.guid = str(vector_obj.guid)
        self._proto_data.name = vector_obj.name
        self._proto_data.x = vector_obj.x
        self._proto_data.y = vector_obj.y
        self._proto_data.z = vector_obj.z

        return self._proto_data

    @staticmethod
    def from_pb(proto_data):
        """Convert a protobuf message to a Vector object.

        Parameters:
            proto_data : :class: `compas_pb.data.proto.vector_pb2.VectorData`
                The protobuf message type of VectorData.

        Returns:
            :class: `compas.geometry.Vector`
        """

        vector_data = None
        if hasattr(proto_data, "vector"):
            vector_data = Vector(
                proto_data.vector.x,
                proto_data.vector.y,
                proto_data.vector.z,
            )
        else:
            vector_data = Vector(
                proto_data.x,
                proto_data.y,
                proto_data.z,
            )
        return vector_data


class _ProtoBufferFrame(_ProtoBufferData):
    """A class to hold the protobuf data for a Frame object.

    Parameters:
    ----------
    obj : :class: `compas.geometry.Frame`

    Methods:
    -------
    """

    PB_TYPE = AnyData.DataType.FRAME

    def __init__(self, obj=None):
        super().__init__()
        self._obj = obj
        self._proto_data = FrameData.FrameData()

    def to_pb(self):
        """Convert a Frame object to a protobuf message.

        Returns:
        :class: `compas_pb.data.proto.frame_pb2.FrameData`
            The protobuf message type of FrameData.

        """
        frame_obj = self._obj

        if frame_obj is None:
            raise ValueError("No Frame object provided for conversion.")

        self._proto_data.guid = str(frame_obj.guid)
        self._proto_data.name = frame_obj.name
        point = _ProtoBufferPoint(frame_obj.point).to_pb()
        xaxis = _ProtoBufferVector(frame_obj.xaxis).to_pb()
        yaxis = _ProtoBufferVector(frame_obj.yaxis).to_pb()

        self._proto_data.point.CopyFrom(point)
        self._proto_data.xaxis.CopyFrom(xaxis)
        self._proto_data.yaxis.CopyFrom(yaxis)

        return self._proto_data

    @staticmethod
    def from_pb(proto_data):
        """Convert a protobuf message to a Frame object.

        Parameters:
        -----------
            proto_data : :class: `compas_pb.data.proto.frame_pb2.FrameData`
                The protobuf message type of FrameData.

        Returns:
            :class: `compas.geometry.Frame`
        """
        if hasattr(proto_data, "frame"):
            point = _ProtoBufferPoint.from_pb(proto_data.frame.point)
            xaxis = _ProtoBufferVector.from_pb(proto_data.frame.xaxis)
            yaxis = _ProtoBufferVector.from_pb(proto_data.frame.yaxis)
        else:
            point = _ProtoBufferPoint.from_pb(proto_data.point)
            xaxis = _ProtoBufferVector.from_pb(proto_data.xaxis)
            yaxis = _ProtoBufferVector.from_pb(proto_data.yaxis)

        frame = Frame(
            point=point,
            xaxis=xaxis,
            yaxis=yaxis,
        )
        return frame


class _ProtoBufferDefault(_ProtoBufferData):
    """
    A class to hold the protobuf data for python native types.

    Parameters:
    ----------
        obj : :class: `int`, `float`, `bool`, `str`
    """

    PB_TYPE = AnyData.DataType.UNKNOWN

    PY_TYPES_SERIALIZER = {
        int: AnyData.DataType.INT,
        float: AnyData.DataType.FLOAT,
        bool: AnyData.DataType.BOOL,
        str: AnyData.DataType.STR,
    }

    PY_TYPES_DESERIALIZER = {key.__name__.lower(): value for key, value in PY_TYPES_SERIALIZER.items()}

    def __init__(self, obj=None):
        super().__init__()
        self._obj = obj
        self._proto_data = AnyData.AnyData()

    def to_pb(self):
        """
        Convert a python native type to a protobuf message.

        Returns:
            :class: `compas_pb.data.proto.message_pb2.AnyData`
                The protobuf message type of AnyData.
        """
        if self._obj is None:
            raise ValueError("No object provided for conversion.")
        obj = self._obj

        try:
            type_obj = self.PY_TYPES_SERIALIZER.get(type(obj))
            field_name = AnyData.DataType.Name(type_obj).lower()
            setattr(self._proto_data, field_name, obj)
            return self._proto_data

        except TypeError as e:
            raise TypeError(f"Unsupported type: {type(obj)}: {e}")

    @staticmethod
    def from_pb(proto_data):
        """Convert a protobuf message to a python native type.

        Parameters:
        -----------
            proto_data : :class: `compas_pb.data.proto.message_pb2.AnyData`
                The protobuf message type of AnyData.

        Returns:
            data_offset : python object
                The converted python native type.
        """
        proto_type = proto_data.WhichOneof("data")

        try:
            type_proto_data = _ProtoBufferDefault.PY_TYPES_DESERIALIZER.get(proto_type)
            if type_proto_data:
                data_offset = getattr(proto_data, proto_type)
            return data_offset
        except TypeError as e:
            raise TypeError(f"Unsupported type: {proto_type}: {e}")


class _ProtoBufferAny(_ProtoBufferData):
    """A class to hold the protobuf data for any object.

    Parameters:
    ----------
        obj : :class: `compas.geometry.Point`,
                        `compas.geometry.Vector`,
                        `compas.geometry.Line`,
                        `compas.geometry.Frame`
    if the object is not one of the above, and it has the atrribute from the listed above,
    it will be converted to the corresponding object type and as `data`.

    """

    PB_TYPE = AnyData.DataType.UNKNOWN

    # Mapping of COMPAS object types to protobuf data types
    # COMPAS type: {protobuf type: protobuf class}
    SERIALIZER = {
        Point: _ProtoBufferPoint,
        Vector: _ProtoBufferVector,
        Line: _ProtoBufferLine,
        Frame: _ProtoBufferFrame,
    }
    DESERIALIZER = {key.__name__.lower(): value for key, value in SERIALIZER.items()}

    def __init__(self, obj=None, fallback_serializer=None):
        super().__init__()
        self._obj = obj
        self._proto_data = AnyData.AnyData()
        self._fallback_serializer = fallback_serializer

    def to_pb(self) -> AnyData.AnyData:
        """Convert a any object to a protobuf any message.

        Returns:
            :class: `compas_pb.data.proto.message_pb2.AnyData`
                The protobuf message type of AnyData.

        """

        if self._obj is None:
            raise ValueError("No object provided for conversion.")
        obj = self._obj

        try:
            pb_serializer_cls = self.SERIALIZER.get(type(obj))
            if pb_serializer_cls:
                pb_obj = pb_serializer_cls(obj)
                self.PB_TYPE = pb_obj.PB_TYPE
                field_name = AnyData.DataType.Name(self.PB_TYPE).lower()
                data_offset = pb_obj.to_pb()
                getattr(self._proto_data, field_name).CopyFrom(data_offset)
            elif hasattr(obj, "__jsondump__"):
                obj_dict = {obj.__class__.__name__: obj.__jsondump__()}
                data_offset = self._fallback_serializer(obj_dict)
                self._proto_data.type = AnyData.DataType.DICT
                self._proto_data.dict.CopyFrom(data_offset)
            else:
                self._proto_data = _ProtoBufferDefault(obj).to_pb()
            return self._proto_data
        except TypeError as e:
            raise TypeError(f"Unsupported type: {type(obj)}: {e}")

    @staticmethod
    def from_pb(proto_data) -> list | dict | object:
        """Convert a protobuf message to a supported COMPAS object.

        Parameters:
        -----------
            proto_data : :class: `compas_pb.data.proto.message_pb2.AnyData`
                The protobuf message type of AnyData.

        Returns:
        ----------
            data_offset : python object
        """

        proto_type = proto_data.WhichOneof("data")

        try:
            pb_deserializer_cls = _ProtoBufferAny.DESERIALIZER.get(proto_type)
            if pb_deserializer_cls:
                data_offset = pb_deserializer_cls.from_pb(proto_data)
            else:
                data_offset = _ProtoBufferDefault.from_pb(proto_data)
            return data_offset

        except TypeError as e:
            raise TypeError(f"Unsupported type: {proto_type}: {e}")


#######################
# NOT IMPLEMENTED YET
#######################
class _ProtoBufferElement(_ProtoBufferData):
    """
    A class to hold the protobuf data for an Element object.

    Parameters:
    ----------
    obj : :class: `compas_model.elements.Element`

    """

    PB_TYPE = AnyData.DataType.ELEMENT

    def __init__(self, obj=None):
        super().__init__()
        self._obj = obj
        self._proto_data = ElementData.ElementData()

    def to_pb(self):
        """Convert a Element object to a protobuf message."""
        raise NotImplementedError("Need to be define")

    # TODO:
    @staticmethod
    def from_pb(proto_data):
        """Convert a protobuf message to a Vector object."""
        raise NotImplementedError("Need to be define")
