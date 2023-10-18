def handle_error(result):
    """
    Extracts the last Windows error message into a python unicode string

    :param result:
        A function result, 0 or None indicates failure

    :return:
        A unicode string error message
    """

    if result:
        return

    code, error_string = get_error()

    if code == Advapi32Const.NTE_BAD_SIGNATURE:
        raise SignatureError('Signature is invalid')

    if not isinstance(error_string, str_cls):
        error_string = _try_decode(error_string)

    raise OSError(error_string)