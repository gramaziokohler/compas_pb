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
        instance = cls(
            data.pop("version"),
            data.pop("title"),
            data.pop("aliases"),
            data.pop("properties", None),
        )
        instance.external_attrs = data
        return instance

    def to_json(self):
        data = {
            "version": str(self.version),
            "title": self.title,
            "aliases": list(self.aliases),
        }
        if self.properties:
            data["properties"] = self.properties
        if getattr(self, "external_attrs", None):
            data.update(self.external_attrs)
        return data

    VersionInfo.from_json = from_json
    VersionInfo.to_json = to_json


@task()
def mike_deploy(ctx, version: str):
    from mike import driver
    from argparse import Namespace

    _patch_versions_info()

    args = Namespace(
        version=version,
        title=version,
        aliases=["latest"],
        update_aliases=True,
        push=False,  # TODO: enable push later
        branch="gh-pages",
        remote="origin",
        message=None,
        config_file=None,
        allow_empty=False,
        deploy_prefix=None,
        ignore_remote_status=False,
        alias_type="symlink",
        template=None,
        set_props=None,
        quiet=False,
    )

    driver.deploy(None, args)


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
    mike_deploy,
)

ns.configure(
    {
        "base_folder": Path(__file__).parent,
        "proto_folder": Path("./src") / "compas_pb" / "protobuf_defs" / "compas_pb" / "generated",
        "proto_include_paths": [Path("./src") / "compas_pb" / "protobuf_defs"],
        "proto_out_folder": Path("./src"),
    }
)
