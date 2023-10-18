def calculate_global_tanimoto_set_distances(dict_of_sets: Mapping[X, Set]) -> Mapping[X, Mapping[X, float]]:
    r"""Calculate an alternative distance matrix based on the following equation.

    .. math:: distance(A, B)=1- \|A \cup B\| / \| \cup_{s \in S} s\|

    :param dict_of_sets: A dict of {x: set of y}
    :return: A similarity matrix based on the alternative tanimoto distance as a dict of dicts
    """
    universe = set(itt.chain.from_iterable(dict_of_sets.values()))
    universe_size = len(universe)

    result: Dict[X, Dict[X, float]] = defaultdict(dict)

    for x, y in itt.combinations(dict_of_sets, 2):
        result[x][y] = result[y][x] = 1.0 - len(dict_of_sets[x] | dict_of_sets[y]) / universe_size

    for x in dict_of_sets:
        result[x][x] = 1.0 - len(x) / universe_size

    return dict(result)