# Missing COMPAS Type?

!!! note
    We're doing our best to add support for as many COMPAS types as possible. Is the type you'd like to send still missing? Helps us out by adding it yourself!

This guide explains how to extend compas_pb with support for more COMPAS types.

## Creating New Serializers

### 1. Add a protobuf definition for the type you wish to add

Add a protobuf message definition for the new type to the appropriate proto file:

- **`geometry.proto`** - For geometry primitives (points, vectors, curves, surfaces, transformations)
- **`datastructures.proto`** - For COMPAS datastructures (mesh, polyhedron)
- **`message.proto`** - For serialization framework types (internal use only)

For example, to add a custom geometry type, add it to `src/compas_pb/protobuf_defs/compas_pb/generated/geometry.proto`:

```protobuf title="src/compas_pb/protobuf_defs/compas_pb/generated/geometry.proto"
// Add to the appropriate section in geometry.proto

message CustomShapeData {
    string guid = 1;
    string name = 2;
    float radius = 3;
    FrameData frame = 4;
}
```

Or, for a COMPAS datastructure type, add it to `src/compas_pb/protobuf_defs/compas_pb/generated/datastructures.proto`:

```protobuf title="src/compas_pb/protobuf_defs/compas_pb/generated/datastructures.proto"
// Import geometry types if needed
import "compas_pb/generated/geometry.proto";

message CustomDataStructureData {
    string guid = 1;
    string name = 2;
    repeated PointData vertices = 3;
}
```

!!! note
    Proto definitions are organized to match COMPAS package structure:
    - `geometry.proto` → `compas.geometry`
    - `datastructures.proto` → `compas.datastructures`
    - `message.proto` → internal serialization framework

### 2. Generate the python code for the updated proto file

Now run the following command to regenerate the python code from the updated proto files:

```bash
invoke generate-proto-classes -t python
```

The generated modules (`geometry_pb2`, `datastructures_pb2`, `message_pb2`) in `src/compas_pb/generated/` will now include your new type.

### 3. Create a (de)serializer for the new type

To create a (de)serializer for a custom type, use the `@pb_serializer` and `@pb_deserializer` decorators. These decorators will be used to register the serializer and deserializer with the plugin system.

```python title="compas_pb/conversions.py"
from compas_pb.registry import pb_serializer
from compas_pb.registry import pb_deserializer
from compas_pb.generated import geometry_pb2  # or datastructures_pb2


@pb_serializer(CustomShape)
def custom_shape_to_pb(obj: CustomShape) -> geometry_pb2.CustomShapeData:
    """Convert CustomShape to protobuf message."""
    result = geometry_pb2.CustomShapeData()
    result.guid = str(obj.guid)
    result.name = obj.name
    result.radius = obj.radius
    result.frame.CopyFrom(frame_to_pb(obj.frame))
    return result

@pb_deserializer(geometry_pb2.CustomShapeData)
def custom_shape_from_pb(proto_data: geometry_pb2.CustomShapeData) -> CustomShape:
    """Convert protobuf message to CustomShape."""
    return CustomShape(
        guid=proto_data.guid,
        name=proto_data.name,
        radius=proto_data.radius,
        frame=frame_from_pb(proto_data.frame)
    )
```
