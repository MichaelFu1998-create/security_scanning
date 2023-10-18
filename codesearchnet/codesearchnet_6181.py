def safe_re_encode(s, encoding_to, errors="backslashreplace"):
    """Re-encode str or binary so that is compatible with a given encoding (replacing
    unsupported chars).

    We use ASCII as default, which gives us some output that contains \x99 and \u9999
    for every character > 127, for easier debugging.
    (e.g. if we don't know the encoding, see #87, #96)
    """
    # prev = s
    if not encoding_to:
        encoding_to = "ASCII"
    if compat.is_bytes(s):
        s = s.decode(encoding_to, errors=errors).encode(encoding_to)
    else:
        s = s.encode(encoding_to, errors=errors).decode(encoding_to)
    # print("safe_re_encode({}, {}) => {}".format(prev, encoding_to, s))
    return s