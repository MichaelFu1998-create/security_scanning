def count_defaultdict(dict_of_lists: Mapping[X, List[Y]]) -> Mapping[X, typing.Counter[Y]]:
    """Count the number of elements in each value of the dictionary."""
    return {
        k: Counter(v)
        for k, v in dict_of_lists.items()
    }