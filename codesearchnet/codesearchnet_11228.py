def pairwise_similarity_statistics(
    src_collection,
    tar_collection,
    metric=sim,
    mean_func=amean,
    symmetric=False,
):
    """Calculate the pairwise similarity statistics a collection of strings.

    Calculate pairwise similarities among members of two collections,
    returning the maximum, minimum, mean (according to a supplied function,
    arithmetic mean, by default), and (population) standard deviation
    of those similarities.

    Parameters
    ----------
    src_collection : list
        A collection of terms or a string that can be split
    tar_collection : list
        A collection of terms or a string that can be split
    metric : function
        A similarity metric function
    mean_func : function
        A mean function that takes a list of values and returns a float
    symmetric : bool
        Set to True if all pairwise similarities should be calculated in both
        directions

    Returns
    -------
    tuple
        The max, min, mean, and standard deviation of similarities

    Raises
    ------
    ValueError
        mean_func must be a function
    ValueError
        metric must be a function
    ValueError
        src_collection is neither a string nor iterable
    ValueError
        tar_collection is neither a string nor iterable

    Example
    -------
    >>> tuple(round(_, 12) for _ in pairwise_similarity_statistics(
    ... ['Christopher', 'Kristof', 'Christobal'], ['Niall', 'Neal', 'Neil']))
    (0.2, 0.0, 0.118614718615, 0.075070477184)

    """
    if not callable(mean_func):
        raise ValueError('mean_func must be a function')
    if not callable(metric):
        raise ValueError('metric must be a function')

    if hasattr(src_collection, 'split'):
        src_collection = src_collection.split()
    if not hasattr(src_collection, '__iter__'):
        raise ValueError('src_collection is neither a string nor iterable')

    if hasattr(tar_collection, 'split'):
        tar_collection = tar_collection.split()
    if not hasattr(tar_collection, '__iter__'):
        raise ValueError('tar_collection is neither a string nor iterable')

    src_collection = list(src_collection)
    tar_collection = list(tar_collection)

    pairwise_values = []

    for src in src_collection:
        for tar in tar_collection:
            pairwise_values.append(metric(src, tar))
            if symmetric:
                pairwise_values.append(metric(tar, src))

    return (
        max(pairwise_values),
        min(pairwise_values),
        mean_func(pairwise_values),
        std(pairwise_values, mean_func, 0),
    )