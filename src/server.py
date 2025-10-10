# import json
import os
import groupdocs_parser_cloud
from groupdocs_parser_cloud import *
from mcp.server.fastmcp import FastMCP, Image
from server_models import StorageFile,ImageFile, Barcode, obj_to_model_kwargs
import shutil

# Initialize MCP server
mcp  = FastMCP("mcp-groupdocs-cloud")
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
if not client_id or not client_secret:
    raise ValueError("CLIENT_ID and CLIENT_SECRET must be set in environment variables")
configuration = groupdocs_parser_cloud.Configuration(client_id, client_secret)
configuration.api_base_url = "https://api.groupdocs.cloud"

@mcp.tool()
def parser_get_supported_formats() -> str:
    """Get list of supported file formats from GroupDocs Parser Cloud."""
    infoApi = groupdocs_parser_cloud.InfoApi.from_config(configuration)
    result = infoApi.get_supported_file_formats()
    return f"Supported file formats: {', '.join([fmt.extension for fmt in result.formats])}"

@mcp.tool()
def get_files_list(path: str = "/") -> list[StorageFile]:
    """Get list of files from a specific folder in GroupDocs Cloud storage."""
    folderApi = groupdocs_parser_cloud.FolderApi.from_config(configuration)
    result = folderApi.get_files_list(GetFilesListRequest(path))
    items = getattr(result, "value", []) or []
    storage_files = [StorageFile(**obj_to_model_kwargs(it, StorageFile)) for it in items]
    return storage_files

@mcp.tool()
def parser_extract_text(path: str) -> str:
    """Extract text from a document in GroupDocs Cloud storage."""
    parseApi = groupdocs_parser_cloud.ParseApi.from_config(configuration)
    request = TextRequest(TextOptions(file_info=FileInfo(file_path=path)))
    text = parseApi.text(request)
    return text.text

@mcp.tool()
def parser_extract_images(path: str) -> list[ImageFile]:
    """Extract images from a document in GroupDocs Cloud storage."""
    parseApi = groupdocs_parser_cloud.ParseApi.from_config(configuration)
    request = ImagesRequest(ImagesOptions(file_info=FileInfo(file_path=path)))
    response = parseApi.images(request)
    image_files = [ImageFile(**obj_to_model_kwargs(it, ImageFile)) for it in getattr(response, "images", []) or []]
    return image_files

@mcp.tool()
def parser_extract_barcodes(path: str) -> list[Barcode]:
    """Extract barcodes from a document in GroupDocs Cloud storage."""
    parseApi = groupdocs_parser_cloud.ParseApi.from_config(configuration)
    request = BarcodesRequest(BarcodesOptions(file_info=FileInfo(file_path=path)))
    response = parseApi.barcodes(request)
    barcodes = [Barcode(**obj_to_model_kwargs(it, Barcode)) for it in getattr(response, "barcodes", []) or []]
    return barcodes

@mcp.tool()
def download_file(path: str) -> str:
    """Download a file from GroupDocs Cloud storage to local workspace."""
    fileApi = groupdocs_parser_cloud.FileApi.from_config(configuration)
    request = groupdocs_parser_cloud.DownloadFileRequest(path)
    response = fileApi.download_file(request)
    shutil.move(response, os.path.basename(path))
    return f"File downloaded: {os.path.basename(path)}"

# @mcp.tool()
# def get_image(image_path: str) -> Image:
#     """Get an image from GroupDocs Cloud storage"""
#     fileApi = groupdocs_parser_cloud.FileApi.from_config(configuration)
#     request = groupdocs_parser_cloud.DownloadFileRequest(image_path)
#     response = fileApi.download_file(request)
#     return Image(path=response, format="jpeg")

@mcp.tool()
def upload_file(local_path: str, cloud_path: str) -> str:
    """Upload a file from local workspace to GroupDocs Cloud storage."""
    fileApi = groupdocs_parser_cloud.FileApi.from_config(configuration)
    request = groupdocs_parser_cloud.UploadFileRequest(cloud_path, local_path)
    fileApi.upload_file(request)
    return f"File uploaded: {cloud_path}"

@mcp.tool()
def file_exists(path: str) -> bool:
    """Check if a file exists in GroupDocs Cloud storage."""
    storageApi = groupdocs_parser_cloud.StorageApi.from_config(configuration)
    request = groupdocs_parser_cloud.ObjectExistsRequest(path)
    response = storageApi.object_exists(request)
    return response.exists

@mcp.tool()
def delete_file(path: str) -> str:
    """Delete a file from GroupDocs Cloud storage."""
    fileApi = groupdocs_parser_cloud.FileApi.from_config(configuration)
    request = groupdocs_parser_cloud.DeleteFileRequest(path)
    response = fileApi.delete_file(request)
    return "File deleted."

def main():
    """Entry point for the direct execution server."""
    mcp.run()


if __name__ == "__main__":
    main()
