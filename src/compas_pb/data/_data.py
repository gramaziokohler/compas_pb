from compas.datastructures import Mesh
from compas.geometry import Point
from compas.geometry import Line
from compas.geometry import Vector
from compas.geometry import Frame

from compas_pb.generated import point_pb2
from compas_pb.generated import line_pb2
from compas_pb.generated import vector_pb2
from compas_pb.generated import frame_pb2
from compas_pb.generated import mesh_pb2

from .registry import pb_serializer
from .registry import pb_deserializer


@pb_serializer(Point)
def point_to_pb(obj: Point) -> point_pb2.PointData:
    proto_data = point_pb2.PointData()
    proto_data.guid = str(obj.guid)
    proto_data.name = obj.name
    proto_data.x = obj.x
    proto_data.y = obj.y
    proto_data.z = obj.z
    return proto_data


@pb_deserializer(point_pb2)
def point_from_pb(proto_data: point_pb2.PointData) -> Point:
    return Point(
        x=proto_data.x,
        y=proto_data.y,
        z=proto_data.z,
        guid=proto_data.guid,
        name=proto_data.name
    )


@pb_serializer(Line)
def line_to_pb(line_obj: Line) -> point_pb2.LineData:
    proto_data = point_pb2.LineData()
    proto_data.guid = str(line_obj.guid)
    proto_data.name = line_obj.name

    start = point_to_pb(line_obj.start)
    end = point_to_pb(line_obj.end)

    proto_data.start.CopyFrom(start)
    proto_data.end.CopyFrom(end)

    return proto_data


@pb_deserializer(line_pb2)
def line_from_pb(proto_data: point_pb2.LineData) -> Line:
    start = point_from_pb(proto_data.start)
    end = point_from_pb(proto_data.end)

    return Line(
        start=start,
        end=end,
        guid=proto_data.guid,
        name=proto_data.name
    )


@pb_serializer(Vector)
def vector_to_pb(obj: Vector) -> vector_pb2.VectorData:
    proto_data = vector_pb2.VectorData()
    proto_data.guid = str(obj.guid)
    proto_data.name = obj.name
    proto_data.x = obj.x
    proto_data.y = obj.y
    proto_data.z = obj.z
    return proto_data


@pb_deserializer(vector_pb2)
def vector_from_pb(proto_data: vector_pb2.VectorData) -> Vector:
    return Vector(
        x=proto_data.x,
        y=proto_data.y,
        z=proto_data.z,
        guid=proto_data.guid,
        name=proto_data.name
    )


@pb_serializer(frame_pb2.FrameData)
def frame_to_pb(frame_obj: frame_pb2.FrameData) -> frame_pb2.FrameData
    proto_data = frame_pb2.FrameData()
    proto_data.guid = str(frame_obj.guid)
    proto_data.name = frame_obj.name

    origin = point_to_pb(frame_obj.origin)
    xaxis = vector_to_pb(frame_obj.xaxis)
    yaxis = vector_to_pb(frame_obj.yaxis)
    zaxis = vector_to_pb(frame_obj.zaxis)

    proto_data.origin.CopyFrom(origin)
    proto_data.xaxis.CopyFrom(xaxis)
    proto_data.yaxis.CopyFrom(yaxis)
    proto_data.zaxis.CopyFrom(zaxis)

    return proto_data


@pb_deserializer(frame_pb2)
def frame_from_pb(proto_data: frame_pb2.FrameData) -> Frame:
    origin = point_from_pb(proto_data.origin)
    xaxis = vector_from_pb(proto_data.xaxis)
    yaxis = vector_from_pb(proto_data.yaxis)
    return Frame(
        point=origin,
        xaxis=xaxis,
        yaxis=yaxis,
        guid=proto_data.guid,
        name=proto_data.name
    )


@pb_serializer(mesh_pb2.MeshData)
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


@pb_deserializer(mesh_pb2)
def from_pb(proto_data: mesh_pb2.MeshData) -> Mesh:

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

