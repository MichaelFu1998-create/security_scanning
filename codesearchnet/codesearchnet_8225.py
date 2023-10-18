def serpentine_x(x, y, matrix):
    """Every other row is indexed in reverse."""
    if y % 2:
        return matrix.columns - 1 - x, y
    return x, y