# import json
import os
import groupdocs_parser_cloud
from groupdocs_parser_cloud import *
from mcp.server.fastmcp import FastMCP
from PIL import Image
from server_models import StorageFile,ImageFile, Barcode, DownloadedFile
from server_helpers import obj_to_model_kwargs, decode_base64_bytes
import shutil
import base64
import tempfile
import binascii

# Initialize MCP server
mcp  = FastMCP("mcp-groupdocs-cloud", port=os.getenv("MCP_PORT"))
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
if not client_id or not client_secret:
    raise ValueError("CLIENT_ID and CLIENT_SECRET must be set in environment variables")
configuration = groupdocs_parser_cloud.Configuration(client_id, client_secret)
configuration.api_base_url = "https://api.groupdocs.cloud"

@mcp.tool()
def parser_get_supported_formats() -> list[str]:
    """Get list of supported file formats from GroupDocs Parser Cloud."""
    infoApi = groupdocs_parser_cloud.InfoApi.from_config(configuration)
    result = infoApi.get_supported_file_formats()
    # structured list for clients/LLMs
    return [fmt.extension for fmt in result.formats]

@mcp.tool()
def extract_text(path: str) -> str:
    """Extract text from a document in GroupDocs Cloud storage."""
    parseApi = groupdocs_parser_cloud.ParseApi.from_config(configuration)
    request = TextRequest(TextOptions(file_info=FileInfo(file_path=path)))
    text = parseApi.text(request)
    return text.text

@mcp.tool()
def extract_images(path: str) -> list[ImageFile]:
    """Extract images from a document in GroupDocs Cloud storage."""
    parseApi = groupdocs_parser_cloud.ParseApi.from_config(configuration)
    request = ImagesRequest(ImagesOptions(file_info=FileInfo(file_path=path)))
    response = parseApi.images(request)
    image_files = [ImageFile(**obj_to_model_kwargs(it, ImageFile)) for it in getattr(response, "images", []) or []]
    return image_files

@mcp.tool()
def extract_barcodes(path: str) -> list[Barcode]:
    """Extract barcodes from a document in GroupDocs Cloud storage."""
    parseApi = groupdocs_parser_cloud.ParseApi.from_config(configuration)
    request = BarcodesRequest(BarcodesOptions(file_info=FileInfo(file_path=path)))
    response = parseApi.barcodes(request)
    barcodes = [Barcode(**obj_to_model_kwargs(it, Barcode)) for it in getattr(response, "barcodes", []) or []]
    return barcodes

@mcp.tool()
def get_image(image_path: str) -> Image.Image:
    """Get an image from GroupDocs Cloud storage as PIL Image."""
    fileApi = groupdocs_parser_cloud.FileApi.from_config(configuration)
    request = groupdocs_parser_cloud.DownloadFileRequest(image_path)
    local_path = fileApi.download_file(request)

    if not os.path.exists(local_path):
        raise FileNotFoundError(f"Downloaded file not found at: {local_path}")

    try:
        with open(local_path, "rb") as f:
            img = Image.open(f).convert("RGBA")

        # normalize format hint (optional)
        ext = os.path.splitext(image_path)[1].lower().lstrip(".")
        valid_exts = ["jpeg", "jpg", "png", "gif", "bmp", "tiff", "webp"]
        img.format = ext.upper() if ext in valid_exts else "PNG"

        return img
    finally:
        try:
            os.remove(local_path)
        except Exception:
            pass


@mcp.tool()
def upload_file(file_stream: bytes, cloud_path: str) -> str:
    """
    Upload a file stream to GroupDocs Cloud storage.
    - file_stream: file content as bytes or base64 string
    - cloud_path: relative path in cloud storage (e.g., '/folder/sample.pdf')
    """

    # 1) Normalize to bytes
    if isinstance(file_stream, str):
        # String must be base64 text
        file_stream = base64.b64decode(file_stream, validate=True)
    elif isinstance(file_stream, (bytearray, memoryview)):
        file_stream = bytes(file_stream)
    elif not isinstance(file_stream, bytes):
        raise TypeError(f"Unsupported type for file_stream: {type(file_stream)}")

    # 2) If bytes actually contain base64 text, decode them
    file_stream = decode_base64_bytes(file_stream)

    # 3) Temp file + SDK call
    _, ext = os.path.splitext(cloud_path)
    tmp_path = None

    try:
        # Create a temporary file (delete=False for Windows compatibility)
        with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp_file:
            tmp_path = tmp_file.name
            tmp_file.write(file_stream)
            tmp_file.flush()

        # Call the SDK (which requires a file path)
        request = groupdocs_parser_cloud.UploadFileRequest(cloud_path, tmp_path)

        fileApi = groupdocs_parser_cloud.FileApi.from_config(configuration)
        fileApi.upload_file(request)

        return f"✅ File uploaded successfully to: {cloud_path}"

    finally:
        # Always delete temp file
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except Exception:
                pass

@mcp.tool()
def download_file(path: str) -> DownloadedFile:
    """Download a file from GroupDocs Cloud storage and return its content as base64."""
    fileApi = groupdocs_parser_cloud.FileApi.from_config(configuration)
    request = groupdocs_parser_cloud.DownloadFileRequest(path)

    # SDK downloads to a temp/local path and returns that path
    local_path = fileApi.download_file(request)

    if not os.path.exists(local_path):
        raise FileNotFoundError(f"Downloaded file not found at: {local_path}")

    try:
        with open(local_path, "rb") as f:
            data = f.read()

        b64 = base64.b64encode(data).decode("ascii")

        return DownloadedFile(
            path=path,
            name=os.path.basename(path),
            base64_data=b64,
            size=len(data),
        )
    finally:
        # cleanup the SDK temp file
        try:
            os.remove(local_path)
        except Exception:
            pass

@mcp.tool()
def get_files_list(path: str = "/") -> list[StorageFile]:
    """Get list of files from a specific folder in GroupDocs Cloud storage."""
    folderApi = groupdocs_parser_cloud.FolderApi.from_config(configuration)
    result = folderApi.get_files_list(GetFilesListRequest(path))
    items = getattr(result, "value", []) or []
    storage_files = [StorageFile(**obj_to_model_kwargs(it, StorageFile)) for it in items]
    return storage_files

@mcp.tool()
def file_exists(path: str) -> bool:
    """Check if a file exists in GroupDocs Cloud storage."""
    storageApi = groupdocs_parser_cloud.StorageApi.from_config(configuration)
    request = groupdocs_parser_cloud.ObjectExistsRequest(path)
    response = storageApi.object_exists(request)
    return response.exists

@mcp.tool()
def folder_exists(path: str) -> bool:
    """Check if a folder exists in GroupDocs Cloud storage."""
    storageApi = groupdocs_parser_cloud.StorageApi.from_config(configuration)
    request = groupdocs_parser_cloud.ObjectExistsRequest(path)
    response = storageApi.object_exists(request)
    return response.exists

@mcp.tool()
def delete_file(path: str) -> bool:
    """Delete a file from GroupDocs Cloud storage. Returns True if deleted."""
    fileApi = groupdocs_parser_cloud.FileApi.from_config(configuration)
    request = groupdocs_parser_cloud.DeleteFileRequest(path)
    fileApi.delete_file(request)
    return True

@mcp.tool()
def delete_folder(path: str, recursive: bool = True) -> bool:
    """Delete a file from GroupDocs Cloud storage. Returns True if deleted."""
    folderApi = groupdocs_parser_cloud.FolderApi.from_config(configuration)
    request = groupdocs_parser_cloud.DeleteFolderRequest(path, recursive=recursive)
    folderApi.delete_folder(request)
    return True

def main():
    """Entry point for the direct execution server."""
    #mcp.run()
    mcp.run(transport="streamable-http")


if __name__ == "__main__":
    main()
