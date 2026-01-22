# Missing COMPAS Type?

!!! note
    We're doing our best to add support for as many COMPAS types as possible. Is the type you'd like to send still missing? Helps us out by adding it yourself!

This guide explains how to extend compas_pb with support for more COMPAS types.

## Creating New Serializers

### 1. Add a protobuf definition for the type you wish to add

Add a protobuf message definition for the new type to the unified `geometry.proto` file located at `src/compas_pb/protobuf_defs/compas_pb/generated/geometry.proto`.

For example, to add a custom `CustomShape` type:

```protobuf title="src/compas_pb/protobuf_defs/compas_pb/generated/geometry.proto"
// Add to the appropriate section in geometry.proto

message CustomShapeData {
    string guid = 1;
    string name = 2;
    float radius = 3;
    FrameData frame = 4;
}
```

!!! note
    All geometry types are now defined in a single `geometry.proto` file. This makes it easier to manage dependencies between types and see the full structure at a glance.

### 2. Generate the python code for the updated proto file

Now run the following command to regenerate the python code from the updated proto file:

```bash
invoke generate-proto-classes -t python
```

The generated `geometry_pb2` module in `src/compas_pb/generated/` will now include your new type.

### 3. Create a (de)serializer for the new type

To create a (de)serializer for a custom type, use the `@pb_serializer` and `@pb_deserializer` decorators. These decorators will be used to register the serializer and deserializer with the plugin system.

```python title="compas_pb/conversions.py"
from compas_pb.registry import pb_serializer
from compas_pb.registry import pb_deserializer
from compas_pb.generated import geometry_pb2


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
