def check_X_y(X, y, accept_sparse=None, dtype=None, order=None, copy=False,
              force_all_finite=True, ensure_2d=True, allow_nd=False,
              multi_output=False):
    """Input validation for standard estimators.

    Checks X and y for consistent length, enforces X 2d and y 1d.
    Standard input checks are only applied to y. For multi-label y,
    set multi_ouput=True to allow 2d and sparse y.

    Parameters
    ----------
    X : nd-array, list or sparse matrix
        Input data.

    y : nd-array, list or sparse matrix
        Labels.

    accept_sparse : string, list of string or None (default=None)
        String[s] representing allowed sparse matrix formats, such as 'csc',
        'csr', etc.  None means that sparse matrix input will raise an error.
        If the input is sparse but not in the allowed format, it will be
        converted to the first listed format.

    order : 'F', 'C' or None (default=None)
        Whether an array will be forced to be fortran or c-style.

    copy : boolean (default=False)
        Whether a forced copy will be triggered. If copy=False, a copy might
        be triggered by a conversion.

    force_all_finite : boolean (default=True)
        Whether to raise an error on np.inf and np.nan in X.

    ensure_2d : boolean (default=True)
        Whether to make X at least 2d.

    allow_nd : boolean (default=False)
        Whether to allow X.ndim > 2.

    Returns
    -------
    X_converted : object
        The converted and validated X.
    """
    X = check_array(X, accept_sparse, dtype, order, copy, force_all_finite,
                    ensure_2d, allow_nd)
    if multi_output:
        y = check_array(y, 'csr', force_all_finite=True, ensure_2d=False)
    else:
        y = column_or_1d(y, warn=True)
        _assert_all_finite(y)

    check_consistent_length(X, y)

    return X, y