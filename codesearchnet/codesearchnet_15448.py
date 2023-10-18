def extract_cycles(series, left=False, right=False):
    """Iterate cycles in the series.

    Parameters
    ----------
    series : iterable sequence of numbers
    left: bool, optional
        If True, treat the first point in the series as a reversal.
    right: bool, optional
        If True, treat the last point in the series as a reversal.

    Yields
    ------
    cycle : tuple
        Each tuple contains three floats (low, high, mult), where low and high
        define cycle amplitude and mult equals to 1.0 for full cycles and 0.5
        for half cycles.
    """
    points = deque()

    for x in reversals(series, left=left, right=right):
        points.append(x)
        while len(points) >= 3:
            # Form ranges X and Y from the three most recent points
            X = abs(points[-2] - points[-1])
            Y = abs(points[-3] - points[-2])

            if X < Y:
                # Read the next point
                break
            elif len(points) == 3:
                # Y contains the starting point
                # Count Y as one-half cycle and discard the first point
                yield points[0], points[1], 0.5
                points.popleft()
            else:
                # Count Y as one cycle and discard the peak and the valley of Y
                yield points[-3], points[-2], 1.0
                last = points.pop()
                points.pop()
                points.pop()
                points.append(last)
    else:
        # Count the remaining ranges as one-half cycles
        while len(points) > 1:
            yield points[0], points[1], 0.5
            points.popleft()