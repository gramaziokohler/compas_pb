from compas_timber.elements import Beam
from compas.geometry import Frame

from compas_pb.data.data import _ProtoBufferData, _ProtoBufferFrame
from compas_pb.data.proto import message_pb2 as AnyData
from compas_timber_pb.data.proto import beam_pb2 as BeamData
from compas_pb.data.proto import frame_pb2 as FrameData


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
        self._proto_data = BeamData.BeamData()

    def to_pb(self):
        """Convert a Beam object to a protobuf message.

        Returns:
        :class :`compas_pb.data.proto.beam_pb2.BeamData`
            The protobuf message type of BeamData.

        """
        beam_obj = self._obj

        if beam_obj is None:
            raise ValueError("No Beam object provided for conversion.")

        self._proto_data.guid = str(beam_obj.guid)
        self._proto_data.name = beam_obj.name
        self._proto_data.frame = _ProtoBufferFrame.to_pb(beam_obj.frame)
        self._proto_data.width = beam_obj.width
        self._proto_data.height = beam_obj.height
        self._proto_data.length = beam_obj.length

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

        if hasattr(proto_data, "beam"):
            frame = (_ProtoBufferFrame.from_pb(proto_data.beam.frame),)
            length = (proto_data.beam.length,)
            width = (proto_data.beam.width,)
            height = (proto_data.beam.height,)
        else:
            frame = (_ProtoBufferFrame.from_pb(proto_data.frame),)
            length = (proto_data.length,)
            width = (proto_data.width,)
            height = (proto_data.height,)
        beam = Beam(
            frame=frame,
            length=length,
            width=width,
            height=height,
        )
        return beam
