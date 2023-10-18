def affine_horizontal_flip_matrix(prob=0.5):
    """Create an affine transformation matrix for image horizontal flipping.
    NOTE: In OpenCV, x is width and y is height.

    Parameters
    ----------
    prob : float
        Probability to flip the image. 1.0 means always flip.

    Returns
    -------
    numpy.array
        An affine transform matrix.

    """
    factor = np.random.uniform(0, 1)
    if prob >= factor:
        filp_matrix = np.array([[ -1. , 0., 0. ], \
              [ 0., 1., 0. ], \
              [ 0., 0., 1. ]])
        return filp_matrix
    else:
        filp_matrix = np.array([[ 1. , 0., 0. ], \
              [ 0., 1., 0. ], \
              [ 0., 0., 1. ]])
        return filp_matrix