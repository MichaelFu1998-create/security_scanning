def calculate_tanimoto_set_distances(dict_of_sets: Mapping[X, Set]) -> Mapping[X, Mapping[X, float]]:
    """Return a distance matrix keyed by the keys in the given dict.

    Distances are calculated based on pairwise tanimoto similarity of the sets contained.

    :param dict_of_sets: A dict of {x: set of y}
    :return: A similarity matrix based on the set overlap (tanimoto) score between each x as a dict of dicts
    """
    result: Dict[X, Dict[X, float]] = defaultdict(dict)

    for x, y in itt.combinations(dict_of_sets, 2):
        result[x][y] = result[y][x] = tanimoto_set_similarity(dict_of_sets[x], dict_of_sets[y])

    for x in dict_of_sets:
        result[x][x] = 1.0

    return dict(result)