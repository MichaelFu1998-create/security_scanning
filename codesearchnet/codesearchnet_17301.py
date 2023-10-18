def group_dict_set(iterator: Iterable[Tuple[A, B]]) -> Mapping[A, Set[B]]:
    """Make a dict that accumulates the values for each key in an iterator of doubles."""
    d = defaultdict(set)
    for key, value in iterator:
        d[key].add(value)
    return dict(d)