********************************************************************************
Missing COMPAS Type?
********************************************************************************

.. note::

    We're doing our best to add support for as many COMPAS types as possible. Is the type you'd like to send still missing? Helps us out by adding it yourself!

This guide explains how to extend compas_pb with support for more COMPAS types.

Creating New Serializers
========================


1. Create a protobuf definition for the type you wish to add (for example ``Circle``)
-------------------------------------------------------------------------------------

Create a protobuf definition for the new type you wish to add. This should be placed in ``IDL/compas_pb/generated/``.

.. code-block:: protobuf
    :caption: IDL/compas_pb/generated/custom_point.proto

    syntax = "proto3";

    package compas_pb.data;

    import "compas_pb/generated/frame.proto";

    message CircleData {
        string guid = 1;
        string name = 2;
        float radius = 3;
        FrameData frame = 4;
    }


3. Generate the python code for the new type
--------------------------------------------

Now run the following command to generate the python code:

.. code-block:: bash

    invoke protobuf.generate-proto-classes -t python

A new module called ``circle_pb2`` should now be available in ``compas_pb/generated/``.

4. Create a (de)serializer for the new type
-------------------------------------------

To create a (de)serializer for a custom type, use the ``@pb_serializer`` and ``@pb_deserializer`` decorators. These decorators will be used to register the serializer and deserializer with the plugin system.

.. code-block:: python
    :caption: compas_pb/conversions.py

    from compas_pb.data import pb_serializer
    from compas_pb.data import pb_deserializer
    from compas_pb.generated import circle_pb2


    @pb_serializer(Circle)
    def my_circle_to_pb(obj: Circle) -> circle_pb2.CircleData:
        """Convert Circle to protobuf message."""
        result = circle_pb2.CircleData()
        result.guid = obj.guid
        result.name = obj.name
        result.radius = obj.radius
        result.frame = frame_to_pb(obj.frame)
        return result

    @pb_deserializer(circle_pb2.CircleData)
    def my_circle_from_pb(proto_data: circle_pb2.CircleData) -> Circle:
        """Convert protobuf message to Circle."""
        return Circle(
            guid=proto_data.guid,
            name=proto_data.name,
            radius=proto_data.radius,
            frame=frame_from_pb(proto_data.frame)
        )
