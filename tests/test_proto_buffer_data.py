import pytest
from compas.geometry import Frame, Line, Point, Vector

from compas_pb.data.data import _ProtoBufferFrame, _ProtoBufferLine, _ProtoBufferPoint, _ProtoBufferVector


@pytest.fixture
def point():
    return Point(1, 2, 3)


@pytest.fixture
def line():
    return Line(Point(1, 2, 3), Point(4, 5, 6))


@pytest.fixture
def frame():
    return Frame(Point(1, 2, 3), Vector(4, 5, 6), Vector(7, 8, 9))


@pytest.fixture
def vector():
    return Vector(1, 2, 3)


# test protobuf class
def test_point(point):
    # Test to_pb method
    point_data = _ProtoBufferPoint(point).to_pb()
    assert point_data.name == point.name
    assert point_data.x == point.x
    assert point_data.y == point.y
    assert point_data.z == point.z

    # Test from_pb method
    restored_point = _ProtoBufferPoint.from_pb(point_data)
    assert restored_point.x == point.x
    assert restored_point.y == point.y
    assert restored_point.z == point.z


def test_line(line):
    line_data = _ProtoBufferLine(line).to_pb()
    field_names = ["start", "end"]
    attribute_names = ["name", "x", "y", "z"]

    # Test to_pb method
    for field in field_names:
        line_compas = getattr(line, field)
        line_pb = getattr(line_data, field)

        for attr in attribute_names:
            expected = getattr(line_compas, attr)
            actual = getattr(line_pb, attr)
            assert actual == expected

    # Test from_pb method
    restored_line = _ProtoBufferLine.from_pb(line_data)

    for field in field_names:
        original_point = getattr(line, field)
        restored_point = getattr(restored_line, field)

        for attr in attribute_names:
            expected = getattr(original_point, attr)
            actual = getattr(restored_point, attr)
            assert actual == expected


def test_vector(vector):
    # Test to_pb method
    vector_data = _ProtoBufferVector(vector).to_pb()
    assert vector_data.name == vector.name
    assert vector_data.x == vector.x
    assert vector_data.y == vector.y
    assert vector_data.z == vector.z

    # Test from_pb method
    restored_vector = _ProtoBufferVector.from_pb(vector_data)
    assert restored_vector.name == vector.name
    assert restored_vector.x == vector.x
    assert restored_vector.y == vector.y
    assert restored_vector.z == vector.z


def test_frame(frame):
    frame_data = _ProtoBufferFrame(frame).to_pb()
    field_names = ["point", "xaxis", "yaxis"]
    attribute_names = ["name", "x", "y", "z"]

    for field in field_names:
        frame_comaps = getattr(frame, field)
        frame_pb = getattr(frame_data, field)

        for attr in attribute_names:
            expected = getattr(frame_comaps, attr)
            actual = getattr(frame_pb, attr)
            # similair to compas.geometry close
            assert actual == pytest.approx(expected)
