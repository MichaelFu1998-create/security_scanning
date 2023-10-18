def check_arrays(*arrays, **options):
    """Check that all arrays have consistent first dimensions.

    Checks whether all objects in arrays have the same shape or length.
    By default lists and tuples are converted to numpy arrays.

    It is possible to enforce certain properties, such as dtype, continguity
    and sparse matrix format (if a sparse matrix is passed).

    Converting lists to arrays can be disabled by setting ``allow_lists=True``.
    Lists can then contain arbitrary objects and are not checked for dtype,
    finiteness or anything else but length. Arrays are still checked
    and possibly converted.

    Parameters
    ----------
    *arrays : sequence of arrays or scipy.sparse matrices with same shape[0]
        Python lists or tuples occurring in arrays are converted to 1D numpy
        arrays, unless allow_lists is specified.
    sparse_format : 'csr', 'csc' or 'dense', None by default
        If not None, any scipy.sparse matrix is converted to
        Compressed Sparse Rows or Compressed Sparse Columns representations.
        If 'dense', an error is raised when a sparse array is
        passed.
    copy : boolean, False by default
        If copy is True, ensure that returned arrays are copies of the original
        (if not already converted to another format earlier in the process).
    check_ccontiguous : boolean, False by default
        Check that the arrays are C contiguous
    dtype : a numpy dtype instance, None by default
        Enforce a specific dtype.
    warn_nans : boolean, False by default
        Prints warning if nans in the arrays
        Disables allow_nans
    replace_nans : boolean, False by default
        Replace nans in the arrays with zeros
    allow_lists : bool
        Allow lists of arbitrary objects as input, just check their length.
        Disables
    allow_nans : boolean, False by default
        Allows nans in the arrays
    allow_nd : boolean, False by default
        Allows arrays of more than 2 dimensions.
    """
    sparse_format = options.pop('sparse_format', None)
    if sparse_format not in (None, 'csr', 'csc', 'dense'):
        raise ValueError('Unexpected sparse format: %r' % sparse_format)
    copy = options.pop('copy', False)
    check_ccontiguous = options.pop('check_ccontiguous', False)
    dtype = options.pop('dtype', None)
    warn_nans = options.pop('warn_nans', False)
    replace_nans = options.pop('replace_nans', False)
    allow_lists = options.pop('allow_lists', False)
    allow_nans = options.pop('allow_nans', False)
    allow_nd = options.pop('allow_nd', False)

    if options:
        raise TypeError("Unexpected keyword arguments: %r" % options.keys())

    if len(arrays) == 0:
        return None

    n_samples = num_samples(arrays[0])

    checked_arrays = []
    for array in arrays:
        array_orig = array
        if array is None:
            # special case: ignore optional y=None kwarg pattern
            checked_arrays.append(array)
            continue
        size = num_samples(array)

        if size != n_samples:
            raise ValueError("Found array with dim %d. Expected %d"
                             % (size, n_samples))

        if not allow_lists or hasattr(array, "shape"):
            if sp.issparse(array):
                if sparse_format == 'csr':
                    array = array.tocsr()
                elif sparse_format == 'csc':
                    array = array.tocsc()
                elif sparse_format == 'dense':
                    raise TypeError('A sparse matrix was passed, but dense '
                                    'data is required. Use X.toarray() to '
                                    'convert to a dense numpy array.')
                if check_ccontiguous:
                    array.data = np.ascontiguousarray(array.data, dtype=dtype)
                elif hasattr(array, 'data'):
                    array.data = np.asarray(array.data, dtype=dtype)
                elif array.dtype != dtype:
                    array = array.astype(dtype)
                if not allow_nans:
                    if hasattr(array, 'data'):
                        _assert_all_finite(array.data)
                    else:
                        _assert_all_finite(array.values())
            else:
                if check_ccontiguous:
                    array = np.ascontiguousarray(array, dtype=dtype)
                else:
                    array = np.asarray(array, dtype=dtype)
                if warn_nans:
                    allow_nans = True
                    _warn_if_not_finite(array)
                if replace_nans:
                    array = np.nan_to_num(array)
                if not allow_nans:
                    _assert_all_finite(array)

            if not allow_nd and array.ndim >= 3:
                raise ValueError("Found array with dim %d. Expected <= 2" %
                                 array.ndim)

        if copy and array is array_orig:
            array = array.copy()
        checked_arrays.append(array)

    return checked_arrays