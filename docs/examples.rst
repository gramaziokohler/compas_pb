********************************************************************************
Examples
********************************************************************************

This page contains practical examples demonstrating various use cases of compas_pb.

Basic Geometry Serialization
============================

Serialize and deserialize basic COMPAS geometry objects:

.. code-block:: python

    from compas.geometry import Point, Vector, Frame, Line
    from compas_pb.data import pb_dump, pb_load

    # Create geometry objects
    point = Point(1.0, 2.0, 3.0)
    vector = Vector(1.0, 0.0, 0.0)
    frame = Frame.worldXY()
    line = Line(Point(0, 0, 0), Point(1, 1, 1))

    # Serialize to files
    pb_dump(point, "examples/point.data")
    pb_dump(vector, "examples/vector.data")
    pb_dump(frame, "examples/frame.data")
    pb_dump(line, "examples/line.data")

    # Load from files
    loaded_point = pb_load("examples/point.data")
    loaded_vector = pb_load("examples/vector.data")
    loaded_frame = pb_load("examples/frame.data")
    loaded_line = pb_load("examples/line.data")

    print(f"Point: {loaded_point}")
    print(f"Vector: {loaded_vector}")
    print(f"Frame: {loaded_frame}")
    print(f"Line: {loaded_line}")

Working with Meshes
===================

Serialize and deserialize COMPAS meshes:

.. code-block:: python

    from compas.datastructures import Mesh
    from compas_pb.data import pb_dump, pb_load

    # Create a simple mesh
    mesh = Mesh.from_polyhedron(6)  # Create a cube

    # Serialize mesh
    pb_dump(mesh, "examples/mesh.data")

    # Load mesh
    loaded_mesh = pb_load("examples/mesh.data")

    print(f"Original mesh vertices: {len(mesh.vertices())}")
    print(f"Loaded mesh vertices: {len(loaded_mesh.vertices())}")
    print(f"Original mesh faces: {len(mesh.faces())}")
    print(f"Loaded mesh faces: {len(loaded_mesh.faces())}")

Complex Data Structures
=======================

Serialize complex nested data structures:

.. code-block:: python

    from compas.geometry import Point, Vector, Frame
    from compas_pb.data import pb_dump, pb_load

    # Create a complex scene with multiple objects
    scene = {
        "camera": {
            "position": Point(0, 0, 10),
            "target": Point(0, 0, 0),
            "up": Vector(0, 1, 0)
        },
        "objects": [
            {
                "type": "point",
                "position": Point(1, 2, 3),
                "name": "point_1"
            },
            {
                "type": "frame",
                "frame": Frame.worldXY(),
                "name": "world_frame"
            }
        ],
        "metadata": {
            "version": "1.0",
            "author": "User",
            "created": "2024-01-01"
        }
    }

    # Serialize the entire scene
    pb_dump(scene, "examples/scene.data")

    # Load the scene
    loaded_scene = pb_load("examples/scene.data")

    print(f"Scene camera position: {loaded_scene['camera']['position']}")
    print(f"Number of objects: {len(loaded_scene['objects'])}")
    print(f"Scene metadata: {loaded_scene['metadata']}")

Binary vs JSON Serialization
============================

Compare different serialization formats:

.. code-block:: python

    from compas.geometry import Point, Vector, Frame
    from compas_pb.data import pb_dump, pb_dump_bts, pb_dump_json
    import os

    # Create test data
    data = {
        "point": Point(1, 2, 3),
        "vector": Vector(1, 0, 0),
        "frame": Frame.worldXY()
    }

    # Binary serialization
    binary_data = pb_dump_bts(data)
    print(f"Binary size: {len(binary_data)} bytes")

    # JSON serialization
    json_data = pb_dump_json(data)
    print(f"JSON size: {len(json_data)} bytes")
    print(f"JSON preview: {json_data[:100]}...")

    # File serialization
    pb_dump(data, "examples/data.data")
    file_size = os.path.getsize("examples/data.data")
    print(f"File size: {file_size} bytes")

Network Communication
=====================

Use compas_pb for network communication:

.. code-block:: python

    import socket
    from compas.geometry import Point, Vector
    from compas_pb.data import pb_dump_bts, pb_load_bts

    # Server side
    def server():
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('localhost', 12345))
        server_socket.listen(1)

        print("Server listening...")
        client, addr = server_socket.accept()

        # Receive data
        data = client.recv(4096)
        received_objects = pb_load_bts(data)

        print(f"Received: {received_objects}")
        client.close()
        server_socket.close()

    # Client side
    def client():
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('localhost', 12345))

        # Send data
        objects = [Point(1, 2, 3), Vector(1, 0, 0)]
        binary_data = pb_dump_bts(objects)
        client_socket.send(binary_data)

        client_socket.close()

    # Run server and client (in separate processes)
    # server()
    # client()

Custom Type Serialization
==========================

Example of extending compas_pb with custom types:

.. code-block:: python

    from compas_pb.data import pb_serializer, pb_deserializer
    from compas_pb.generated import message_pb2

    # Define a custom type
    class CustomBox:
        def __init__(self, width, height, depth):
            self.width = width
            self.height = height
            self.depth = depth

    # Create a simple protobuf-like structure
    class BoxData:
        def __init__(self):
            self.width = 0.0
            self.height = 0.0
            self.depth = 0.0

    # Register serializer
    @pb_serializer(CustomBox)
    def box_to_pb(box: CustomBox) -> message_pb2.AnyData:
        """Convert CustomBox to protobuf message."""
        # For this example, we'll use a simple approach
        # In practice, you'd define proper protobuf messages
        proto_data = message_pb2.PrimitiveData()
        proto_data.str = f"{box.width},{box.height},{box.depth}"

        any_data = message_pb2.AnyData()
        any_data.data.Pack(proto_data)
        return any_data

    # Register deserializer
    @pb_deserializer(message_pb2.PrimitiveData)
    def box_from_pb(proto_data: message_pb2.PrimitiveData) -> CustomBox:
        """Convert protobuf message to CustomBox."""
        if hasattr(proto_data, 'str') and proto_data.str:
            width, height, depth = map(float, proto_data.str.split(','))
            return CustomBox(width, height, depth)
        return CustomBox(0, 0, 0)

    # Use the custom type
    from compas_pb.data import pb_dump, pb_load

    box = CustomBox(1.0, 2.0, 3.0)
    pb_dump(box, "examples/custom_box.data")

    loaded_box = pb_load("examples/custom_box.data")
    print(f"Original box: {box.width}x{box.height}x{box.depth}")
    print(f"Loaded box: {loaded_box.width}x{loaded_box.height}x{loaded_box.depth}")

Performance Comparison
======================

Compare performance with other serialization methods:

.. code-block:: python

    import time
    import pickle
    import json
    from compas.geometry import Point, Vector, Frame
    from compas_pb.data import pb_dump_bts, pb_load_bts

    # Create test data
    test_data = [Point(i, i, i) for i in range(1000)]

    # Test Protocol Buffers
    start_time = time.time()
    pb_data = pb_dump_bts(test_data)
    pb_serialize_time = time.time() - start_time

    start_time = time.time()
    pb_loaded = pb_load_bts(pb_data)
    pb_deserialize_time = time.time() - start_time

    # Test Pickle
    start_time = time.time()
    pickle_data = pickle.dumps(test_data)
    pickle_serialize_time = time.time() - start_time

    start_time = time.time()
    pickle_loaded = pickle.loads(pickle_data)
    pickle_deserialize_time = time.time() - start_time

    print("Performance Comparison:")
    print(f"Protocol Buffers - Serialize: {pb_serialize_time:.4f}s, Deserialize: {pb_deserialize_time:.4f}s")
    print(f"Pickle - Serialize: {pickle_serialize_time:.4f}s, Deserialize: {pickle_deserialize_time:.4f}s")
    print(f"Protocol Buffers size: {len(pb_data)} bytes")
    print(f"Pickle size: {len(pickle_data)} bytes")
