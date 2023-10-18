def make_segments(strip, length):
    """Return a list of Segments that evenly split the strip."""
    if len(strip) % length:
        raise ValueError('The length of strip must be a multiple of length')

    s = []
    try:
        while True:
            s.append(s[-1].next(length) if s else Segment(strip, length))
    except ValueError:
        return s