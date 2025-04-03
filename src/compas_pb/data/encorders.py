from compas.data import Data

class DataEncoder:
    """Data Encoder for COMPAS objects to protobuf messages."""

    @classmethod
    def encode(cls, obj):
        if not isinstance(obj, Data):
            raise TypeError("Expected a COMPAS Data object")



if __name__ == "__main__":
    # Example usage
    from compas.geometry import Point

    point = [0,0,0]
    encoder = DataEncoder()
    encoded_point = encoder.encode(point)
    print(encoded_point)
