def serpentine_y(x, y, matrix):
    """Every other column is indexed in reverse."""
    if x % 2:
        return x, matrix.rows - 1 - y
    return x, y