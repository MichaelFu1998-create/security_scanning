def encodestring(s):
    """Encode a string into multiple lines of base-64 data."""
    pieces = []
    for i in range(0, len(s), MAXBINSIZE):
        chunk = s[i : i + MAXBINSIZE]
        pieces.append(binascii.b2a_base64(chunk))
    return "".join(pieces)