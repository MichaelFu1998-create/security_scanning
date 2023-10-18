def affine_shift_matrix(wrg=(-0.1, 0.1), hrg=(-0.1, 0.1), w=200, h=200):
    """Create an affine transform matrix for image shifting.
    NOTE: In OpenCV, x is width and y is height.

    Parameters
    -----------
    wrg : float or tuple of floats
        Range to shift on width axis, -1 ~ 1.
            - float, a fixed distance.
            - tuple of 2 floats, randomly sample a value as the distance between these 2 values.
    hrg : float or tuple of floats
        Range to shift on height axis, -1 ~ 1.
            - float, a fixed distance.
            - tuple of 2 floats, randomly sample a value as the distance between these 2 values.
    w, h : int
        The width and height of the image.

    Returns
    -------
    numpy.array
        An affine transform matrix.

    """
    if isinstance(wrg, tuple):
        tx = np.random.uniform(wrg[0], wrg[1]) * w
    else:
        tx = wrg * w
    if isinstance(hrg, tuple):
        ty = np.random.uniform(hrg[0], hrg[1]) * h
    else:
        ty = hrg * h
    shift_matrix = np.array([[1, 0, tx], \
                        [0, 1, ty], \
                        [0, 0, 1]])
    return shift_matrix