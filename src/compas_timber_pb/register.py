from compas.plugins import plugin

from compas_pb.data.data import register
from compas_timber_pb.data.data import _ProtoBufferBeam


@plugin
def register_serializer():
    """Register serializer for compas_timber_pb"""
    from compas_timber.elements import Beam

    register(Beam, _ProtoBufferBeam)
