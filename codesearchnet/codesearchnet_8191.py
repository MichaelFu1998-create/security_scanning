def fill(strip, item, start=0, stop=None, step=1):
    """Fill a portion of a strip from start to stop by step with a given item.
    If stop is not given, it defaults to the length of the strip.
    """
    if stop is None:
        stop = len(strip)

    for i in range(start, stop, step):
        strip[i] = item