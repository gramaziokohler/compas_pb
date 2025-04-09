import platform
from pathlib import Path

import invoke


def generate_compiler_path():
    path = ""
    if platform.system() == "Windows":
        path = Path("proto/win64/bin/protoc.exe")
    elif platform.system() == "Linux":
        path = Path("proto/linux64/bin/protoc")
    elif platform.system() == "Darwin":
        path = Path("./proto/macaarch64/bin/protoc")
    return path


@invoke.task(help={"target_language": "Directory containing the .proto files"})
def generate_proto_classes(ctx, target_language: str = "python"):
    idl_root = Path("./IDL")
    idl_dir = idl_root / "compas_pb" / "data" / "proto"
    out_dir = Path("./src")

    path_to_compiler = generate_compiler_path()

    for idl_file in idl_dir.glob("*.proto"):
        cmd = f"./{path_to_compiler} --proto_path=./IDL --{target_language}_out={out_dir} {idl_file}"
        print(cmd)
        ctx.run(cmd)


