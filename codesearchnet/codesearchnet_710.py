def _compute_threshold(x):
    """
    ref: https://github.com/XJTUWYD/TWN
    Computing the threshold.
    """
    x_sum = tf.reduce_sum(tf.abs(x), reduction_indices=None, keepdims=False, name=None)
    threshold = tf.div(x_sum, tf.cast(tf.size(x), tf.float32), name=None)
    threshold = tf.multiply(0.7, threshold, name=None)
    return threshold