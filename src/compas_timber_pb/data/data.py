from compas_pb.data.data import _ProtoBufferData
from compas_timber.elements import Beam


class _ProtoBufferBeam(_ProtoBufferData):
    """A class to hold the protobuf data for a Point object.

    Parameters:
    ----------
    obj : :class: `compas.timber.elements.Beam`

    Methods:
    -------

    """

    PB_TYPE = AnyData.DataType.BEAM

    def __init__(self, obj=None):
        super().__init__()
        self._obj = obj
        self._proto_data = BeamData.PointData()

    def to_pb(self):
        """Convert a Beam object to a protobuf message.

        Returns:

        """

        beam_obj = self._obj

        if beam_obj is None:
            raise ValueError("No Point object provided for conversion.")

        self._proto_data.guid = str(beam_obj.guid)
        self._proto_data.name = beam_obj.name
        return self._proto_data

    @staticmethod
    def from_pb(proto_data):
        """Convert a protobuf message to a Point object.

        Parameters:
        proto_data : :class: `compas_pb.data.proto.point_pb2.BeamData`
            The protobuf message type of BeamData.

        Returns:
        :class: `compas.geometry.Beam`

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

