def break_array(a, threshold=numpy.pi, other=None):
    """Create a array which masks jumps >= threshold.

    Extra points are inserted between two subsequent values whose
    absolute difference differs by more than threshold (default is
    pi).

    Other can be a secondary array which is also masked according to
    *a*.

    Returns (*a_masked*, *other_masked*) (where *other_masked* can be
    ``None``)
    """
    assert len(a.shape) == 1, "Only 1D arrays supported"

    if other is not None and a.shape != other.shape:
        raise ValueError("arrays must be of identical shape")

    # jump occurs after the index in break
    breaks = numpy.where(numpy.abs(numpy.diff(a)) >= threshold)[0]
    # insert a blank after
    breaks += 1

    # is this needed?? -- no, but leave it here as a reminder
    #f2 = numpy.diff(a, 2)
    #up = (f2[breaks - 1] >= 0)  # >0: up, <0: down
    # sort into up and down breaks:
    #breaks_up = breaks[up]
    #breaks_down = breaks[~up]

    # new array b including insertions for all the breaks
    m = len(breaks)
    b = numpy.empty((len(a) + m))
    # calculate new indices for breaks in b, taking previous insertions into account
    b_breaks = breaks + numpy.arange(m)
    mask =  numpy.zeros_like(b, dtype=numpy.bool)
    mask[b_breaks] = True
    b[~mask] = a
    b[mask] = numpy.NAN

    if other is not None:
        c = numpy.empty_like(b)
        c[~mask] = other
        c[mask] = numpy.NAN
        ma_c = numpy.ma.array(c, mask=mask)
    else:
        ma_c = None

    return numpy.ma.array(b, mask=mask), ma_c