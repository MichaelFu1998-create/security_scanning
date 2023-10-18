def merge_dict_of_lists(adict, indices, pop_later=True, copy=True):
    """Extend the within a dict of lists. The indices will indicate which
    list have to be extended by which other list.

    Parameters
    ----------
    adict: OrderedDict
        An ordered dictionary of lists

    indices: list or tuple of 2 iterables of int, bot having the same length
        The indices of the lists that have to be merged, both iterables items
         will be read pair by pair, the first is the index to the list that
         will be extended with the list of the second index.
         The indices can be constructed with Numpy e.g.,
         indices = np.where(square_matrix)

    pop_later: bool
        If True will oop out the lists that are indicated in the second
         list of indices.

    copy: bool
        If True will perform a deep copy of the input adict before
         modifying it, hence not changing the original input.

    Returns
    -------
    Dictionary of lists

    Raises
    ------
    IndexError
        If the indices are out of range
    """
    def check_indices(idxs, x):
        for i in chain(*idxs):
            if i < 0 or i >= x:
                raise IndexError("Given indices are out of dict range.")

    check_indices(indices, len(adict))

    rdict = adict.copy() if copy else adict

    dict_keys = list(rdict.keys())
    for i, j in zip(*indices):
        rdict[dict_keys[i]].extend(rdict[dict_keys[j]])

    if pop_later:
        for i, j in zip(*indices):
            rdict.pop(dict_keys[j], '')

    return rdict