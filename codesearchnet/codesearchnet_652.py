def seq_minibatches(inputs, targets, batch_size, seq_length, stride=1):
    """Generate a generator that return a batch of sequence inputs and targets.
    If `batch_size=100` and `seq_length=5`, one return will have 500 rows (examples).

    Parameters
    ----------
    inputs : numpy.array
        The input features, every row is a example.
    targets : numpy.array
        The labels of inputs, every element is a example.
    batch_size : int
        The batch size.
    seq_length : int
        The sequence length.
    stride : int
        The stride step, default is 1.

    Examples
    --------
    Synced sequence input and output.

    >>> X = np.asarray([['a','a'], ['b','b'], ['c','c'], ['d','d'], ['e','e'], ['f','f']])
    >>> y = np.asarray([0, 1, 2, 3, 4, 5])
    >>> for batch in tl.iterate.seq_minibatches(inputs=X, targets=y, batch_size=2, seq_length=2, stride=1):
    >>>     print(batch)
    (array([['a', 'a'], ['b', 'b'], ['b', 'b'], ['c', 'c']], dtype='<U1'), array([0, 1, 1, 2]))
    (array([['c', 'c'], ['d', 'd'], ['d', 'd'], ['e', 'e']], dtype='<U1'), array([2, 3, 3, 4]))

    Many to One

    >>> return_last = True
    >>> num_steps = 2
    >>> X = np.asarray([['a','a'], ['b','b'], ['c','c'], ['d','d'], ['e','e'], ['f','f']])
    >>> Y = np.asarray([0,1,2,3,4,5])
    >>> for batch in tl.iterate.seq_minibatches(inputs=X, targets=Y, batch_size=2, seq_length=num_steps, stride=1):
    >>>     x, y = batch
    >>>     if return_last:
    >>>         tmp_y = y.reshape((-1, num_steps) + y.shape[1:])
    >>>     y = tmp_y[:, -1]
    >>>     print(x, y)
    [['a' 'a']
    ['b' 'b']
    ['b' 'b']
    ['c' 'c']] [1 2]
    [['c' 'c']
    ['d' 'd']
    ['d' 'd']
    ['e' 'e']] [3 4]

    """
    if len(inputs) != len(targets):
        raise AssertionError("The length of inputs and targets should be equal")

    n_loads = (batch_size * stride) + (seq_length - stride)

    for start_idx in range(0, len(inputs) - n_loads + 1, (batch_size * stride)):
        seq_inputs = np.zeros((batch_size, seq_length) + inputs.shape[1:], dtype=inputs.dtype)
        seq_targets = np.zeros((batch_size, seq_length) + targets.shape[1:], dtype=targets.dtype)
        for b_idx in xrange(batch_size):
            start_seq_idx = start_idx + (b_idx * stride)
            end_seq_idx = start_seq_idx + seq_length
            seq_inputs[b_idx] = inputs[start_seq_idx:end_seq_idx]
            seq_targets[b_idx] = targets[start_seq_idx:end_seq_idx]
        flatten_inputs = seq_inputs.reshape((-1, ) + inputs.shape[1:])
        flatten_targets = seq_targets.reshape((-1, ) + targets.shape[1:])
        yield flatten_inputs, flatten_targets