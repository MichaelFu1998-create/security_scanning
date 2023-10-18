def sequences_add_end_id(sequences, end_id=888):
    """Add special end token(id) in the end of each sequence.

    Parameters
    -----------
    sequences : list of list of int
        All sequences where each row is a sequence.
    end_id : int
        The end ID.

    Returns
    ----------
    list of list of int
        The processed sequences.

    Examples
    ---------
    >>> sequences = [[1,2,3],[4,5,6,7]]
    >>> print(sequences_add_end_id(sequences, end_id=999))
    [[1, 2, 3, 999], [4, 5, 6, 999]]

    """
    sequences_out = [[] for _ in range(len(sequences))]  #[[]] * len(sequences)
    for i, _ in enumerate(sequences):
        sequences_out[i] = sequences[i] + [end_id]
    return sequences_out