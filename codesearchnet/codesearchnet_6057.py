def get_http_status_string(v):
    """Return HTTP response string, e.g. 204 -> ('204 No Content').
    The return string always includes descriptive text, to satisfy Apache mod_dav.

    `v`: status code or DAVError
    """
    code = get_http_status_code(v)
    try:
        return ERROR_DESCRIPTIONS[code]
    except KeyError:
        return "{} Status".format(code)