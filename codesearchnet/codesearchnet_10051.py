def handle_openssl_error(result, exception_class=None):
    """
    Checks if an error occured, and if so throws an OSError containing the
    last OpenSSL error message

    :param result:
        An integer result code - 1 or greater indicates success

    :param exception_class:
        The exception class to use for the exception if an error occurred

    :raises:
        OSError - when an OpenSSL error occurs
    """

    if result > 0:
        return

    if exception_class is None:
        exception_class = OSError

    error_num = libcrypto.ERR_get_error()
    buffer = buffer_from_bytes(120)
    libcrypto.ERR_error_string(error_num, buffer)

    # Since we are dealing with a string, it is NULL terminated
    error_string = byte_string_from_buffer(buffer)

    raise exception_class(_try_decode(error_string))