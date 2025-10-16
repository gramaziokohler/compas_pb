# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

### Added

### Changed

### Removed


## [0.4.4] 2025-10-16

### Added

### Changed

### Removed


## [0.4.3] 2025-10-16

### Added

### Changed

### Removed


## [0.4.2] 2025-10-16

### Added

* Added support for `compas.geometry.Capsule` serialization and deserialization.
* Added support for `compas.geometry.Quaternion` serialization and deserialization.
* Added support for `compas.geometry.Scale` serialization and deserialization.
* Added support for `compas.geometry.Reflection` serialization and deserialization.
* Added support for `compas.geometry.Shear` serialization and deserialization.
* Added support for `compas.geometry.Projection` serialization and deserialization.
* Added support for `compas.geometry.Bezier` serialization and deserialization.
* Added support for `compas.geometry.Hyperbola` serialization and deserialization.
* Added support for `compas.geometry.Parabola` serialization and deserialization.
* Added support for `compas.geometry.Polyhedron` serialization and deserialization.

### Changed

* Fixed running `protoc` fails with permission denied on Mac.

### Removed


## [0.4.1] 2025-10-13

### Added

### Changed

* Fixed `invoke` task to work on MacOS with Apple Silicon.

### Removed


## [0.4.0] 2025-09-10

### Added

* Added attribute `version` in `message.proto` to track/ship the package version
* Added `.proto` file into build package.
* Added `FallbackData` member `fallback` to `AnyData` to allow for fallback serialization of unknown types.

### Changed

* Changed plugin discovery to use entry points instead of the COMPAS plugin system's name scanning.
* Added `importlib_metadata` as a conditional dependency to support Python <= 3.9.
* Renamed `compas_pb.IDL` to `compas_pb.PROTOBUF_DEFS`.

### Removed

* Removed `compas_pb.DATA`.
* Removed `compas_pb.DOCS`.
* Removed `compas_pb.TEMP`.


## [0.3.1] 2025-08-27

### Added

* Added `create_class_assets` for invoke task to package the proto generated class file with `cpp`, `csharp` into assets.

### Changed

* Fixed `compas_pb` support in Python 3.9.

### Removed


## [0.3.0] 2025-08-26

### Added

* Added module `compas_pb.invocations` which offers re-usable protobuf related tasks for plugins. 

### Changed

* remove `PrimitiveData` into `AnyData` with `Google.WellKownType.value`.

### Removed


## [0.2.0] 2025-08-20

### Added

* change `ListData.data` and `DictData.data` to better naming of `ListData.items` `DictData.items`.
* Added support for `compas.geometry.Plane` serialization and deserialization.
* Added support for `compas.geometry.Polygon` serialization and deserialization.
* Added support for `compas.geometry.Box` serialization and deserialization.
* Added support for `compas.geometry.Arc` serialization and deserialization.
* Added support for `compas.geometry.Sphere` serialization and deserialization.
* Added support for `compas.geometry.Cylinder` serialization and deserialization.
* Added support for `compas.geometry.Cone` serialization and deserialization.
* Added support for `compas.geometry.Torus` serialization and deserialization.
* Added support for `compas.geometry.Ellipse` serialization and deserialization.
* Added support for `compas.geometry.Polyline` serialization and deserialization.
* Added support for `compas.geometry.Pointcloud` serialization and deserialization.
* Added support for `compas.geometry.Transformation` serialization and deserialization.
* Added support for `compas.geometry.Translation` serialization and deserialization.
* Added support for `compas.geometry.Rotation` serialization and deserialization.

### Changed

### Removed


## [0.1.1] 2025-08-07

### Added

### Changed

* Removed debug print from registration.
* Added missing docs URL to the README.

### Removed


## [0.1.0] 2025-08-07

### Added

### Changed

* Changed to use the native protobuf Any to deal with our arbitrary data.

### Removed

