from pathlib import Path

from compas.geometry import Point
from compas.geometry import Polyline
from compas.geometry import Frame
from compas.geometry import Vector

from compas_pb.data.data_handling import pb_dump
from compas_pb.data.data_handling import pb_dump_bts
from compas_pb.data.data_handling import pb_dump_json
from compas_pb.data.data_handling import pb_load
from compas_pb.data.data_handling import pb_load_bts
from compas_pb.data.data_handling import pb_load_json


def main():

    FILEPATH = Path(__file__).parent / "temp" / "nested_data.bin"

    # LOAD THE DATA FROM THE FILE
    # pb_dump(data_dict, filepath=FILEPATH.as_posix())

    # DESERIALIZE THE DATA
    loaded_data = pb_load(filepath=FILEPATH.as_posix())
    print(f"pb_load type: {type(loaded_data)}")
    print(f"loaded_data_from_bin: {loaded_data}\n")

    # TO JSONSTRING AND FROM JSONSTRING
    # data_json_string = pb_dump_json(nested_data_diff_types)
    # print(f"data_json_string type: {type(data_json_string)}")
    # print(f"data_json_string: {data_json_string}\n")

    # loaded_data_json = pb_load_json(data_json_string)
    # print(f"loaded_data_from_json type: {type(loaded_data_json)}")
    # print(f"loaded_data_from_json: {loaded_data_json}")

    # TO BTS AND FROM BTS
    # data_bts = pb_dump_bts(nested_data_diff_types)
    # print(f"data_bts type: {type(data_bts)}")
    # loaded_data_bts = pb_load_bts(data_bts)
    # print(f"loaded_data_from_bts type: {type(loaded_data_bts)}")


if __name__ == "__main__":
    main()
