********************************************************************************
compas_pb.data
********************************************************************************

.. currentmodule:: compas_pb.data

The main data module provides high-level functions for serializing and deserializing COMPAS objects using Protocol Buffers.

Data Handling Functions
=======================

.. autosummary::
    :toctree: generated/
    :nosignatures:

    pb_dump
    pb_load
    pb_dump_bts
    pb_load_bts
    pb_dump_json
    pb_load_json

Core Classes
============

.. autosummary::
    :toctree: generated/
    :nosignatures:

    ProtoBufferData
    ProtoBufferAny

Registry Decorators
===================

.. autosummary::
    :toctree: generated/
    :nosignatures:

    pb_serializer
    pb_deserializer

Conversion Functions
====================

.. autosummary::
    :toctree: generated/
    :nosignatures:

    point_to_pb
    point_from_pb
    vector_to_pb
    vector_from_pb
    line_to_pb
    line_from_pb
    frame_to_pb
    frame_from_pb
