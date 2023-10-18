def _str_to_path(s, result_type):
    """Given an ASCII str, returns a path of the given type."""

    assert isinstance(s, str)
    if isinstance(s, bytes) and result_type is text_type:
        return s.decode('ascii')
    elif isinstance(s, text_type) and result_type is bytes:
        return s.encode('ascii')
    return s