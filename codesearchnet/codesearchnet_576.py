def zca_whitening(x, principal_components):
    """Apply ZCA whitening on an image by given principal components matrix.

    Parameters
    -----------
    x : numpy.array
        An image with dimension of [row, col, channel] (default).
    principal_components : matrix
        Matrix from ``get_zca_whitening_principal_components_img``.

    Returns
    -------
    numpy.array
        A processed image.

    """
    flatx = np.reshape(x, (x.size))
    # tl.logging.info(principal_components.shape, x.shape)  # ((28160, 28160), (160, 176, 1))
    # flatx = np.reshape(x, (x.shape))
    # flatx = np.reshape(x, (x.shape[0], ))
    # tl.logging.info(flatx.shape)  # (160, 176, 1)
    whitex = np.dot(flatx, principal_components)
    x = np.reshape(whitex, (x.shape[0], x.shape[1], x.shape[2]))
    return x