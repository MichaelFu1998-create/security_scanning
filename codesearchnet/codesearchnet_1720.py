def b64decode(s, altchars=None):
    """Decode a Base64 encoded string.

    s is the string to decode.  Optional altchars must be a string of at least
    length 2 (additional characters are ignored) which specifies the
    alternative alphabet used instead of the '+' and '/' characters.

    The decoded string is returned.  A TypeError is raised if s is
    incorrectly padded.  Characters that are neither in the normal base-64
    alphabet nor the alternative alphabet are discarded prior to the padding
    check.
    """
    if altchars is not None:
        s = s.translate(string.maketrans(altchars[:2], '+/'))
    try:
        return binascii.a2b_base64(s)
    except binascii.Error, msg:
        # Transform this exception for consistency
        raise TypeError(msg)