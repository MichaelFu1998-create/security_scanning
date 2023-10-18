def _difference_map(image, color_axis):
    """Difference map of the image.
    Approximate derivatives of the function image[c, :, :]
    (e.g. PyTorch) or image[:, :, c] (e.g. Keras).
    dfdx, dfdy = difference_map(image)
    In:
    image: numpy.ndarray
        of shape C x h x w or h x w x C, with C = 1 or C = 3
        (color channels), h, w >= 3, and [type] is 'Float' or
        'Double'. Contains the values of functions f_b:
        R ^ 2 -> R ^ C, b = 1, ..., B, on the grid
        {0, ..., h - 1} x {0, ..., w - 1}.
    Out:
    dfdx: numpy.ndarray
    dfdy: numpy.ndarray
        of shape C x h x w or h x w x C contain the x and
        y derivatives of f at the points on the grid,
        approximated by central differences (except on
        boundaries):
        For c = 0, ... , C, i = 1, ..., h - 2,
        j = 1, ..., w - 2.
        e.g. for shape = c x h x w:
        dfdx[c, i, j] = (image[c, i, j + 1] -
            image[c, i, j - 1]) / 2
        dfdx[c, i, j] = (image[c, i + 1, j] -
            image[c, i - 1, j]) / 2
    positive x-direction is along rows from left to right.
    positive y-direction is along columns from above to below.
    """

    if color_axis == 2:
        image = _transpose_image(image)
    # Derivative in x direction (rows from left to right)
    dfdx = np.zeros_like(image)
    # forward difference in first column
    dfdx[:, :, 0] = image[:, :, 1] - image[:, :, 0]
    # backwards difference in last column
    dfdx[:, :, -1] = image[:, :, -1] - image[:, :, -2]
    # central difference elsewhere
    dfdx[:, :, 1:-1] = 0.5 * (image[:, :, 2:] - image[:, :, :-2])

    # Derivative in y direction (columns from above to below)
    dfdy = np.zeros_like(image)
    # forward difference in first row
    dfdy[:, 0, :] = image[:, 1, :] - image[:, 0, :]
    # backwards difference in last row
    dfdy[:, -1, :] = image[:, -1, :] - image[:, -2, :]
    # central difference elsewhere
    dfdy[:, 1:-1, :] = 0.5 * (image[:, 2:, :] - image[:, :-2, :])

    return dfdx, dfdy