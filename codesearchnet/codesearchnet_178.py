def pool(arr, block_size, func, cval=0, preserve_dtype=True):
    """
    Resize an array by pooling values within blocks.

    dtype support::

        * ``uint8``: yes; fully tested
        * ``uint16``: yes; tested
        * ``uint32``: yes; tested (2)
        * ``uint64``: no (1)
        * ``int8``: yes; tested
        * ``int16``: yes; tested
        * ``int32``: yes; tested (2)
        * ``int64``: no (1)
        * ``float16``: yes; tested
        * ``float32``: yes; tested
        * ``float64``: yes; tested
        * ``float128``: yes; tested (2)
        * ``bool``: yes; tested

        - (1) results too inaccurate (at least when using np.average as func)
        - (2) Note that scikit-image documentation says that the wrapped pooling function converts
              inputs to float64. Actual tests showed no indication of that happening (at least when
              using preserve_dtype=True).

    Parameters
    ----------
    arr : (H,W) ndarray or (H,W,C) ndarray
        Image-like array to pool. Ideally of datatype ``numpy.float64``.

    block_size : int or tuple of int
        Spatial size of each group of values to pool, aka kernel size.
        If a single integer, then a symmetric block of that size along height and width will be used.
        If a tuple of two values, it is assumed to be the block size along height and width of the image-like,
        with pooling happening per channel.
        If a tuple of three values, it is assumed to be the block size along height, width and channels.

    func : callable
        Function to apply to a given block in order to convert it to a single number,
        e.g. :func:`numpy.average`, :func:`numpy.min`, :func:`numpy.max`.

    cval : number, optional
        Value to use in order to pad the array along its border if the array cannot be divided
        by `block_size` without remainder.

    preserve_dtype : bool, optional
        Whether to convert the array back to the input datatype if it is changed away from
        that in the pooling process.

    Returns
    -------
    arr_reduced : (H',W') ndarray or (H',W',C') ndarray
        Array after pooling.

    """
    # TODO find better way to avoid circular import
    from . import dtypes as iadt
    iadt.gate_dtypes(arr,
                     allowed=["bool", "uint8", "uint16", "uint32", "int8", "int16", "int32",
                              "float16", "float32", "float64", "float128"],
                     disallowed=["uint64", "uint128", "uint256", "int64", "int128", "int256",
                                 "float256"],
                     augmenter=None)

    do_assert(arr.ndim in [2, 3])
    is_valid_int = is_single_integer(block_size) and block_size >= 1
    is_valid_tuple = is_iterable(block_size) and len(block_size) in [2, 3] \
        and [is_single_integer(val) and val >= 1 for val in block_size]
    do_assert(is_valid_int or is_valid_tuple)

    if is_single_integer(block_size):
        block_size = [block_size, block_size]
    if len(block_size) < arr.ndim:
        block_size = list(block_size) + [1]

    input_dtype = arr.dtype
    arr_reduced = skimage.measure.block_reduce(arr, tuple(block_size), func, cval=cval)
    if preserve_dtype and arr_reduced.dtype.type != input_dtype:
        arr_reduced = arr_reduced.astype(input_dtype)
    return arr_reduced