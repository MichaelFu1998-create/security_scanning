def cross_entropy_seq_with_mask(logits, target_seqs, input_mask, return_details=False, name=None):
    """Returns the expression of cross-entropy of two sequences, implement
    softmax internally. Normally be used for Dynamic RNN with Synced sequence input and output.

    Parameters
    -----------
    logits : Tensor
        2D tensor with shape of [batch_size * ?, n_classes], `?` means dynamic IDs for each example.
        - Can be get from `DynamicRNNLayer` by setting ``return_seq_2d`` to `True`.
    target_seqs : Tensor
        int of tensor, like word ID. [batch_size, ?], `?` means dynamic IDs for each example.
    input_mask : Tensor
        The mask to compute loss, it has the same size with `target_seqs`, normally 0 or 1.
    return_details : boolean
        Whether to return detailed losses.
            - If False (default), only returns the loss.
            - If True, returns the loss, losses, weights and targets (see source code).

    Examples
    --------
    >>> batch_size = 64
    >>> vocab_size = 10000
    >>> embedding_size = 256
    >>> input_seqs = tf.placeholder(dtype=tf.int64, shape=[batch_size, None], name="input")
    >>> target_seqs = tf.placeholder(dtype=tf.int64, shape=[batch_size, None], name="target")
    >>> input_mask = tf.placeholder(dtype=tf.int64, shape=[batch_size, None], name="mask")
    >>> net = tl.layers.EmbeddingInputlayer(
    ...         inputs = input_seqs,
    ...         vocabulary_size = vocab_size,
    ...         embedding_size = embedding_size,
    ...         name = 'seq_embedding')
    >>> net = tl.layers.DynamicRNNLayer(net,
    ...         cell_fn = tf.contrib.rnn.BasicLSTMCell,
    ...         n_hidden = embedding_size,
    ...         dropout = (0.7 if is_train else None),
    ...         sequence_length = tl.layers.retrieve_seq_length_op2(input_seqs),
    ...         return_seq_2d = True,
    ...         name = 'dynamicrnn')
    >>> print(net.outputs)
    (?, 256)
    >>> net = tl.layers.DenseLayer(net, n_units=vocab_size, name="output")
    >>> print(net.outputs)
    (?, 10000)
    >>> loss = tl.cost.cross_entropy_seq_with_mask(net.outputs, target_seqs, input_mask)

    """
    targets = tf.reshape(target_seqs, [-1])  # to one vector
    weights = tf.to_float(tf.reshape(input_mask, [-1]))  # to one vector like targets
    losses = tf.nn.sparse_softmax_cross_entropy_with_logits(logits=logits, labels=targets, name=name) * weights
    # losses = tf.reduce_mean(tf.nn.sparse_softmax_cross_entropy_with_logits(logits=logits, labels=targets, name=name)) # for TF1.0 and others

    loss = tf.divide(
        tf.reduce_sum(losses),  # loss from mask. reduce_sum before element-wise mul with mask !!
        tf.reduce_sum(weights),
        name="seq_loss_with_mask"
    )

    if return_details:
        return loss, losses, weights, targets
    else:
        return loss