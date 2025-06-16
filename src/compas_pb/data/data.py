from abc import ABC
from abc import abstractmethod
from typing import Any

from compas.geometry import Frame
from compas.geometry import Line
from compas.geometry import Point
from compas.geometry import Vector
from compas.plugins import pluggable

from compas_pb.generated import frame_pb2 as FrameData
from compas_pb.generated import line_pb2 as LineData
from compas_pb.generated import message_pb2 as MessageData
from compas_pb.generated import point_pb2 as PointData
from compas_pb.generated import vector_pb2 as VectorData


# NOTE: PUT More Docstring in the class docstring
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

    def __init__(self, obj=None):
        super().__init__()
        self._obj = obj
        self._proto_data = PointData.PointData()

    @property
    def proto_data_type(self):
        return self._proto_data

    def to_pb(self) -> PointData.PointData:
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
    def from_pb(proto_data: PointData.PointData | MessageData.AnyData) -> Point:
        """Convert a protobuf message to a Point object.

        Parameters
        ----------
        proto_data: :class:`compas_pb.data.proto.point_pb2.PointData` or\
                    :class:`compas_pb.data.proto.message_pb2.AnyData`

        The protobuf message type of PointData, or the protobuf message type of AnyData which contains PointData.

        Returns
        -------
        :class:`compas.geometry.Point`
            The Point object created from the protobuf data.
        """
        point_data = PointData.PointData()
        # check if the proto_data is any message
        if hasattr(proto_data, "data"):
            proto_data.data.Unpack(point_data)
        else:
            point_data = proto_data
        if not point_data.IsInitialized():
            raise ValueError("No PointData has been initialized.")
        point = Point(
            point_data.x,
            point_data.y,
            point_data.z,
        )
        return point


class _ProtoBufferLine(_ProtoBufferData):
    """A class to hold the protobuf data for a Line object.

    Parameters:
    ----------
    obj : :class: `compas.geometry.Line`

    Methods:
    -------

    """

    def __init__(self, obj=None):
        super().__init__()
        self._obj = obj
        self._proto_data = LineData.LineData()

    @property
    def proto_data_type(self):
        return self._proto_data

    def to_pb(self) -> LineData.LineData:
        """Convert a Line object to a protobuf message.

        Returns
        --------
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
    def from_pb(proto_data: LineData.LineData | MessageData.AnyData) -> Line:
        """Convert a protobuf message to a Line object.

        Parameters
        -----------
        proto_data: :class:`compas_pb.data.proto.line_pb2.LineData` | :class:`compas_pb.data.proto.message_pb2.AnyData`
            The protobuf message type of LineData, or the protobuf message type of AnyData which contains LineData.

        Returns
        -------
        :class: `compas.geometry.Line`
            The converted Line object.
        """
        line_data = LineData.LineData()
        if hasattr(proto_data, "data"):
            proto_data.data.Unpack(line_data)
        else:
            line_data = proto_data
        if not line_data.IsInitialized():
            raise ValueError("No LineData has been initialized.")
        start = _ProtoBufferPoint.from_pb(line_data.start)
        end = _ProtoBufferPoint.from_pb(line_data.end)
        line = Line(start, end)
        return line


class _ProtoBufferVector(_ProtoBufferData):
    """A class to hold the protobuf data for a Vector object.

    Parameters:
    ----------
    obj : :class: `compas.geometry.Vector`

    Methods:
    -------

    """

    def __init__(self, obj=None):
        super().__init__()
        self._obj = obj
        self._proto_data = VectorData.VectorData()

    @property
    def proto_data_type(self):
        return self._proto_data

    def to_pb(self) -> VectorData.VectorData:
        """Convert a Vector object to a protobuf message.

        Returns
        -------
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
    def from_pb(proto_data: VectorData.VectorData | MessageData.AnyData) -> Vector:
        """Convert a protobuf message to a Vector object.

        Parameters
        ----------
            proto_data : :class: `compas_pb.data.proto.vector_pb2.VectorData` or \
                        :class: `compas_pb.data.proto.message_pb2.AnyData`
                The protobuf message type of VectorData.
                The protobuf message type of AnyData which contains VectorData.

        Returns
        -------
            :class: `compas.geometry.Vector`
        """
        vector_data = VectorData.VectorData()

        if hasattr(proto_data, "data"):
            proto_data.data.Unpack(vector_data)
        else:
            vector_data = proto_data
        if not vector_data.IsInitialized():
            raise ValueError("No VectorData has been initialized.")
        vector = Vector(
            vector_data.x,
            vector_data.y,
            vector_data.z,
        )
        return vector


class _ProtoBufferFrame(_ProtoBufferData):
    """A class to hold the protobuf data for a Frame object.

    Parameters:
    ----------
    obj : :class: `compas.geometry.Frame`

    Methods:
    -------
    """

    def __init__(self, obj=None):
        super().__init__()
        self._obj = obj
        self._proto_data = FrameData.FrameData()

    @property
    def proto_data_type(self):
        return self._proto_data

    def to_pb(self) -> FrameData.FrameData:
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
    def from_pb(proto_data: FrameData.FrameData | MessageData.AnyData) -> Frame:
        """Convert a protobuf message to a Frame object.

        Parameters:
        -----------
            proto_data : :class: `compas_pb.data.proto.frame_pb2.FrameData` | \
                         :class: `compas_pb.data.proto.message_pb2.AnyData`
                The protobuf message type of FrameData.
                The protobuf message type of AnyData which contains FrameData.

        Returns:
            :class: `compas.geometry.Frame`
        """
        # NOTE: Should test with Beam.
        frame_data = FrameData.FrameData()
        if hasattr(proto_data, "data"):
            proto_data.data.Unpack(frame_data)
        else:
            frame_data = proto_data

        if frame_data.IsInitialized():
            point = _ProtoBufferPoint.from_pb(frame_data.point)
            xaxis = _ProtoBufferVector.from_pb(frame_data.xaxis)
            yaxis = _ProtoBufferVector.from_pb(frame_data.yaxis)
            frame = Frame(
                point=point,
                xaxis=xaxis,
                yaxis=yaxis,
            )
            return frame
        else:
            raise ValueError("Failed to unpack FrameData from protobuf message.")


class _ProtoBufferDefault(_ProtoBufferData):
    """
    A class to hold the protobuf data for python native types.

    Parameters:
    ----------
        obj : :class: `int`, `float`, `bool`, `str`
    """

    PB_TYPE = "PrimitiveData"

    PY_TYPES_SERIALIZER = {
        int: MessageData.DataType.INT,
        float: MessageData.DataType.FLOAT,
        bool: MessageData.DataType.BOOL,
        str: MessageData.DataType.STR,
    }

    PY_TYPES_DESERIALIZER = {key.__name__.lower(): value for key, value in PY_TYPES_SERIALIZER.items()}

    def __init__(self, obj=None):
        super().__init__()
        self._obj = obj
        self._proto_data = MessageData.AnyData()

    def to_pb(self) -> MessageData.AnyData:
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
            field_name = MessageData.DataType.Name(type_obj).lower()
            data_offset = MessageData.PrimitiveData()
            setattr(data_offset, field_name, obj)
            self._proto_data.data.Pack(data_offset)
            return self._proto_data

        except TypeError as e:
            raise TypeError(f"Unsupported type: {type(obj)}: {e}")

    @staticmethod
    def from_pb(proto_data: MessageData.PrimitiveData) -> int | float | bool | str | bytes:
        """Convert a protobuf message to a python native type.

        Parameters
        -----------
            proto_data : :class: `compas_pb.data.proto.message_pb2.PrimitiveData`
                The protobuf message type of PrimitiveData.

        Returns
        -------
            data_offset : python object
                The converted python native type.
        """
        primitive_data = MessageData.PrimitiveData()
        is_unpacked = proto_data.data.Unpack(primitive_data)
        if is_unpacked:
            primitive_data_type = primitive_data.WhichOneof("data")
        try:
            type_proto_data = _ProtoBufferDefault.PY_TYPES_DESERIALIZER.get(primitive_data_type)
            if type_proto_data:
                data_offset = getattr(primitive_data, primitive_data_type)
            return data_offset
        except TypeError as e:
            raise TypeError(f"Unsupported type: {primitive_data_type}: {e}")


class ProtoBufManager(ABC):
    """Interface for plugins to use. An instance of an object implementing this interface is passed to all  ``register_serializers`` plugins."""

    @staticmethod
    def register(native_type: Any, serializer: _ProtoBufferData) -> None:
        """Register a native type and its corresponding protobuf type.

        Parameters
        ----------
        native_type : :class:`~compas.data.Data`
            The native type to register.
        protobuf_type : _ProtoBufferData
            The protobuf type to register.
        """
        raise NotImplementedError


@pluggable(category="factories", selector="collect_all")
def register_serializers(manager: ProtoBufManager) -> None:
    """Collects all the plugins which register custom serializers with _ProtoBufferAny."""
    pass


class _ProtoBufferAny(_ProtoBufferData, ProtoBufManager):
    """A class to hold the protobuf data for any object.

    Parameters
    ----------
        obj : :class:   `compas.geometry.Point`,
                        `compas.geometry.Vector`,
                        `compas.geometry.Line`,
                        `compas.geometry.Frame`
    if the object is not one of the above, and it has the atrribute from the listed above,
    it will be converted to the corresponding object type and as `data`.

    """

    # Mapping of COMPAS object types to protobuf data types
    # COMPAS type: {protobuf type: protobuf class}
    SERIALIZER = {
        Point: _ProtoBufferPoint,
        Vector: _ProtoBufferVector,
        Line: _ProtoBufferLine,
        Frame: _ProtoBufferFrame,
    }
    DESERIALIZER = {value()._proto_data.DESCRIPTOR.full_name: value for key, value in SERIALIZER.items()}
    _INITIALIZED = False

    def __init__(self, obj=None, fallback_serializer=None):
        super().__init__()
        self._obj = obj
        self._proto_data = MessageData.AnyData()
        self._fallback_serializer = fallback_serializer
        if not _ProtoBufferAny._INITIALIZED:
            register_serializers(_ProtoBufferAny)
            _ProtoBufferAny._INITIALIZED = True

    @staticmethod
    def register(native_type, serializer) -> None:
        """Register a native type and its corresponding protobuf type.

        Parameters
        ----------
        native_type : :class:`~compas.data.Data`
            The native type to register.
        serializer : _ProtoBufferData
            The serializer class to register for the native type.
        """
        if native_type in _ProtoBufferAny.SERIALIZER:
            raise ValueError(f"{native_type} is already registered.")
        _ProtoBufferAny.SERIALIZER[native_type] = serializer
        _ProtoBufferAny.DESERIALIZER[serializer().proto_data_type.DESCRIPTOR.full_name] = serializer

    def to_pb(self) -> MessageData.AnyData:
        """Convert a any object to a protobuf any message.

        Returns
        -------
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
                data_offset = pb_obj.to_pb()
                self._proto_data.data.Pack(data_offset)
            elif hasattr(obj, "__jsondump__"):
                obj_dict = {obj.__class__.__name__: obj.__jsondump__()}
                data_offset = self._fallback_serializer(obj_dict)
                self._proto_data.data.Pack(data_offset)
            else:
                self._proto_data = _ProtoBufferDefault(obj).to_pb()
            return self._proto_data
        except TypeError as e:
            raise TypeError(f"Unsupported type: {type(obj)}: {e}")

    @staticmethod
    def from_pb(proto_data: MessageData.AnyData) -> list | dict | object:
        """Convert a protobuf message to a supported COMPAS object.

        Parameters
        -----------
            proto_data : :class: `compas_pb.data.proto.message_pb2.AnyData`
                The protobuf message type of AnyData.

        Returns
        ----------
            data_offset : python object
        """
        # proto_data is a protobuf message of type AnyData
        # proto_data.data is the inner message with any message type
        # such as PointData, VectorData, LineData, FrameData, etc.

        # type.googleapis.com/<fully.qualified.message.name>
        proto_type = proto_data.data.type_url.split("/")[-1]

        try:
            pb_deserializer_cls = _ProtoBufferAny.DESERIALIZER.get(proto_type)
            if pb_deserializer_cls:
                data_offset = pb_deserializer_cls.from_pb(proto_data)
            else:
                data_offset = _ProtoBufferDefault.from_pb(proto_data)
            return data_offset
        except TypeError as e:
            raise TypeError(f"Unsupported type: {proto_type}: {e}")
