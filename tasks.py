import json
import shutil
import tempfile
from pathlib import Path

from invoke.collection import Collection
from invoke.tasks import task
from compas_invocations2 import build
from compas_invocations2 import style
from compas_invocations2 import tests

from compas_pb.invocations import generate_proto_classes
from compas_pb.invocations import create_class_assets
from compas_pb.invocations import proto_docs

# Old Sphinx-built doc versions that predate the MkDocs/mike migration.
# These use a different versions.json schema (with ``name`` and ``url`` fields)
# that is incompatible with mike's VersionInfo class.
# They are kept in a ``legacy/`` subdirectory on gh-pages with their own
# ``versions.json`` so that mike can manage the root file without conflicts.
LEGACY_VERSIONS = ["0.4.6", "0.3.1", "0.2.0", "0.1.1"]
SITE_BASE_URL = "https://gramaziokohler.github.io/compas_pb"


@task(
    help={
        "push_to_origin": "Whether to push the changes to the origin remote",
        "branch": "The gh-pages branch name (default: gh-pages)",
    }
)
def migrate_legacy_docs(ctx, push_to_origin=False, branch="gh-pages"):
    """One-time migration: move old Sphinx doc versions into a legacy/ subdirectory on gh-pages.

    This separates the Sphinx-style ``versions.json`` (which carries extra
    ``name`` / ``url`` fields) from mike's ``versions.json`` so they no longer
    conflict.  After running this task, ``mike_deploy`` can be used without any
    monkey-patching.

    The task:

    1. Checks out the *gh-pages* branch into a temporary git worktree.
    2. Moves each legacy version directory into ``legacy/<version>/``.
    3. Writes ``legacy/versions.json`` with the Sphinx-compatible entries.
    4. Cleans up the root ``versions.json`` (removes legacy entries and any
       extra fields that mike does not understand).
    5. Commits the result (and optionally pushes).
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        worktree = Path(tmpdir) / "gh-pages"
        ctx.run(f'git worktree add "{worktree}" {branch}')

        try:
            legacy_dir = worktree / "legacy"
            legacy_dir.mkdir(exist_ok=True)

            # --- move old version directories into legacy/ ---
            for ver in LEGACY_VERSIONS:
                src = worktree / ver
                if src.exists():
                    dst = legacy_dir / ver
                    if dst.exists():
                        shutil.rmtree(str(dst))
                    shutil.move(str(src), str(dst))

            # move any "stable" symlink / directory too
            stable = worktree / "stable"
            if stable.exists():
                dst = legacy_dir / "stable"
                if dst.exists():
                    shutil.rmtree(str(dst))
                shutil.move(str(stable), str(dst))

            # --- write legacy/versions.json for the Sphinx version selector ---
            legacy_entries = [
                {
                    "version": ver,
                    "title": ver,
                    "aliases": [],
                    "name": ver,
                    "url": f"{SITE_BASE_URL}/legacy/{ver}/",
                }
                for ver in LEGACY_VERSIONS
            ]
            (legacy_dir / "versions.json").write_text(json.dumps(legacy_entries, indent=2) + "\n")

            # --- clean up root versions.json ---
            root_versions_file = worktree / "versions.json"
            if root_versions_file.exists():
                versions = json.loads(root_versions_file.read_text())
                mike_fields = {"version", "title", "aliases", "properties"}
                cleaned = []
                for entry in versions:
                    if entry.get("version") in LEGACY_VERSIONS:
                        continue
                    cleaned.append({k: v for k, v in entry.items() if k in mike_fields})
                root_versions_file.write_text(json.dumps(cleaned, indent=2) + "\n")

            # --- commit ---
            ctx.run(f'git -C "{worktree}" add -A')
            ctx.run(f'git -C "{worktree}" commit -m "Migrate legacy Sphinx docs to legacy/ subdirectory"')

            if push_to_origin:
                ctx.run(f'git -C "{worktree}" push origin {branch}')

        finally:
            ctx.run(f'git worktree remove --force "{worktree}"')


@task(
    help={
        "version": "The library version for which the documentation is to be deployed (e.g., '1.0.0')",
        "push_to_origin": "Whether to push the changes to the origin remote",
    }
)
def mike_deploy(ctx, version: str, push_to_origin: bool = False):
    """Deploy MkDocs documentation for *version* using mike."""
    from mike import driver
    from argparse import Namespace

    args = Namespace(
        version=version,
        title=version,
        aliases=["latest"],
        update_aliases=True,
        push=push_to_origin,
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
    migrate_legacy_docs,
)

ns.configure(
    {
        "base_folder": Path(__file__).parent,
        "proto_folder": Path("./src") / "compas_pb" / "protobuf_defs" / "compas_pb" / "generated",
        "proto_include_paths": [Path("./src") / "compas_pb" / "protobuf_defs"],
        "proto_out_folder": Path("./src"),
    }
)
