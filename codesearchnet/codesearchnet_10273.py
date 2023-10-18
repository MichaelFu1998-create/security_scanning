def smart_str(string, encoding='utf-8', strings_only=False, errors='strict'):
    """
    Returns a bytestring version of 's', encoded as specified in 'encoding'.

    If strings_only is True, don't convert (some) non-string-like objects.
    """
    if strings_only and isinstance(string, (type(None), int)):
        return string
    # if isinstance(s, Promise):
    #     return unicode(s).encode(encoding, errors)
    if isinstance(string, str):
        try:
            return string.encode(encoding, errors)
        except UnicodeEncodeError:
            return string.encode('utf-8', errors)
    elif not isinstance(string, bytes):
        try:
            return str(string).encode(encoding, errors)
        except UnicodeEncodeError:
            if isinstance(string, Exception):
                # An Exception subclass containing non-ASCII data that doesn't
                # know how to print itself properly. We shouldn't raise a
                # further exception.
                return ' '.join([smart_str(arg, encoding, strings_only,
                                           errors) for arg in string])
            return str(string).encode(encoding, errors)
    else:
        return string