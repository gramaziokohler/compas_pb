import pytest
import tempfile
from pathlib import Path

from compas.geometry import Frame

from compas_pb.data import pb_dump
from compas_pb.data import pb_load
from compas_pb.data import ProtoBufferAny


@pytest.fixture
def frame_data_path():
    return "tests/test_data/frame.data"


def test_register_plugins_called(mocker, frame_data_path):
    mock_register = mocker.patch("compas_pb.data.data._discover_serializers")
    data = pb_load(frame_data_path)

    # register_serializers should be called at least once during deserialization
    mock_register.assert_called()

    assert data is not None
    assert data == Frame.worldXY()


def test_pb_dump_and_load_equivalence(mocker):
    """Test that pb_dump and pb_load work correctly together."""
    ProtoBufferAny._INITIALIZED = False
    # Create a temporary file
    mock_register = mocker.patch("compas_pb.data.data._discover_serializers")

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir) / "frame_out.data"
        tmp_path = str(tmp_path)
        frame = Frame.worldXY()

        # Dump the Frame
        pb_dump(frame, tmp_path)

        # register_serializers should be called during serialization
        mock_register.assert_called()

        # Load it back
        loaded = pb_load(tmp_path)

        # Verify contents
        assert isinstance(loaded, Frame)
        assert loaded == frame  # Assumes __eq__ is implemented correctly
