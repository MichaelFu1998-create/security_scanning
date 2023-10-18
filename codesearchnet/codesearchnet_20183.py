def smooth(x, rho, penalty, axis=0, newshape=None):
    """
    Applies a smoothing operator along one dimension

    currently only accepts a matrix as input

    Parameters
    ----------
    penalty : float

    axis : int, optional
        Axis along which to apply the smoothing (Default: 0)

    newshape : tuple, optional
        Desired shape of the parameters to apply the nuclear norm to. The given
        parameters are reshaped to an array with this shape, or not reshaped if
        the value of newshape is None. (Default: None)
    """

    orig_shape = x.shape

    if newshape is not None:
        x = x.reshape(newshape)

    # Apply Laplacian smoothing (l2 norm on the parameters multiplied by
    # the laplacian)
    n = x.shape[axis]
    lap_op = spdiags([(2 + rho / penalty) * np.ones(n),
                      -1 * np.ones(n), -1 * np.ones(n)],
                     [0, -1, 1], n, n, format='csc')

    A = penalty * lap_op
    b = rho * np.rollaxis(x, axis, 0)
    return np.rollaxis(spsolve(A, b), axis, 0).reshape(orig_shape)