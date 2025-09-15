from unittest.mock import patch

from compas.datastructures import Graph
from compas.geometry import Point
from compas_pb import pb_dump_json
from compas_pb import pb_load_json
from compas_pb.registry import SerializerRegistry


def test_graph_fallback_serialization():
    """Test that Graph uses fallback serialization by patching the serializer registry."""
    graph = Graph()
    graph.add_node(0, name="A")
    graph.add_node(1, name="B")
    graph.add_edge(0, 1)

    with patch.object(SerializerRegistry, "get_serializer", return_value=None):
        json_data = pb_dump_json(graph)

    loaded_graph = pb_load_json(json_data)

    assert isinstance(loaded_graph, Graph)
    assert loaded_graph.number_of_nodes() == 2
    assert loaded_graph.number_of_edges() == 1
    assert loaded_graph.node_attribute(0, "name") == "A"
    assert loaded_graph.node_attribute(1, "name") == "B"


def test_forced_fallback_serialization():
    """Test that patching the serializer registry forces fallback serialization for a normally supported type."""
    point = Point(1.0, 2.0, 3.0)

    with patch.object(SerializerRegistry, "get_serializer", return_value=None):
        json_data = pb_dump_json(point)

    loaded_point = pb_load_json(json_data)

    assert isinstance(loaded_point, Point)
    assert loaded_point.x == 1.0
    assert loaded_point.y == 2.0
    assert loaded_point.z == 3.0
