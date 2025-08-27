from typing import Dict
from typing import List
from typing import Union

from compas.data import Data

from compas_pb.core import deserialize_message
from compas_pb.core import deserialize_message_from_json
from compas_pb.core import serialize_message_bts
from compas_pb.core import serialize_message_to_json


def pb_dump(data: Union[Data, Dict[str, Data], List[Data]], filepath: str) -> None:
    """Write a collection of COMPAS object to a binary file.

    Parameters
    ----------
    data : Union[Data, Dict, List]
        Any  protobuffer serializable object.
        This includes any (combination of) COMPAS object(s).
    filepath : path string or file-like object
        A writeable file-like object or the path to a file.

    Returns
    -------
    None

    """
    message_bts = serialize_message_bts(data)

    with open(filepath, "wb") as f:
        f.write(message_bts)


def pb_load(filepath: str) -> Union[Data, Dict, List]:
    """Read a collection of COMPAS object from a binary file.

    Parameters
    ----------
    filepath : path string or file-like object

        A readable file-like object or the path to a file.

    Returns
    -------
    Union[Data, Dict, List]

        The (COMPAS) object(s) contained in the file.

    """

    with open(filepath, "rb") as f:
        message_bts = f.read()
        message = deserialize_message(message_bts)
        return message


def pb_dump_json(data: Union[Data, Dict, List]) -> str:
    """Write a collection of COMPAS object to a JSON string.


    Parameters
    ----------
    data : Union[Data, Dict, List]

        Any  protobuffer serializable object. This includes any (combination of) COMPAS object(s).


    Returns
    -------
    string

        The JSON string representation of the data.

    """
    json_str = serialize_message_to_json(data)
    return json_str


def pb_load_json(data: str) -> Union[Data, Dict, List]:
    """Read a collection of COMPAS object from a JSON string.


    Parameters
    ----------
    data : str

        A JSON string representation of the data.


    Returns
    -------
    Union[Data, Dict, List]


        The (COMPAS) object(s) contained in the JSON string.

    """
    message = deserialize_message_from_json(data)
    return message


def pb_dump_bts(data: Union[Data, Dict, list]) -> bytes:
    """Write a collection of COMPAS object to a btye string.


    Parameters
    ----------
    data : Union[Data, Dict, List]

        Any  protobuffer serializable object.
        This includes any (combination of) COMPAS object(s).

    Returns
    -------
    None

    """
    message_bts = serialize_message_bts(data)

    return message_bts


def pb_load_bts(data: bytes) -> Union[Data, Dict, List]:
    """Read a collection of COMPAS object from a binary file.

    Parameters
    ----------
    filepath : path string or file-like object
        A readable file-like object or the path to a file.


    Returns
    -------
    Union[Data, Dict, List]
        The (COMPAS) object(s) contained in the file.

    """
    message_bts = deserialize_message(data)
    return message_bts
