def str2fp(data):
    """
    Convert bytes data to file handle object (StringIO or BytesIO).

    :arg data: String data to transform
    """
    return BytesIO(bytearray(data, const.ENCODING)) if const.PY3 else StringIO(data)