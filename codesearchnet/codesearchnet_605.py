def sequences_get_mask(sequences, pad_val=0):
    """Return mask for sequences.

    Parameters
    -----------
    sequences : list of list of int
        All sequences where each row is a sequence.
    pad_val : int
        The pad value.

    Returns
    ----------
    list of list of int
        The mask.

    Examples
    ---------
    >>> sentences_ids = [[4, 0, 5, 3, 0, 0],
    ...                  [5, 3, 9, 4, 9, 0]]
    >>> mask = sequences_get_mask(sentences_ids, pad_val=0)
    [[1 1 1 1 0 0]
     [1 1 1 1 1 0]]

    """
    mask = np.ones_like(sequences)
    for i, seq in enumerate(sequences):
        for i_w in reversed(range(len(seq))):
            if seq[i_w] == pad_val:
                mask[i, i_w] = 0
            else:
                break  # <-- exit the for loop, prepcess next sequence
    return mask