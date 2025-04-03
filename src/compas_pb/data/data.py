
# import os
# import sys
#
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from compas.data import Data
from compas.geometry import Frame, Line, Point, Vector

from compas_pb.data import point_pb2 as PointData
from compas_pb.data import line_pb2 as LineData
from compas_pb.data import frame_pb2 as FrameData
from compas_pb.data import vector_pb2 as VectorData
from compas_pb.data import element_pb2 as ElementData
from compas_pb.data import message_pb2 as AnyData


class Element(Data):
    """Mock class to simulate a data structure"""

    def __init__(self, frame, xsize, ysize, zsize, name=None):
        super(Element, self).__init__(name)
        self.name = name
        self.frame = frame
        self.xsize = xsize
        self.ysize = ysize
        self.zsize = zsize


def point_to_pb(point):
    point_data = PointData.PointData()

    point_data.guid = str(point.guid)
    point_data.name = point.name
    point_data.x = point.x
    point_data.y = point.y
    point_data.z = point.z

    return point_data, AnyData.DataType.POINT


def vector_to_pb(vector):
    vector_data = VectorData.VectorData()

    vector_data.guid = str(vector.guid)
    vector_data.name = vector.name
    vector_data.x = vector.x
    vector_data.y = vector.y
    vector_data.z = vector.z

    return vector_data, AnyData.DataType.VECTOR


def line_to_pb(line):
    line_data = LineData.LineData()
    start, _ = point_to_pb(line.start)
    end, _ = point_to_pb(line.end)

    line_data.guid = str(line.guid)
    line_data.name = line.name
    line_data.start.CopyFrom(start)
    line_data.end.CopyFrom(end)

    return line_data, AnyData.DataType.LINE


def frame_to_pb(frame):
    frame_data = FrameData.FrameData()
    point, _ = point_to_pb(frame.point)
    xaxis, _ = vector_to_pb(frame.xaxis)
    yaxis, _ = vector_to_pb(frame.yaxis)

    frame_data.guid = str(frame.guid)
    frame_data.name = frame.name
    frame_data.point.CopyFrom(point)
    frame_data.xaxis.CopyFrom(xaxis)
    frame_data.yaxis.CopyFrom(yaxis)

    return frame_data, AnyData.DataType.FRAME


def element_to_pb(element):
    element_data = ElementData.ElementData()
    frame, _ = frame_to_pb(element.frame)

    element_data.guid = str(element.guid)
    element_data.name = element.name
    element_data.frame.CopyFrom(frame)
    element_data.xsize = element.xsize
    element_data.ysize = element.ysize
    element_data.zsize = element.zsize

    return element_data, AnyData.DataType.ELEMENT


SERIALIZERS = {
    Point: point_to_pb,
    Vector: vector_to_pb,
    Line: line_to_pb,
    Frame: frame_to_pb,
    Element: element_to_pb,
}


def serialize_any(obj):
    """Serialize any object to a protobuf message"""
    if isinstance(obj, list):
        type_enum = AnyData.DataType.LIST
        offset = serialize_list(obj)
    elif isinstance(obj, dict):
        type_enum = AnyData.DataType.DICT
        offset = serialize_dict(obj)
    else:
        serializer = SERIALIZERS.get(type(obj))
        if not serializer:
            raise ValueError(f"Unsupported type: {type(obj)}")
        offset, type_enum = serializer(obj)
    return type_enum, offset


def serialize_any_wrapper(obj):
    """Wraps Any protobuf data in a protobuf AnyData."""
    type_enum, offset = serialize_any(obj)
    any_data = AnyData.AnyData()
    any_data.type = type_enum

    dtype = AnyData.DataType.Name(type_enum).lower()
    getattr(any_data, dtype).CopyFrom(offset)

    return any_data


def serialize_list(data_list):
    """Serialize a Python list containing mixed data types."""
    list_data = AnyData.ListData()
    for item in data_list:
        list_data.data.append(serialize_any_wrapper(item))
    return list_data


def serialize_dict(data_dict):
    """Serialize a Python dictionary containing mixed data types."""
    dict_data = AnyData.DictData()
    for key, value in data_dict.items():
        dict_data.data[key].CopyFrom(serialize_any_wrapper(value))
    return dict_data


def serialize_message(data):
    """Serialize a top-level protobuf message."""
    message_data = serialize_any_wrapper(data)
    message = AnyData.MessageData(data=message_data)
    return message.SerializeToString()


def main():
    # Example nested data structure
    frame = Frame.worldXY()
    element = Element(frame, 1.0, 2.0, 3.0, name="Element")
    nested_data = {
        "point": Point(1.0, 2.0, 3.0),
        "line": Line(Point(1.0, 2.0, 3.0), Point(4.0, 5.0, 6.0)),
        "list": [Point(4.0, 5.0, 6.0), [Vector(7.0, 8.0, 9.0)]],  # Nested list
        "frame": frame,
        "element": element,
    }

    # Serialize and save
    binary_data = serialize_message(nested_data)
    print("Successfully serialized")
    with open("./temp/nested_data.bin", "wb") as f:
        f.write(binary_data)

    # Deserialize
    with open("./temp/nested_data.bin", "rb") as f:
        binary_data = f.read()
        proto_data = AnyData.MessageData()
        proto_data.ParseFromString(binary_data)

        # for debug
        print(f"Successfully deserialized\n{proto_data}")


if __name__ == "__main__":
    main()
