def compute_alpha(x):
    """Computing the scale parameter."""
    threshold = _compute_threshold(x)
    alpha1_temp1 = tf.where(tf.greater(x, threshold), x, tf.zeros_like(x, tf.float32))
    alpha1_temp2 = tf.where(tf.less(x, -threshold), x, tf.zeros_like(x, tf.float32))
    alpha_array = tf.add(alpha1_temp1, alpha1_temp2, name=None)
    alpha_array_abs = tf.abs(alpha_array)
    alpha_array_abs1 = tf.where(
        tf.greater(alpha_array_abs, 0), tf.ones_like(alpha_array_abs, tf.float32),
        tf.zeros_like(alpha_array_abs, tf.float32)
    )
    alpha_sum = tf.reduce_sum(alpha_array_abs)
    n = tf.reduce_sum(alpha_array_abs1)
    alpha = tf.div(alpha_sum, n)
    return alpha