def find_exception_by_code(code):
    """Find name of exception by WebDriver defined error code.

    Args:
        code(str): Error code defined in protocol.

    Returns:
        The error name defined in protocol.
    """
    errorName = None
    for error in WebDriverError:
        if error.value.code == code:
            errorName = error
            break
    return errorName