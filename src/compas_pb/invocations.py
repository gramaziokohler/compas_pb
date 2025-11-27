import gzip
import os
import platform
import stat
import tarfile
import urllib.request
import zipfile
from pathlib import Path

import invoke

PROTOC_VERSION = "31.1"
PROTOC_GEN_DOCS_VERSION = "1.5.1"
# typescript,javascript, and go need other compiler plugins
PROTO_TARGET_LANGUAGES = ["cpp", "csharp", "java", "objc", "php", "ruby"]


def _get_protoc_download_url(version=PROTOC_VERSION):
    base_url = f"https://github.com/protocolbuffers/protobuf/releases/download/v{version}/"
    system = platform.system()
    arch = platform.machine()

    if system == "Linux" and arch == "x86_64":
        return base_url + f"protoc-{version}-linux-x86_64.zip"
    elif system == "Darwin":
        return base_url + f"protoc-{version}-osx-universal_binary.zip"  # universal binary (allegedly) works on intel + apple silicon
    elif system == "Windows":
        return base_url + f"protoc-{version}-win64.zip"

    raise RuntimeError(f"Unsupported platform: {system} {arch}")


def _get_docsplugin_download_url(version=PROTOC_GEN_DOCS_VERSION):
    base_url = f"https://github.com/pseudomuto/protoc-gen-doc/releases/download/v{version}/"
    system = platform.system()
    arch = platform.machine().lower()

    arch_mapping = {
        "x86_64": "amd64",
        "aarch64": "arm64",
        "arm64": "arm64",
        "amd64": "amd64",
    }

    selected_arch = arch_mapping.get(arch)
    if not selected_arch:
        raise RuntimeError(f"Unsupported architecture: {arch}")

    if system == "Linux":
        return base_url + f"protoc-gen-doc_{version}_linux_{selected_arch}.tar.gz"
    elif system == "Darwin":
        return base_url + f"protoc-gen-doc_{version}_darwin_{selected_arch}.tar.gz"
    elif system == "Windows":
        return base_url + f"protoc-gen-doc_{version}_windows_{selected_arch}.tar.gz"

    raise RuntimeError(f"Unsupported platform: {system} {arch}")


def _get_cached_protoc_path():
    cache_dir = Path.home() / ".cache" / "protoc" / PROTOC_VERSION
    protoc_bin = cache_dir / "bin" / "protoc"
    if platform.system() == "Windows":
        protoc_bin = protoc_bin.with_suffix(".exe")

    return protoc_bin, cache_dir


def _download_and_extract_docsplugin(url, extract_path):
    archive_path = extract_path / "protoc-gen-doc.tar.gz"
    urllib.request.urlretrieve(url, archive_path)

    with gzip.open(archive_path, "rb") as gz_ref:
        with tarfile.TarFile(fileobj=gz_ref, mode="r") as tar_ref:
            tar_ref.extractall(extract_path)

    archive_path.unlink()


def _download_and_extract_protoc(url, extract_path):
    archive_path = extract_path / "protoc.zip"
    print(f"Downloading protoc from {url} to {archive_path}")
    urllib.request.urlretrieve(url, archive_path)

    with zipfile.ZipFile(archive_path, "r") as zip_ref:
        zip_ref.extractall(extract_path)

    archive_path.unlink()


def setup_protoc():
    protoc_bin, cache_dir = _get_cached_protoc_path()
    plugin_executable = protoc_bin.parent / "protoc-gen-doc"

    if platform.system() == "Windows":
        plugin_executable = plugin_executable.with_suffix(".exe")
        protoc_bin = protoc_bin.with_suffix(".exe")

    if not protoc_bin.exists() or not plugin_executable.exists():
        print(f"protoc not found in cache. Downloading to: {cache_dir}")
        cache_dir.mkdir(parents=True, exist_ok=True)

        url = _get_protoc_download_url()
        _download_and_extract_protoc(url, cache_dir)

        docsplugin_url = _get_docsplugin_download_url()
        _download_and_extract_docsplugin(docsplugin_url, protoc_bin.parent)

        if platform.system() in ["Linux", "Darwin"]:
            mode = os.stat(protoc_bin)
            os.chmod(protoc_bin, mode.st_mode | stat.S_IEXEC)

            mode = os.stat(plugin_executable)
            os.chmod(plugin_executable, mode.st_mode | stat.S_IEXEC)

        if not protoc_bin.exists():
            raise FileNotFoundError("Failed to find protoc binary after extraction.")
        print("Download complete.")
    else:
        print(f"Using cached protoc at: {protoc_bin}")

    return protoc_bin, plugin_executable


@invoke.task(help={"target_language": "Output language for generated classes (e.g., 'python')"})
def generate_proto_classes(ctx, target_language: str = "python"):
    protoc_path, _ = setup_protoc()

    proto_out_folder = ""
    if target_language == "python":
        proto_out_folder = Path(ctx.proto_out_folder)
    elif target_language in PROTO_TARGET_LANGUAGES:
        proto_out_folder = Path(ctx.proto_out_folder) / "compas_pb" / "generated" / target_language
        proto_out_folder.mkdir(parents=True, exist_ok=True)
    else:
        print(f"Target language '{target_language}' not supported.")

    for idl_file in ctx.proto_folder.glob("*.proto"):
        cmd = f"{protoc_path} "
        cmd += " ".join(f"--proto_path={p}" for p in ctx.proto_include_paths)

        cmd += f" --{target_language}_out={proto_out_folder} {idl_file}"

        if target_language == "python":
            cmd += f" --pyi_out={proto_out_folder}"

        print(f"Running: {cmd}")
        ctx.run(cmd)


@invoke.task()
def create_class_assets(ctx):
    base_dir = ctx.base_folder
    dist_dir = base_dir / "dist"
    dist_dir.mkdir(parents=True, exist_ok=True)

    for existing_file in dist_dir.glob("compas_pb-generated-*.zip"):
        existing_file.unlink()
        print(f"Removed existing asset: {existing_file}")

    class_assests = []

    for language in PROTO_TARGET_LANGUAGES:
        generate_proto_classes(ctx, target_language=language)

        generated_dir = base_dir / "src" / "compas_pb" / "generated" / language
        zip_path = dist_dir / "proto" / f"compas_pb-generated-{language}-{PROTOC_VERSION}.zip"
        zip_path.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for item in generated_dir.rglob("*"):
                if item.is_file():
                    arcname = f"{item.relative_to(generated_dir)}"
                    zipf.write(item, arcname)
                    print(f"Added {arcname}")
        class_assests.append(zip_path)
        # clean up
        if generated_dir.exists():
            import shutil

            shutil.rmtree(generated_dir)
            print(f"Removed temporary generated files in: {generated_dir}")
    if class_assests:
        print("protobuf class assets are ready for GitHub release upload! find them in: {dist_dir}")


@invoke.task(
    help={
        "rebuild": "True to clean all previously built docs before starting, otherwise False.",
        "doctest": "True to run doctests, otherwise False.",
        "check_links": "True to check all web links in docs for validity, otherwise False.",
    }
)
def docs(ctx, doctest=False, rebuild=False, check_links=False):
    # intercepting the `invoke docs` call so that the protobuf docs are generated first
    # the single html file is linked to from the main docs site
    from compas_invocations2.docs import docs

    protoc_path, plugin_path = setup_protoc()
    proto_files = ctx.proto_folder / "*.proto"
    target_dir = Path(ctx.base_folder) / "docs" / "_static" / "protobuf"
    target_dir.mkdir(parents=True, exist_ok=True)

    cmd = f"{protoc_path} "
    cmd += f"--plugin=protoc-gen-doc={plugin_path} "
    cmd += " ".join(f"--proto_path={p}" for p in ctx.proto_include_paths)
    cmd += f" --doc_out={target_dir}"
    cmd += f" --doc_opt=html,index.html {proto_files}"
    print(f"Generating protobuf docs with command: {cmd}")
    ctx.run(cmd)

    # now call the original docs task
    docs(ctx, doctest, rebuild, check_links)
