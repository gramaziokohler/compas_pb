from compas.datastructures import Mesh
from compas.geometry import Arc
from compas.geometry import Box
from compas.geometry import Circle
from compas.geometry import Cone
from compas.geometry import Cylinder
from compas.geometry import Ellipse
from compas.geometry import Frame
from compas.geometry import Line
from compas.geometry import Plane
from compas.geometry import Point
from compas.geometry import Pointcloud
from compas.geometry import Polygon
from compas.geometry import Polyline
from compas.geometry import Rotation
from compas.geometry import Sphere
from compas.geometry import Torus
from compas.geometry import Transformation
from compas.geometry import Translation
from compas.geometry import Vector

from compas_pb.generated import arc_pb2
from compas_pb.generated import box_pb2
from compas_pb.generated import circle_pb2
from compas_pb.generated import cone_pb2
from compas_pb.generated import cylinder_pb2
from compas_pb.generated import ellipse_pb2
from compas_pb.generated import frame_pb2
from compas_pb.generated import line_pb2
from compas_pb.generated import mesh_pb2
from compas_pb.generated import plane_pb2
from compas_pb.generated import point_pb2
from compas_pb.generated import pointcloud_pb2
from compas_pb.generated import polygon_pb2
from compas_pb.generated import polyline_pb2
from compas_pb.generated import rotation_pb2
from compas_pb.generated import sphere_pb2
from compas_pb.generated import torus_pb2
from compas_pb.generated import transformation_pb2
from compas_pb.generated import translation_pb2
from compas_pb.generated import vector_pb2

from .registry import pb_deserializer
from .registry import pb_serializer


# =============================================================================
# Point
# =============================================================================


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


# =============================================================================
# Line
# =============================================================================


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


# =============================================================================
# Vector
# =============================================================================


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


# =============================================================================
# Frame
# =============================================================================


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


# =============================================================================
# Mesh
# =============================================================================


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


# =============================================================================
# Circle
# =============================================================================


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


# =============================================================================
# Plane
# =============================================================================


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


# =============================================================================
# Polygon
# =============================================================================


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


# =============================================================================
# Box
# =============================================================================


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


# =============================================================================
# Arc
# =============================================================================


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


# =============================================================================
# Sphere
# =============================================================================


@pb_serializer(Sphere)
def sphere_to_pb(sphere: Sphere) -> sphere_pb2.SphereData:
    """
    Convert a COMPAS Sphere to protobuf message.

    Parameters
    ----------
    sphere : Sphere
        The COMPAS Sphere object to serialize.

    Returns
    -------
    sphere_pb2.SphereData
        The protobuf message representing the Sphere.
    """
    proto_data = sphere_pb2.SphereData()
    proto_data.guid = str(sphere.guid)
    proto_data.name = sphere.name
    proto_data.radius = sphere.radius

    frame = frame_to_pb(sphere.frame)
    proto_data.frame.CopyFrom(frame)

    return proto_data


@pb_deserializer(sphere_pb2.SphereData)
def sphere_from_pb(proto_data: sphere_pb2.SphereData) -> Sphere:
    """
    Convert a protobuf message to COMPAS Sphere.

    Parameters
    ----------
    proto_data : sphere_pb2.SphereData
        The protobuf message representing a Sphere.

    Returns
    -------
    Sphere
        The deserialized COMPAS Sphere object.
    """
    frame = frame_from_pb(proto_data.frame)
    result = Sphere(radius=proto_data.radius, frame=frame, name=proto_data.name)
    result._guid = proto_data.guid
    return result


# =============================================================================
# Cylinder
# =============================================================================


@pb_serializer(Cylinder)
def cylinder_to_pb(cylinder: Cylinder) -> cylinder_pb2.CylinderData:
    """
    Convert a COMPAS Cylinder to protobuf message.

    Parameters
    ----------
    cylinder : Cylinder
        The COMPAS Cylinder object to serialize.

    Returns
    -------
    cylinder_pb2.CylinderData
        The protobuf message representing the Cylinder.
    """
    proto_data = cylinder_pb2.CylinderData()
    proto_data.guid = str(cylinder.guid)
    proto_data.name = cylinder.name
    proto_data.radius = cylinder.radius
    proto_data.height = cylinder.height

    frame = frame_to_pb(cylinder.frame)
    proto_data.frame.CopyFrom(frame)

    return proto_data


@pb_deserializer(cylinder_pb2.CylinderData)
def cylinder_from_pb(proto_data: cylinder_pb2.CylinderData) -> Cylinder:
    """
    Convert a protobuf message to COMPAS Cylinder.

    Parameters
    ----------
    proto_data : cylinder_pb2.CylinderData
        The protobuf message representing a Cylinder.

    Returns
    -------
    Cylinder
        The deserialized COMPAS Cylinder object.
    """
    frame = frame_from_pb(proto_data.frame)
    result = Cylinder(radius=proto_data.radius, height=proto_data.height, frame=frame, name=proto_data.name)
    result._guid = proto_data.guid
    return result


# =============================================================================
# Cone
# =============================================================================


@pb_serializer(Cone)
def cone_to_pb(cone: Cone) -> cone_pb2.ConeData:
    """
    Convert a COMPAS Cone to protobuf message.

    Parameters
    ----------
    cone : Cone
        The COMPAS Cone object to serialize.

    Returns
    -------
    cone_pb2.ConeData
        The protobuf message representing the Cone.
    """
    proto_data = cone_pb2.ConeData()
    proto_data.guid = str(cone.guid)
    proto_data.name = cone.name
    proto_data.radius = cone.radius
    proto_data.height = cone.height

    frame = frame_to_pb(cone.frame)
    proto_data.frame.CopyFrom(frame)

    return proto_data


@pb_deserializer(cone_pb2.ConeData)
def cone_from_pb(proto_data: cone_pb2.ConeData) -> Cone:
    """
    Convert a protobuf message to COMPAS Cone.

    Parameters
    ----------
    proto_data : cone_pb2.ConeData
        The protobuf message representing a Cone.

    Returns
    -------
    Cone
        The deserialized COMPAS Cone object.
    """
    frame = frame_from_pb(proto_data.frame)
    result = Cone(radius=proto_data.radius, height=proto_data.height, frame=frame, name=proto_data.name)
    result._guid = proto_data.guid
    return result


# =============================================================================
# Torus
# =============================================================================


@pb_serializer(Torus)
def torus_to_pb(torus: Torus) -> torus_pb2.TorusData:
    """
    Convert a COMPAS Torus to protobuf message.

    Parameters
    ----------
    torus : Torus
        The COMPAS Torus object to serialize.

    Returns
    -------
    torus_pb2.TorusData
        The protobuf message representing the Torus.
    """
    proto_data = torus_pb2.TorusData()
    proto_data.guid = str(torus.guid)
    proto_data.name = torus.name
    proto_data.radius_axis = torus.radius_axis
    proto_data.radius_pipe = torus.radius_pipe

    frame = frame_to_pb(torus.frame)
    proto_data.frame.CopyFrom(frame)

    return proto_data


@pb_deserializer(torus_pb2.TorusData)
def torus_from_pb(proto_data: torus_pb2.TorusData) -> Torus:
    """
    Convert a protobuf message to COMPAS Torus.

    Parameters
    ----------
    proto_data : torus_pb2.TorusData
        The protobuf message representing a Torus.

    Returns
    -------
    Torus
        The deserialized COMPAS Torus object.
    """
    frame = frame_from_pb(proto_data.frame)
    result = Torus(radius_axis=proto_data.radius_axis, radius_pipe=proto_data.radius_pipe, frame=frame, name=proto_data.name)
    result._guid = proto_data.guid
    return result


# =============================================================================
# Ellipse
# =============================================================================


@pb_serializer(Ellipse)
def ellipse_to_pb(ellipse: Ellipse) -> ellipse_pb2.EllipseData:
    """
    Convert a COMPAS Ellipse to protobuf message.

    Parameters
    ----------
    ellipse : Ellipse
        The COMPAS Ellipse object to serialize.

    Returns
    -------
    ellipse_pb2.EllipseData
        The protobuf message representing the Ellipse.
    """
    proto_data = ellipse_pb2.EllipseData()
    proto_data.guid = str(ellipse.guid)
    proto_data.name = ellipse.name
    proto_data.major = ellipse.major
    proto_data.minor = ellipse.minor

    frame = frame_to_pb(ellipse.frame)
    proto_data.frame.CopyFrom(frame)

    return proto_data


@pb_deserializer(ellipse_pb2.EllipseData)
def ellipse_from_pb(proto_data: ellipse_pb2.EllipseData) -> Ellipse:
    """
    Convert a protobuf message to COMPAS Ellipse.

    Parameters
    ----------
    proto_data : ellipse_pb2.EllipseData
        The protobuf message representing an Ellipse.

    Returns
    -------
    Ellipse
        The deserialized COMPAS Ellipse object.
    """
    frame = frame_from_pb(proto_data.frame)
    result = Ellipse(major=proto_data.major, minor=proto_data.minor, frame=frame, name=proto_data.name)
    result._guid = proto_data.guid
    return result


# =============================================================================
# Polyline
# =============================================================================


@pb_serializer(Polyline)
def polyline_to_pb(polyline: Polyline) -> polyline_pb2.PolylineData:
    """
    Convert a COMPAS Polyline to protobuf message.

    Parameters
    ----------
    polyline : Polyline
        The COMPAS Polyline object to serialize.

    Returns
    -------
    polyline_pb2.PolylineData
        The protobuf message representing the Polyline.
    """
    proto_data = polyline_pb2.PolylineData()
    proto_data.guid = str(polyline.guid)
    proto_data.name = polyline.name

    for point in polyline.points:
        proto_point = point_to_pb(point)
        proto_data.points.append(proto_point)

    return proto_data


@pb_deserializer(polyline_pb2.PolylineData)
def polyline_from_pb(proto_data: polyline_pb2.PolylineData) -> Polyline:
    """
    Convert a protobuf message to COMPAS Polyline.

    Parameters
    ----------
    proto_data : polyline_pb2.PolylineData
        The protobuf message representing a Polyline.

    Returns
    -------
    Polyline
        The deserialized COMPAS Polyline object.
    """
    points = [point_from_pb(proto_point) for proto_point in proto_data.points]
    result = Polyline(points=points, name=proto_data.name)
    result._guid = proto_data.guid
    return result


# =============================================================================
# Pointcloud
# =============================================================================


@pb_serializer(Pointcloud)
def pointcloud_to_pb(pointcloud: Pointcloud) -> pointcloud_pb2.PointcloudData:
    """
    Convert a COMPAS Pointcloud to protobuf message.

    Parameters
    ----------
    pointcloud : Pointcloud
        The COMPAS Pointcloud object to serialize.

    Returns
    -------
    pointcloud_pb2.PointcloudData
        The protobuf message representing the Pointcloud.
    """
    proto_data = pointcloud_pb2.PointcloudData()
    proto_data.guid = str(pointcloud.guid)
    proto_data.name = pointcloud.name

    for point in pointcloud.points:
        proto_point = point_to_pb(point)
        proto_data.points.append(proto_point)

    return proto_data


@pb_deserializer(pointcloud_pb2.PointcloudData)
def pointcloud_from_pb(proto_data: pointcloud_pb2.PointcloudData) -> Pointcloud:
    """
    Convert a protobuf message to COMPAS Pointcloud.

    Parameters
    ----------
    proto_data : pointcloud_pb2.PointcloudData
        The protobuf message representing a Pointcloud.

    Returns
    -------
    Pointcloud
        The deserialized COMPAS Pointcloud object.
    """
    points = [point_from_pb(proto_point) for proto_point in proto_data.points]
    result = Pointcloud(points=points, name=proto_data.name)
    result._guid = proto_data.guid
    return result


# =============================================================================
# Transformation
# =============================================================================


@pb_serializer(Transformation)
def transformation_to_pb(transformation: Transformation) -> transformation_pb2.TransformationData:
    """
    Convert a COMPAS Transformation to protobuf message.

    Parameters
    ----------
    transformation : Transformation
        The COMPAS Transformation object to serialize.

    Returns
    -------
    transformation_pb2.TransformationData
        The protobuf message representing the Transformation.
    """
    proto_data = transformation_pb2.TransformationData()
    proto_data.guid = str(transformation.guid)
    proto_data.name = transformation.name

    # Flatten 4x4 matrix to list of 16 floats
    matrix = transformation.matrix
    for row in matrix:
        for value in row:
            proto_data.matrix.append(value)

    return proto_data


@pb_deserializer(transformation_pb2.TransformationData)
def transformation_from_pb(proto_data: transformation_pb2.TransformationData) -> Transformation:
    """
    Convert a protobuf message to COMPAS Transformation.

    Parameters
    ----------
    proto_data : transformation_pb2.TransformationData
        The protobuf message representing a Transformation.

    Returns
    -------
    Transformation
        The deserialized COMPAS Transformation object.
    """
    # Convert flat list of 16 floats back to 4x4 matrix
    matrix_flat = list(proto_data.matrix)
    matrix = []
    for i in range(4):
        row = []
        for j in range(4):
            row.append(matrix_flat[i * 4 + j])
        matrix.append(row)

    result = Transformation.from_matrix(matrix)
    result.name = proto_data.name
    result._guid = proto_data.guid
    return result


# =============================================================================
# Translation
# =============================================================================


@pb_serializer(Translation)
def translation_to_pb(translation: Translation) -> translation_pb2.TranslationData:
    """
    Convert a COMPAS Translation to protobuf message.

    Parameters
    ----------
    translation : Translation
        The COMPAS Translation object to serialize.

    Returns
    -------
    translation_pb2.TranslationData
        The protobuf message representing the Translation.
    """
    proto_data = translation_pb2.TranslationData()
    proto_data.guid = str(translation.guid)
    proto_data.name = translation.name

    vector = vector_to_pb(translation.translation_vector)
    proto_data.translation_vector.CopyFrom(vector)

    return proto_data


@pb_deserializer(translation_pb2.TranslationData)
def translation_from_pb(proto_data: translation_pb2.TranslationData) -> Translation:
    """
    Convert a protobuf message to COMPAS Translation.

    Parameters
    ----------
    proto_data : translation_pb2.TranslationData
        The protobuf message representing a Translation.

    Returns
    -------
    Translation
        The deserialized COMPAS Translation object.
    """
    vector = vector_from_pb(proto_data.translation_vector)
    result = Translation.from_vector(vector)
    result.name = proto_data.name
    result._guid = proto_data.guid
    return result


# =============================================================================
# Rotation
# =============================================================================


@pb_serializer(Rotation)
def rotation_to_pb(rotation: Rotation) -> rotation_pb2.RotationData:
    """
    Convert a COMPAS Rotation to protobuf message.

    Parameters
    ----------
    rotation : Rotation
        The COMPAS Rotation object to serialize.

    Returns
    -------
    rotation_pb2.RotationData
        The protobuf message representing the Rotation.
    """
    proto_data = rotation_pb2.RotationData()
    proto_data.guid = str(rotation.guid)
    proto_data.name = rotation.name

    # Get axis and angle from the rotation
    axis_angle = rotation.axis_and_angle
    axis = axis_angle[0]
    angle = axis_angle[1]

    proto_axis = vector_to_pb(axis)
    proto_data.axis.CopyFrom(proto_axis)
    proto_data.angle = angle

    # Use origin as the default point of rotation
    from compas.geometry import Point

    point = Point(0, 0, 0)
    proto_point = point_to_pb(point)
    proto_data.point.CopyFrom(proto_point)

    return proto_data


@pb_deserializer(rotation_pb2.RotationData)
def rotation_from_pb(proto_data: rotation_pb2.RotationData) -> Rotation:
    """
    Convert a protobuf message to COMPAS Rotation.

    Parameters
    ----------
    proto_data : rotation_pb2.RotationData
        The protobuf message representing a Rotation.

    Returns
    -------
    Rotation
        The deserialized COMPAS Rotation object.
    """
    axis = vector_from_pb(proto_data.axis)
    angle = proto_data.angle

    result = Rotation.from_axis_and_angle(axis, angle)
    result.name = proto_data.name
    result._guid = proto_data.guid
    return result
