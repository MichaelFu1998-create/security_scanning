def nucnorm(x, rho, penalty, newshape=None):
    """
    Nuclear norm

    Parameters
    ----------
    penalty : float
        nuclear norm penalty hyperparameter

    newshape : tuple, optional
        Desired shape of the parameters to apply the nuclear norm to. The given
        parameters are reshaped to an array with this shape, or not reshaped if
        the value of newshape is None. (Default: None)
    """

    orig_shape = x.shape

    if newshape is not None:
        x = x.reshape(newshape)

    u, s, v = np.linalg.svd(x, full_matrices=False)
    sthr = np.maximum(s - (penalty / rho), 0)

    return np.linalg.multi_dot((u, np.diag(sthr), v)).reshape(orig_shape)