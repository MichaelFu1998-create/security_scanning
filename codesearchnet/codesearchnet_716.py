def alphas(shape, alpha_value, name=None):
    """Creates a tensor with all elements set to `alpha_value`.
    This operation returns a tensor of type `dtype` with shape `shape` and all
    elements set to alpha.

    Parameters
    ----------
    shape: A list of integers, a tuple of integers, or a 1-D `Tensor` of type `int32`.
        The shape of the desired tensor
    alpha_value: `float32`, `float64`, `int8`, `uint8`, `int16`, `uint16`, int32`, `int64`
        The value used to fill the resulting `Tensor`.
    name: str
        A name for the operation (optional).

    Returns
    -------
    A `Tensor` with all elements set to alpha.

    Examples
    --------
    >>> tl.alphas([2, 3], tf.int32)  # [[alpha, alpha, alpha], [alpha, alpha, alpha]]
    """
    with ops.name_scope(name, "alphas", [shape]) as name:

        alpha_tensor = convert_to_tensor(alpha_value)
        alpha_dtype = dtypes.as_dtype(alpha_tensor.dtype).base_dtype

        if not isinstance(shape, ops.Tensor):
            try:
                shape = constant_op._tensor_shape_tensor_conversion_function(tensor_shape.TensorShape(shape))
            except (TypeError, ValueError):
                shape = ops.convert_to_tensor(shape, dtype=dtypes.int32)

        if not shape._shape_tuple():
            shape = reshape(shape, [-1])  # Ensure it's a vector

        try:
            output = constant(alpha_value, shape=shape, dtype=alpha_dtype, name=name)

        except (TypeError, ValueError):
            output = fill(shape, constant(alpha_value, dtype=alpha_dtype), name=name)

        if output.dtype.base_dtype != alpha_dtype:
            raise AssertionError("Dtypes do not corresponds: %s and %s" % (output.dtype.base_dtype, alpha_dtype))

        return output