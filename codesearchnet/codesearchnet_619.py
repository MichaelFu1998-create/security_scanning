def sigmoid_cross_entropy(output, target, name=None):
    """Sigmoid cross-entropy operation, see ``tf.nn.sigmoid_cross_entropy_with_logits``.

    Parameters
    ----------
    output : Tensor
        A batch of distribution with shape: [batch_size, num of classes].
    target : Tensor
        A batch of index with shape: [batch_size, ].
    name : string
        Name of this loss.

    """
    return tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(labels=target, logits=output), name=name)