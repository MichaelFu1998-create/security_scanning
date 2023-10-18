def _compute_resized_shape(from_shape, to_shape):
    """
    Computes the intended new shape of an image-like array after resizing.

    Parameters
    ----------
    from_shape : tuple or ndarray
        Old shape of the array. Usually expected to be a tuple of form ``(H, W)`` or ``(H, W, C)`` or
        alternatively an array with two or three dimensions.

    to_shape : None or tuple of ints or tuple of floats or int or float or ndarray
        New shape of the array.

            * If None, then `from_shape` will be used as the new shape.
            * If an int ``V``, then the new shape will be ``(V, V, [C])``, where ``C`` will be added if it
              is part of `from_shape`.
            * If a float ``V``, then the new shape will be ``(H*V, W*V, [C])``, where ``H`` and ``W`` are the old
              height/width.
            * If a tuple ``(H', W', [C'])`` of ints, then ``H'`` and ``W'`` will be used as the new height
              and width.
            * If a tuple ``(H', W', [C'])`` of floats (except ``C``), then ``H'`` and ``W'`` will
              be used as the new height and width.
            * If a numpy array, then the array's shape will be used.

    Returns
    -------
    to_shape_computed : tuple of int
        New shape.

    """
    if is_np_array(from_shape):
        from_shape = from_shape.shape
    if is_np_array(to_shape):
        to_shape = to_shape.shape

    to_shape_computed = list(from_shape)

    if to_shape is None:
        pass
    elif isinstance(to_shape, tuple):
        do_assert(len(from_shape) in [2, 3])
        do_assert(len(to_shape) in [2, 3])

        if len(from_shape) == 3 and len(to_shape) == 3:
            do_assert(from_shape[2] == to_shape[2])
        elif len(to_shape) == 3:
            to_shape_computed.append(to_shape[2])

        do_assert(all([v is None or is_single_number(v) for v in to_shape[0:2]]),
                  "Expected the first two entries in to_shape to be None or numbers, "
                  + "got types %s." % (str([type(v) for v in to_shape[0:2]]),))

        for i, from_shape_i in enumerate(from_shape[0:2]):
            if to_shape[i] is None:
                to_shape_computed[i] = from_shape_i
            elif is_single_integer(to_shape[i]):
                to_shape_computed[i] = to_shape[i]
            else:  # float
                to_shape_computed[i] = int(np.round(from_shape_i * to_shape[i]))
    elif is_single_integer(to_shape) or is_single_float(to_shape):
        to_shape_computed = _compute_resized_shape(from_shape, (to_shape, to_shape))
    else:
        raise Exception("Expected to_shape to be None or ndarray or tuple of floats or tuple of ints or single int "
                        + "or single float, got %s." % (type(to_shape),))

    return tuple(to_shape_computed)