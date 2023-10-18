def vector_clip(vector, lowest, highest):
    """Return vector, except if any element is less than the corresponding
    value of lowest or more than the corresponding value of highest, clip to
    those values.
    >>> vector_clip((-1, 10), (0, 0), (9, 9))
    (0, 9)
    """
    return type(vector)(map(clip, vector, lowest, highest))