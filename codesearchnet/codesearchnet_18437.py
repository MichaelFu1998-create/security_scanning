def compress(obj, level=6, return_type="bytes"):
    """Compress anything to bytes or string.

    :params obj: 
    :params level: 
    :params return_type: if bytes, then return bytes; if str, then return
      base64.b64encode bytes in utf-8 string. 
    """
    if isinstance(obj, binary_type):
        b = zlib.compress(obj, level)
    elif isinstance(obj, string_types):
        b = zlib.compress(obj.encode("utf-8"), level)
    else:
        b = zlib.compress(pickle.dumps(obj, protocol=2), level)

    if return_type == "bytes":
        return b
    elif return_type == "str":
        return base64.b64encode(b).decode("utf-8")
    else:
        raise ValueError("'return_type' has to be one of 'bytes', 'str'!")