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

- Protobuf version 6.30.2

#### Re-generate pb_to_py files
- Windows

```powershell
# version check
.\proto\win64\bin\protoc.exe --version

# proto to python
.\proto\win64\bin\protoc.exe --proto_path=.\IDL --python_out=.\src .\IDL\compas_pb\data\proto\*.proto


# proto to c#
.\proto\win64\bin\protoc.exe --proto_path=IDL\compas_pb\data\proto\ --csharp_out=compas_cSharp --csharp_opt=base_namespace=IDL\compas_pb\data\proto\*.proto
```

- Linux/ MacOS

```bash
# version check
./proto/linux64/bin/protoc --version


# proto file location "./IDL/compas_pb/data/proto/*.proto"
# proto to python
./proto/linux64/bin/protoc --proto_path=./IDL --python_out=./src ./IDL/**/*.proto
./proto/macaarch64/bin/protoc --proto_path=./IDL --python_out=./src ./IDL/**/*.proto

# proto to c#
protoc --proto_path=bar --csharp_out=src --csharp_opt=base_namespace=Example player.proto


```

## Documentation

For further "getting started" instructions, a tutorial, examples, and an API reference,
please check out the online documentation here: [compas_pb docs](https://gramaziokohler.github.io/compas_pb)

## Issue Tracker

If you find a bug or if you have a problem with running the code, please file an issue on the [Issue Tracker](https://github.com/gramaziokohler/compas_pb/issues).
