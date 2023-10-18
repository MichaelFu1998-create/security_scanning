def rsolve(A, y):
    """
    Robust solve Ax=y.
    """
    from numpy_sugar.linalg import rsolve as _rsolve

    try:
        beta = _rsolve(A, y)
    except LinAlgError:
        msg = "Could not converge to solve Ax=y."
        msg += " Setting x to zero."
        warnings.warn(msg, RuntimeWarning)
        beta = zeros(A.shape[0])

    return beta