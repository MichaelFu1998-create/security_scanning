def angle_between_vectors(v1, v2):
    """
    Returns the angle in radians between vectors `v1` and `v2`.

    From http://stackoverflow.com/questions/2827393/angles-between-two-n-dimensional-vectors-in-python

    Parameters
    ----------
    v1 : (N,) ndarray
        First vector.

    v2 : (N,) ndarray
        Second vector.

    Returns
    -------
    out : float
        Angle in radians.

    Examples
    --------
    >>> angle_between_vectors(np.float32([1, 0, 0]), np.float32([0, 1, 0]))
    1.570796...

    >>> angle_between_vectors(np.float32([1, 0, 0]), np.float32([1, 0, 0]))
    0.0

    >>> angle_between_vectors(np.float32([1, 0, 0]), np.float32([-1, 0, 0]))
    3.141592...

    """
    l1 = np.linalg.norm(v1)
    l2 = np.linalg.norm(v2)
    v1_u = (v1 / l1) if l1 > 0 else np.float32(v1) * 0
    v2_u = (v2 / l2) if l2 > 0 else np.float32(v2) * 0
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))