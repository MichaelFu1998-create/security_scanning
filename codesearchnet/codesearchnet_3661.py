def interval_intersection(min1, max1, min2, max2):
    """
    Given two intervals, (min1, max1) and (min2, max2) return their intersecting interval,
    or None if they do not overlap.
    """
    left, right = max(min1, min2), min(max1, max2)
    if left < right:
        return left, right
    return None