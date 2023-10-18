def affine_shear_matrix(x_shear=(-0.1, 0.1), y_shear=(-0.1, 0.1)):
    """Create affine transform matrix for image shearing.
    NOTE: In OpenCV, x is width and y is height.

    Parameters
    -----------
    shear : tuple of two floats
        Percentage of shears for width and height directions.

    Returns
    -------
    numpy.array
        An affine transform matrix.

    """
    # if len(shear) != 2:
    #     raise AssertionError(
    #         "shear should be tuple of 2 floats, or you want to use tl.prepro.shear rather than tl.prepro.shear2 ?"
    #     )
    # if isinstance(shear, tuple):
    #     shear = list(shear)
    # if is_random:
    #     shear[0] = np.random.uniform(-shear[0], shear[0])
    #     shear[1] = np.random.uniform(-shear[1], shear[1])
    if isinstance(x_shear, tuple):
        x_shear = np.random.uniform(x_shear[0], x_shear[1])
    if isinstance(y_shear, tuple):
        y_shear = np.random.uniform(y_shear[0], y_shear[1])

    shear_matrix = np.array([[1, x_shear, 0], \
                            [y_shear, 1, 0], \
                            [0, 0, 1]])
    return shear_matrix