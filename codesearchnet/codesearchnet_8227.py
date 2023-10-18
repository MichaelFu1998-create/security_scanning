def to_triplets(colors):
    """
    Coerce a list into a list of triplets.

    If `colors` is a list of lists or strings, return it as is.  Otherwise,
    divide it into tuplets of length three, silently discarding any extra
    elements beyond a multiple of three.
    """
    try:
        colors[0][0]
        return colors
    except:
        pass

    # It's a 1-dimensional list
    extra = len(colors) % 3
    if extra:
        colors = colors[:-extra]
    return list(zip(*[iter(colors)] * 3))