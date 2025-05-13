from pathlib import Path

from compas.geometry import Point
from compas.geometry import Polyline
from compas.geometry import Vector

from compas_pb.data.data_handling import pb_dump
from compas_pb.data.data_handling import pb_dump_bts
from compas_pb.data.data_handling import pb_dump_json
from compas_pb.data.data_handling import pb_load
from compas_pb.data.data_handling import pb_load_bts
from compas_pb.data.data_handling import pb_load_json


def main():
    # Example nested data structure
    # element = Element(frame, 1.0, 2.0, 3.0, name="Element")
    nested_data_diff_types = {
        "point": Point(1.0, 2.0, 3.0),
        "list": [Point(4.0, 5.0, 6.0), [Vector(7.0, 8.0, 9.0)]],  # Nested list
        # "polyline": Polyline([[0, 0, 0], [1, 0, 0], [2, 0, 0], [3, 0, 0]]),
        # "list": ["hey", [0.0, 0.5, 1.5], True, 5, 10]
    }

    FILEPATH = Path(__file__).parent / "temp" / "nested_data.bin"

    # LOAD THE DATA FROM THE FILE
    pb_dump(nested_data_diff_types, filepath=FILEPATH.as_posix())

    # # DESERIALIZE THE DATA
    loaded_data = pb_load(filepath=FILEPATH.as_posix())
    print(f"pb_load type: {type(loaded_data)}")
    print(f"loaded_data_from_bin: {loaded_data}\n")

    # # TO JSONSTRING AND FROM JSONSTRING
    # data_json_string = pb_dump_json(nested_data_diff_types)
    # print(f"data_json_string type: {type(data_json_string)}")
    # # print(f"data_json_string: {data_json_string}\n")

    # loaded_data_json = pb_load_json(data_json_string)
    # print(f"loaded_data_from_json type: {type(loaded_data_json)}")
    # # print(f"loaded_data_from_json: {loaded_data_json}")

    # # TO BTS AND FROM BTS
    # data_bts = pb_dump_bts(nested_data_diff_types)
    # print(f"data_bts type: {type(data_bts)}")
    # loaded_data_bts = pb_load_bts(data_bts)
    # print(f"loaded_data_from_bts type: {type(loaded_data_bts)}")


if __name__ == "__main__":
    main()
