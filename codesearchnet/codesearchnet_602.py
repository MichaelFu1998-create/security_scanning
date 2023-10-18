def sequences_add_start_id(sequences, start_id=0, remove_last=False):
    """Add special start token(id) in the beginning of each sequence.

    Parameters
    ------------
    sequences : list of list of int
        All sequences where each row is a sequence.
    start_id : int
        The start ID.
    remove_last : boolean
        Remove the last value of each sequences. Usually be used for removing the end ID.

    Returns
    ----------
    list of list of int
        The processed sequences.

    Examples
    ---------
    >>> sentences_ids = [[4,3,5,3,2,2,2,2], [5,3,9,4,9,2,2,3]]
    >>> sentences_ids = sequences_add_start_id(sentences_ids, start_id=2)
    [[2, 4, 3, 5, 3, 2, 2, 2, 2], [2, 5, 3, 9, 4, 9, 2, 2, 3]]
    >>> sentences_ids = sequences_add_start_id(sentences_ids, start_id=2, remove_last=True)
    [[2, 4, 3, 5, 3, 2, 2, 2], [2, 5, 3, 9, 4, 9, 2, 2]]

    For Seq2seq

    >>> input = [a, b, c]
    >>> target = [x, y, z]
    >>> decode_seq = [start_id, a, b] <-- sequences_add_start_id(input, start_id, True)

    """
    sequences_out = [[] for _ in range(len(sequences))]  #[[]] * len(sequences)
    for i, _ in enumerate(sequences):
        if remove_last:
            sequences_out[i] = [start_id] + sequences[i][:-1]
        else:
            sequences_out[i] = [start_id] + sequences[i]
    return sequences_out