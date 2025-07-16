********************************************************************************
Tutorial
********************************************************************************

This tutorial will guide you through the basic usage of compas_pb for serializing and deserializing COMPAS objects.

Basic Usage
===========

Serializing and Loading Simple Objects
--------------------------------------

The most common use case is to serialize COMPAS geometry objects to files and load them back:

.. code-block:: python

    from compas.geometry import Point, Vector, Frame, Line
    from compas_pb.data import pb_dump, pb_load

    # Create some COMPAS objects
    point = Point(1, 2, 3)
    vector = Vector(1, 0, 0)
    frame = Frame.worldXY()
    line = Line(Point(0, 0, 0), Point(1, 1, 1))

    # Serialize to file
    pb_dump(point, "point.data")
    pb_dump(frame, "frame.data")

    # Load from file
    loaded_point = pb_load("point.data")
    loaded_frame = pb_load("frame.data")

    print(f"Original point: {point}")
    print(f"Loaded point: {loaded_point}")
    print(f"Are equal: {point == loaded_point}")

Working with Collections
------------------------

You can also serialize collections of objects:

.. code-block:: python

    from compas.geometry import Point
    from compas_pb.data import pb_dump, pb_load

    # List of points
    points = [Point(0, 0, 0), Point(1, 0, 0), Point(1, 1, 0)]
    pb_dump(points, "points.data")
    loaded_points = pb_load("points.data")

    # Dictionary of objects
    data = {
        "origin": Point(0, 0, 0),
        "direction": Vector(1, 0, 0),
        "frame": Frame.worldXY()
    }
    pb_dump(data, "scene.data")
    loaded_data = pb_load("scene.data")

Binary and JSON Formats
=======================

Binary Serialization
--------------------

For maximum efficiency, use binary serialization:

.. code-block:: python

    from compas.geometry import Point
    from compas_pb.data import pb_dump_bts, pb_load_bts

    point = Point(1, 2, 3)

    # Serialize to bytes
    binary_data = pb_dump_bts(point)

    # Deserialize from bytes
    loaded_point = pb_load_bts(binary_data)

JSON Serialization
------------------

For human-readable output or web APIs, use JSON serialization:

.. code-block:: python

    from compas.geometry import Point
    from compas_pb.data import pb_dump_json, pb_load_json

    point = Point(1, 2, 3)

    # Serialize to JSON string
    json_data = pb_dump_json(point)
    print(json_data)

    # Deserialize from JSON string
    loaded_point = pb_load_json(json_data)

Supported Types
===============

Built-in COMPAS Types
---------------------

The following COMPAS types are supported out of the box:

* :class:`compas.geometry.Point`
* :class:`compas.geometry.Vector`
* :class:`compas.geometry.Line`
* :class:`compas.geometry.Frame`
* :class:`compas.datastructures.Mesh`

Primitive Types
---------------

Python primitive types are also supported:

* ``int``
* ``float``
* ``bool``
* ``str``
* ``None`` (converted to "None" string)

Collections
-----------

* Lists and tuples
* Dictionaries

Error Handling
==============

When working with unsupported types, you'll get clear error messages:

.. code-block:: python

    from compas_pb.data import pb_dump

    try:
        pb_dump({"unsupported": object()}, "test.data")
    except TypeError as e:
        print(f"Error: {e}")
        # Output: Error: Unsupported type: <class 'object'>

Performance Considerations
==========================

* Binary serialization (``pb_dump``, ``pb_dump_bts``) is the fastest and most space-efficient
* JSON serialization is slower but human-readable
* Large collections of objects are handled efficiently
* The plugin system ensures only necessary serializers are loaded
