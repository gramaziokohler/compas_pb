#!/bin/bash

# TODO: Implement it
echo "Clear the old generated files"
rm -rf ./src/compas_pb/data/*.py
./proto/linux64/bin/protoc --proto_path=./src/compas_pb/IDL/ --python_out=./src/compas_pb/ ./src/compas_pb/IDL/**/*.proto
