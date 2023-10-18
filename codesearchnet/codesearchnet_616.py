def log_weight(probs, weights, name='log_weight'):
    """Log weight.

    Parameters
    -----------
    probs : tensor
        If it is a network output, usually we should scale it to [0, 1] via softmax.
    weights : tensor
        The weights.

    Returns
    --------
    Tensor
        The Tensor after appling the log weighted expression.

    """
    with tf.variable_scope(name):
        exp_v = tf.reduce_mean(tf.log(probs) * weights)
        return exp_v