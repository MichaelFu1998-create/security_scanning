def handle_error(result, exception_class=None):
    """
    Extracts the last Windows error message into a python unicode string

    :param result:
        A function result, 0 or None indicates failure

    :param exception_class:
        The exception class to use for the exception if an error occurred

    :return:
        A unicode string error message
    """

    if result == 0:
        return

    if result == Secur32Const.SEC_E_OUT_OF_SEQUENCE:
        raise TLSError('A packet was received out of order')

    if result == Secur32Const.SEC_E_MESSAGE_ALTERED:
        raise TLSError('A packet was received altered')

    if result == Secur32Const.SEC_E_CONTEXT_EXPIRED:
        raise TLSError('The TLS session expired')

    _, error_string = get_error()

    if not isinstance(error_string, str_cls):
        error_string = _try_decode(error_string)

    if exception_class is None:
        exception_class = OSError

    raise exception_class(('SECURITY_STATUS error 0x%0.2X: ' % result) + error_string)