def plugin_setup():
    from compas_timber.elements import Beam  # Replace with the actual import path for Beam

    from compas_pb.data.data import _ProtoBufferAny
    from compas_pb.data.data import register
    from compas_timber_pb.data.data import _ProtoBufferBeam

    """Setup function for registering the Beam serializer."""
    try:
        register(Beam, _ProtoBufferBeam)
    except ValueError as e:
        print(f"Registration failed: {e}")

    # Debug: Verify registration
    print("_ProtoBufferAny.SERIALIZER contents:", _ProtoBufferAny.SERIALIZER)
