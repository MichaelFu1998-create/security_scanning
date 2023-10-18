def remove_pad_sequences(sequences, pad_id=0):
    """Remove padding.

    Parameters
    -----------
    sequences : list of list of int
        All sequences where each row is a sequence.
    pad_id : int
        The pad ID.

    Returns
    ----------
    list of list of int
        The processed sequences.

    Examples
    ----------
    >>> sequences = [[2,3,4,0,0], [5,1,2,3,4,0,0,0], [4,5,0,2,4,0,0,0]]
    >>> print(remove_pad_sequences(sequences, pad_id=0))
    [[2, 3, 4], [5, 1, 2, 3, 4], [4, 5, 0, 2, 4]]

    """
    sequences_out = copy.deepcopy(sequences)

    for i, _ in enumerate(sequences):
        # for j in range(len(sequences[i])):
        #     if sequences[i][j] == pad_id:
        #         sequences_out[i] = sequences_out[i][:j]
        #         break
        for j in range(1, len(sequences[i])):
            if sequences[i][-j] != pad_id:
                sequences_out[i] = sequences_out[i][0:-j + 1]
                break

    return sequences_out