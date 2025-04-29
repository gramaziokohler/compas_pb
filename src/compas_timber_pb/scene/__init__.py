from __future__ import absolute_import

from compas.plugins import plugin
from compas_pb.data import register
from compas_timber.elements import Beam
from compas_timber_pb.data import _ProtoBufferBeam

"""
# this is now the plugin side (for example in compas_timber)

"""
@plugin
def register_serializer():
   register(Beam, _ProtoBufferBeam)
