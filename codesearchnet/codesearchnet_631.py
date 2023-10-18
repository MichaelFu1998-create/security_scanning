def maxnorm_regularizer(scale=1.0):
    """Max-norm regularization returns a function that can be used to apply max-norm regularization to weights.

    More about max-norm, see `wiki-max norm <https://en.wikipedia.org/wiki/Matrix_norm#Max_norm>`_.
    The implementation follows `TensorFlow contrib <https://github.com/tensorflow/tensorflow/blob/master/tensorflow/contrib/layers/python/layers/regularizers.py>`__.

    Parameters
    ----------
    scale : float
        A scalar multiplier `Tensor`. 0.0 disables the regularizer.

    Returns
    ---------
    A function with signature `mn(weights, name=None)` that apply Lo regularization.

    Raises
    --------
    ValueError : If scale is outside of the range [0.0, 1.0] or if scale is not a float.

    """
    if isinstance(scale, numbers.Integral):
        raise ValueError('scale cannot be an integer: %s' % scale)

    if isinstance(scale, numbers.Real):
        if scale < 0.:
            raise ValueError('Setting a scale less than 0 on a regularizer: %g' % scale)
        # if scale >= 1.:
        #   raise ValueError('Setting a scale greater than 1 on a regularizer: %g' %
        #                    scale)
        if scale == 0.:
            tl.logging.info('Scale of 0 disables regularizer.')
            return lambda _, name=None: None

    def mn(weights, name='max_regularizer'):
        """Applies max-norm regularization to weights."""
        with tf.name_scope(name) as scope:
            my_scale = ops.convert_to_tensor(scale, dtype=weights.dtype.base_dtype, name='scale')
            #   if tf.__version__ <= '0.12':
            #       standard_ops_fn = standard_ops.mul
            #   else:
            standard_ops_fn = standard_ops.multiply
            return standard_ops_fn(my_scale, standard_ops.reduce_max(standard_ops.abs(weights)), name=scope)

    return mn