from compas.datastructures import Mesh
from compas.geometry import Arc
from compas.geometry import Box
from compas.geometry import Circle
from compas.geometry import Frame
from compas.geometry import Line
from compas.geometry import Plane
from compas.geometry import Point
from compas.geometry import Polygon
from compas.geometry import Vector

from compas_pb.generated import arc_pb2
from compas_pb.generated import box_pb2
from compas_pb.generated import circle_pb2
from compas_pb.generated import frame_pb2
from compas_pb.generated import line_pb2
from compas_pb.generated import mesh_pb2
from compas_pb.generated import plane_pb2
from compas_pb.generated import point_pb2
from compas_pb.generated import polygon_pb2
from compas_pb.generated import vector_pb2

from .registry import pb_deserializer
from .registry import pb_serializer


@pb_serializer(Point)
def point_to_pb(obj: Point) -> point_pb2.PointData:
    """
    Convert a COMPAS Point to protobuf message.

    Parameters
    ----------
    obj : Point
        The COMPAS Point object to serialize.

    Returns
    -------
    point_pb2.PointData
        The protobuf message representing the Point.
    """
    proto_data = point_pb2.PointData()
    proto_data.guid = str(obj.guid)
    proto_data.name = obj.name
    proto_data.x = obj.x
    proto_data.y = obj.y
    proto_data.z = obj.z
    return proto_data


@pb_deserializer(point_pb2.PointData)
def point_from_pb(proto_data: point_pb2.PointData) -> Point:
    """
    Convert a protobuf message to COMPAS Point.

    Parameters
    ----------
    proto_data : point_pb2.PointData
        The protobuf message representing a Point.

    Returns
    -------
    Point
        The deserialized COMPAS Point object.
    """
    return Point(x=proto_data.x, y=proto_data.y, z=proto_data.z, name=proto_data.name)


@pb_serializer(Line)
def line_to_pb(line_obj: Line) -> line_pb2.LineData:
    """
    Convert a COMPAS Line to protobuf message.

    Parameters
    ----------
    line_obj : Line
        The COMPAS Line object to serialize.

    Returns
    -------
    line_pb2.LineData
        The protobuf message representing the Line.
    """
    proto_data = line_pb2.LineData()
    proto_data.guid = str(line_obj.guid)
    proto_data.name = line_obj.name

    start = point_to_pb(line_obj.start)
    end = point_to_pb(line_obj.end)

    proto_data.start.CopyFrom(start)
    proto_data.end.CopyFrom(end)

    return proto_data


@pb_deserializer(line_pb2.LineData)
def line_from_pb(proto_data: line_pb2.LineData) -> Line:
    """
    Convert a protobuf message to COMPAS Line.

    Parameters
    ----------
    proto_data : line_pb2.LineData
        The protobuf message representing a Line.

    Returns
    -------
    Line
        The deserialized COMPAS Line object.
    """
    start = point_from_pb(proto_data.start)
    end = point_from_pb(proto_data.end)

    return Line(start=start, end=end, name=proto_data.name)


@pb_serializer(Vector)
def vector_to_pb(obj: Vector) -> vector_pb2.VectorData:
    """
    Convert a COMPAS Vector to protobuf message.

    Parameters
    ----------
    obj : Vector
        The COMPAS Vector object to serialize.

    Returns
    -------
    vector_pb2.VectorData
        The protobuf message representing the Vector.
    """
    proto_data = vector_pb2.VectorData()
    proto_data.name = obj.name
    proto_data.x = obj.x
    proto_data.y = obj.y
    proto_data.z = obj.z
    return proto_data


@pb_deserializer(vector_pb2.VectorData)
def vector_from_pb(proto_data: vector_pb2.VectorData) -> Vector:
    """
    Convert a protobuf message to COMPAS Vector.

    Parameters
    ----------
    proto_data : vector_pb2.VectorData
        The protobuf message representing a Vector.

    Returns
    -------
    Vector
        The deserialized COMPAS Vector object.
    """
    return Vector(x=proto_data.x, y=proto_data.y, z=proto_data.z, name=proto_data.name)


@pb_serializer(Frame)
def frame_to_pb(frame_obj: Frame) -> frame_pb2.FrameData:
    """
    Convert a COMPAS Frame to protobuf message.

    Parameters
    ----------
    frame_obj : Frame
        The COMPAS Frame object to serialize.

    Returns
    -------
    frame_pb2.FrameData
        The protobuf message representing the Frame.
    """
    proto_data = frame_pb2.FrameData()
    proto_data.guid = str(frame_obj.guid)
    proto_data.name = frame_obj.name

    origin = point_to_pb(frame_obj.point)
    xaxis = vector_to_pb(frame_obj.xaxis)
    yaxis = vector_to_pb(frame_obj.yaxis)

    proto_data.point.CopyFrom(origin)
    proto_data.xaxis.CopyFrom(xaxis)
    proto_data.yaxis.CopyFrom(yaxis)

    return proto_data


@pb_deserializer(frame_pb2.FrameData)
def frame_from_pb(proto_data: frame_pb2.FrameData) -> Frame:
    """
    Convert a protobuf message to COMPAS Frame.

    Parameters
    ----------
    proto_data : frame_pb2.FrameData
        The protobuf message representing a Frame.

    Returns
    -------
    Frame
        The deserialized COMPAS Frame object.
    """
    origin = point_from_pb(proto_data.point)
    xaxis = vector_from_pb(proto_data.xaxis)
    yaxis = vector_from_pb(proto_data.yaxis)
    return Frame(point=origin, xaxis=xaxis, yaxis=yaxis, name=proto_data.name)


@pb_serializer(Mesh)
def mesh_to_pb(mesh: Mesh) -> mesh_pb2.MeshData:
    """
    Convert a COMPAS Mesh to protobuf message.

    Parameters
    ----------
    mesh : Mesh
        The COMPAS Mesh object to serialize.

    Returns
    -------
    mesh_pb2.MeshData
        The protobuf message representing the Mesh.
    """
    proto_data = mesh_pb2.MeshData()
    proto_data.guid = str(mesh.guid)
    proto_data.name = mesh.name or "Mesh"

    index_map = {}  # vertex_key → index
    for index, (key, attr) in enumerate(mesh.vertices(data=True)):
        point = Point(*mesh.vertex_coordinates(key))
        proto_data.vertices.append(point_to_pb(point))
        index_map[key] = index

    for fkey in mesh.faces():
        indices = [index_map[vkey] for vkey in mesh.face_vertices(fkey)]
        face_msg = mesh_pb2.FaceList()
        face_msg.indices.extend(indices)
        proto_data.faces.append(face_msg)

    return proto_data


@pb_deserializer(mesh_pb2.MeshData)
def mesh_from_pb(proto_data: mesh_pb2.MeshData) -> Mesh:
    """
    Convert a protobuf message to COMPAS Mesh.

    Parameters
    ----------
    proto_data : mesh_pb2.MeshData
        The protobuf message representing a Mesh.

    Returns
    -------
    Mesh
        The deserialized COMPAS Mesh object.
    """
    mesh = Mesh(guid=proto_data.guid, name=proto_data.name)
    vertex_map = []

    for pb_point in proto_data.vertices:
        point = point_from_pb(pb_point)
        key = mesh.add_vertex(x=point.x, y=point.y, z=point.z)
        vertex_map.append(key)

    for face in proto_data.faces:
        indices = [vertex_map[i] for i in face.indices]
        mesh.add_face(indices)

    return mesh


@pb_serializer(Circle)
def circle_to_pb(circle: Circle) -> circle_pb2.CircleData:
    """
    Convert a COMPAS Circle to protobuf message.

    Parameters
    ----------
    circle : Circle
        The COMPAS Circle object to serialize.

    Returns
    -------
    circle_pb2.CircleData
        The protobuf message representing the Circle.
    """
    result = circle_pb2.CircleData()
    result.guid = str(circle.guid)
    result.name = circle.name or "Circle"
    result.radius = circle.radius
    result.frame.CopyFrom(frame_to_pb(circle.frame))
    return result


@pb_deserializer(circle_pb2.CircleData)
def circle_from_pb(proto_data: circle_pb2.CircleData) -> Circle:
    """
    Convert a protobuf message to COMPAS Circle.

    Parameters
    ----------
    proto_data : circle_pb2.CircleData
        The protobuf message representing a Circle.

    Returns
    -------
    Circle
        The deserialized COMPAS Circle object.
    """
    frame = frame_from_pb(proto_data.frame)
    result = Circle(radius=proto_data.radius, frame=frame, name=proto_data.name)
    result._guid = proto_data.guid
    return result


@pb_serializer(Plane)
def plane_to_pb(plane: Plane) -> plane_pb2.PlaneData:
    """
    Convert a COMPAS Plane to protobuf message.

    Parameters
    ----------
    plane : Plane
        The COMPAS Plane object to serialize.

    Returns
    -------
    plane_pb2.PlaneData
        The protobuf message representing the Plane.
    """
    proto_data = plane_pb2.PlaneData()
    proto_data.guid = str(plane.guid)
    proto_data.name = plane.name

    point = point_to_pb(plane.point)
    normal = vector_to_pb(plane.normal)

    proto_data.point.CopyFrom(point)
    proto_data.normal.CopyFrom(normal)

    return proto_data


@pb_deserializer(plane_pb2.PlaneData)
def plane_from_pb(proto_data: plane_pb2.PlaneData) -> Plane:
    """
    Convert a protobuf message to COMPAS Plane.

    Parameters
    ----------
    proto_data : plane_pb2.PlaneData
        The protobuf message representing a Plane.

    Returns
    -------
    Plane
        The deserialized COMPAS Plane object.
    """
    point = point_from_pb(proto_data.point)
    normal = vector_from_pb(proto_data.normal)
    result = Plane(point=point, normal=normal, name=proto_data.name)
    result._guid = proto_data.guid
    return result


@pb_serializer(Polygon)
def polygon_to_pb(polygon: Polygon) -> polygon_pb2.PolygonData:
    """
    Convert a COMPAS Polygon to protobuf message.

    Parameters
    ----------
    polygon : Polygon
        The COMPAS Polygon object to serialize.

    Returns
    -------
    polygon_pb2.PolygonData
        The protobuf message representing the Polygon.
    """
    proto_data = polygon_pb2.PolygonData()
    proto_data.guid = str(polygon.guid)
    proto_data.name = polygon.name

    for point in polygon.points:
        proto_point = point_to_pb(point)
        proto_data.points.append(proto_point)

    return proto_data


@pb_deserializer(polygon_pb2.PolygonData)
def polygon_from_pb(proto_data: polygon_pb2.PolygonData) -> Polygon:
    """
    Convert a protobuf message to COMPAS Polygon.

    Parameters
    ----------
    proto_data : polygon_pb2.PolygonData
        The protobuf message representing a Polygon.

    Returns
    -------
    Polygon
        The deserialized COMPAS Polygon object.
    """
    points = [point_from_pb(proto_point) for proto_point in proto_data.points]
    result = Polygon(points=points, name=proto_data.name)
    result._guid = proto_data.guid
    return result


@pb_serializer(Box)
def box_to_pb(box: Box) -> box_pb2.BoxData:
    """
    Convert a COMPAS Box to protobuf message.

    Parameters
    ----------
    box : Box
        The COMPAS Box object to serialize.

    Returns
    -------
    box_pb2.BoxData
        The protobuf message representing the Box.
    """
    proto_data = box_pb2.BoxData()
    proto_data.guid = str(box.guid)
    proto_data.name = box.name
    proto_data.xsize = box.xsize
    proto_data.ysize = box.ysize
    proto_data.zsize = box.zsize

    frame = frame_to_pb(box.frame)
    proto_data.frame.CopyFrom(frame)

    return proto_data


@pb_deserializer(box_pb2.BoxData)
def box_from_pb(proto_data: box_pb2.BoxData) -> Box:
    """
    Convert a protobuf message to COMPAS Box.

    Parameters
    ----------
    proto_data : box_pb2.BoxData
        The protobuf message representing a Box.

    Returns
    -------
    Box
        The deserialized COMPAS Box object.
    """
    frame = frame_from_pb(proto_data.frame)
    result = Box(frame=frame, xsize=proto_data.xsize, ysize=proto_data.ysize, zsize=proto_data.zsize, name=proto_data.name)
    result._guid = proto_data.guid
    return result


@pb_serializer(Arc)
def arc_to_pb(arc: Arc) -> arc_pb2.ArcData:
    """
    Convert a COMPAS Arc to protobuf message.

    Parameters
    ----------
    arc : Arc
        The COMPAS Arc object to serialize.

    Returns
    -------
    arc_pb2.ArcData
        The protobuf message representing the Arc.
    """
    proto_data = arc_pb2.ArcData()
    proto_data.guid = str(arc.guid)
    proto_data.name = arc.name
    proto_data.start_angle = arc.start_angle
    proto_data.end_angle = arc.end_angle

    circle = circle_to_pb(arc.circle)
    proto_data.circle.CopyFrom(circle)

    return proto_data


@pb_deserializer(arc_pb2.ArcData)
def arc_from_pb(proto_data: arc_pb2.ArcData) -> Arc:
    """
    Convert a protobuf message to COMPAS Arc.

    Parameters
    ----------
    proto_data : arc_pb2.ArcData
        The protobuf message representing an Arc.

    Returns
    -------
    Arc
        The deserialized COMPAS Arc object.
    """
    circle = circle_from_pb(proto_data.circle)
    result = Arc.from_circle(circle, proto_data.start_angle, proto_data.end_angle)
    result.name = proto_data.name
    result._guid = proto_data.guid
    return result
