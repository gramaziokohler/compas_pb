# Protocol Documentation
<a name="top"></a>

## Table of Contents

- [compas_pb/generated/arc.proto](#compas_pb_generated_arc-proto)
    - [ArcData](#compas_pb-data-ArcData)
  
- [compas_pb/generated/bezier.proto](#compas_pb_generated_bezier-proto)
    - [BezierData](#compas_pb-data-BezierData)
  
- [compas_pb/generated/box.proto](#compas_pb_generated_box-proto)
    - [BoxData](#compas_pb-data-BoxData)
  
- [compas_pb/generated/capsule.proto](#compas_pb_generated_capsule-proto)
    - [CapsuleData](#compas_pb-data-CapsuleData)
  
- [compas_pb/generated/circle.proto](#compas_pb_generated_circle-proto)
    - [CircleData](#compas_pb-data-CircleData)
  
- [compas_pb/generated/cone.proto](#compas_pb_generated_cone-proto)
    - [ConeData](#compas_pb-data-ConeData)
  
- [compas_pb/generated/cylinder.proto](#compas_pb_generated_cylinder-proto)
    - [CylinderData](#compas_pb-data-CylinderData)
  
- [compas_pb/generated/ellipse.proto](#compas_pb_generated_ellipse-proto)
    - [EllipseData](#compas_pb-data-EllipseData)
  
- [compas_pb/generated/frame.proto](#compas_pb_generated_frame-proto)
    - [FrameData](#compas_pb-data-FrameData)
  
- [compas_pb/generated/hyperbola.proto](#compas_pb_generated_hyperbola-proto)
    - [HyperbolaData](#compas_pb-data-HyperbolaData)
  
- [compas_pb/generated/line.proto](#compas_pb_generated_line-proto)
    - [LineData](#compas_pb-data-LineData)
  
- [compas_pb/generated/mesh.proto](#compas_pb_generated_mesh-proto)
    - [FaceList](#compas_pb-data-FaceList)
    - [MeshData](#compas_pb-data-MeshData)
  
- [compas_pb/generated/message.proto](#compas_pb_generated_message-proto)
    - [AnyData](#compas_pb-data-AnyData)
    - [DictData](#compas_pb-data-DictData)
    - [DictData.ItemsEntry](#compas_pb-data-DictData-ItemsEntry)
    - [FallbackData](#compas_pb-data-FallbackData)
    - [ListData](#compas_pb-data-ListData)
    - [MessageData](#compas_pb-data-MessageData)
  
- [compas_pb/generated/parabola.proto](#compas_pb_generated_parabola-proto)
    - [ParabolaData](#compas_pb-data-ParabolaData)
  
- [compas_pb/generated/plane.proto](#compas_pb_generated_plane-proto)
    - [PlaneData](#compas_pb-data-PlaneData)
  
- [compas_pb/generated/point.proto](#compas_pb_generated_point-proto)
    - [PointData](#compas_pb-data-PointData)
  
- [compas_pb/generated/pointcloud.proto](#compas_pb_generated_pointcloud-proto)
    - [PointcloudData](#compas_pb-data-PointcloudData)
  
- [compas_pb/generated/polygon.proto](#compas_pb_generated_polygon-proto)
    - [PolygonData](#compas_pb-data-PolygonData)
  
- [compas_pb/generated/polyhedron.proto](#compas_pb_generated_polyhedron-proto)
    - [FaceData](#compas_pb-data-FaceData)
    - [PolyhedronData](#compas_pb-data-PolyhedronData)
  
- [compas_pb/generated/polyline.proto](#compas_pb_generated_polyline-proto)
    - [PolylineData](#compas_pb-data-PolylineData)
  
- [compas_pb/generated/projection.proto](#compas_pb_generated_projection-proto)
    - [ProjectionData](#compas_pb-data-ProjectionData)
  
- [compas_pb/generated/quaternion.proto](#compas_pb_generated_quaternion-proto)
    - [QuaternionData](#compas_pb-data-QuaternionData)
  
- [compas_pb/generated/reflection.proto](#compas_pb_generated_reflection-proto)
    - [ReflectionData](#compas_pb-data-ReflectionData)
  
- [compas_pb/generated/rotation.proto](#compas_pb_generated_rotation-proto)
    - [RotationData](#compas_pb-data-RotationData)
  
- [compas_pb/generated/scale.proto](#compas_pb_generated_scale-proto)
    - [ScaleData](#compas_pb-data-ScaleData)
  
- [compas_pb/generated/shear.proto](#compas_pb_generated_shear-proto)
    - [ShearData](#compas_pb-data-ShearData)
  
- [compas_pb/generated/sphere.proto](#compas_pb_generated_sphere-proto)
    - [SphereData](#compas_pb-data-SphereData)
  
- [compas_pb/generated/torus.proto](#compas_pb_generated_torus-proto)
    - [TorusData](#compas_pb-data-TorusData)
  
- [compas_pb/generated/transformation.proto](#compas_pb_generated_transformation-proto)
    - [TransformationData](#compas_pb-data-TransformationData)
  
- [compas_pb/generated/translation.proto](#compas_pb_generated_translation-proto)
    - [TranslationData](#compas_pb-data-TranslationData)
  
- [compas_pb/generated/vector.proto](#compas_pb_generated_vector-proto)
    - [VectorData](#compas_pb-data-VectorData)
  
- [Scalar Value Types](#scalar-value-types)



<a name="compas_pb_generated_arc-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## compas_pb/generated/arc.proto



<a name="compas_pb-data-ArcData"></a>

### ArcData



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| guid | [string](#string) |  |  |
| name | [string](#string) |  |  |
| circle | [CircleData](#compas_pb-data-CircleData) |  |  |
| start_angle | [float](#float) |  |  |
| end_angle | [float](#float) |  |  |





 

 

 

 



<a name="compas_pb_generated_bezier-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## compas_pb/generated/bezier.proto



<a name="compas_pb-data-BezierData"></a>

### BezierData



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| guid | [string](#string) |  |  |
| name | [string](#string) |  |  |
| points | [PointData](#compas_pb-data-PointData) | repeated | control points |
| degree | [int32](#int32) |  |  |





 

 

 

 



<a name="compas_pb_generated_box-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## compas_pb/generated/box.proto



<a name="compas_pb-data-BoxData"></a>

### BoxData



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| guid | [string](#string) |  |  |
| name | [string](#string) |  |  |
| frame | [FrameData](#compas_pb-data-FrameData) |  |  |
| xsize | [float](#float) |  |  |
| ysize | [float](#float) |  |  |
| zsize | [float](#float) |  |  |





 

 

 

 



<a name="compas_pb_generated_capsule-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## compas_pb/generated/capsule.proto



<a name="compas_pb-data-CapsuleData"></a>

### CapsuleData



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| guid | [string](#string) |  |  |
| name | [string](#string) |  |  |
| radius | [float](#float) |  |  |
| height | [float](#float) |  |  |
| frame | [FrameData](#compas_pb-data-FrameData) |  |  |





 

 

 

 



<a name="compas_pb_generated_circle-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## compas_pb/generated/circle.proto



<a name="compas_pb-data-CircleData"></a>

### CircleData



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| guid | [string](#string) |  |  |
| name | [string](#string) |  |  |
| radius | [float](#float) |  |  |
| frame | [FrameData](#compas_pb-data-FrameData) |  |  |





 

 

 

 



<a name="compas_pb_generated_cone-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## compas_pb/generated/cone.proto



<a name="compas_pb-data-ConeData"></a>

### ConeData



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| guid | [string](#string) |  |  |
| name | [string](#string) |  |  |
| radius | [float](#float) |  |  |
| height | [float](#float) |  |  |
| frame | [FrameData](#compas_pb-data-FrameData) |  |  |





 

 

 

 



<a name="compas_pb_generated_cylinder-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## compas_pb/generated/cylinder.proto



<a name="compas_pb-data-CylinderData"></a>

### CylinderData



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| guid | [string](#string) |  |  |
| name | [string](#string) |  |  |
| radius | [float](#float) |  |  |
| height | [float](#float) |  |  |
| frame | [FrameData](#compas_pb-data-FrameData) |  |  |





 

 

 

 



<a name="compas_pb_generated_ellipse-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## compas_pb/generated/ellipse.proto



<a name="compas_pb-data-EllipseData"></a>

### EllipseData



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| guid | [string](#string) |  |  |
| name | [string](#string) |  |  |
| major | [float](#float) |  |  |
| minor | [float](#float) |  |  |
| frame | [FrameData](#compas_pb-data-FrameData) |  |  |





 

 

 

 



<a name="compas_pb_generated_frame-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## compas_pb/generated/frame.proto



<a name="compas_pb-data-FrameData"></a>

### FrameData



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| guid | [string](#string) |  |  |
| name | [string](#string) |  |  |
| point | [PointData](#compas_pb-data-PointData) |  |  |
| xaxis | [VectorData](#compas_pb-data-VectorData) |  |  |
| yaxis | [VectorData](#compas_pb-data-VectorData) |  |  |





 

 

 

 



<a name="compas_pb_generated_hyperbola-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## compas_pb/generated/hyperbola.proto



<a name="compas_pb-data-HyperbolaData"></a>

### HyperbolaData



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| guid | [string](#string) |  |  |
| name | [string](#string) |  |  |
| major | [float](#float) |  |  |
| minor | [float](#float) |  |  |
| frame | [FrameData](#compas_pb-data-FrameData) |  |  |





 

 

 

 



<a name="compas_pb_generated_line-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## compas_pb/generated/line.proto



<a name="compas_pb-data-LineData"></a>

### LineData



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| guid | [string](#string) |  |  |
| name | [string](#string) |  |  |
| start | [PointData](#compas_pb-data-PointData) |  |  |
| end | [PointData](#compas_pb-data-PointData) |  |  |





 

 

 

 



<a name="compas_pb_generated_mesh-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## compas_pb/generated/mesh.proto



<a name="compas_pb-data-FaceList"></a>

### FaceList



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| indices | [uint32](#uint32) | repeated |  |






<a name="compas_pb-data-MeshData"></a>

### MeshData



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| guid | [string](#string) | optional |  |
| name | [string](#string) | optional |  |
| vertices | [PointData](#compas_pb-data-PointData) | repeated |  |
| faces | [FaceList](#compas_pb-data-FaceList) | repeated |  |





 

 

 

 



<a name="compas_pb_generated_message-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## compas_pb/generated/message.proto



<a name="compas_pb-data-AnyData"></a>

### AnyData
arbitrate container to hold message data and default data


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| message | [google.protobuf.Any](#google-protobuf-Any) |  |  |
| value | [google.protobuf.Value](#google-protobuf-Value) |  |  |
| fallback | [FallbackData](#compas_pb-data-FallbackData) |  |  |






<a name="compas_pb-data-DictData"></a>

### DictData
repeated serves as a dict in protobuf


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| items | [DictData.ItemsEntry](#compas_pb-data-DictData-ItemsEntry) | repeated |  |






<a name="compas_pb-data-DictData-ItemsEntry"></a>

### DictData.ItemsEntry



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| key | [string](#string) |  |  |
| value | [AnyData](#compas_pb-data-AnyData) |  |  |






<a name="compas_pb-data-FallbackData"></a>

### FallbackData



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| data | [DictData](#compas_pb-data-DictData) |  |  |






<a name="compas_pb-data-ListData"></a>

### ListData
repeated serves as a list in protobuf


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| items | [AnyData](#compas_pb-data-AnyData) | repeated |  |






<a name="compas_pb-data-MessageData"></a>

### MessageData
root serialization element


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| data | [AnyData](#compas_pb-data-AnyData) |  |  |
| version | [string](#string) | optional |  |





 

 

 

 



<a name="compas_pb_generated_parabola-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## compas_pb/generated/parabola.proto



<a name="compas_pb-data-ParabolaData"></a>

### ParabolaData



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| guid | [string](#string) |  |  |
| name | [string](#string) |  |  |
| focal | [float](#float) |  |  |
| frame | [FrameData](#compas_pb-data-FrameData) |  |  |





 

 

 

 



<a name="compas_pb_generated_plane-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## compas_pb/generated/plane.proto



<a name="compas_pb-data-PlaneData"></a>

### PlaneData



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| guid | [string](#string) |  |  |
| name | [string](#string) |  |  |
| point | [PointData](#compas_pb-data-PointData) |  |  |
| normal | [VectorData](#compas_pb-data-VectorData) |  |  |





 

 

 

 



<a name="compas_pb_generated_point-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## compas_pb/generated/point.proto



<a name="compas_pb-data-PointData"></a>

### PointData



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| guid | [string](#string) |  | no inheritance, so Data will have to repeate but apparently |
| name | [string](#string) |  |  |
| x | [float](#float) |  |  |
| y | [float](#float) |  |  |
| z | [float](#float) |  |  |





 

 

 

 



<a name="compas_pb_generated_pointcloud-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## compas_pb/generated/pointcloud.proto



<a name="compas_pb-data-PointcloudData"></a>

### PointcloudData



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| guid | [string](#string) |  |  |
| name | [string](#string) |  |  |
| points | [PointData](#compas_pb-data-PointData) | repeated |  |





 

 

 

 



<a name="compas_pb_generated_polygon-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## compas_pb/generated/polygon.proto



<a name="compas_pb-data-PolygonData"></a>

### PolygonData



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| guid | [string](#string) |  |  |
| name | [string](#string) |  |  |
| points | [PointData](#compas_pb-data-PointData) | repeated |  |





 

 

 

 



<a name="compas_pb_generated_polyhedron-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## compas_pb/generated/polyhedron.proto



<a name="compas_pb-data-FaceData"></a>

### FaceData



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| vertex_indices | [int32](#int32) | repeated | indices into the vertices array |






<a name="compas_pb-data-PolyhedronData"></a>

### PolyhedronData



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| guid | [string](#string) |  |  |
| name | [string](#string) |  |  |
| vertices | [PointData](#compas_pb-data-PointData) | repeated |  |
| faces | [FaceData](#compas_pb-data-FaceData) | repeated |  |





 

 

 

 



<a name="compas_pb_generated_polyline-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## compas_pb/generated/polyline.proto



<a name="compas_pb-data-PolylineData"></a>

### PolylineData



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| guid | [string](#string) |  |  |
| name | [string](#string) |  |  |
| points | [PointData](#compas_pb-data-PointData) | repeated |  |





 

 

 

 



<a name="compas_pb_generated_projection-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## compas_pb/generated/projection.proto



<a name="compas_pb-data-ProjectionData"></a>

### ProjectionData



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| guid | [string](#string) |  |  |
| name | [string](#string) |  |  |
| matrix | [float](#float) | repeated | 4x4 matrix stored as flat array of 16 floats |





 

 

 

 



<a name="compas_pb_generated_quaternion-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## compas_pb/generated/quaternion.proto



<a name="compas_pb-data-QuaternionData"></a>

### QuaternionData



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| guid | [string](#string) |  |  |
| name | [string](#string) |  |  |
| w | [float](#float) |  |  |
| x | [float](#float) |  |  |
| y | [float](#float) |  |  |
| z | [float](#float) |  |  |





 

 

 

 



<a name="compas_pb_generated_reflection-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## compas_pb/generated/reflection.proto



<a name="compas_pb-data-ReflectionData"></a>

### ReflectionData



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| guid | [string](#string) |  |  |
| name | [string](#string) |  |  |
| matrix | [float](#float) | repeated | 4x4 matrix stored as flat array of 16 floats |





 

 

 

 



<a name="compas_pb_generated_rotation-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## compas_pb/generated/rotation.proto



<a name="compas_pb-data-RotationData"></a>

### RotationData



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| guid | [string](#string) |  |  |
| name | [string](#string) |  |  |
| axis | [VectorData](#compas_pb-data-VectorData) |  |  |
| angle | [float](#float) |  |  |
| point | [PointData](#compas_pb-data-PointData) |  | point of rotation (optional, default to origin) |





 

 

 

 



<a name="compas_pb_generated_scale-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## compas_pb/generated/scale.proto



<a name="compas_pb-data-ScaleData"></a>

### ScaleData



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| guid | [string](#string) |  |  |
| name | [string](#string) |  |  |
| matrix | [float](#float) | repeated | 4x4 matrix stored as flat array of 16 floats |





 

 

 

 



<a name="compas_pb_generated_shear-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## compas_pb/generated/shear.proto



<a name="compas_pb-data-ShearData"></a>

### ShearData



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| guid | [string](#string) |  |  |
| name | [string](#string) |  |  |
| matrix | [float](#float) | repeated | 4x4 matrix stored as flat array of 16 floats |





 

 

 

 



<a name="compas_pb_generated_sphere-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## compas_pb/generated/sphere.proto



<a name="compas_pb-data-SphereData"></a>

### SphereData



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| guid | [string](#string) |  |  |
| name | [string](#string) |  |  |
| radius | [float](#float) |  |  |
| frame | [FrameData](#compas_pb-data-FrameData) |  |  |





 

 

 

 



<a name="compas_pb_generated_torus-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## compas_pb/generated/torus.proto



<a name="compas_pb-data-TorusData"></a>

### TorusData



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| guid | [string](#string) |  |  |
| name | [string](#string) |  |  |
| radius_axis | [float](#float) |  |  |
| radius_pipe | [float](#float) |  |  |
| frame | [FrameData](#compas_pb-data-FrameData) |  |  |





 

 

 

 



<a name="compas_pb_generated_transformation-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## compas_pb/generated/transformation.proto



<a name="compas_pb-data-TransformationData"></a>

### TransformationData



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| guid | [string](#string) |  |  |
| name | [string](#string) |  |  |
| matrix | [float](#float) | repeated | 4x4 matrix stored as flat array of 16 floats |





 

 

 

 



<a name="compas_pb_generated_translation-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## compas_pb/generated/translation.proto



<a name="compas_pb-data-TranslationData"></a>

### TranslationData



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| guid | [string](#string) |  |  |
| name | [string](#string) |  |  |
| translation_vector | [VectorData](#compas_pb-data-VectorData) |  |  |





 

 

 

 



<a name="compas_pb_generated_vector-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## compas_pb/generated/vector.proto



<a name="compas_pb-data-VectorData"></a>

### VectorData



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| guid | [string](#string) |  |  |
| name | [string](#string) |  |  |
| x | [float](#float) |  |  |
| y | [float](#float) |  |  |
| z | [float](#float) |  |  |





 

 

 

 



## Scalar Value Types

| .proto Type | Notes | C++ | Java | Python | Go | C# | PHP | Ruby |
| ----------- | ----- | --- | ---- | ------ | -- | -- | --- | ---- |
| <a name="double" /> double |  | double | double | float | float64 | double | float | Float |
| <a name="float" /> float |  | float | float | float | float32 | float | float | Float |
| <a name="int32" /> int32 | Uses variable-length encoding. Inefficient for encoding negative numbers – if your field is likely to have negative values, use sint32 instead. | int32 | int | int | int32 | int | integer | Bignum or Fixnum (as required) |
| <a name="int64" /> int64 | Uses variable-length encoding. Inefficient for encoding negative numbers – if your field is likely to have negative values, use sint64 instead. | int64 | long | int/long | int64 | long | integer/string | Bignum |
| <a name="uint32" /> uint32 | Uses variable-length encoding. | uint32 | int | int/long | uint32 | uint | integer | Bignum or Fixnum (as required) |
| <a name="uint64" /> uint64 | Uses variable-length encoding. | uint64 | long | int/long | uint64 | ulong | integer/string | Bignum or Fixnum (as required) |
| <a name="sint32" /> sint32 | Uses variable-length encoding. Signed int value. These more efficiently encode negative numbers than regular int32s. | int32 | int | int | int32 | int | integer | Bignum or Fixnum (as required) |
| <a name="sint64" /> sint64 | Uses variable-length encoding. Signed int value. These more efficiently encode negative numbers than regular int64s. | int64 | long | int/long | int64 | long | integer/string | Bignum |
| <a name="fixed32" /> fixed32 | Always four bytes. More efficient than uint32 if values are often greater than 2^28. | uint32 | int | int | uint32 | uint | integer | Bignum or Fixnum (as required) |
| <a name="fixed64" /> fixed64 | Always eight bytes. More efficient than uint64 if values are often greater than 2^56. | uint64 | long | int/long | uint64 | ulong | integer/string | Bignum |
| <a name="sfixed32" /> sfixed32 | Always four bytes. | int32 | int | int | int32 | int | integer | Bignum or Fixnum (as required) |
| <a name="sfixed64" /> sfixed64 | Always eight bytes. | int64 | long | int/long | int64 | long | integer/string | Bignum |
| <a name="bool" /> bool |  | bool | boolean | boolean | bool | bool | boolean | TrueClass/FalseClass |
| <a name="string" /> string | A string must always contain UTF-8 encoded or 7-bit ASCII text. | string | String | str/unicode | string | string | string | String (UTF-8) |
| <a name="bytes" /> bytes | May contain any arbitrary sequence of bytes. | string | ByteString | str | []byte | ByteString | string | String (ASCII-8BIT) |

