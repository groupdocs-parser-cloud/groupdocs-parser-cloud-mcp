from datetime import datetime, date

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

def decode_base64_bytes(data: bytes) -> bytes:
    # If bytes contain non-ASCII, they're not base64 text; return as-is.
    try:
        txt = data.decode("ascii")
    except UnicodeDecodeError:
        return data

    # Remove whitespace/newlines commonly present in base64
    compact = "".join(txt.split())

    # Quick base64 shape checks
    if not compact:
        return data
    if len(compact) % 4 != 0:
        return data
    # Only base64 alphabet?
    if not all(c.isalnum() or c in "+/=" for c in compact):
        return data

    try:
        return base64.b64decode(compact, validate=True)
    except (binascii.Error, ValueError):
        return data