# TODO: check the path
$protoCompiler = ".\proto\win64\bin\protoc.exe"

$protoPath = ".\idl"
$pythonOut = "."
$protoFile = "$protoPath\compas_buff\**\*.proto"

Write-Host "Compiling proto files..."

if (Test-Path $protoCompiler) {
  $protoCompiler --proto_path=$protoPath --python_out=$pythonOut $protoFile
} else {
  Write-Host "Protoc compiler not found at $protoCompiler"
}
