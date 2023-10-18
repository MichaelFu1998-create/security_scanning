def _extract_error():
    """
    Extracts the last OS error message into a python unicode string

    :return:
        A unicode string error message
    """

    error_num = errno()

    try:
        error_string = os.strerror(error_num)
    except (ValueError):
        return str_cls(error_num)

    if isinstance(error_string, str_cls):
        return error_string

    return _try_decode(error_string)