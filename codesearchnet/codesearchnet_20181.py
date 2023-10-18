def sparse(x, rho, penalty):
    """
    Proximal operator for the l1-norm: soft thresholding

    Parameters
    ----------
    penalty : float
        Strength or weight on the l1-norm
    """

    lmbda = penalty / rho
    return (x - lmbda) * (x >= lmbda) + (x + lmbda) * (x <= -lmbda)