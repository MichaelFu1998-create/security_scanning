def process_sequences(sequences, end_id=0, pad_val=0, is_shorten=True, remain_end_id=False):
    """Set all tokens(ids) after END token to the padding value, and then shorten (option) it to the maximum sequence length in this batch.

    Parameters
    -----------
    sequences : list of list of int
        All sequences where each row is a sequence.
    end_id : int
        The special token for END.
    pad_val : int
        Replace the `end_id` and the IDs after `end_id` to this value.
    is_shorten : boolean
        Shorten the sequences. Default is True.
    remain_end_id : boolean
        Keep an `end_id` in the end. Default is False.

    Returns
    ----------
    list of list of int
        The processed sequences.

    Examples
    ---------
    >>> sentences_ids = [[4, 3, 5, 3, 2, 2, 2, 2],  <-- end_id is 2
    ...                  [5, 3, 9, 4, 9, 2, 2, 3]]  <-- end_id is 2
    >>> sentences_ids = precess_sequences(sentences_ids, end_id=vocab.end_id, pad_val=0, is_shorten=True)
    [[4, 3, 5, 3, 0], [5, 3, 9, 4, 9]]

    """
    max_length = 0
    for _, seq in enumerate(sequences):
        is_end = False
        for i_w, n in enumerate(seq):
            if n == end_id and is_end == False:  # 1st time to see end_id
                is_end = True
                if max_length < i_w:
                    max_length = i_w
                if remain_end_id is False:
                    seq[i_w] = pad_val  # set end_id to pad_val
            elif is_end ==True:
                seq[i_w] = pad_val

    if remain_end_id is True:
        max_length += 1
    if is_shorten:
        for i, seq in enumerate(sequences):
            sequences[i] = seq[:max_length]
    return sequences