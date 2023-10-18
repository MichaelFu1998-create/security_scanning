def affine_rotation_matrix(angle=(-20, 20)):
    """Create an affine transform matrix for image rotation.
    NOTE: In OpenCV, x is width and y is height.

    Parameters
    -----------
    angle : int/float or tuple of two int/float
        Degree to rotate, usually -180 ~ 180.
            - int/float, a fixed angle.
            - tuple of 2 floats/ints, randomly sample a value as the angle between these 2 values.

    Returns
    -------
    numpy.array
        An affine transform matrix.

    """
    if isinstance(angle, tuple):
        theta = np.pi / 180 * np.random.uniform(angle[0], angle[1])
    else:
        theta = np.pi / 180 * angle
    rotation_matrix = np.array([[np.cos(theta), np.sin(theta), 0], \
                                [-np.sin(theta), np.cos(theta), 0], \
                                [0, 0, 1]])
    return rotation_matrix