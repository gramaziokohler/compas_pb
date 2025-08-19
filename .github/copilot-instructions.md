This repository is a COMPAS extension which allows users to serialize and deserialize COMPAS data structures to and from Protocol Buffers.
Adding support for additional data types is acheived by adding new `.proto` files to the `IDL` directory and running the code generation script.
Serializers to and from protobuf are then defined in the `src/conversions.py` file.
The public API for the library is imported from the root level and includes `pb_dump` and `pb_load` functions and others.

### Required Before Each Commit
- Run `make fmt` before committing any changes to ensure proper code formatting
- This will run gofmt on all Go files to maintain consistent style

### Development Flow
- make a virtual environment and install with developer setting using `pip install -e .[dev]`
- use `invoke lint` for linting check
- use `invoke format` for auto formatting
- use `invoke tests` to run the unittests
- use `invoke generate-proto-classes -t python` to create the python classes for the `.proto` definitions.

## Repository Structure
- `src/`: is where the library code is
- `src/core.py`: contains core library logic
- `src/conversions.py`: contains conversion functions between COMPAS types to their protobuf representation.
- `src/api.py`: contains  
- `src/generated`: contains the auto-generated python class definitions created from the IDL files.
- `IDL` contains protobuf definitions for types in the compas library, typically geometry primitives etc importable from `compas.geometry`.

## Key Guidelines
1. Follow python's best practices and idiomatic patterns
2. Maintain existing code structure and organization
3. Write unit tests for new functionality. prefer one or two concise tests rather than many different ones
4. Add numpy style docstrings to public API functions and classes.
