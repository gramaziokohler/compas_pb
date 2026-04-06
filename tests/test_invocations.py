from unittest.mock import patch

import pytest

from compas_pb.invocations import _get_docsplugin_download_url
from compas_pb.invocations import _get_protoc_download_url

PROTOC_EXPECTED_URLS = {
    ("Linux", "x86_64"): "protoc-31.1-linux-x86_64.zip",
    ("Linux", "aarch64"): "protoc-31.1-linux-aarch_64.zip",
    ("Linux", "amd64"): "protoc-31.1-linux-x86_64.zip",
    ("Linux", "ARM64"): "protoc-31.1-linux-aarch_64.zip",
    ("Darwin", "x86_64"): "protoc-31.1-osx-universal_binary.zip",
    ("Darwin", "arm64"): "protoc-31.1-osx-universal_binary.zip",
    ("Windows", "x86_64"): "protoc-31.1-win64.zip",
    ("Windows", "AMD64"): "protoc-31.1-win64.zip",
    ("Windows", "arm64"): "protoc-31.1-win64.zip",
}

DOCSPLUGIN_EXPECTED_URLS = {
    ("Linux", "x86_64"): "protoc-gen-doc_1.5.1_linux_amd64.tar.gz",
    ("Linux", "aarch64"): "protoc-gen-doc_1.5.1_linux_arm64.tar.gz",
    ("Linux", "amd64"): "protoc-gen-doc_1.5.1_linux_amd64.tar.gz",
    ("Linux", "ARM64"): "protoc-gen-doc_1.5.1_linux_arm64.tar.gz",
    ("Darwin", "x86_64"): "protoc-gen-doc_1.5.1_darwin_amd64.tar.gz",
    ("Darwin", "arm64"): "protoc-gen-doc_1.5.1_darwin_arm64.tar.gz",
    ("Windows", "x86_64"): "protoc-gen-doc_1.5.1_windows_amd64.tar.gz",
    ("Windows", "AMD64"): "protoc-gen-doc_1.5.1_windows_amd64.tar.gz",
    ("Windows", "arm64"): "protoc-gen-doc_1.5.1_windows_arm64.tar.gz",
}


@pytest.mark.parametrize("system,machine", PROTOC_EXPECTED_URLS.keys())
def test_protoc_download_url(system, machine):
    with patch("compas_pb.invocations.platform.system", return_value=system), patch("compas_pb.invocations.platform.machine", return_value=machine):
        url = _get_protoc_download_url()
        assert url.endswith(PROTOC_EXPECTED_URLS[(system, machine)])


@pytest.mark.parametrize("system,machine", DOCSPLUGIN_EXPECTED_URLS.keys())
def test_docsplugin_download_url(system, machine):
    with patch("compas_pb.invocations.platform.system", return_value=system), patch("compas_pb.invocations.platform.machine", return_value=machine):
        url = _get_docsplugin_download_url()
        assert url.endswith(DOCSPLUGIN_EXPECTED_URLS[(system, machine)])


@pytest.mark.parametrize("system,machine", [("FreeBSD", "x86_64"), ("Linux", "mips64")])
def test_unsupported_platform_raises(system, machine):
    with patch("compas_pb.invocations.platform.system", return_value=system), patch("compas_pb.invocations.platform.machine", return_value=machine):
        with pytest.raises(RuntimeError):
            _get_protoc_download_url()
