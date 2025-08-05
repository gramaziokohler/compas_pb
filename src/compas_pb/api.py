from typing import Dict
from typing import List

from compas.data import Data

from compas_pb.io_tool import open_file
from compas_pb.serializer import serialize_message_bts
from compas_pb.serializer import serialize_message_to_json
from compas_pb.serializer import deserialize_message
from compas_pb.serializer import deserialize_message_from_json


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
    message_bts = serialize_message_bts(data)

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
        message = deserialize_message(message_bts)
        return message


def pb_dump_json(data: Data | Dict | List) -> str:
    """Write a collection of COMPAS object to a JSON string.


    Parameters:
    ----------
    data : Data | Dict | List

        Any  protobuffer serializable object. This includes any (combination of) COMPAS object(s).


    Returns:
    -------
    string

        The JSON string representation of the data.

    Example:
    --------
    pass

    """
    json_str = serialize_message_to_json(data)
    return json_str


def pb_load_json(data: str) -> Data | Dict | List:
    """Read a collection of COMPAS object from a JSON string.


    Parameters:
    ----------
    data : str

        A JSON string representation of the data.


    Returns:
    -------
    Data | Dict | List


        The (COMPAS) object(s) contained in the JSON string.

    Example:
    --------
    pass

    """
    message = deserialize_message_from_json(data)
    return message


def pb_dump_bts(data: Data | Dict | list) -> bytes:
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
    message_bts = serialize_message_bts(data)

    return message_bts


def pb_load_bts(data: bytes) -> Data | Dict | List:
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
    message_bts = deserialize_message(data)
    return message_bts
