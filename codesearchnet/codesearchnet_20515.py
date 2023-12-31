def as_ndarray(arr, copy=False, dtype=None, order='K'):
    """Convert an arbitrary array to numpy.ndarray.

    In the case of a memmap array, a copy is automatically made to break the
    link with the underlying file (whatever the value of the "copy" keyword).

    The purpose of this function is mainly to get rid of memmap objects, but
    it can be used for other purposes. In particular, combining copying and
    casting can lead to performance improvements in some cases, by avoiding
    unnecessary copies.

    If not specified, input array order is preserved, in all cases, even when
    a copy is requested.

    Caveat: this function does not copy during bool to/from 1-byte dtype
    conversions. This can lead to some surprising results in some rare cases.
    Example:

        a = numpy.asarray([0, 1, 2], dtype=numpy.int8)
        b = as_ndarray(a, dtype=bool)  # array([False, True, True], dtype=bool)
        c = as_ndarray(b, dtype=numpy.int8)  # array([0, 1, 2], dtype=numpy.int8)

    The usually expected result for the last line would be array([0, 1, 1])
    because True evaluates to 1. Since there is no copy made here, the original
    array is recovered.

    Parameters
    ----------
    arr: array-like
        input array. Any value accepted by numpy.asarray is valid.

    copy: bool
        if True, force a copy of the array. Always True when arr is a memmap.

    dtype: any numpy dtype
        dtype of the returned array. Performing copy and type conversion at the
        same time can in some cases avoid an additional copy.

    order: string
        gives the order of the returned array.
        Valid values are: "C", "F", "A", "K", None.
        default is "K". See ndarray.copy() for more information.

    Returns
    -------
    ret: np.ndarray
        Numpy array containing the same data as arr, always of class
        numpy.ndarray, and with no link to any underlying file.
    """
    if order not in ('C', 'F', 'A', 'K', None):
        raise ValueError("Invalid value for 'order': {}".format(str(order)))

    if isinstance(arr, np.memmap):
        if dtype is None:
            if order in ('K', 'A', None):
                ret = np.array(np.asarray(arr), copy=True)
            else:
                ret = np.array(np.asarray(arr), copy=True, order=order)
        else:
            if order in ('K', 'A', None):
                # always copy (even when dtype does not change)
                ret = np.asarray(arr).astype(dtype)
            else:
                # load data from disk without changing order
                # Changing order while reading through a memmap is incredibly
                # inefficient.
                ret = _asarray(np.array(arr, copy=True), dtype=dtype, order=order)

    elif isinstance(arr, np.ndarray):
        ret = _asarray(arr, dtype=dtype, order=order)
        # In the present cas, np.may_share_memory result is always reliable.
        if np.may_share_memory(ret, arr) and copy:
            # order-preserving copy
            ret = ret.T.copy().T if ret.flags['F_CONTIGUOUS'] else ret.copy()

    elif isinstance(arr, (list, tuple)):
        if order in ("A", "K"):
            ret = np.asarray(arr, dtype=dtype)
        else:
            ret = np.asarray(arr, dtype=dtype, order=order)

    else:
        raise ValueError("Type not handled: {}".format(arr.__class__))

    return ret