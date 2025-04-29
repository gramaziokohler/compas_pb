from compas.plugins import pluggable

from compas_pb.data.data import _ProtoBufferAny


@pluggable(category="factories", selector="collect_all")
def register_serializer():
    # having no plugins is not necessarily a problem
    pass


def register(item_type, serializer):
    """Register a serializer for a specific item type."""
    if item_type not in _ProtoBufferAny.SERIALIZER:
        _ProtoBufferAny.SERIALIZER[item_type] = serializer
    else:
        raise ValueError(f"Serializer for {item_type} already registered.")
