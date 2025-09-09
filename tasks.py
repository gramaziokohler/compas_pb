from pathlib import Path
from invoke.collection import Collection

from compas_invocations2 import build
from compas_invocations2 import style
from compas_invocations2 import tests

from compas_pb.invocations import generate_proto_classes
from compas_pb.invocations import create_class_assets
from compas_pb.invocations import docs

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
    generate_proto_classes,
    create_class_assets,
)

ns.configure(
    {
        "base_folder": Path(__file__).parent,
        "proto_folder": Path("./IDL") / "compas_pb" / "generated",
        "proto_include_paths": [Path("./IDL")],
        "proto_out_folder": Path("./src"),
         # typescript,javascript, and go need other compiler plugins
        "proto_target_languages": ["cpp", "csharp", "java", "objc", "php", "ruby"],
    }
)
