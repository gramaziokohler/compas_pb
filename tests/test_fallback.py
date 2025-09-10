from compas.datastructures import Graph
from compas_pb import pb_dump_json
from compas_pb import pb_load_json


def test_graph_fallback_serialization():
    graph = Graph()
    graph.add_node(0, name="A")
    graph.add_node(1, name="B")
    graph.add_edge(0, 1)

    json_data = pb_dump_json(graph)

    loaded_graph = pb_load_json(json_data)

    assert isinstance(loaded_graph, Graph)
    assert loaded_graph.number_of_nodes() == 2
    assert loaded_graph.number_of_edges() == 1
    assert loaded_graph.node_attribute(0, "name") == "A"
    assert loaded_graph.node_attribute(1, "name") == "B"
