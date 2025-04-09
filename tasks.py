from __future__ import print_function

import os

from compas_invocations2 import build
from compas_invocations2 import docs
from compas_invocations2 import style
from compas_invocations2 import tests
from invoke import Collection
from compile_protos import generate_proto_classes

protobuf = Collection("protobuf")

protobuf.add_task(generate_proto_classes, name="generate_proto_classes")

ns = Collection(
    docs.help,
    style.check,
    style.lint,
    style.format,
    docs.docs,
    docs.linkcheck,
    tests.test,
    tests.testdocs,
    tests.testcodeblocks,
    build.prepare_changelog,
    build.clean,
    build.release,
    build.build_ghuser_components,
    protobuf,
)

ns.configure(
    {
        "base_folder": os.path.dirname(__file__),
        "ghuser": {
            "source_dir": "src/compas_pb_ghpython/components",
            "target_dir": "src/compas_pb_ghpython/components/ghuser",
            "prefix": "compas_pb: ",
        },
    }
)
