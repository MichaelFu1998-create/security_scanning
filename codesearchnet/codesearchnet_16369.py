def heappushpop_max(heap, item):
    """Fast version of a heappush followed by a heappop."""
    if heap and heap[0] > item:
        # if item >= heap[0], it will be popped immediately after pushed
        item, heap[0] = heap[0], item
        _siftup_max(heap, 0)
    return item