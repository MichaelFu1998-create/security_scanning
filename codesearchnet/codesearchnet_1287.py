def partitionAtIntervals(data, intervals):
    """ Generator to allow iterating slices at dynamic intervals

    Parameters:
    ----------------------------------------------------------------
    data:       Any data structure that supports slicing (i.e. list or tuple)
    *intervals: Iterable of intervals.  The sum of intervals should be less
                than, or equal to the length of data.

    """
    assert sum(intervals) <= len(data)

    start = 0
    for interval in intervals:
      end = start + interval
      yield data[start:end]
      start = end

    raise StopIteration