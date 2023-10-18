def cross_entropy_seq(logits, target_seqs, batch_size=None):  # , batch_size=1, num_steps=None):
    """Returns the expression of cross-entropy of two sequences, implement
    softmax internally. Normally be used for fixed length RNN outputs, see `PTB example <https://github.com/tensorlayer/tensorlayer/blob/master/example/tutorial_ptb_lstm_state_is_tuple.py>`__.

    Parameters
    ----------
    logits : Tensor
        2D tensor with shape of `[batch_size * n_steps, n_classes]`.
    target_seqs : Tensor
        The target sequence, 2D tensor `[batch_size, n_steps]`, if the number of step is dynamic, please use ``tl.cost.cross_entropy_seq_with_mask`` instead.
    batch_size : None or int.
        Whether to divide the cost by batch size.
            - If integer, the return cost will be divided by `batch_size`.
            - If None (default), the return cost will not be divided by anything.

    Examples
    --------
    >>> see `PTB example <https://github.com/tensorlayer/tensorlayer/blob/master/example/tutorial_ptb_lstm_state_is_tuple.py>`__.for more details
    >>> input_data = tf.placeholder(tf.int32, [batch_size, n_steps])
    >>> targets = tf.placeholder(tf.int32, [batch_size, n_steps])
    >>> # build the network
    >>> print(net.outputs)
    (batch_size * n_steps, n_classes)
    >>> cost = tl.cost.cross_entropy_seq(network.outputs, targets)

    """
    sequence_loss_by_example_fn = tf.contrib.legacy_seq2seq.sequence_loss_by_example

    loss = sequence_loss_by_example_fn(
        [logits], [tf.reshape(target_seqs, [-1])], [tf.ones_like(tf.reshape(target_seqs, [-1]), dtype=tf.float32)]
    )
    # [tf.ones([batch_size * num_steps])])
    cost = tf.reduce_sum(loss)  # / batch_size
    if batch_size is not None:
        cost = cost / batch_size
    return cost