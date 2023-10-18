def response_status_string(code):
    """e.g. ``200 OK`` """
    mean = HTTP_STATUS_CODES.get(code, 'unknown').upper()
    return '{code} {mean}'.format(code=code, mean=mean)