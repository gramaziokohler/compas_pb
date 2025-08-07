from __future__ import print_function

import os

# please don't remove me! I trigger the registration of all the core serializers
import compas_pb.conversions  # noqa: F401  #

from .api import pb_load
from .api import pb_dump
from .api import pb_dump_bts
from .api import pb_load_bts
from .api import pb_dump_json
from .api import pb_load_json


__author__ = ["Chen Kasirer"]
__copyright__ = "Gramazio Kohler Research"
__license__ = "MIT License"
__email__ = "kasirer@arch.ethz.ch"
__version__ = "0.0.0"


HERE = os.path.dirname(__file__)

HOME = os.path.abspath(os.path.join(HERE, "../../"))
DATA = os.path.abspath(os.path.join(HOME, "data"))
DOCS = os.path.abspath(os.path.join(HOME, "docs"))
TEMP = os.path.abspath(os.path.join(HOME, "temp"))
IDL = os.path.abspath(os.path.join(HOME, "IDL"))

__all__ = [
    "HOME",
    "DATA",
    "DOCS",
    "TEMP",
    "IDL",
    "pb_load",
    "pb_dump",
    "pb_dump_bts",
    "pb_load_bts",
    "pb_dump_json",
    "pb_load_json",
]
