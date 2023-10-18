def is_empty_object(n, last):
    """n may be the inside of block or object"""
    if n.strip():
        return False
    # seems to be but can be empty code
    last = last.strip()
    markers = {
        ')',
        ';',
    }
    if not last or last[-1] in markers:
        return False
    return True