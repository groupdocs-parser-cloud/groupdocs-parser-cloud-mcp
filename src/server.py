# import json
import os
import groupdocs_parser_cloud
from groupdocs_parser_cloud import *
from mcp.server.fastmcp import FastMCP
from PIL import Image
from server_models import StorageFile, ImageFile, Barcode, DownloadedFile
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

# ======================================================================
# Parser-scoped tools
# ======================================================================

@mcp.tool()
def parser_supported_formats() -> list[str]:
    """
    Get list of formats supported by GroupDocs.Parser Cloud.

    Returns:
        list[str]: A list of supported extensions (e.g., ".pdf", ".docx").
    """
    infoApi = groupdocs_parser_cloud.InfoApi.from_config(configuration)
    result = infoApi.get_supported_file_formats()
    return [fmt.extension for fmt in result.formats]


@mcp.tool()
def parser_extract_text(path: str) -> str:
    """
    Extract text from a document in GroupDocs Cloud storage.

    Args:
        path (str): Cloud storage path to the document 
                    (e.g., "/docs/sample.pdf").

    Returns:
        str: Extracted textual content.
    """
    parseApi = groupdocs_parser_cloud.ParseApi.from_config(configuration)
    request = TextRequest(TextOptions(file_info=FileInfo(file_path=path)))
    text = parseApi.text(request)
    return text.text


@mcp.tool()
def parser_extract_images(path: str) -> list[ImageFile]:
    """
    Extract images from a document in Cloud storage.

    Args:
        path (str): Cloud path of the document to analyze.

    Returns:
        list[ImageFile]: List of image metadata entries.
    """
    parseApi = groupdocs_parser_cloud.ParseApi.from_config(configuration)
    request = ImagesRequest(ImagesOptions(file_info=FileInfo(file_path=path)))
    response = parseApi.images(request)
    return [
        ImageFile(**obj_to_model_kwargs(it, ImageFile))
        for it in getattr(response, "images", []) or []
    ]


@mcp.tool()
def parser_extract_barcodes(path: str) -> list[Barcode]:
    """
    Extract barcodes from a document in Cloud storage.

    Args:
        path (str): Cloud path of the document to analyze.

    Returns:
        list[Barcode]: List of detected barcode entries.
    """
    parseApi = groupdocs_parser_cloud.ParseApi.from_config(configuration)
    request = BarcodesRequest(BarcodesOptions(file_info=FileInfo(file_path=path)))
    response = parseApi.barcodes(request)
    return [
        Barcode(**obj_to_model_kwargs(it, Barcode))
        for it in getattr(response, "barcodes", []) or []
    ]

# ======================================================================
# Shared storage/file methods (same for all GD products)
# ======================================================================

@mcp.tool()
def file_get_image(image_path: str) -> Image.Image:
    """
    Download an image file from Cloud storage and return it as a PIL image.

    Args:
        image_path (str): Full cloud storage path to the image file 
                          (e.g., "/images/page-1.png").

    Returns:
        Image.Image: The downloaded image in RGBA format.
    """
    fileApi = groupdocs_parser_cloud.FileApi.from_config(configuration)
    request = groupdocs_parser_cloud.DownloadFileRequest(image_path)
    local_path = fileApi.download_file(request)

    if not os.path.exists(local_path):
        raise FileNotFoundError(f"Downloaded file not found at: {local_path}")

    try:
        with open(local_path, "rb") as f:
            img = Image.open(f).convert("RGBA")

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
def file_upload(file_stream: bytes, cloud_path: str) -> str:
    """
    Upload a file stream to GroupDocs Cloud storage.

    Args:
        file_stream (bytes | str): File contents as raw bytes or 
                                   a base64-encoded string.
        cloud_path (str): Destination path in Cloud storage 
                           (e.g., "/uploads/sample.pdf").

    Returns:
        str: Success message with target path.
    """

    if isinstance(file_stream, str):
        file_stream = base64.b64decode(file_stream, validate=True)
    elif isinstance(file_stream, (bytearray, memoryview)):
        file_stream = bytes(file_stream)
    elif not isinstance(file_stream, bytes):
        raise TypeError(f"Unsupported type for file_stream: {type(file_stream)}")

    file_stream = decode_base64_bytes(file_stream)

    _, ext = os.path.splitext(cloud_path)
    tmp_path = None

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp_file:
            tmp_path = tmp_file.name
            tmp_file.write(file_stream)
            tmp_file.flush()

        request = groupdocs_parser_cloud.UploadFileRequest(cloud_path, tmp_path)
        fileApi = groupdocs_parser_cloud.FileApi.from_config(configuration)
        fileApi.upload_file(request)

        return f"✅ File uploaded successfully to: {cloud_path}"

    finally:
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except Exception:
                pass


@mcp.tool()
def file_download(path: str) -> DownloadedFile:
    """
    Download a file from Cloud storage and return it as base64 content.

    Args:
        path (str): Cloud file path (e.g., "/docs/sample.pdf").

    Returns:
        DownloadedFile: Object containing path, filename, size, base64 data.
    """
    fileApi = groupdocs_parser_cloud.FileApi.from_config(configuration)
    request = groupdocs_parser_cloud.DownloadFileRequest(path)
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
        try:
            os.remove(local_path)
        except Exception:
            pass


@mcp.tool()
def folder_list(path: str = "/") -> list[StorageFile]:
    """
    List the contents of a folder (files + subfolders).

    Args:
        path (str): Cloud folder path (default "/").

    Returns:
        list[StorageFile]: Entries including files and subfolders.
    """
    folderApi = groupdocs_parser_cloud.FolderApi.from_config(configuration)
    result = folderApi.get_files_list(GetFilesListRequest(path))
    items = getattr(result, "value", []) or []
    return [StorageFile(**obj_to_model_kwargs(it, StorageFile)) for it in items]


@mcp.tool()
def file_exists(path: str) -> bool:
    """
    Check if the given path points to an existing file.

    Args:
        path (str): Cloud storage path to check.

    Returns:
        bool: True if a file exists at the specified path.
    """
    storageApi = groupdocs_parser_cloud.StorageApi.from_config(configuration)
    request = groupdocs_parser_cloud.ObjectExistsRequest(path)
    response = storageApi.object_exists(request)
    return bool(response.exists and not getattr(response, "is_folder", False))


@mcp.tool()
def folder_exists(path: str) -> bool:
    """
    Check if the given path points to an existing folder.

    Args:
        path (str): Cloud folder path.

    Returns:
        bool: True if a folder exists at the specified path.
    """
    storageApi = groupdocs_parser_cloud.StorageApi.from_config(configuration)
    request = groupdocs_parser_cloud.ObjectExistsRequest(path)
    response = storageApi.object_exists(request)
    return bool(response.exists and getattr(response, "is_folder", False))


@mcp.tool()
def file_delete(path: str) -> bool:
    """
    Delete a file in Cloud storage.

    Args:
        path (str): Path of the file to delete.

    Returns:
        bool: Always True if no exception was thrown.
    """
    fileApi = groupdocs_parser_cloud.FileApi.from_config(configuration)
    request = groupdocs_parser_cloud.DeleteFileRequest(path)
    fileApi.delete_file(request)
    return True


@mcp.tool()
def folder_delete(path: str, recursive: bool = True) -> bool:
    """
    Delete a folder from Cloud storage.

    Args:
        path (str): Folder path to delete.
        recursive (bool): Delete folder contents recursively.

    Returns:
        bool: True if deletion succeeded.
    """
    folderApi = groupdocs_parser_cloud.FolderApi.from_config(configuration)
    request = groupdocs_parser_cloud.DeleteFolderRequest(path, recursive=recursive)
    folderApi.delete_folder(request)
    return True


def main():
    """Entry point for the MCP server."""
    mcp.run(transport="streamable-http")


if __name__ == "__main__":
    main()
