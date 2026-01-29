from compas_pb.generated import geometry_pb2 as _geometry_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FaceList(_message.Message):
    __slots__ = ("indices",)
    INDICES_FIELD_NUMBER: _ClassVar[int]
    indices: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, indices: _Optional[_Iterable[int]] = ...) -> None: ...

class MeshData(_message.Message):
    __slots__ = ("guid", "name", "vertices", "faces")
    GUID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    VERTICES_FIELD_NUMBER: _ClassVar[int]
    FACES_FIELD_NUMBER: _ClassVar[int]
    guid: str
    name: str
    vertices: _containers.RepeatedCompositeFieldContainer[_geometry_pb2.PointData]
    faces: _containers.RepeatedCompositeFieldContainer[FaceList]
    def __init__(self, guid: _Optional[str] = ..., name: _Optional[str] = ..., vertices: _Optional[_Iterable[_Union[_geometry_pb2.PointData, _Mapping]]] = ..., faces: _Optional[_Iterable[_Union[FaceList, _Mapping]]] = ...) -> None: ...

class FaceData(_message.Message):
    __slots__ = ("vertex_indices",)
    VERTEX_INDICES_FIELD_NUMBER: _ClassVar[int]
    vertex_indices: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, vertex_indices: _Optional[_Iterable[int]] = ...) -> None: ...

class PolyhedronData(_message.Message):
    __slots__ = ("guid", "name", "vertices", "faces")
    GUID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    VERTICES_FIELD_NUMBER: _ClassVar[int]
    FACES_FIELD_NUMBER: _ClassVar[int]
    guid: str
    name: str
    vertices: _containers.RepeatedCompositeFieldContainer[_geometry_pb2.PointData]
    faces: _containers.RepeatedCompositeFieldContainer[FaceData]
    def __init__(self, guid: _Optional[str] = ..., name: _Optional[str] = ..., vertices: _Optional[_Iterable[_Union[_geometry_pb2.PointData, _Mapping]]] = ..., faces: _Optional[_Iterable[_Union[FaceData, _Mapping]]] = ...) -> None: ...
