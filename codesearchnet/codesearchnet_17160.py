def calculate_single_tanimoto_set_distances(target: Iterable[X], dict_of_sets: Mapping[Y, Set[X]]) -> Mapping[Y, float]:
    """Return a dictionary of distances keyed by the keys in the given dict.

    Distances are calculated based on pairwise tanimoto similarity of the sets contained

    :param set target: A set
    :param dict_of_sets: A dict of {x: set of y}
    :type dict_of_sets: dict
    :return: A similarity dicationary based on the set overlap (tanimoto) score between the target set and the sets in
            dos
    :rtype: dict
    """
    target_set = set(target)

    return {
        k: tanimoto_set_similarity(target_set, s)
        for k, s in dict_of_sets.items()
    }