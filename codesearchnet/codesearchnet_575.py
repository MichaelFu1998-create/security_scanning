def get_zca_whitening_principal_components_img(X):
    """Return the ZCA whitening principal components matrix.

    Parameters
    -----------
    x : numpy.array
        Batch of images with dimension of [n_example, row, col, channel] (default).

    Returns
    -------
    numpy.array
        A processed image.

    """
    flatX = np.reshape(X, (X.shape[0], X.shape[1] * X.shape[2] * X.shape[3]))
    tl.logging.info("zca : computing sigma ..")
    sigma = np.dot(flatX.T, flatX) / flatX.shape[0]
    tl.logging.info("zca : computing U, S and V ..")
    U, S, _ = linalg.svd(sigma)  # USV
    tl.logging.info("zca : computing principal components ..")
    principal_components = np.dot(np.dot(U, np.diag(1. / np.sqrt(S + 10e-7))), U.T)
    return principal_components