def topological_sort(deps):
    '''
    Topologically sort a DAG, represented by a dict of child => set of parents.
    The dependency dict is destroyed during operation.

    Uses the Kahn algorithm: http://en.wikipedia.org/wiki/Topological_sorting
    Not a particularly good implementation, but we're just running it on tiny
    graphs.
    '''
    order = []
    available = set()

    def _move_available():
        to_delete = []
        for n, parents in iteritems(deps):
            if not parents:
                available.add(n)
                to_delete.append(n)
        for n in to_delete:
            del deps[n]

    _move_available()
    while available:
        n = available.pop()
        order.append(n)
        for parents in itervalues(deps):
            parents.discard(n)
        _move_available()

    if available:
        raise ValueError("dependency cycle found")
    return order