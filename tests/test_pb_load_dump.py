import pytest
from pathlib import Path

from compas.geometry import Point
from compas.geometry import Frame
from compas.geometry import Vector
from compas.geometry import Line

from compas_pb.data.data_handling import pb_dump
from compas_pb.data.data_handling import pb_dump_bts
from compas_pb.data.data_handling import pb_dump_json
from compas_pb.data.data_handling import pb_load
from compas_pb.data.data_handling import pb_load_bts
from compas_pb.data.data_handling import pb_load_json


@pytest.fixture
def temp_file():
    filepath = Path(__file__).parent / "nested_data.bin"
    return filepath


@pytest.fixture
def point():
    return Point(1, 2, 3)


@pytest.fixture
def line():
    return Line(Point(1, 2, 3), Point(4, 5, 6))


@pytest.fixture
def frame():
    return Frame(Point(1, 2, 3), Vector(4, 5, 6), Vector(7, 8, 9))


@pytest.fixture
def vector():
    return Vector(1, 2, 3)


@pytest.fixture
def nested_list():
    return [Point(4.0, 5.0, 6.0), [Vector(7.0, 8.0, 9.0), [Point(10.0, 11.0, 12.0)]]]


@pytest.fixture
def primitive_data():
    return (["I am String", [0.0, 0.5, 1.5], True, 5, 10],)


@pytest.fixture
def nested_dict():
    return {
        "point": Point(1.0, 2.0, 3.0),
        "line": [Point(1.0, 2.0, 3.0), Point(4.0, 5.0, 6.0)],
        "list of Object": [Point(4.0, 5.0, 6.0), [Vector(7.0, 8.0, 9.0), Point(0.0, 0.5, 0.3)]],  # Nested list
        "frame": Frame(Point(1.0, 2.0, 3.0), Vector(4.0, 5.0, 6.0), Vector(7.0, 8.0, 9.0)),
        "list of primtive": ["I am String", [0.0, 0.5, 1.5], True, 5, 10],
    }


data = nested_dict


def test_pb_dump(temp_file, data):
    # Test pb_dump with a file path
    pb_dump(data, filepath=temp_file.as_posix())
    assert temp_file.exists()


def test_pb_load(temp_file, data):
    # Test pb_load with a file path
    pb_dump(data, filepath=temp_file.as_posix())
    loaded_data = pb_load(filepath=temp_file.as_posix())
    assert loaded_data == data


# def test_pb_dump_json(temp_file, data):
#     # Test pb_dump_json with a file path
#     json_string = pb_dump_json(data)
#     assert isinstance(json_string, str)

# def test_pb_load_json(temp_file, data):
#     # Test pb_load_json with a JSON string
#     json_string = pb_dump_json(data)
#     loaded_data = pb_load_json(json_string)
#     assert loaded_data == data

# def test_pb_dump_bts(temp_file, data):
#     # Test pb_dump_bts with a file path
#     bts_data = pb_dump_bts(data)
#     assert isinstance(bts_data, bytes)

# def test_pb_load_bts(temp_file, data):
#     # Test pb_load_bts with a bytes object
#     bts_data = pb_dump_bts(data)
#     loaded_data = pb_load_bts(bts_data)
#     assert loaded_data == data
