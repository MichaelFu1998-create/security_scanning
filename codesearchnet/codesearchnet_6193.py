def calc_base64(s):
    """Return base64 encoded binarystring."""
    s = compat.to_bytes(s)
    s = compat.base64_encodebytes(s).strip()  # return bytestring
    return compat.to_native(s)