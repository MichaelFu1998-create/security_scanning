def b16decode(s, casefold=False):
    """Decode a Base16 encoded string.

    s is the string to decode.  Optional casefold is a flag specifying whether
    a lowercase alphabet is acceptable as input.  For security purposes, the
    default is False.

    The decoded string is returned.  A TypeError is raised if s is
    incorrectly padded or if there are non-alphabet characters present in the
    string.
    """
    if casefold:
        s = s.upper()
    if re.search('[^0-9A-F]', s):
        raise TypeError('Non-base16 digit found')
    return binascii.unhexlify(s)