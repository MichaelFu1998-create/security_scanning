def handle_error(error_num):
    """
    Extracts the last Windows error message into a python unicode string

    :param error_num:
        The number to get the error string for

    :return:
        A unicode string error message
    """

    if error_num == 0:
        return

    messages = {
        BcryptConst.STATUS_NOT_FOUND: 'The object was not found',
        BcryptConst.STATUS_INVALID_PARAMETER: 'An invalid parameter was passed to a service or function',
        BcryptConst.STATUS_NO_MEMORY: (
            'Not enough virtual memory or paging file quota is available to complete the specified operation'
        ),
        BcryptConst.STATUS_INVALID_HANDLE: 'An invalid HANDLE was specified',
        BcryptConst.STATUS_INVALID_SIGNATURE: 'The cryptographic signature is invalid',
        BcryptConst.STATUS_NOT_SUPPORTED: 'The request is not supported',
        BcryptConst.STATUS_BUFFER_TOO_SMALL: 'The buffer is too small to contain the entry',
        BcryptConst.STATUS_INVALID_BUFFER_SIZE: 'The size of the buffer is invalid for the specified operation',
    }

    output = 'NTSTATUS error 0x%0.2X' % error_num

    if error_num is not None and error_num in messages:
        output += ': ' + messages[error_num]

    raise OSError(output)