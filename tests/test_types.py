from compas.geometry import Point
from compas.geometry import Frame
from compas.geometry import Vector
from compas.geometry import Line

from compas_pb.data import pb_dump_bts
from compas_pb.data import pb_load_bts


def test_serialize_frame():
    frame = Frame([1, 2, 3], [4, 5, 6], [7, 8, 9])

    bts = pb_dump_bts(frame)
    new_frame = pb_load_bts(bts)

    assert isinstance(new_frame, Frame)
    assert new_frame.point == frame.point
    assert new_frame.xaxis == frame.xaxis
    assert new_frame.yaxis == frame.yaxis


def test_serialize_point():
    point = Point(1, 2, 3)

    bts = pb_dump_bts(point)
    new_point = pb_load_bts(bts)

    assert isinstance(new_point, Point)
    assert new_point.x == point.x
    assert new_point.y == point.y
    assert new_point.z == point.z


def test_serialize_vector():
    vector = Vector(1, 2, 3)

    bts = pb_dump_bts(vector)
    new_vector = pb_load_bts(bts)

    assert isinstance(new_vector, Vector)
    assert new_vector.x == vector.x
    assert new_vector.y == vector.y
    assert new_vector.z == vector.z


def test_serialize_line():
    line = Line(Point(1, 2, 3), Point(4, 5, 6))

    bts = pb_dump_bts(line)
    new_line = pb_load_bts(bts)

    assert isinstance(new_line, Line)
    assert new_line.start == line.start
    assert new_line.end == line.end


def test_serialize_nested_data():
    nested_data = {
        "point": Point(1.0, 2.0, 3.0),
        "line": [Point(1.0, 2.0, 3.0), Point(4.0, 5.0, 6.0)],
        "list of Object": [Point(4.0, 5.0, 6.0), [Vector(7.0, 8.0, 9.0), Point(10.0, 11.0, 12.0)]],
        "frame": Frame(Point(1.0, 2.0, 3.0), Vector(4.0, 5.0, 6.0), Vector(7.0, 8.0, 9.0)),
        "list of primitive": ["I am String", [0.0, 0.5, 1.5], True, 5, 10],
    }

    bts = pb_dump_bts(nested_data)
    new_data = pb_load_bts(bts)

    assert isinstance(new_data["point"], Point)
    assert isinstance(new_data["line"], list) and all(isinstance(pt, Point) for pt in new_data["line"])
    assert isinstance(new_data["list of Object"], list)
    assert isinstance(new_data["frame"], Frame)
    assert isinstance(new_data["list of primitive"], list)
    assert new_data["point"] == nested_data["point"]
    assert new_data["line"] == nested_data["line"]
    assert new_data["list of Object"] == nested_data["list of Object"]
    assert new_data["frame"].point == nested_data["frame"].point
    assert new_data["frame"].xaxis == nested_data["frame"].xaxis
    assert new_data["frame"].yaxis == nested_data["frame"].yaxis
