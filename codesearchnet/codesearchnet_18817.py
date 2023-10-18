def _warning(code):
    """
    Return a warning message of code 'code'.

    If code = (cd, str) it returns the warning message of code 'cd' and appends
    str at the end
    """
    if isinstance(code, str):
        return code

    message = ''
    if isinstance(code, tuple):
        if isinstance(code[0], str):
            message = code[1]
            code = code[0]
    return CFG_BIBRECORD_WARNING_MSGS.get(code, '') + message