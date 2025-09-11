<p align="center">
    <img src="compas_pb.png" alt="compas_pb" width="200">
</p>

A COMPAS extension which lets you serialize and deserialize COMPAS `Data` types using protobuf.

## Installation

Stable releases can be installed from PyPI.

```bash
pip install compas_pb
```

## Basic Usage

### Serialize to file

```python
from compas.geometry import Vector
from compas_pb import pb_dump
from compas_pb import pb_load

PATH = "vector.data"

vector = Vector(1.0, 2.0, 3.0)

pb_dump(vector, PATH)

loaded_vector = pb_load(PATH)

```

### (De)serialize to bytes

```python
from compas.geometry import Vector
from compas_pb import pb_dump_bts
from compas_pb import pb_load_bts

vector = Vector(1.0, 2.0, 3.0)

bytes_vector = pb_dump_bts(vector)

loaded_vector = pb_load_bts(bytes_vector)

```

### Serialization of arbitrarily nested data structures

```python
from compas.geometry import Vector
from compas.geometry import Polyline
from compas_pb import pb_dump_bts
from compas_pb import pb_load_bts

data = {
    "direction": Vector(1.0, 2.0, 3.0),
    "outlines": 
        [
            Polyline([0, 0, 0], [1, 1, 1], [2, 2, 2]), 
            Polyline([3, 3, 3], [4, 4, 4], [5, 5, 5])
        ],
}

pb_data = pb_dump_bts(data)

loaded_data = pb_load_bts(pb_data)

```

## Documentation

For further "getting started" instructions, a tutorial, examples, and an API reference,
please check out the online documentation here: [compas_pb docs](https://gramaziokohler.github.io/compas_pb)

## Issue Tracker

If you find a bug or if you have a problem with running the code, please file an issue on the [Issue Tracker](https://github.com/gramaziokohler/compas_pb/issues).
