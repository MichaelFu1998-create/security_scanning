def http_exception_error_handler(
        exception):
    """
    Handle HTTP exception

    :param werkzeug.exceptions.HTTPException exception: Raised exception

    A response is returned, as formatted by the :py:func:`response` function.
    """

    assert issubclass(type(exception), HTTPException), type(exception)
    assert hasattr(exception, "code")
    assert hasattr(exception, "description")

    return response(exception.code, exception.description)