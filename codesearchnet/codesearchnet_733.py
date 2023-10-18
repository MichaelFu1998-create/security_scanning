def generate_skip_gram_batch(data, batch_size, num_skips, skip_window, data_index=0):
    """Generate a training batch for the Skip-Gram model.

    See `Word2Vec example <https://github.com/tensorlayer/tensorlayer/blob/master/example/tutorial_word2vec_basic.py>`__.

    Parameters
    ----------
    data : list of data
        To present context, usually a list of integers.
    batch_size : int
        Batch size to return.
    num_skips : int
        How many times to reuse an input to generate a label.
    skip_window : int
        How many words to consider left and right.
    data_index : int
        Index of the context location. This code use `data_index` to instead of yield like ``tl.iterate``.

    Returns
    -------
    batch : list of data
        Inputs.
    labels : list of data
        Labels
    data_index : int
        Index of the context location.

    Examples
    --------
    Setting num_skips=2, skip_window=1, use the right and left words.
    In the same way, num_skips=4, skip_window=2 means use the nearby 4 words.

    >>> data = [1,2,3,4,5,6,7,8,9,10,11]
    >>> batch, labels, data_index = tl.nlp.generate_skip_gram_batch(data=data, batch_size=8, num_skips=2, skip_window=1, data_index=0)
    >>> print(batch)
    [2 2 3 3 4 4 5 5]
    >>> print(labels)
    [[3]
    [1]
    [4]
    [2]
    [5]
    [3]
    [4]
    [6]]

    """
    # global data_index   # you can put data_index outside the function, then
    #       modify the global data_index in the function without return it.
    # note: without using yield, this code use data_index to instead.

    if batch_size % num_skips != 0:
        raise Exception("batch_size should be able to be divided by num_skips.")
    if num_skips > 2 * skip_window:
        raise Exception("num_skips <= 2 * skip_window")
    batch = np.ndarray(shape=(batch_size), dtype=np.int32)
    labels = np.ndarray(shape=(batch_size, 1), dtype=np.int32)
    span = 2 * skip_window + 1  # [ skip_window target skip_window ]
    buffer = collections.deque(maxlen=span)
    for _ in range(span):
        buffer.append(data[data_index])
        data_index = (data_index + 1) % len(data)
    for i in range(batch_size // num_skips):
        target = skip_window  # target label at the center of the buffer
        targets_to_avoid = [skip_window]
        for j in range(num_skips):
            while target in targets_to_avoid:
                target = random.randint(0, span - 1)
            targets_to_avoid.append(target)
            batch[i * num_skips + j] = buffer[skip_window]
            labels[i * num_skips + j, 0] = buffer[target]
        buffer.append(data[data_index])
        data_index = (data_index + 1) % len(data)
    return batch, labels, data_index