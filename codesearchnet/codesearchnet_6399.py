def _hashable_bytes(data):
    """
    Coerce strings to hashable bytes.
    """
    if isinstance(data, bytes):
        return data
    elif isinstance(data, str):
        return data.encode('ascii')  # Fail on anything non-ASCII.
    else:
        raise TypeError(data)