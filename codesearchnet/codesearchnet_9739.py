def return_segments(shape, break_points):
    """Break a shape into segments between stops using break_points.

    This function can use the `break_points` outputs from
    `find_segments`, and cuts the shape-sequence into pieces
    corresponding to each stop.
    """
    # print 'xxx'
    # print stops
    # print shape
    # print break_points
    # assert len(stops) == len(break_points)
    segs = []
    bp = 0 # not used
    bp2 = 0
    for i in range(len(break_points)-1):
        bp = break_points[i] if break_points[i] is not None else bp2
        bp2 = break_points[i+1] if break_points[i+1] is not None else bp
        segs.append(shape[bp:bp2+1])
    segs.append([])
    return segs