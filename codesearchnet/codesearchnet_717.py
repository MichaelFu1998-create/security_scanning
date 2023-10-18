def alphas_like(tensor, alpha_value, name=None, optimize=True):
    """Creates a tensor with all elements set to `alpha_value`.
    Given a single tensor (`tensor`), this operation returns a tensor of the same
    type and shape as `tensor` with all elements set to `alpha_value`.

    Parameters
    ----------
    tensor: tf.Tensor
        The Tensorflow Tensor that will be used as a template.
    alpha_value: `float32`, `float64`, `int8`, `uint8`, `int16`, `uint16`, int32`, `int64`
        The value used to fill the resulting `Tensor`.
    name: str
        A name for the operation (optional).
    optimize: bool
        if true, attempt to statically determine the shape of 'tensor' and encode it as a constant.

    Returns
    -------
    A `Tensor` with all elements set to `alpha_value`.

    Examples
    --------
    >>> tensor = tf.constant([[1, 2, 3], [4, 5, 6]])
    >>> tl.alphas_like(tensor, 0.5)  # [[0.5, 0.5, 0.5], [0.5, 0.5, 0.5]]
    """
    with ops.name_scope(name, "alphas_like", [tensor]) as name:
        tensor = ops.convert_to_tensor(tensor, name="tensor")

        if context.in_eager_mode():  # and dtype is not None and dtype != tensor.dtype:
            ret = alphas(shape_internal(tensor, optimize=optimize), alpha_value=alpha_value, name=name)

        else:  # if context.in_graph_mode():

            # For now, variant types must be created via zeros_like; as we need to
            # pass the input variant object to the proper zeros callback.

            if (optimize and tensor.shape.is_fully_defined()):
                # We can produce a zeros tensor independent of the value of 'tensor',
                # since the shape is known statically.
                ret = alphas(tensor.shape, alpha_value=alpha_value, name=name)

            # elif dtype is not None and dtype != tensor.dtype and dtype != dtypes.variant:
            else:
                ret = alphas(shape_internal(tensor, optimize=optimize), alpha_value=alpha_value, name=name)

            ret.set_shape(tensor.get_shape())

        return ret