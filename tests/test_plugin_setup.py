import pytest

from compas_pb.data.data import _ProtoBufferAny

from compas_pb.data.plugin_setup import initialize_plugins
from compas_timber.elements import Beam
from compas.geometry import Frame
from compas.geometry import Point
from compas.geometry import Vector

@pytest.fixture
def beam():
    return Beam(frame=..., length=10, width=5, height=3)

def test_beam_serialization():
    # Initialize plugins
    initialize_plugins()

    # Create a Beam object
    frame = Frame(Point(1.0, 2.0, 3.0), Vector(4.0, 5.0, 6.0), Vector(7.0, 8.0, 9.0))
    beam = Beam(frame=frame, length=10.0, width=5.0, height=3.0)

    # Serialize the Beam object
    proto_data = _ProtoBufferAny(beam).to_pb()

    # Deserialize the Beam object
    restored_beam = _ProtoBufferAny.from_pb(proto_data)

    # Assert equality
    assert beam.frame == restored_beam.frame
    assert beam.length == restored_beam.length
    assert beam.width == restored_beam.width
    assert beam.height == restored_beam.height
