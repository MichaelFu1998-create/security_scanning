def absolute_difference_error(output, target, is_mean=False, name="absolute_difference_error_loss"):
    """Return the TensorFlow expression of absolute difference error (L1) of two batch of data.

    Parameters
    ----------
    output : Tensor
        2D, 3D or 4D tensor i.e. [batch_size, n_feature], [batch_size, height, width] or [batch_size, height, width, channel].
    target : Tensor
        The target distribution, format the same with `output`.
    is_mean : boolean
        Whether compute the mean or sum for each example.
            - If True, use ``tf.reduce_mean`` to compute the loss between one target and predict data.
            - If False, use ``tf.reduce_sum`` (default).
    name : str
        An optional name to attach to this function.

    """
    # with tf.name_scope("absolute_difference_error_loss"):
    if output.get_shape().ndims == 2:  # [batch_size, n_feature]
        if is_mean:
            loss = tf.reduce_mean(tf.reduce_mean(tf.abs(output - target), 1), name=name)
        else:
            loss = tf.reduce_mean(tf.reduce_sum(tf.abs(output - target), 1), name=name)
    elif output.get_shape().ndims == 3:  # [batch_size, w, h]
        if is_mean:
            loss = tf.reduce_mean(tf.reduce_mean(tf.abs(output - target), [1, 2]), name=name)
        else:
            loss = tf.reduce_mean(tf.reduce_sum(tf.abs(output - target), [1, 2]), name=name)
    elif output.get_shape().ndims == 4:  # [batch_size, w, h, c]
        if is_mean:
            loss = tf.reduce_mean(tf.reduce_mean(tf.abs(output - target), [1, 2, 3]), name=name)
        else:
            loss = tf.reduce_mean(tf.reduce_sum(tf.abs(output - target), [1, 2, 3]), name=name)
    else:
        raise Exception("Unknow dimension")
    return loss