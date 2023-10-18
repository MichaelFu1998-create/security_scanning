def seq_minibatches2(inputs, targets, batch_size, num_steps):
    """Generate a generator that iterates on two list of words. Yields (Returns) the source contexts and
    the target context by the given batch_size and num_steps (sequence_length).
    In TensorFlow's tutorial, this generates the `batch_size` pointers into the raw PTB data, and allows minibatch iteration along these pointers.

    Parameters
    ----------
    inputs : list of data
        The context in list format; note that context usually be represented by splitting by space, and then convert to unique word IDs.
    targets : list of data
        The context in list format; note that context usually be represented by splitting by space, and then convert to unique word IDs.
    batch_size : int
        The batch size.
    num_steps : int
        The number of unrolls. i.e. sequence length

    Yields
    ------
    Pairs of the batched data, each a matrix of shape [batch_size, num_steps].

    Raises
    ------
    ValueError : if batch_size or num_steps are too high.

    Examples
    --------
    >>> X = [i for i in range(20)]
    >>> Y = [i for i in range(20,40)]
    >>> for batch in tl.iterate.seq_minibatches2(X, Y, batch_size=2, num_steps=3):
    ...     x, y = batch
    ...     print(x, y)

    [[  0.   1.   2.]
    [ 10.  11.  12.]]
    [[ 20.  21.  22.]
    [ 30.  31.  32.]]

    [[  3.   4.   5.]
    [ 13.  14.  15.]]
    [[ 23.  24.  25.]
    [ 33.  34.  35.]]

    [[  6.   7.   8.]
    [ 16.  17.  18.]]
    [[ 26.  27.  28.]
    [ 36.  37.  38.]]

    Notes
    -----
    - Hint, if the input data are images, you can modify the source code `data = np.zeros([batch_size, batch_len)` to `data = np.zeros([batch_size, batch_len, inputs.shape[1], inputs.shape[2], inputs.shape[3]])`.
    """
    if len(inputs) != len(targets):
        raise AssertionError("The length of inputs and targets should be equal")

    data_len = len(inputs)
    batch_len = data_len // batch_size
    # data = np.zeros([batch_size, batch_len])
    data = np.zeros((batch_size, batch_len) + inputs.shape[1:], dtype=inputs.dtype)
    data2 = np.zeros([batch_size, batch_len])

    for i in range(batch_size):
        data[i] = inputs[batch_len * i:batch_len * (i + 1)]
        data2[i] = targets[batch_len * i:batch_len * (i + 1)]

    epoch_size = (batch_len - 1) // num_steps

    if epoch_size == 0:
        raise ValueError("epoch_size == 0, decrease batch_size or num_steps")

    for i in range(epoch_size):
        x = data[:, i * num_steps:(i + 1) * num_steps]
        x2 = data2[:, i * num_steps:(i + 1) * num_steps]
        yield (x, x2)