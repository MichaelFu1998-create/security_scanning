def _get_col_index(name):
    """Convert column name to index."""

    index = string.ascii_uppercase.index
    col = 0
    for c in name.upper():
        col = col * 26 + index(c) + 1
    return col