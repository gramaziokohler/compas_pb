from pathlib import Path
from invoke.collection import Collection

from compas_invocations2 import build
from compas_invocations2 import style
from compas_invocations2 import tests

from .compile_protos import generate_proto_classes
from .compile_protos import docs

ns = Collection(
    style.check,
    style.lint,
    style.format,
    tests.test,
    tests.testdocs,
    tests.testcodeblocks,
    build.prepare_changelog,
    build.clean,
    build.release,
    docs,
    generate_proto_classes
)

ns.configure({ "base_folder": Path(__file__).parent.parent })
