def columns(x, rho, proxop):
    """Applies a proximal operator to the columns of a matrix"""

    xnext = np.zeros_like(x)

    for ix in range(x.shape[1]):
        xnext[:, ix] = proxop(x[:, ix], rho)

    return xnext