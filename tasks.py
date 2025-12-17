from pathlib import Path
from invoke.collection import Collection
from invoke.tasks import task
from compas_invocations2 import build
from compas_invocations2 import style
from compas_invocations2 import tests

from compas_pb.invocations import generate_proto_classes
from compas_pb.invocations import create_class_assets
from compas_pb.invocations import proto_docs


def _patch_versions_info():
    from mike.versions import VersionInfo

    @classmethod
    def from_json(cls, data: dict):
        instance = cls(data.pop("version"), data.pop("title"), data.pop("aliases"), data.pop("properties", None))
        instance.external_attrs = data
        return instance

    def to_json(self):
        data = {"version": str(self.version), "title": self.title, "aliases": list(self.aliases)}
        if self.properties:
            data["properties"] = self.properties
        if self.external_attrs:
            data.update(self.external_attrs)
        return data

    VersionInfo.from_json = from_json
    VersionInfo.to_json = to_json


@task()
def mike_deploy(ctx, version: str):
    _patch_versions_info()
    cmd = f"mike deploy --push --update-aliases {version} latest"
    print(f"Running: {cmd}")
    ctx.run(cmd)


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
    generate_proto_classes,
    create_class_assets,
    proto_docs,
)

ns.configure(
    {
        "base_folder": Path(__file__).parent,
        "proto_folder": Path("./src") / "compas_pb" / "protobuf_defs" / "compas_pb" / "generated",
        "proto_include_paths": [Path("./src") / "compas_pb" / "protobuf_defs"],
        "proto_out_folder": Path("./src"),
    }
)
