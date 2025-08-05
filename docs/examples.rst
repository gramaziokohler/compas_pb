********************************************************************************
Examples
********************************************************************************

``compas_pb`` lets you serialize and de-serialize arbitrarily nested COMPAS types and python builtins.

Serialization to file
=====================

Serialize and deserialize basic COMPAS geometry objects:

.. code-block:: python

    from compas.datastructures import Mesh
    from compas.geometry import Box
    from compas_pb import pb_dump
    from compas_pb import pb_load

    box = Box.from_width_height_depth(1.0, 2.0, 3.0)
    mesh = Mesh.from_shape(box)

    PATH = r"box_mesh.data"

    pb_dump({"box": box, "mesh": mesh}, PATH)

    data = pb_load(PATH)

    box = data["box"]
    mesh = data["mesh"]


Serialization to bytes
======================


.. code-block:: python

    from compas.datastructures import Mesh
    from compas.geometry import Box
    from compas_pb import pb_dump_bts

    from spaceship_controller import space_interface

    box = Box.from_width_height_depth(1.0, 2.0, 3.0)
    mesh = Mesh.from_shape(box)

    message = pb_dump_bts({"box": box, "mesh": mesh})

    space_interface.send_bytes(message)


Or, if you don't have a spaceship:

.. code-block:: python

    from compas.datastructures import Mesh
    from compas.geometry import Box
    from compas_pb import pb_dump_bts
    from compas_pb import pb_load_bts

    box = Box.from_width_height_depth(1.0, 2.0, 3.0)
    mesh = Mesh.from_shape(box)

    message = pb_dump_bts({"box": box, "mesh": mesh})

    data = pb_load_bts(message)

