from __future__ import print_function

import os

# this is imported for side effects, to register the protobuf types
import compas_pb.data._data  # type: ignore # noqa: F401


__author__ = ["Chen Kasirer"]
__copyright__ = "Gramazio Kohler Research"
__license__ = "MIT License"
__email__ = "kasirer@arch.ethz.ch"
__version__ = "0.1.0"


HERE = os.path.dirname(__file__)

HOME = os.path.abspath(os.path.join(HERE, "../../"))
DATA = os.path.abspath(os.path.join(HOME, "data"))
DOCS = os.path.abspath(os.path.join(HOME, "docs"))
TEMP = os.path.abspath(os.path.join(HOME, "temp"))
IDL = os.path.abspath(os.path.join(HOME, "IDL"))

__all__ = ["HOME", "DATA", "DOCS", "TEMP"]
