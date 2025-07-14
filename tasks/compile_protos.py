from pathlib import Path
import invoke
import platform
import urllib.request
import zipfile

PROTOC_VERSION = "31.1"


def _get_protoc_download_url(version=PROTOC_VERSION):
    base_url = f"https://github.com/protocolbuffers/protobuf/releases/download/v{version}/"
    system = platform.system()
    arch = platform.machine()

    if system == "Linux" and arch == "x86_64":
        return base_url + f"protoc-{version}-linux-x86_64.zip"
    elif system == "Darwin":
        return base_url + f"protoc-{version}-osx-x86_64.zip"
    elif system == "Windows":
        return base_url + f"protoc-{version}-win64.zip"

    raise RuntimeError(f"Unsupported platform: {system} {arch}")


def _get_cached_protoc_path():
    cache_dir = Path.home() / ".cache" / "protoc" / PROTOC_VERSION
    protoc_bin = cache_dir / "bin" / "protoc"
    if platform.system() == "Windows":
        protoc_bin = protoc_bin.with_suffix(".exe")

    return protoc_bin, cache_dir


def _download_and_extract_protoc(url, extract_path):
    archive_path = extract_path / "protoc.zip"
    urllib.request.urlretrieve(url, archive_path)

    with zipfile.ZipFile(archive_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)

    archive_path.unlink()


def setup_protoc():
    protoc_bin, cache_dir = _get_cached_protoc_path()

    if not protoc_bin.exists():
        print(f"protoc not found in cache. Downloading to: {cache_dir}")
        cache_dir.mkdir(parents=True, exist_ok=True)
        url = _get_protoc_download_url()
        _download_and_extract_protoc(url, cache_dir)
        if not protoc_bin.exists():
            raise FileNotFoundError("Failed to find protoc binary after extraction.")
        print("Download complete.")
    else:
        print(f"Using cached protoc at: {protoc_bin}")

    return str(protoc_bin)


@invoke.task(help={"target_language": "Output language for generated classes (e.g., 'python')"})
def generate_proto_classes(ctx, target_language: str = "python"):
    protoc_path = setup_protoc()

    idl_dir = Path("./IDL") / "compas_pb" / "generated"
    out_dir = Path("./src")

    for idl_file in idl_dir.glob("*.proto"):
        cmd = f'"{protoc_path}" --proto_path=./IDL --{target_language}_out={out_dir} {idl_file}'
        print(f"Running: {cmd}")
        ctx.run(cmd)
