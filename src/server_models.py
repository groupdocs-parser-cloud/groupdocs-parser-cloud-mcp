from pydantic import BaseModel, Field

class StorageFile(BaseModel):
    """File information structure."""
    name: str = Field(description="File name")
    is_folder: bool = Field(description="Is it a folder")
    size: int = Field(description="File size in bytes")
    modified_date: str = Field(description="Last modified date")

class ImageFile(BaseModel):
    """Contains path of extracted image."""
    path: str = Field(description="Image file path in cloud storage")

class Barcode(BaseModel):
    """Contains information of extracted barcode."""
    code_type_name: str = Field(description="Barcode type name")
    value: str = Field(description="Barcode value")

class DownloadedFile(BaseModel):
    """Downloaded file payload."""
    path: str = Field(description="Cloud path requested")
    name: str = Field(description="File name")
    base64_data: str = Field(description="File content encoded as base64")
    size: int = Field(description="Size in bytes")