def li_regularizer(scale, scope=None):
    """Li regularization removes the neurons of previous layer. The `i` represents `inputs`.
    Returns a function that can be used to apply group li regularization to weights.
    The implementation follows `TensorFlow contrib <https://github.com/tensorflow/tensorflow/blob/master/tensorflow/contrib/layers/python/layers/regularizers.py>`__.

    Parameters
    ----------
    scale : float
        A scalar multiplier `Tensor`. 0.0 disables the regularizer.
    scope: str
        An optional scope name for this function.

    Returns
    --------
    A function with signature `li(weights, name=None)` that apply Li regularization.

    Raises
    ------
    ValueError : if scale is outside of the range [0.0, 1.0] or if scale is not a float.

    """
    if isinstance(scale, numbers.Integral):
        raise ValueError('scale cannot be an integer: %s' % scale)
    if isinstance(scale, numbers.Real):
        if scale < 0.:
            raise ValueError('Setting a scale less than 0 on a regularizer: %g' % scale)
        if scale >= 1.:
            raise ValueError('Setting a scale greater than 1 on a regularizer: %g' % scale)
        if scale == 0.:
            tl.logging.info('Scale of 0 disables regularizer.')
            return lambda _, name=None: None

    def li(weights):
        """Applies li regularization to weights."""
        with tf.name_scope('li_regularizer') as scope:
            my_scale = ops.convert_to_tensor(scale, dtype=weights.dtype.base_dtype, name='scale')
            # if tf.__version__ <= '0.12':
            #     standard_ops_fn = standard_ops.mul
            # else:
            standard_ops_fn = standard_ops.multiply
            return standard_ops_fn(
                my_scale, standard_ops.reduce_sum(standard_ops.sqrt(standard_ops.reduce_sum(tf.square(weights), 1))),
                name=scope
            )

    return li