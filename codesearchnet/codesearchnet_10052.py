def peek_openssl_error():
    """
    Peeks into the error stack and pulls out the lib, func and reason

    :return:
        A three-element tuple of integers (lib, func, reason)
    """

    error = libcrypto.ERR_peek_error()
    lib = int((error >> 24) & 0xff)
    func = int((error >> 12) & 0xfff)
    reason = int(error & 0xfff)

    return (lib, func, reason)