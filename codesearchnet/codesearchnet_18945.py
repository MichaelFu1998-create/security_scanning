def get_exception_from_status_and_error_codes(status_code, error_code, value):
    """
    Return an exception given status and error codes.

    :param status_code: HTTP status code.
    :type status_code: None | int
    :param error_code: Midas Server error code.
    :type error_code: None | int
    :param value: Message to display.
    :type value: string
    :returns: Exception.
    :rtype : pydas.exceptions.ResponseError
    """
    if status_code == requests.codes.bad_request:
        exception = BadRequest(value)
    elif status_code == requests.codes.unauthorized:
        exception = Unauthorized(value)
    elif status_code == requests.codes.forbidden:
        exception = Unauthorized(value)
    elif status_code in [requests.codes.not_found, requests.codes.gone]:
        exception = NotFound(value)
    elif status_code == requests.codes.method_not_allowed:
        exception = MethodNotAllowed(value)
    elif status_code >= requests.codes.bad_request:
        exception = HTTPError(value)
    else:
        exception = ResponseError(value)

    if error_code == -100:  # MIDAS_INTERNAL_ERROR
        exception = InternalError(value)
    elif error_code == -101:  # MIDAS_INVALID_TOKEN
        exception = InvalidToken(value)
    elif error_code == -105:  # MIDAS_UPLOAD_FAILED
        exception = UploadFailed(value)
    elif error_code == -140:  # MIDAS_UPLOAD_TOKEN_GENERATION_FAILED
        exception = UploadTokenGenerationFailed(value)
    elif error_code == -141:  # MIDAS_INVALID_UPLOAD_TOKEN
        exception = InvalidUploadToken(value)
    elif error_code == -150:  # MIDAS_INVALID_PARAMETER
        exception = InvalidParameter(value)
    elif error_code == -151:  # MIDAS_INVALID_POLICY
        exception = InvalidPolicy(value)

    return exception