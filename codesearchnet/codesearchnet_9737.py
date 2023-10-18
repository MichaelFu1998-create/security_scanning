def find_segments(stops, shape):
    """Find corresponding shape points for a list of stops and create shape break points.

    Parameters
    ----------
    stops: stop-sequence (list)
        List of stop points
    shape: list of shape points
        shape-sequence of shape points

    Returns
    -------
    break_points: list[int]
        stops[i] corresponds to shape[break_points[i]].  This list can
        be used to partition the shape points into segments between
        one stop and the next.
    badness: float
        Lower indicates better fit to the shape.  This is the sum of
        distances (in meters) between every each stop and its closest
        shape point.  This is not needed in normal use, but in the
        cases where you must determine the best-fitting shape for a
        stop-sequence, use this.
    """
    if not shape:
        return [], 0
    break_points = []
    last_i = 0
    cumul_d = 0
    badness = 0
    d_last_stop = float('inf')
    lstlat, lstlon = None, None
    break_shape_points = []
    for stop in stops:
        stlat, stlon = stop['lat'], stop['lon']
        best_d = float('inf')
        # print stop
        if badness > 500 and badness > 30 * len(break_points):
            return [], badness
        for i in range(last_i, len(shape)):
            d = wgs84_distance(stlat, stlon, shape[i]['lat'], shape[i]['lon'])
            if lstlat:
                d_last_stop = wgs84_distance(lstlat, lstlon, shape[i]['lat'], shape[i]['lon'])
            # If we are getting closer to next stop, record this as
            # the best stop so far.continue
            if d < best_d:
                best_d = d
                best_i = i
                # print best_d, i, last_i, len(shape)
                cumul_d += d
            # We have to be very careful about our stop condition.
            # This is trial and error, basically.
            if (d_last_stop < d) or (d > 500) or (i < best_i + 100):
                    continue
            # We have decided our best stop, stop looking and continue
            # the outer loop.
            else:
                badness += best_d
                break_points.append(best_i)
                last_i = best_i
                lstlat, lstlon = stlat, stlon
                break_shape_points.append(shape[best_i])
                break
        else:
            # Executed if we did *not* break the inner loop
            badness += best_d
            break_points.append(best_i)
            last_i = best_i
            lstlat, lstlon = stlat, stlon
            break_shape_points.append(shape[best_i])
            pass
    # print "Badness:", badness
    # print_coords(stops, 'stop')
    # print_coords(shape, 'shape')
    # print_coords(break_shape_points, 'break')
    return break_points, badness