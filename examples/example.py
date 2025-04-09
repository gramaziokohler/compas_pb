from pathlib import Path

from compas.geometry import Frame, Line, Point, Vector

from compas_pb.data.data_handling import pb_dump, pb_dump_bts, pb_load, pb_load_bts


def main():
    # Example nested data structure
    # element = Element(frame, 1.0, 2.0, 3.0, name="Element")
    nested_data = {
        "point": Point(1.0, 2.0, 3.0),
        "line": Line(Point(1.0, 2.0, 3.0), Point(4.0, 5.0, 6.0)),
        "list": [Point(4.0, 5.0, 6.0), [Vector(7.0, 8.0, 9.0)]],  # Nested list
        "frame": Frame(point=Point(1.0, 2.0, 3.0), xaxis=Vector(4.0, 5.0, 6.0), yaxis=Vector(7.0, 8.0, 9.0)),
        # "element": element,
    }

    FILEPATH = Path(__file__).parent / "temp" / "nested_data.bin"

    # Load the data from the file
    pb_dump(nested_data, filepath=FILEPATH.as_posix())

    # Deserialize the data
    loaded_data = pb_load(filepath=FILEPATH.as_posix())
    print(type(loaded_data))
    print(f"loaded_data_from_bin: {loaded_data}\n")

    # bts
    data_bts = pb_dump_bts(nested_data)
    print(f"data_bts: {data_bts}\n")
    loaded_data_bts = pb_load_bts(data_bts)
    print(f"loaded_data_from_bts: {loaded_data_bts}")


if __name__ == "__main__":
    main()
