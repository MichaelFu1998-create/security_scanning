def interpolate_shape_times(shape_distances, shape_breaks, stop_times):
    """
    Interpolate passage times for shape points.

    Parameters
    ----------
    shape_distances: list
        list of cumulative distances along the shape
    shape_breaks: list
        list of shape_breaks
    stop_times: list
        list of stop_times

    Returns
    -------
    shape_times: list of ints (seconds) / numpy array
        interpolated shape passage times

    The values of stop times before the first shape-break are given the first
    stopping time, and the any shape points after the last break point are
    given the value of the last shape point.
    """
    shape_times = np.zeros(len(shape_distances))
    shape_times[:shape_breaks[0]] = stop_times[0]
    for i in range(len(shape_breaks)-1):
        cur_break = shape_breaks[i]
        cur_time = stop_times[i]
        next_break = shape_breaks[i+1]
        next_time = stop_times[i+1]
        if cur_break == next_break:
            shape_times[cur_break] = stop_times[i]
        else:
            cur_distances = shape_distances[cur_break:next_break+1]
            norm_distances = ((np.array(cur_distances)-float(cur_distances[0])) /
                              float(cur_distances[-1] - cur_distances[0]))
            times = (1.-norm_distances)*cur_time+norm_distances*next_time
            shape_times[cur_break:next_break] = times[:-1]
    # deal final ones separately:
    shape_times[shape_breaks[-1]:] = stop_times[-1]
    return list(shape_times)