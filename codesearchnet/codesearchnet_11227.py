def mean_pairwise_similarity(
    collection, metric=sim, mean_func=hmean, symmetric=False
):
    """Calculate the mean pairwise similarity of a collection of strings.

    Takes the mean of the pairwise similarity between each member of a
    collection, optionally in both directions (for asymmetric similarity
    metrics.

    Parameters
    ----------
    collection : list
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
    float
        The mean pairwise similarity of a collection of strings

    Raises
    ------
    ValueError
        mean_func must be a function
    ValueError
        metric must be a function
    ValueError
        collection is neither a string nor iterable type
    ValueError
        collection has fewer than two members

    Examples
    --------
    >>> round(mean_pairwise_similarity(['Christopher', 'Kristof',
    ... 'Christobal']), 12)
    0.519801980198
    >>> round(mean_pairwise_similarity(['Niall', 'Neal', 'Neil']), 12)
    0.545454545455

    """
    if not callable(mean_func):
        raise ValueError('mean_func must be a function')
    if not callable(metric):
        raise ValueError('metric must be a function')

    if hasattr(collection, 'split'):
        collection = collection.split()
    if not hasattr(collection, '__iter__'):
        raise ValueError('collection is neither a string nor iterable type')
    elif len(collection) < 2:
        raise ValueError('collection has fewer than two members')

    collection = list(collection)

    pairwise_values = []

    for i in range(len(collection)):
        for j in range(i + 1, len(collection)):
            pairwise_values.append(metric(collection[i], collection[j]))
            if symmetric:
                pairwise_values.append(metric(collection[j], collection[i]))

    return mean_func(pairwise_values)