def _warn_if_not_finite(X):
    """UserWarning if array contains non-finite elements"""
    X = np.asanyarray(X)
    # First try an O(n) time, O(1) space solution for the common case that
    # everything is finite; fall back to O(n) space np.isfinite to prevent
    # false positives from overflow in sum method
    if (X.dtype.char in np.typecodes['AllFloat'] and
            not np.isfinite(X.sum()) and not np.isfinite(X).all()):
        warnings.warn("Result contains NaN, infinity"
                      " or a value too large for %r." % X.dtype,
                      category=UserWarning)