from typing import Dict, List

from compas.data import Data
from compas_pb.data.serializer import DataSerializer, DataDeserializer

from compas_pb.data.io_tool import open_file


def pb_dump(data: Data | Dict[str, Data] | List[Data], filepath: str) -> None:
    """Write a collection of COMPAS object to a binary file.

    Parameters:
    ----------
    data : Data | Dict | List
        Any  protobuffer serializable object.
        This includes any (combination of) COMPAS object(s).
    filepath : path string or file-like object
        A writeable file-like object or the path to a file.

    Returns:
    -------
    None

    Example:
    --------
    pass

    """
    message_bts = DataSerializer(data).serialize_message_bts()

    with open_file(filepath, "wb") as f:
        f.write(message_bts)


def pb_load(filepath: str) -> Data | Dict | List:
    """Read a collection of COMPAS object from a binary file.

    Parameters:
    ----------
    filepath : path string or file-like object
        A readable file-like object or the path to a file.


    Returns:
    -------
    Data | Dict | List
        The (COMPAS) object(s) contained in the file.

    """

    with open_file(filepath, "rb") as f:
        message_bts = f.read()
        message = DataDeserializer(message_bts).deserialize_message()
        return message

def pb_dump_json(data):
    pass


def pb_loads_json(data):
    pass


def pb_dump_bts(data):

    """Write a collection of COMPAS object to a btye string.

    Parameters:
    ----------
    data : Data | Dict | List
        Any  protobuffer serializable object.
        This includes any (combination of) COMPAS object(s).
    Returns:
    -------
    None

    Example:
    --------
    pass

    """
    message_bts = DataSerializer(data).serialize_message_bts()

    return message_bts


def pb_load_bts(data: bytes):

    """Read a collection of COMPAS object from a binary file.

    Parameters:
    ----------
    filepath : path string or file-like object
        A readable file-like object or the path to a file.


    Returns:
    -------
    Data | Dict | List
        The (COMPAS) object(s) contained in the file.

    """
    message_bts = DataDeserializer(data).deserialize_message_bts()
    return message_bts
