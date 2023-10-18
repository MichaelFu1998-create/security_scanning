def max_pool(arr, block_size, cval=0, preserve_dtype=True):
    """
    Resize an array using max-pooling.

    dtype support::

        See :func:`imgaug.imgaug.pool`.

    Parameters
    ----------
    arr : (H,W) ndarray or (H,W,C) ndarray
        Image-like array to pool. See :func:`imgaug.pool` for details.

    block_size : int or tuple of int or tuple of int
        Size of each block of values to pool. See `imgaug.pool` for details.

    cval : number, optional
        Padding value. See :func:`imgaug.pool` for details.

    preserve_dtype : bool, optional
        Whether to preserve the input array dtype. See :func:`imgaug.pool` for details.

    Returns
    -------
    arr_reduced : (H',W') ndarray or (H',W',C') ndarray
        Array after max-pooling.

    """
    return pool(arr, block_size, np.max, cval=cval, preserve_dtype=preserve_dtype)