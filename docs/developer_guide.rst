********************************************************************************
Developer Guide
********************************************************************************

This guide explains how to extend compas_pb with custom serializers and deserializers for your own types.

Creating New Serializers
========================

1. Create a new type
--------------------

For this example class we will create a serializer for a custom point type.

.. code-block:: python

    from compas.geometry import Point

    class CustomPoint:
        def __init__(self, special_attr: str, x: float, y: float, z: float):
            self.special_attr = special_attr
            self.point = Point(x, y, z)


2. Create a protobuf definition for the new type
-------------------------------------------------

Create a protobuf definition for the new type you wish to add. This should be placed in ``IDL/compas_pb/generated/``.

.. code-block:: protobuf
    :caption: IDL/compas_pb/generated/custom_point.proto

    syntax = "proto3";

    package compas_pb.data;

    import "compas_pb/generated/point.proto";

    message CustomPointData {
        string special_attr = 1;
        PointData point = 2;
    }

3. Generate the python code for the new type
---------------------------------------------

Now run the following command to generate the python code:

.. code-block:: bash

    invoke protobuf.generate-proto-classes -t python

A new module called ``custom_point_pb2`` should now be available in ``compas_pb/generated/``.

4. Create a serializer for the new type
----------------------------------------

To create a serializer for a custom type, use the ``@pb_serializer`` decorator. This decorator will be used to register the serializer with the plugin system.

.. code-block:: python
    :caption: compas_pb/conversions.py

    from compas_pb.data import pb_serializer
    from compas_pb.data import pb_deserializer
    from compas_pb.generated import custom_point_pb2


    @pb_serializer(CustomPoint)
    def my_custom_point_to_pb(obj: CustomPoint) -> custom_point_pb2.CustomPointData:
        """Convert CustomPoint to protobuf message."""
        result = custom_point_pb2.CustomPointData()
        result.special_attr = obj.special_attr
        result.point = point_to_pb(obj.point)
        return result

    @pb_deserializer(custom_point_pb2.CustomPointData)
    def my_custom_point_from_pb(proto_data: custom_point_pb2.CustomPointData) -> CustomPoint:
        """Convert protobuf message to CustomPoint."""
        return CustomPoint(
            special_attr=proto_data.special_attr,
            point=point_from_pb(proto_data.point)
        )
