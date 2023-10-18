def iso_reference_valid_char(c, raise_error=True):
    """Helper to make sure the given character is valid for a reference number"""
    if c in ISO_REFERENCE_VALID:
        return True
    if raise_error:
        raise ValueError("'%s' is not in '%s'" % (c, ISO_REFERENCE_VALID))
    return False