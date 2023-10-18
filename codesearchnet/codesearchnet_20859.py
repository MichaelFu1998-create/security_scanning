def as_flat_array(iterables):
    '''Given a sequence of sequences, return a flat numpy array.

    Parameters
    ----------
    iterables : sequence of sequence of number
        A sequence of tuples or lists containing numbers. Typically these come
        from something that represents each joint in a skeleton, like angle.

    Returns
    -------
    ndarray :
        An array of flattened data from each of the source iterables.
    '''
    arr = []
    for x in iterables:
        arr.extend(x)
    return np.array(arr)