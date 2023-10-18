def _digest_hasher(hasher, hashlen, base):
    """ counterpart to _update_hasher """
    # Get a 128 character hex string
    hex_text = hasher.hexdigest()
    # Shorten length of string (by increasing base)
    base_text = _convert_hexstr_base(hex_text, base)
    # Truncate
    text = base_text[:hashlen]
    return text