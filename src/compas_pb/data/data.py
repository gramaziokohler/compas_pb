from abc import ABC
from abc import abstractmethod

from compas.plugins import pluggable

from compas_pb.generated import message_pb2 as MessageData

from .registry import SerialzerRegistry


# NOTE: PUT More Docstring in the class docstring
class ProtoBufferData(ABC):
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


# TODO: eventually make this class just `primitive_to_pb` and `primitive_from_pb`
# TODO: the state is not really needed here
class ProtoBufferDefault(ProtoBufferData):
    """
    A class to hold the protobuf data for python native types.

    Parameters:
    ----------
        obj : :class: `int`, `float`, `bool`, `str`
    """

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
            self._obj = "None"  # HACK: find proper way to handle None
            # raise ValueError("No object provided for conversion.")
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
        if not is_unpacked:
            # TODO: this really shouldn't be reached. if we're here it means it's some type which is not a primitive and hasn't been registered
            raise ValueError(f"Unknown data type: {proto_data.data.type_url}")
        type_ = primitive_data.WhichOneof("data")
        if type_ == "int":
            data_offset = primitive_data.int
        elif type_ == "float":
            data_offset = primitive_data.float
        elif type_ == "bool":
            data_offset = primitive_data.bool
        elif type_ == "str":
            data_offset = primitive_data.str
        else:
            raise ValueError(f"Unsupported primitive type: {type_}")

        return data_offset


@pluggable(category="factories", selector="collect_all")
def register_serializers() -> None:
    """Collects all the plugins which register custom serializers with _ProtoBufferAny."""
    pass


# TODO: eventually make this class just `any_to_pb` and `any_from_pb`
# TODO: the state is not really needed here
class ProtoBufferAny(ProtoBufferData):
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
    _INITIALIZED = False

    def __init__(self, obj=None, fallback_serializer=None):
        super().__init__()
        self._obj = obj
        self._proto_data = MessageData.AnyData()
        self._fallback_serializer = fallback_serializer
        if not ProtoBufferAny._INITIALIZED:
            register_serializers()
            ProtoBufferAny._INITIALIZED = True

    def to_pb(self) -> MessageData.AnyData:
        """Convert a any object to a protobuf any message.

        Returns
        -------
            :class: `compas_pb.data.proto.message_pb2.AnyData`
                The protobuf message type of AnyData.

        """

        if self._obj is None:
            obj = "None"  # HACK: find proper way to handle None
            # raise ValueError("No object provided for conversion.")

        obj = self._obj

        try:
            serializer = SerialzerRegistry.get_serializer(obj)
            if serializer:
                pb_obj = serializer(obj)
                self._proto_data.data.Pack(pb_obj)
            elif hasattr(obj, "__jsondump__"):
                obj_dict = {obj.__class__.__name__: obj.__jsondump__()}
                data_offset = self._fallback_serializer(obj_dict)
                self._proto_data.data.Pack(data_offset)
            else:
                self._proto_data = ProtoBufferDefault(obj).to_pb()
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
            deserializer = SerialzerRegistry.get_deserializer(proto_type)
            if deserializer:
                unpacked_instance = deserializer.__deserializer_type__()
                _ = proto_data.data.Unpack(unpacked_instance)
                data_offset = deserializer(unpacked_instance)
            else:
                data_offset = ProtoBufferDefault.from_pb(proto_data)
            return data_offset
        except TypeError as e:
            raise TypeError(f"Unsupported type: {proto_type}: {e}")
