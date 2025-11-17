from compas_pb import pb_dump_bts
from compas_pb import pb_load_bts


def test_none_serialization():
    serialized = pb_dump_bts({"none_data": None})
    deserialized = pb_load_bts(serialized)

    assert deserialized["none_data"] is None
