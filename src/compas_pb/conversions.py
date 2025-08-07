from compas.datastructures import Mesh
from compas.geometry import Circle
from compas.geometry import Frame
from compas.geometry import Line
from compas.geometry import Point
from compas.geometry import Vector

from compas_pb.generated import circle_pb2
from compas_pb.generated import frame_pb2
from compas_pb.generated import line_pb2
from compas_pb.generated import mesh_pb2
from compas_pb.generated import point_pb2
from compas_pb.generated import vector_pb2

from .registry import pb_deserializer
from .registry import pb_serializer


@pb_serializer(Point)
def point_to_pb(obj: Point) -> point_pb2.PointData:
    proto_data = point_pb2.PointData()
    proto_data.guid = str(obj.guid)
    proto_data.name = obj.name
    proto_data.x = obj.x
    proto_data.y = obj.y
    proto_data.z = obj.z
    return proto_data


@pb_deserializer(point_pb2.PointData)
def point_from_pb(proto_data: point_pb2.PointData) -> Point:
    return Point(x=proto_data.x, y=proto_data.y, z=proto_data.z, name=proto_data.name)


@pb_serializer(Line)
def line_to_pb(line_obj: Line) -> line_pb2.LineData:
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
    start = point_from_pb(proto_data.start)
    end = point_from_pb(proto_data.end)

    return Line(start=start, end=end, name=proto_data.name)


@pb_serializer(Vector)
def vector_to_pb(obj: Vector) -> vector_pb2.VectorData:
    proto_data = vector_pb2.VectorData()
    proto_data.name = obj.name
    proto_data.x = obj.x
    proto_data.y = obj.y
    proto_data.z = obj.z
    return proto_data


@pb_deserializer(vector_pb2.VectorData)
def vector_from_pb(proto_data: vector_pb2.VectorData) -> Vector:
    return Vector(x=proto_data.x, y=proto_data.y, z=proto_data.z, name=proto_data.name)


@pb_serializer(Frame)
def frame_to_pb(frame_obj: Frame) -> frame_pb2.FrameData:
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
    origin = point_from_pb(proto_data.point)
    xaxis = vector_from_pb(proto_data.xaxis)
    yaxis = vector_from_pb(proto_data.yaxis)
    return Frame(point=origin, xaxis=xaxis, yaxis=yaxis, name=proto_data.name)


@pb_serializer(Mesh)
def mesh_to_pb(mesh: Mesh) -> mesh_pb2.MeshData:
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
    result = circle_pb2.CircleData()
    result.guid = str(circle.guid)
    result.name = circle.name or "Circle"
    result.radius = circle.radius
    result.frame.CopyFrom(frame_to_pb(circle.frame))
    return result


@pb_deserializer(circle_pb2.CircleData)
def circle_from_pb(proto_data: circle_pb2.CircleData) -> Circle:
    frame = frame_from_pb(proto_data.frame)
    result = Circle(radius=proto_data.radius, frame=frame, name=proto_data.name)
    result._guid = proto_data.guid
    return result
