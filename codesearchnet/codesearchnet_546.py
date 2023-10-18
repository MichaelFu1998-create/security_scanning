def transform_matrix_offset_center(matrix, y, x):
    """Convert the matrix from Cartesian coordinates (the origin in the middle of image) to Image coordinates (the origin on the top-left of image).

    Parameters
    ----------
    matrix : numpy.array
        Transform matrix.
    x and y : 2 int
        Size of image.

    Returns
    -------
    numpy.array
        The transform matrix.

    Examples
    --------
    - See ``tl.prepro.rotation``, ``tl.prepro.shear``, ``tl.prepro.zoom``.
    """
    o_x = (x - 1) / 2.0
    o_y = (y - 1) / 2.0
    offset_matrix = np.array([[1, 0, o_x], [0, 1, o_y], [0, 0, 1]])
    reset_matrix = np.array([[1, 0, -o_x], [0, 1, -o_y], [0, 0, 1]])
    transform_matrix = np.dot(np.dot(offset_matrix, matrix), reset_matrix)
    return transform_matrix