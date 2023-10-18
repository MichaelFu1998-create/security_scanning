def cross_entropy(output, target, name=None):
    """Softmax cross-entropy operation, returns the TensorFlow expression of cross-entropy for two distributions,
    it implements softmax internally. See ``tf.nn.sparse_softmax_cross_entropy_with_logits``.

    Parameters
    ----------
    output : Tensor
        A batch of distribution with shape: [batch_size, num of classes].
    target : Tensor
        A batch of index with shape: [batch_size, ].
    name : string
        Name of this loss.

    Examples
    --------
    >>> ce = tl.cost.cross_entropy(y_logits, y_target_logits, 'my_loss')

    References
    -----------
    - About cross-entropy: `<https://en.wikipedia.org/wiki/Cross_entropy>`__.
    - The code is borrowed from: `<https://en.wikipedia.org/wiki/Cross_entropy>`__.

    """
    if name is None:
        raise Exception("Please give a unique name to tl.cost.cross_entropy for TF1.0+")
    return tf.reduce_mean(tf.nn.sparse_softmax_cross_entropy_with_logits(labels=target, logits=output), name=name)