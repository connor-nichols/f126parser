import ctypes


def struct_to_dict(value):
    """Recursively convert a ctypes Structure/Union/Array/scalar into plain
    Python dicts/lists/values (e.g. for logging or JSON export)."""

    if isinstance(value, (ctypes.Structure, ctypes.Union)):
        return {name: struct_to_dict(getattr(value, name)) for name, *_ in value._fields_}
    if isinstance(value, ctypes.Array):
        if value._type_ is ctypes.c_char:
            return bytes(value).split(b"\x00", 1)[0].decode("utf-8", errors="replace")
        return [struct_to_dict(item) for item in value]
    return value
