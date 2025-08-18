from compas.geometry import Point
from compas.geometry import Frame
from compas.geometry import Vector
from compas.geometry import Line
from compas.geometry import Plane
from compas.geometry import Polygon
from compas.geometry import Box
from compas.geometry import Arc
from compas.geometry import Circle

from compas_pb import pb_dump_bts
from compas_pb import pb_load_bts


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


def test_serialize_plane():
    plane = Plane(Point(1, 2, 3), Vector(0, 0, 1))

    bts = pb_dump_bts(plane)
    new_plane = pb_load_bts(bts)

    assert isinstance(new_plane, Plane)
    assert new_plane.point == plane.point
    assert new_plane.normal == plane.normal


def test_serialize_polygon():
    polygon = Polygon([(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)])

    bts = pb_dump_bts(polygon)
    new_polygon = pb_load_bts(bts)

    assert isinstance(new_polygon, Polygon)
    assert len(new_polygon.points) == len(polygon.points)
    for orig_pt, new_pt in zip(polygon.points, new_polygon.points):
        assert orig_pt == new_pt


def test_serialize_box():
    box = Box.from_width_height_depth(2, 3, 4)

    bts = pb_dump_bts(box)
    new_box = pb_load_bts(bts)

    assert isinstance(new_box, Box)
    assert new_box.xsize == box.xsize
    assert new_box.ysize == box.ysize
    assert new_box.zsize == box.zsize
    assert new_box.frame.point == box.frame.point


def test_serialize_arc():
    import math
    
    frame = Frame.worldXY()
    circle = Circle(frame=frame, radius=2.0)
    arc = Arc.from_circle(circle, 0, math.pi/2)  # quarter circle

    bts = pb_dump_bts(arc)
    new_arc = pb_load_bts(bts)

    assert isinstance(new_arc, Arc)
    assert abs(new_arc.start_angle - arc.start_angle) < 1e-6
    assert abs(new_arc.end_angle - arc.end_angle) < 1e-6
    assert new_arc.circle.radius == arc.circle.radius
