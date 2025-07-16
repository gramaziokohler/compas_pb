********************************************************************************
Developer Guide
********************************************************************************

This guide explains how to extend compas_pb with custom serializers and deserializers for your own types.

Plugin System Overview
======================

compas_pb uses COMPAS's plugin system to automatically discover and register serializers and deserializers. This allows you to add support for new types without modifying the core library.

The plugin system works as follows:

1. **Registration**: Serializers and deserializers are registered using decorators
2. **Discovery**: The plugin system automatically discovers registered functions
3. **Loading**: Serializers are loaded when needed during serialization/deserialization

Creating Custom Serializers
===========================

Basic Serializer
---------------

To create a serializer for a custom type, use the ``@pb_serializer`` decorator:

.. code-block:: python

    from compas_pb.data import pb_serializer
    from compas_pb.generated import message_pb2

    class MyCustomType:
        def __init__(self, x, y, z):
            self.x = x
            self.y = y
            self.z = z

    @pb_serializer(MyCustomType)
    def my_custom_type_to_pb(obj: MyCustomType) -> message_pb2.AnyData:
        """Convert MyCustomType to protobuf message."""
        # Create a protobuf message for your type
        proto_data = message_pb2.PrimitiveData()
        proto_data.x = obj.x
        proto_data.y = obj.y
        proto_data.z = obj.z

        # Wrap in AnyData
        any_data = message_pb2.AnyData()
        any_data.data.Pack(proto_data)
        return any_data

Creating Custom Deserializers
=============================

To create a deserializer, use the ``@pb_deserializer`` decorator:

.. code-block:: python

    from compas_pb.data import pb_deserializer
    from compas_pb.generated import message_pb2

    @pb_deserializer(message_pb2.PrimitiveData)
    def my_custom_type_from_pb(proto_data: message_pb2.PrimitiveData) -> MyCustomType:
        """Convert protobuf message to MyCustomType."""
        return MyCustomType(
            x=proto_data.x,
            y=proto_data.y,
            z=proto_data.z
        )

Complete Example
===============

Here's a complete example of adding support for a custom 3D box type:

.. code-block:: python

    from compas_pb.data import pb_serializer, pb_deserializer
    from compas_pb.generated import message_pb2

    class Box:
        def __init__(self, width, height, depth):
            self.width = width
            self.height = height
            self.depth = depth

    # Create a custom protobuf message (you would define this in a .proto file)
    class BoxData:
        def __init__(self):
            self.width = 0.0
            self.height = 0.0
            self.depth = 0.0

    @pb_serializer(Box)
    def box_to_pb(box: Box) -> message_pb2.AnyData:
        """Convert Box to protobuf message."""
        proto_data = BoxData()
        proto_data.width = box.width
        proto_data.height = box.height
        proto_data.depth = box.depth

        any_data = message_pb2.AnyData()
        any_data.data.Pack(proto_data)
        return any_data

    @pb_deserializer(BoxData)
    def box_from_pb(proto_data: BoxData) -> Box:
        """Convert protobuf message to Box."""
        return Box(
            width=proto_data.width,
            height=proto_data.height,
            depth=proto_data.depth
        )

    # Now you can use it
    from compas_pb.data import pb_dump, pb_load

    box = Box(1.0, 2.0, 3.0)
    pb_dump(box, "box.data")
    loaded_box = pb_load("box.data")

Plugin Discovery
===============

For your custom serializers to be discovered, they need to be in a module that's part of a COMPAS plugin. Here's how to set it up:

1. **Create a plugin package**:

.. code-block:: python

    # my_compas_plugin/__init__.py
    from . import serializers

    # my_compas_plugin/serializers.py
    from compas.plugins import plugin
    from compas_pb.data import register_serializers

    @plugin(category="factories", selector="collect_all")
    def register_my_serializers():
        """Register custom serializers."""
        # Import your serializer modules here
        from . import my_serializers
        return True

2. **Install your plugin**:

.. code-block:: bash

    pip install -e my_compas_plugin

3. **Use your serializers**:

.. code-block:: python

    from compas_pb.data import pb_dump, pb_load
    from my_compas_plugin import MyCustomType

    obj = MyCustomType(1, 2, 3)
    pb_dump(obj, "custom.data")  # Will use your custom serializer

Best Practices
=============

1. **Type Safety**: Always use type hints in your serializer/deserializer functions
2. **Error Handling**: Handle edge cases and provide clear error messages
3. **Documentation**: Document your serializers with clear docstrings
4. **Testing**: Write tests for your custom serializers
5. **Versioning**: Consider versioning your protobuf messages for backward compatibility

Debugging
=========

If your serializers aren't being used, check:

1. **Plugin Registration**: Ensure your plugin is properly registered
2. **Import Paths**: Make sure your serializer modules are imported
3. **Type Matching**: Verify the type matches exactly (including inheritance)
4. **Protobuf Messages**: Ensure your protobuf messages are properly defined

Example: Debugging a Serializer

.. code-block:: python

    from compas_pb.data import SerialzerRegistry

    # Check if your serializer is registered
    serializer = SerialzerRegistry.get_serializer(MyCustomType)
    print(f"Serializer found: {serializer is not None}")

    # Check registered types
    from compas_pb.data.registry import _SERIALIZERS
    print(f"Registered types: {list(_SERIALIZERS.keys())}")

Advanced Topics
==============

Custom Protobuf Messages
-----------------------

For complex types, you may need to define custom protobuf messages. Create a `.proto` file:

.. code-block:: protobuf

    syntax = "proto3";

    package my_plugin;

    message ComplexData {
        string name = 1;
        repeated double values = 2;
        map<string, string> metadata = 3;
    }

Then generate the Python code and use it in your serializers.

Fallback Serialization
---------------------

If your type has a ``__jsondump__`` method, it can be automatically serialized using JSON fallback:

.. code-block:: python

    class MyType:
        def __init__(self, data):
            self.data = data

        def __jsondump__(self):
            return {"data": self.data}

    # This will work automatically without a custom serializer
    from compas_pb.data import pb_dump
    pb_dump(MyType("test"), "test.data")
