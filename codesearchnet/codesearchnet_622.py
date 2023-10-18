def normalized_mean_square_error(output, target, name="normalized_mean_squared_error_loss"):
    """Return the TensorFlow expression of normalized mean-square-error of two distributions.

    Parameters
    ----------
    output : Tensor
        2D, 3D or 4D tensor i.e. [batch_size, n_feature], [batch_size, height, width] or [batch_size, height, width, channel].
    target : Tensor
        The target distribution, format the same with `output`.
    name : str
        An optional name to attach to this function.

    """
    # with tf.name_scope("normalized_mean_squared_error_loss"):
    if output.get_shape().ndims == 2:  # [batch_size, n_feature]
        nmse_a = tf.sqrt(tf.reduce_sum(tf.squared_difference(output, target), axis=1))
        nmse_b = tf.sqrt(tf.reduce_sum(tf.square(target), axis=1))
    elif output.get_shape().ndims == 3:  # [batch_size, w, h]
        nmse_a = tf.sqrt(tf.reduce_sum(tf.squared_difference(output, target), axis=[1, 2]))
        nmse_b = tf.sqrt(tf.reduce_sum(tf.square(target), axis=[1, 2]))
    elif output.get_shape().ndims == 4:  # [batch_size, w, h, c]
        nmse_a = tf.sqrt(tf.reduce_sum(tf.squared_difference(output, target), axis=[1, 2, 3]))
        nmse_b = tf.sqrt(tf.reduce_sum(tf.square(target), axis=[1, 2, 3]))
    nmse = tf.reduce_mean(nmse_a / nmse_b, name=name)
    return nmse