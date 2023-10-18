def boggle_neighbors(n2, cache={}):
    """Return a list of lists, where the i-th element is the list of indexes
    for the neighbors of square i."""
    if cache.get(n2):
        return cache.get(n2)
    n = exact_sqrt(n2)
    neighbors = [None] * n2
    for i in range(n2):
        neighbors[i] = []
        on_top = i < n
        on_bottom = i >= n2 - n
        on_left = i % n == 0
        on_right = (i+1) % n == 0
        if not on_top:
            neighbors[i].append(i - n)
            if not on_left:  neighbors[i].append(i - n - 1)
            if not on_right: neighbors[i].append(i - n + 1)
        if not on_bottom:
            neighbors[i].append(i + n)
            if not on_left:  neighbors[i].append(i + n - 1)
            if not on_right: neighbors[i].append(i + n + 1)
        if not on_left: neighbors[i].append(i - 1)
        if not on_right: neighbors[i].append(i + 1)
    cache[n2] = neighbors
    return neighbors