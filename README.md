# compas_pb

Protobuf extension for COMPAS Data

## Installation

Stable releases can be installed from PyPI.

```bash
pip install compas_pb
```

To install the latest version for development, do:

```bash
git clone https://github.com/gramaziokohler/compas_pb.git
cd compas_pb
pip install -e ".[dev]"
```

## Development

```
uv pip install -e . --upgrade
```

- Protobuf version 6.31.0(Supported any data type)

#### Re-generate `.proto` files to Python Classes

```bash
invoke protobuf.generate-proto-classes
```

#### Re-generate `.proto` files to cSharp Classes

```bash
./proto/win64/bin/protoc.exe --proto_path=./IDL --csharp_out=./cSharp/CompasProtobuffer/src/proto ./IDL/compas_pb/data/proto/*.proto
```


## Documentation

For further "getting started" instructions, a tutorial, examples, and an API reference,
please check out the online documentation here: [compas_pb docs](https://gramaziokohler.github.io/compas_pb)

## Issue Tracker

If you find a bug or if you have a problem with running the code, please file an issue on the [Issue Tracker](https://github.com/gramaziokohler/compas_pb/issues).
