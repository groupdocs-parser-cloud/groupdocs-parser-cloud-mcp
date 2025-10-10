from pydantic import BaseModel, Field
from datetime import datetime, date

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

# Generic converter: turn a dict/object into kwargs for any pydantic model class
def obj_to_model_kwargs(item, model_cls):
    """
    Convert `item` (dict or object) to kwargs suitable for `model_cls`.
    Performs basic coercions (datetime -> ISO string, int, bool).
    """
    field_map = getattr(model_cls, "model_fields", None) or getattr(model_cls, "__fields__", {})
    names = list(field_map.keys())

    kwargs = {}
    for n in names:
        # read value from dict or attribute
        val = item.get(n) if isinstance(item, dict) else getattr(item, n, None)

        # detect declared annotation/type (pydantic v2 -> .annotation, v1 -> .outer_type_)
        finfo = field_map.get(n)
        annotation = getattr(finfo, "annotation", None) or getattr(finfo, "outer_type_", None)
        ann_str = str(annotation).lower() if annotation is not None else ""

        # basic coercions
        if isinstance(val, (datetime, date)):
            # if model expects a str, convert datetimes to ISO string
            if "str" in ann_str:
                val = val.isoformat()
        elif val is not None:
            if "int" in ann_str:
                try:
                    val = int(val)
                except Exception:
                    pass
            elif "bool" in ann_str:
                val = bool(val)

        kwargs[n] = val

    return kwargs
