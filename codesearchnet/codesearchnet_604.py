def sequences_add_end_id_after_pad(sequences, end_id=888, pad_id=0):
    """Add special end token(id) in the end of each sequence.

    Parameters
    -----------
    sequences : list of list of int
        All sequences where each row is a sequence.
    end_id : int
        The end ID.
    pad_id : int
        The pad ID.

    Returns
    ----------
    list of list of int
        The processed sequences.

    Examples
    ---------
    >>> sequences = [[1,2,0,0], [1,2,3,0], [1,2,3,4]]
    >>> print(sequences_add_end_id_after_pad(sequences, end_id=99, pad_id=0))
    [[1, 2, 99, 0], [1, 2, 3, 99], [1, 2, 3, 4]]

    """
    # sequences_out = [[] for _ in range(len(sequences))]#[[]] * len(sequences)

    sequences_out = copy.deepcopy(sequences)
    # # add a pad to all
    # for i in range(len(sequences)):
    #     for j in range(len(sequences[i])):
    #         sequences_out[i].append(pad_id)
    # # pad -- > end
    # max_len = 0

    for i, v in enumerate(sequences):
        for j, _v2 in enumerate(v):
            if sequences[i][j] == pad_id:
                sequences_out[i][j] = end_id
                # if j > max_len:
                #     max_len = j
                break

    # # remove pad if too long
    # for i in range(len(sequences)):
    #     for j in range(len(sequences[i])):
    #         sequences_out[i] = sequences_out[i][:max_len+1]
    return sequences_out